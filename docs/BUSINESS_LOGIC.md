# 业务逻辑与安全规约

本文档基于对 `lua/` 目录下所有脚本的逆向分析，梳理核心业务流程和安全机制现状。

---

## 一、用户注册流程 (`lua/user.lua` → `Register()`)

### 流程图

```
POST /user/register
  │
  ├─ 校验参数: email, name, pwd (必填)
  ├─ 校验密码长度 >= 6
  ├─ 检查 IP 注册限制: MEM[g_reg_ip_{ip}] 是否存在
  │    └─ 存在 → 拒绝: "该IP重复注册"
  ├─ 查询 Redis: g_user_{email} 是否已存在
  │    └─ 存在 → 拒绝: "该邮箱已被注册"
  │
  ├─ 分配用户 ID: INCR g_all_users_count
  ├─ Pipeline 写入 g_user_{email} Hash:
  │    ├─ id = userID
  │    ├─ name = args['name']
  │    ├─ email = args['email']
  │    ├─ pwd = args['pwd']            ← 明文
  │    ├─ coins = 10                    ← 初始金币
  │    ├─ urlclicks = 0
  │    ├─ devices = 0
  │    ├─ invites = 0
  │    └─ inviteby = args['inviteby']   ← 如果有
  │
  ├─ 设置 IP 限制: MEM[g_reg_ip_{ip}] = 1, TTL=7天
  ├─ SADD g_users_index {email}
  ├─ HSET g_invite_codes_index {userID} {email}
  │
  └─ 如有 inviteby → 调用 Invite() 返利
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `email` | string | 是 | 邮箱，同时作为用户唯一标识 |
| `name` | string | 是 | 用户昵称 |
| `pwd` | string | 是 | 密码（最少 6 位） |
| `inviteby` | string | 否 | 邀请人 ID（首页 URL 参数自动存入 localStorage） |

### 响应格式

```
成功: status=ok&ok=注册成功_
失败: status=err&err=具体原因
```

---

## 二、邀请码返利流程 (`lua/user.lua` → `Invite()`)

```
Invite()
  │
  ├─ 查询 g_invite_codes_index: HGET {args['inviteby']} → email
  │    └─ 不存在 → "无法获取邀请人信息"
  │
  ├─ 读取邀请人数据: g_user_{email}
  │    └─ 不存在 → "邀请人不存在"
  │
  └─ Pipeline 更新邀请人:
       ├─ coins += 100    ← 每次邀请奖励 100 金币
       └─ invites += 1    ← 邀请计数 +1
```

### 邀请码机制

- 用户的 `userID`（自增数字）即为邀请码
- 邀请链接格式：`https://{domain}/in/?{userID}`
- 首页 `index.html` 中的 JS 自动将 URL 查询参数存入 `localStorage.inviteby`
- 注册时从 localStorage 读取并提交

---

## 三、用户登录流程 (`lua/user.lua` → `Login()`)

```
POST /user/login
  │
  ├─ 校验参数: email, pwd
  ├─ 读取 g_user_{email}: {name, email, pwd}
  │    ├─ 不存在 → "用户不存在"
  │    └─ pwd != args['pwd'] → "密码错误"
  │
  ├─ 生成 Token = md5(name + pwd)
  ├─ 写入内存: MEM[g_token_{token}] = email
  ├─ 设置 Cookie: token={token}; path=/; Max-Age=8640000
  │
  └─ 返回: status=ok&ok=loginsuccess&email=...&name=...
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `email` | string | 是 | 邮箱 |
| `pwd` | string | 是 | 密码 |

---

## 四、用户信息查询 (`lua/user.lua` → `UserInfo()`)

```
POST /user/info
  │
  ├─ 检查 Cookie: token
  │    └─ 无 → "还没登录"
  ├─ 查询内存: MEM[g_token_{token}] → email
  │    └─ 无 → "token错误"
  ├─ 读取 Redis: g_user_{email} → {id, name, email, coins, urlclicks, devices, invites}
  │
  └─ 返回: URLSearchParams 格式（所有字段）
