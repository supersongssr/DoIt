# 架构文档

## 系统总览

本项目是一个基于 Hugo 静态生成器 + Nginx/OpenResty 动态后端的混合架构站点（"游戏仓库"）。Hugo 负责页面渲染和静态资源输出，OpenResty (Lua) + Redis 负责用户认证、短链接跳转、邀请码返利等动态功能。

```
┌─────────────┐
│   用户浏览器  │
└──────┬───────┘
       │ HTTPS
       ▼
┌──────────────────────────────────────────────┐
│              Nginx (OpenResty)               │
│                                              │
│  ┌──────────────────┐  ┌──────────────────┐  │
│  │   静态资源路由     │  │   Lua 动态路由    │  │
│  │   /*.html/css/js  │  │                  │  │
│  │   ↓               │  │  /user/*         │  │
│  │  Hugo 生成的文件   │  │  /url            │  │
│  │                   │  │  /admin/url       │  │
│  └──────────────────┘  └────────┬─────────┘  │
│                                 │             │
│                    ┌────────────▼──────────┐   │
│                    │  ngx.shared.dict      │   │
│                    │  (内存缓存层)          │   │
│                    │  - Token 映射          │   │
│                    │  - IP 注册限制         │   │
│                    │  - 点击频率限制        │   │
│                    └────────────┬──────────┘   │
└─────────────────────────────────┼──────────────┘
                                  │
                    ┌─────────────▼──────────┐
                    │       Redis            │
                    │   127.0.0.1:6379       │
                    │                        │
                    │  - 用户数据 (Hash)      │
                    │  - 短链接映射 (Hash)    │
                    │  - 邀请码索引 (Hash)    │
                    │  - 用户邮箱索引 (Set)   │
                    └────────────────────────┘
```

---

## 流量路径详解

### 路径 1：静态页面访问（主要路径）

```
浏览器请求 → Nginx → Hugo 预生成的 HTML/CSS/JS 文件（磁盘）
```

所有博客文章、首页、关于页等均由 Hugo 在构建时生成静态文件，Nginx 直接返回，无后端交互。

### 路径 2：用户认证流程

```
浏览器 → POST /user/login    → Nginx rewrite_by_lua_file → lua/user.lua → Redis (读用户Hash) + ngx.shared.dict (写Token)
浏览器 → POST /user/register → Nginx rewrite_by_lua_file → lua/user.lua → Redis (写用户Hash + 索引) + ngx.shared.dict (写IP限制)
浏览器 → POST /user/info     → Nginx rewrite_by_lua_file → lua/user.lua → ngx.shared.dict (读Token) → Redis (读用户Hash)
```

Nginx 配置片段（`nginx/nginx.conf`）：

```nginx
location /user {
    # CORS 处理
    if ($http_referer ~* '^https?://game\.domain\.com') {
        add_header Access-Control-Allow-Origin $http_origin always;
        add_header Access-Control-Allow-Credentials true always;
    }
    rewrite_by_lua_file /www/server/nginx/waf/game_user.lua;
}
```

### 路径 3：短链接跳转流程

```
浏览器 → GET /url?id=xxx → Nginx rewrite_by_lua_file → lua/url.lua
  → ngx.shared.dict 验证 Token + 频率限制
  → Redis 读取 g_urls Hash 获取真实 URL
  → Redis 读取用户数据，检查金币/设备数
  → Redis 更新用户 urlclicks 计数
  → ngx.redirect(真实URL, 301)
```

### 路径 4：管理接口

```
客户端 → POST /admin/url → Nginx → lua/admin.lua → 验证时间戳+Token签名 → Redis HSET g_urls
```

### 前后端 API 端点映射

| 端点 | 方法 | Lua 处理函数 | 说明 |
|------|------|-------------|------|
| `/user/login` | POST | `Login()` | 用户登录 |
| `/user/register` | POST | `Register()` | 用户注册 |
| `/user/info` | POST | `UserInfo()` | 获取用户信息 |
| `/url?id=xxx` | GET | 主流程 | 短链接跳转 |
| `/admin/url` | POST | `HSetUrls()` | 管理员批量添加短链接 |

