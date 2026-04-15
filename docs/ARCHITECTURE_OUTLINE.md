# 项目架构与业务分布大纲

```
DoIt/
│
├── CHANGELOG.md
├── CLAUDE.md                          # Claude Code 项目指引
├── TODO.md                            # 开发待办事项
├── LICENSE
├── README.md / README.zh-cn.md
├── SECURITY.md
├── go.mod                             # Hugo 模块定义
├── theme.toml                         # Hugo 主题元数据
├── dependencies.json                  # 依赖版本锁定
├── package.json                       # Node.js 依赖声明
├── package-lock.json
├── tailwind.config.js                 # Tailwind CSS 配置（tw- 前缀）
├── .eslintrc.js                       # JS 代码规范
├── .gitignore
│
╔══════════════════════════════════════════════════════════════════════╗
║  一、静态与模板层 (Hugo Engine)                                      ║
╚══════════════════════════════════════════════════════════════════════╝
│
├── config/_default/                   # Hugo 站点核心配置
│   ├── config.toml                    # 站点基础配置（URL、语言、主题）
│   ├── params.toml                    # 主题参数与功能开关
│   ├── menu.toml                      # 导航菜单定义
│   ├── markup.toml                    # Markdown 渲染规则
│   ├── author.toml                    # 作者信息
│   ├── taxonomies.toml                # 分类体系（标签/分类/系列）
│   ├── outputs.toml                   # 页面输出格式
│   ├── outputFormats.toml             # 自定义输出格式
│   ├── mediaTypes.toml                # 媒体类型
│   ├── permalinks.toml                # 固定链接规则
│   ├── privacy.toml                   # 隐私服务配置
│   └── sitemap.toml                   # 站点地图配置
│
├── layouts/                           # Hugo Go 模板（82 个文件）
│   ├── index.html                     # 首页模板
│   ├── 404.html                       # 404 错误页
│   ├── robots.txt                     # 搜索引擎爬虫规则
│   ├── sitemap.xml                    # 站点地图
│   ├── index.json                     # JSON 搜索索引
│   ├── index.algolia.full.json        # Algolia 全文搜索索引
│   ├── index.rss.xml                  # RSS 订阅源
│   │
│   ├── _default/                      # 默认布局模板
│   │   ├── baseof.html                # 全局基础骨架
│   │   ├── single.html                # 通用文章详情页
│   │   ├── section.html               # 分类分区页
│   │   ├── summary.html               # 文章摘要卡片
│   │   ├── single.md                  # Markdown 单页输出
│   │   └── _markup/                   # Markdown 渲染钩子
│   │       ├── render-link.html
│   │       ├── render-image.html
│   │       ├── render-heading.html
│   │       └── render-codeblock-mermaid.html
│   │
│   ├── user/                          # 【用户中心页面】会员个人主页
│   │   └── single.html
│   │
│   ├── login/                         # 【登录/注册页面】用户认证前端
│   │   └── single.html
│   │
│   ├── info/                          # 站点信息页
│   │   └── single.html
│   │
│   ├── posts/                         # 文章专属模板
│   │   ├── single.html
│   │   └── rss.xml
│   │
│   ├── taxonomy/                      # 分类法模板
│   │   ├── list.html                  # 标签/分类列表页
│   │   ├── terms.html                 # 所有标签概览页
│   │   └── rss.xml
│   │
│   ├── partials/                      # 可复用组件（44 个）
│   │   ├── header.html                # 全局页头
│   │   ├── footer.html                # 全局页脚
│   │   ├── assets.html                # 资源加载器
│   │   ├── comment.html               # 评论系统集成
│   │   ├── init.html                  # 页面初始化
│   │   ├── paginator.html             # 分页器
│   │   ├── recentlyUpdated.html       # 最近更新列表
│   │   ├── related.html               # 相关文章推荐
│   │   │
│   │   ├── head/                      # <head> 区域子模块
│   │   │   ├── meta.html              # HTML 元信息
│   │   │   ├── link.html              # 外部样式/预加载
│   │   │   ├── seo.html               # SEO 优化标签
│   │   │   └── https.html             # HTTPS 强制跳转
│   │   │
│   │   ├── home/                      # 首页专属组件
│   │   │   └── profile.html           # 首页个人资料展示
│   │   │
│   │   ├── single/                    # 文章页子模块
│   │   │   ├── footer.html            # 文章页脚（版权/标签）
│   │   │   ├── sponsor.html           # 赞赏/打赏组件
│   │   │   └── outdatedArticleReminder.html  # 过期提醒
│   │   │
│   │   ├── user/                      # 【用户业务组件】
│   │   │   ├── profile.html           # 用户资料编辑卡
│   │   │   └── invite.html            # 【邀请码管理组件】
│   │   │
│   │   ├── plugin/                    # 功能插件
│   │   │   ├── analytics.html         # 流量统计
│   │   │   ├── image.html             # 图片懒加载/灯箱
│   │   │   ├── icon.html              # 图标渲染
│   │   │   ├── link.html              # 链接处理
│   │   │   ├── script.html            # 第三方脚本加载
│   │   │   ├── share.html             # 社交分享
│   │   │   ├── social.html            # 社交链接
│   │   │   ├── style.html             # 第三方样式加载
│   │   │   └── compatibility.html     # 浏览器兼容
│   │   │
│   │   ├── function/                  # 模板工具函数（9 个）
│   │   │   ├── content.html           # 内容处理
│   │   │   ├── author.html            # 作者信息提取
│   │   │   ├── path.html              # 路径处理
│   │   │   ├── resource.html          # 资源获取
│   │   │   ├── id.html                # 唯一 ID 生成
│   │   │   ├── fontawesome.html       # 图标类名转换
│   │   │   ├── getRemoteImage.html    # 远程图片抓取
│   │   │   ├── escape.html            # HTML 转义
│   │   │   ├── fraction.html          # 分数渲染
│   │   │   ├── checkbox.html          # 复选框渲染
│   │   │   ├── ruby.html              # 注音渲染
│   │   │   └── suffixValidation.html  # 后缀校验
│   │   │
│   │   ├── scratch/                   # 运行时脚本/样式注入
│   │   │   ├── script.html
│   │   │   ├── style.html
│   │   │   ├── configScript.html
│   │   │   └── commentScript.html
│   │   │
│   │   ├── rss/
│   │   │   └── item.html              # RSS 条目模板
│   │   │
│   │   └── meta/
│   │       └── author.html            # 结构化作者元数据
│   │
│   └── shortcodes/                    # 短代码（18 个）
│       ├── admonition.html            # 提示框
│       ├── bilibili.html              # B 站视频嵌入
│       ├── echarts.html               # ECharts 图表
│       ├── friend.html                # 友链卡片
│       ├── image.html                 # 增强图片
│       ├── link.html                  # 链接卡片
│       ├── mapbox.html                # 地图
│       ├── math.html                  # 数学公式
│       ├── mermaid.html               # Mermaid 流程图
│       ├── music.html / aplayer.html  # 音乐播放器
│       ├── audio.html                 # 音频播放器
│       ├── script.html                # 自定义脚本
│       ├── showcase.html              # 项目展示
│       ├── style.html                 # 自定义样式
│       ├── typeit.html                # 打字动画
│       └── version.html               # 版本标注
│
├── assets/                            # 源码资源（经 Hugo Pipes 处理）
│   │
│   ├── css/                           # 样式源码
│   │   ├── main.css                   # 主样式入口
│   │   ├── style.scss                 # SCSS 主入口
│   │   ├── tailwind.css               # Tailwind 入口文件
│   │   ├── user.scss                  # 【用户中心专属样式】
│   │   ├── login.scss                 # 【登录/注册专属样式】
│   │   ├── color.css                  # 主题色定义
│   │   ├── _variables.scss            # SCSS 全局变量
│   │   ├── _override.scss             # 样式覆写
│   │   ├── _custom.scss               # 用户自定义样式
│   │   ├── _core/                     # 核心布局样式
│   │   │   ├── _base.scss             # 基础重置
│   │   │   ├── _layout.scss           # 布局框架
│   │   │   └── _media.scss            # 响应式断点
│   │   ├── _mixin/                    # SCSS 混入工具
│   │   │   ├── _blur.scss             # 模糊效果
│   │   │   ├── _compatibility.scss    # 兼容性处理
│   │   │   ├── _link.scss             # 链接样式
│   │   │   └── _index.scss            # 混入索引
│   │   ├── _page/                     # 页面级样式
│   │   │   ├── _home.scss             # 首页
│   │   │   ├── _single.scss           # 文章页
│   │   │   ├── _archive.scss          # 归档页
│   │   │   ├── _taxonomy.scss         # 分类页
│   │   │   ├── _404.scss              # 404 页
│   │   │   ├── _special.scss          # 特殊页
│   │   │   └── _index.scss
│   │   └── _partial/                  # 组件级样式（19 个）
│   │       ├── _header.scss / _footer.scss
│   │       ├── _pagination.scss / _cookieconsent.scss
│   │       ├── _details.scss / _mask.scss
│   │       ├── _icon.scss / _fixed-button.scss
│   │       ├── _archive/              # 归档子样式
│   │       └── _single/               # 文章页子样式
│   │           ├── _code.scss         # 代码高亮
│   │           ├── _admonition.scss   # 提示框
│   │           ├── _katex.scss        # 数学公式
│   │           ├── _echarts.scss      # 图表
│   │           ├── _bilibili.scss     # B站嵌入
│   │           ├── _friend.scss       # 友链
│   │           ├── _comment.scss      # 评论
│   │           ├── _mapbox.scss       # 地图
│   │           └── _footer.scss       # 文章页脚
│   │
│   ├── js/                            # JavaScript 源码
│   │   ├── theme.js                   # 主题核心逻辑（主题切换/搜索/暗色模式等）
│   │   ├── sw.js                      # Service Worker 离线缓存
│   │   ├── lib/                       # 功能模块加载器（14 个）
│   │   │   ├── aplayer.js / artalk.js / echarts.js
│   │   │   ├── cookieconsent.js / giscus.js / gitalk.js
│   │   │   ├── katex.js / remark42.js / twemoji.js
│   │   │   ├── twikoo.js / utterances.js / valine.js
│   │   │   ├── vssue.js / waline.js
│   │   └── shims/                     # 模块兼容垫片（10 个）
│   │
│   ├── lib/                           # 第三方库（28+ 套，本地托管）
│   │   ├── algoliasearch/             # Algolia 搜索 SDK
│   │   ├── animate/                   # CSS 动画库
│   │   ├── aplayer/                   # 音乐播放器
│   │   ├── artalk/                    # Artalk 评论系统
│   │   ├── autocomplete/             # 自动补全
│   │   ├── clipboard/                 # 剪贴板操作
│   │   ├── cookieconsent/             # Cookie 同意
│   │   ├── echarts/                   # 数据可视化
│   │   ├── fontawesome-free/          # 图标字体
│   │   ├── fuse/                      # 模糊搜索引擎
│   │   ├── gitalk/                    # Gitalk 评论
│   │   ├── katex/                     # 数学公式渲染
│   │   ├── lightgallery/              # 图片灯箱
│   │   ├── mapbox-gl/                 # 地图
│   │   ├── meting/                    # 音乐接口
│   │   ├── normalize/                 # CSS 重置
│   │   ├── object-fit-images/         # 图片适配兼容
│   │   ├── sharer/                    # 社交分享
│   │   ├── simple-icons/              # 品牌图标（2,186 个 SVG）
│   │   ├── tablesort/                 # 表格排序
│   │   ├── twemoji/                   # Twitter Emoji
│   │   ├── twikoo/                    # Twikoo 评论
│   │   ├── typeit/                    # 打字动画
│   │   ├── valine/                    # Valine 评论
│   │   ├── vue/                       # Vue.js 运行时
│   │   ├── vssue/                     # Vssue 评论
│   │   └── waline/                    # Waline 评论
│   │
│   ├── data/                          # Hugo 数据文件
│   │   ├── cdn/jsdelivr.yml           # CDN 地址映射
│   │   ├── emoji/                     # Emoji CDN 配置（Apple/Google/Twitter/Facebook）
│   │   ├── social.yml                 # 社交平台链接模板
│   │   └── polyfill.yml               # Polyfill 配置
│   │
│   ├── svg/
│   │   ├── icons/                     # 主题 SVG 图标
│   │   └── version.template.svg       # 版本徽章模板
│   │
│   └── images/
│       └── avatar.webp                # 默认头像
│
├── content/                           # 站点内容（Markdown）
│   ├── about.md                       # 关于页
│   ├── info.md                        # 信息页
│   ├── user.md                        # 【用户中心入口内容】
│   └── in.md                          # 邀请/说明页
│
├── static/                            # 静态文件（直接服务）
│   ├── favicon.ico + 各尺寸图标       # 站点图标套件
│   ├── site.webmanifest               # PWA 清单
│   ├── images/
│   │   └── avatar.png                 # 默认头像
│   └── lib/                           # 编译后/字体的静态资源
│       ├── fonts/                     # lightgallery 字体
│       ├── img/                       # lightgallery 图片
│       ├── katex/fonts/               # KaTeX 数学字体（33 个）
│       └── webfonts/                  # FontAwesome 字体（15 个）
│
├── i18n/                              # 国际化翻译（26 种语言）
│   └── {am,ar,ca,de,en,es,fr,zh-CN...}.toml
│
├── archetypes/
│   └── default.md                     # Hugo 内容模板
│
╔══════════════════════════════════════════════════════════════════════╗
║  二、动态引擎层 (OpenResty / Lua)                                    ║
╚══════════════════════════════════════════════════════════════════════╝
│
├── lua/                               # OpenResty Lua 业务脚本
│   ├── user.lua                       # 【用户认证】登录/注册/会话管理（Redis 后端）
│   ├── url.lua                        # 【短链接服务】URL 缩短与 302 重定向
│   ├── admin.lua                      # 【后台管理】管理操作接口
│   ├── util.lua                       # 【共享工具库】Redis 连接池、HTTP 响应辅助
│   └── test.lua                       # 接口测试脚本
│
├── nginx/
│   └── nginx.conf                     # Nginx 主配置（含 Lua 路由与 rewrite 规则）
│
╔══════════════════════════════════════════════════════════════════════╗
║  三、配置与工具层                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
│
├── package.json                       # Node 依赖与 npm scripts
├── package-lock.json
├── tailwind.config.js                 # Tailwind 配置（tw- 前缀、暗色模式策略）
├── .eslintrc.js                       # ESLint 规则
├── go.mod                             # Hugo Module 声明
├── theme.toml                         # Hugo 主题注册信息
├── dependencies.json                  # 版本锁定
├── .gitignore
│
╔══════════════════════════════════════════════════════════════════════╗
║  四、文档与示例站点                                                  ║
╚══════════════════════════════════════════════════════════════════════╝
│
├── docs/                              # 项目文档
│   ├── ARCHITECTURE.md                # 架构设计文档
│   ├── ARCHITECTURE_OUTLINE.md        # 本文件 — 项目架构与业务分布大纲
│   ├── BUSINESS_LOGIC.md              # 业务逻辑文档
│   ├── FRONTEND_GUIDE.md              # 前端开发指南
│   └── lua 会员 逻辑 调查报告.md      # 会员系统调查报告
│
└── exampleSite/                       # Hugo 开发测试站点
    ├── hugo.toml                      # 测试站点主配置
    ├── schema.json
    ├── config/_default/               # 17 个配置文件（含中英文多语言）
    ├── content/                       # 测试内容
    │   ├── posts/                     # 示例文章（50+ 篇）
    │   ├── about/ / authors/          # 关于页/作者页
    │   ├── categories/ / tags/        # 分类与标签内容
    │   ├── series/                    # 系列文章
    │   ├── showcase/                  # 项目展示
    │   └── offline/                   # 离线页
    ├── data/authors/                  # 测试作者数据
    └── static/                        # 测试站点静态资源
```

## 架构总览

| 模块 | 核心目录 | 关键技术 | 业务职责 |
|------|----------|----------|----------|
| **静态与模板层** | `layouts/`, `assets/`, `config/`, `content/` | Hugo Go Templates, SCSS, Tailwind | 博客内容渲染、页面组装、主题样式、18 个短代码、26 种语言 |
| **动态引擎层** | `lua/`, `nginx/` | OpenResty, Lua, Redis | 用户注册/登录/会话、邀请码、短链接服务、后台管理 |
| **配置与工具层** | 根目录配置文件 | npm, Hugo Modules, ESLint | 构建流程、依赖管理、代码规范 |

## 用户系统数据流

用户系统的前端入口分布在 `layouts/user/`、`layouts/login/`、`assets/css/user.scss`、`assets/css/login.scss`，后端对应 `lua/user.lua`，通过 `nginx/nginx.conf` 路由粘合。Redis 使用 `g_` 前缀键存储用户数据、邀请码、短链接映射和会话 Token。