```

---

## 五、短链接跳转流程 (`lua/url.lua`)

```
GET /url?id={短链ID}
  │
  ├─ 1. Token 验证
  │    ├─ 检查 Cookie: token
  │    ├─ 查询 MEM[g_token_{token}]
  │    └─ 无效 → 302 跳转登录页 /in
  │
  ├─ 2. 频率限制
  │    ├─ 日限: MEM[g_click_rate_daily_{token}] > 9 → 进入7天检查
  │    ├─ 7天限: MEM[g_click_rate_{token}] > 128 → "您点击太快了"
  │    └─ 否则: 计数 +1
  │
  ├─ 3. 查询短链接
  │    ├─ HGET g_urls {id} → 真实URL
  │    └─ 不存在 → 302 /info#下载链接不存在
  │
  ├─ 4. 查询用户
  │    ├─ MEM[g_token_{token}] → email
  │    ├─ HGETALL g_user_{email}
  │    └─ 不存在 → 302 登录页
  │
  ├─ 5. 金币检查
  │    └─ urlclicks > coins → "金币已用完-请充值或邀请返利"
  │
  ├─ 6. 设备检查
  │    └─ devices > 128 → "账号已失效-请重新购买账号"
  │
  ├─ 7. IP 变更检测
  │    ├─ 当前 IP != 已存 ip/ipv6
  │    ├─ 更新 IP + devices += 1
  │    └─ 提示: "您已使用新IP登录"
  │
  ├─ 8. 计数更新
  │    └─ HSET g_user_{email} urlclicks += 1
  │
  └─ 9. 跳转
       └─ ngx.redirect(真实URL, 301)
```

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | query string | 是 | 短链接 ID（`g_urls` Hash 的 field） |

---

## 六、管理接口 (`lua/admin.lua`)

```
POST /admin/url
  │
  ├─ URI 校验: 必须 == "/admin/url"
  ├─ Token 校验: CheckToken()
  │    ├─ 时间窗口: |当前时间 - cookie_time| < 10秒
  │    └─ 签名验证: cookie_token == md5("admintesttoken" + cookie_time)
  │
  └─ 批量写入: HSET g_urls {key} {value}
       └─ 限制: 单次最多 100 个参数
```

---

## 七、安全机制评估

### 现有安全措施

| 机制 | 实现方式 | 说明 |
|------|----------|------|
| IP 注册限制 | `ngx.shared.dict` 记录 IP，TTL 7 天 | 防止同一 IP 短时间重复注册 |
| 邮箱唯一 | Redis `g_users_index` Set 去重 | 防止重复注册 |
| 密码最低长度 | Lua 校验 >= 6 位 | 基础密码策略 |
| Token 鉴权 | Cookie + `ngx.shared.dict` | 登录态管理 |
| 管理员时间窗口 | 10 秒内有效 | 防重放攻击 |
| 管理员签名验证 | md5(固定密钥 + 时间戳) | 接口鉴权 |
| 点击频率限制 | 内存计数（日限 10 / 7天限 128） | 防刷量 |
| 设备数限制 | Redis 记录 devices 计数，上限 128 | 防账号共享 |

### 安全风险与建议

| 风险 | 严重程度 | 说明 |
|------|----------|------|
| **密码明文存储** | 🔴 高 | `pwd` 字段直接存储明文，应使用 bcrypt/scrypt 哈希 |
| **Token 可预测** | 🔴 高 | Token = md5(name + pwd)，已知用户名和密码即可伪造 |
| **管理员硬编码密钥** | 🔴 高 | `ADMIN_TOKEN = 'admintesttoken'` 写死在代码中 |
| **无 CSRF 防护** | 🟡 中 | POST 接口无 CSRF Token，仅依赖 Cookie |
| **无 HTTPS 强制** | 🟡 中 | 密码和 Token 以明文传输（依赖 Nginx 层面的 HTTPS 配置） |
| **Redis 无密码** | 🟡 中 | 生产环境 Redis 连接未设密码（`auth` 传 `nil`） |
| **内存缓存丢失** | 🟡 中 | `ngx.shared.dict` 在 Nginx 重启后丢失，所有用户需重新登录 |
| **无输入过滤** | 🟡 中 | 用户输入直接写入 Redis，无 XSS/注入过滤 |
| **点击限制在内存** | 🟢 低 | Nginx 重启后频率限制重置 |
| **无请求频率限制** | 🟢 低 | 登录/注册接口无请求频率限制，可被暴力破解 |

### 业务数据流（金币体系）

```
注册 → 初始金币 10
  │
  ├─ 邀请他人 → 邀请人 +100 金币
  │
  └─ 下载（短链接跳转）→ urlclicks += 1
       └─ 当 urlclicks > coins → 金币不足，跳转提示
```

金币消耗模型：每次通过 `/url` 跳转消耗 1 金币（urlclicks 计数增加），金币可通过邀请返利获得。