前端 API 基础地址：`https://gameapi.okxz.top`（硬编码在 `layouts/login/single.html` 和 `layouts/user/single.html` 中）。

---

## Redis Key 结构

所有 Key 均使用 `g_` 前缀（Lua 代码中 `PRE = 'g_'`）。

### Hash 类型

| Key 模式 | 字段 | 说明 |
|----------|------|------|
| `g_user_{email}` | `id` | 用户唯一 ID（自增） |
| | `name` | 用户昵称 |
| | `email` | 邮箱地址 |
| | `pwd` | 密码（**明文存储**） |
| | `coins` | 金币余额（注册送 10，邀请返利 +100） |
| | `urlclicks` | 累计点击/下载次数 |
| | `devices` | 设备/IP 变更次数 |
| | `invites` | 成功邀请人数 |
| | `inviteby` | 被谁邀请（邀请码/用户 ID） |
| | `ip` | 最近 IPv4 地址 |
| | `ipv6` | 最近 IPv6 地址 |
| `g_urls` | `{短链ID}` → `{真实URL}` | 所有短链接映射，一个 Hash 存全部 |
| `g_invite_codes_index` | `{userID}` → `{email}` | 邀请码 → 邮箱映射（userID 即为邀请码） |

### String 类型

| Key | 值 | 说明 |
|-----|----|------|
| `g_all_users_count` | 整数 | 用户总数计数器，用于分配新用户 ID |

### Set 类型

| Key | 成员 | 说明 |
|-----|------|------|
| `g_users_index` | `{email}` | 所有已注册邮箱集合，用于遍历/查重 |

### 内存缓存 Key（ngx.shared.dict `limit`）

| Key 模式 | TTL | 说明 |
|----------|-----|------|
| `g_token_{md5hash}` | 8640000s (~100天) | 登录 Token → 邮箱映射 |
| `g_reg_ip_{ip}` | 604800s (7天) | IP 注册限制（7天内不可重复注册） |
| `g_click_rate_{token}` | 604800s (7天) | 7天累计点击次数（上限 128） |
| `g_click_rate_daily_{token}` | 90000s (~25h) | 单日点击次数（上限 10） |

---

## 认证流程

```
注册: POST /user/register
  → 参数: email, name, pwd, inviteby(可选)
  → 创建 g_user_{email} Hash
  → 写入 g_users_index Set
  → 写入 g_invite_codes_index Hash
  → 如有 inviteby，调用 Invite() 返利

登录: POST /user/login
  → 参数: email, pwd
  → 读取 g_user_{email} Hash
  → 比对密码（明文比对）
  → 生成 Token = md5(name + pwd)
  → 写入 ngx.shared.dict: g_token_{token} → email
  → 设置 Cookie: token={token}; Max-Age=8640000

鉴权: POST /user/info 或 GET /url
  → 读取 Cookie: token
  → 从 ngx.shared.dict 查询 g_token_{token} → email
  → 用 email 从 Redis 读取用户数据
```

---

## 前端与后端的数据流

```
┌─────────────────────────────────────────────────────┐
│                    浏览器端                          │
│                                                     │
│  /in (登录页)                                       │
│    │ JS → POST https://gameapi.okxz.top/user/login   │
│    │ 成功 → localStorage.setItem("email", ...)       │
│    │ 跳转 → /user                                    │
│    │                                                 │
│  /user (用户中心)                                    │
│    │ JS → POST https://gameapi.okxz.top/user/info    │
│    │ 渲染: 名称/邮箱/金币/下载次数/邀请链接            │
│    │                                                 │
│  / (首页)                                            │
│    │ JS → URL参数 → localStorage.setItem("inviteby") │
│    │                                                 │
│  /url?id=xxx (短链接跳转)                             │
│    │ 自动触发，无需JS                                  │
│    │ Lua 直接 302/301 跳转                            │
└─────────────────────────────────────────────────────┘
```

**注意：** 前端页面由 Hugo 渲染后静态托管，但 API 请求发往独立的 API 域名 `gameapi.okxz.top`，意味着 Nginx 需要为 API 域名单独配置 location。
