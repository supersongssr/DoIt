# 前端组件与样式指南

## 一、自定义 Shortcodes

所有短代码定义在 `layouts/shortcodes/` 下，可在 Markdown 内容中通过 `{{</* shortcode */>}}` 或 `{{%/* shortcode */%}}` 调用。

### 1. admonition — 提示框

创建可折叠的提示框（callout），支持 12 种类型。

```markdown
{{</* admonition type="warning" title="注意" open="true" */>}}
提示内容
{{</* /admonition */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 默认值 | 说明 |
|------|-------------|----------|--------|------|
| type | 1 | `type` | `"note"` | 提示类型 |
| title | 2 | `title` | 类型对应的翻译文本 | 自定义标题 |
| open | 3 | `open` | `true` | 是否默认展开 |

**支持的 type 值：** `note`, `abstract`, `info`, `tip`, `success`, `question`, `warning`, `failure`, `danger`, `bug`, `example`, `quote`

---

### 2. aplayer — 音频播放器

嵌入 APlayer 音乐播放器，支持播放列表。

```markdown
{{</* aplayer autoplay="false" volume="0.7" */>}}
{{</* audio name="歌名" artist="歌手" url="/music/song.mp3" cover="/images/cover.jpg" */>}}
{{</* audio name="歌名2" artist="歌手2" url="/music/song2.mp3" */>}}
{{</* /aplayer */>}}
```

**参数（仅命名参数）：**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `fixed` | - | 固定底部播放器 |
| `mini` | - | 迷你模式 |
| `autoplay` | - | 自动播放 |
| `theme` | - | 主题颜色 |
| `loop` | - | 循环模式（all/one/none） |
| `order` | - | 播放顺序（list/random） |
| `preload` | - | 预加载（none/metadata/auto） |
| `volume` | - | 音量 0-1 |
| `mutex` | - | 互斥播放 |
| `lrcType` | - | 歌词类型 |
| `listFolded` | - | 列表默认折叠 |
| `listMaxHeight` | - | 列表最大高度 |
| `storageName` | - | 设置存储键名 |

**内部内容：** 使用 `{{</* audio */>}}` 子短代码定义播放列表中的曲目。

---

### 3. audio — 音频曲目定义

定义 APlayer 播放列表中的单曲。**必须嵌套在 `aplayer` 内使用。**

```markdown
{{</* audio name="歌名" artist="歌手" url="/music/song.mp3" cover="/cover.jpg" lrc="/lyrics.lrc" */>}}
可选：歌词内容作为内部文本
{{</* /audio */>}}
```

**参数（仅命名参数）：**

| 参数 | 说明 |
|------|------|
| `name` | 曲目名称 |
| `artist` | 艺术家 |
| `url` | 音频文件 URL |
| `cover` | 封面图 URL |
| `lrc` | 歌词文件 URL |
| `theme` | 此曲目的主题色 |
| `type` | 音频类型 |

---

### 4. bilibili — B站视频

嵌入 Bilibili 视频播放器。

```markdown
{{</* bilibili id="BV1xx411c7mD" p="1" */>}}
{{</* bilibili "BV1xx411c7mD" "2" */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 默认值 | 说明 |
|------|-------------|----------|--------|------|
| id | 1 | `id` | 必填 | BVID 视频ID |
| p | 2 | `p` | `1` | 分P序号 |

---

### 5. echarts — 数据可视化图表

嵌入 Apache ECharts 图表。

```markdown
{{</* echarts width="100%" height="30rem" */>}}
{
  "xAxis": {"type": "category", "data": ["A","B","C"]},
  "yAxis": {"type": "value"},
  "series": [{"data": [120, 200, 150], "type": "bar"}]
}
{{</* /echarts */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 默认值 | 说明 |
|------|-------------|----------|--------|------|
| width | 1 | `width` | `"100%"` | 图表宽度 |
| height | 2 | `height` | `"30rem"` | 图表高度 |

**内部内容：** ECharts option 的 JSON 配置。

---

### 6. friend — 友情链接

创建友链卡片。

```markdown
{{</* friend name="博客名" url="https://example.com" avatar="/avatar.png" bio="一句简介" */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 说明 |
|------|-------------|----------|------|
| name | 1 | `name` | 友链名称 |
| url | 2 | `url` | 链接地址 |
| avatar | 3 | `avatar` | 头像图片 URL |
| bio | 4 | `bio` | 简介文字 |

---

### 7. image — 增强图片

支持响应式、lightbox、标题的图片组件。

```markdown
{{</* image src="/photo.jpg" alt="描述" caption="图注" src_s="/photo-small.jpg" src_l="/photo-large.jpg" */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 默认值 | 说明 |
|------|-------------|----------|--------|------|
| src | 1 | `src` | 必填 | 图片路径 |
| alt | 2 | `alt` | - | 替代文本 |
| caption | 3 | `caption` | - | 图片标题/图注 |
| - | - | `src_s` | - | 小图（响应式） |
| - | - | `src_l` | - | 大图（响应式） |
| - | - | `height` | - | 高度 |
| - | - | `width` | - | 宽度 |
| - | - | `linked` | caption 存在时 true | 点击放大 |
| - | - | `class` | - | figure CSS 类 |

---

### 8. link — 卡片链接

```markdown
{{</* link href="https://example.com" content="链接文字" title="提示" */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 说明 |
|------|-------------|----------|------|
| href | 1 | `href` | 链接地址 |
| content | 2 | `content` | 显示文字（默认为 href） |
| title | 3 | `title` | 标题提示 |
| - | - | `class` | CSS 类 |
| - | - | `rel` | rel 属性 |

---

### 9. mapbox — 地图嵌入

嵌入 Mapbox GL 交互地图。

```markdown
{{</* mapbox lng="116.40" lat="39.90" zoom="12" */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 默认值 | 说明 |
|------|-------------|----------|--------|------|
| lng | 1 | `lng` | 必填 | 经度 |
| lat | 2 | `lat` | 必填 | 纬度 |
| zoom | 3 | `zoom` | `10` | 缩放级别 |
| marked | 4 | `marked` | `true` | 显示标记 |
| light-style | 5 | `light-style` | 配置文件 | 亮色主题样式 URL |
| dark-style | 6 | `dark-style` | 配置文件 | 暗色主题样式 URL |
| - | - | `navigation` | 配置文件 | 导航控件 |
| - | - | `geolocate` | 配置文件 | 定位按钮 |
| - | - | `scale` | 配置文件 | 比例尺 |
| - | - | `fullscreen` | 配置文件 | 全屏按钮 |
| - | - | `width` | `"100%"` | 地图宽度 |
| - | - | `height` | `"20rem"` | 地图高度 |

---

### 10. math — 数学公式

包裹 KaTeX 数学公式内容。

```markdown
{{</* math */>}}
$$E = mc^2$$
{{</* /math */>}}
```

**参数：** 无。内部内容为数学公式文本。

---

### 11. mermaid — 流程图

嵌入 Mermaid 图表。

```markdown
{{</* mermaid */>}}
graph TD
    A[开始] --> B{判断}
    B -->|是| C[结果]
    B -->|否| D[结束]
{{</* /mermaid */>}}
```

**参数：** 无。内部内容为 Mermaid 语法。

---

### 12. music — 音乐播放器

通过 MetingJS 嵌入在线音乐（支持网易云、QQ 音乐等平台）。

```markdown
{{</* music server="netease" type="playlist" id="60198" */>}}
{{</* music url="/song.mp3" name="歌名" artist="歌手" cover="/cover.jpg" */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 说明 |
|------|-------------|----------|------|
| server | 1 | `server` | 平台：netease/tencent/kugou/baidu/xiami |
| type | 2 | `type` | 类型：song/playlist/album/search/artist |
| id | 3 | `id` | 音乐/歌单 ID |
| auto | 1 (URL模式) | `auto` | 自动解析 URL |
| - | - | `url` | 直链模式：音频 URL |
| - | - | `name` | 直链模式：歌名 |
| - | - | `artist` | 直链模式：歌手 |
| - | - | `cover` | 直链模式：封面 |
| - | - | `theme` | 主题色（默认 `#448aff`） |
| - | - | `fixed`/`mini`/`autoplay`/`loop`/`order`/`volume`/`mutex`/`list-folded`/`list-max-height` | APlayer 参数 |

---

### 13. script — 自定义脚本

注入自定义 JavaScript。

```markdown
{{</* script */>}}
console.log('Hello');
{{</* /script */>}}
```

**参数：** 无。内部内容为 JavaScript 代码。

---

### 14. showcase — 作品展示

创建带图片的作品展示卡片。

```markdown
{{</* showcase title="项目名" summary="项目简介" image="/screenshot.png" link="https://github.com/..." */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 默认值 | 说明 |
|------|-------------|----------|--------|------|
| title | 1 | `title` | 必填 | 项目标题 |
| summary | 2 | `summary` | - | 简介 |
| image | 3 | `image` | - | 截图 URL |
| link | 4 | `link` | - | 项目链接 |
| column | 5 | `column` | `"2"` | 列数 |
| link_extra | 6 | `link_extra` | - | 附加链接 |

---

### 15. style — 自定义样式

为内容包裹自定义 CSS 样式。

```markdown
{{</* style "text-align: center; color: red;" */>}}
居中的红色文字
{{</* /style */>}}
```

**参数：**

| 参数 | 位置参数序号 | 命名参数 | 默认值 | 说明 |
|------|-------------|----------|--------|------|
| CSS 样式 | 1 | - | - | 内联样式 |
| HTML 标签 | 2 | `tag` | `"div"` | 包裹标签 |
| - | - | `class` | - | CSS 类名 |

---

### 16. typeit — 打字动画

创建打字机效果。

```markdown
{{</* typeit code="javascript" */>}}
const msg = "Hello World";
{{</* /typeit */>}}
```

**参数：**

| 参数 | 命名参数 | 默认值 | 说明 |
|------|----------|--------|------|
| - | `class` | - | CSS 类 |
| - | `code` | - | 编程语言（启用代码高亮） |
| - | `tag` | `"div"` | 包裹 HTML 标签 |
| - | `group` | - | 分组键（多实例同步） |

---

### 17. version — 版本徽章

显示版本号徽章，链接到 GitHub Releases。

```markdown
{{</* version "1.2.3" "new" */>}}
```

**参数（位置参数）：**

| 序号 | 默认值 | 说明 |
|------|--------|------|
| 1 | 必填 | 版本号 |
| 2 | `"new"` | 类型：`new`(绿) / `changed`(蓝) / `deleted`(红) |

---

## 二、Tailwind CSS 使用情况

### 配置

```js
// tailwind.config.js
module.exports = {
  prefix: 'tw-',                          // 所有类使用 tw- 前缀
  content: ['./layouts/**/*.html'],       // 扫描模板文件
  theme: { extend: {} },
  plugins: []
}
```

### 使用方式

**Tailwind 类名仅在 `assets/css/tailwind.css` 源文件中通过 `@apply` 使用**，不在 Hugo 模板中直接引用。模板使用语义化 class 名（如 `page-home`、`summary-card`、`single`）。

`tailwind.css` 中通过 `@apply` 应用的样式：

```css
@layer base {
  h1 { @apply tw-text-3xl tw-font-bold tw-m-8; }
  h2 { @apply tw-text-2xl tw-font-bold tw-m-6; }
  h3 { @apply tw-text-xl tw-font-bold tw-m-4; }
  ol { @apply tw-list-decimal tw-list-outside; }
  ul { @apply tw-list-disc tw-list-outside; }
}
```

### 编译流程

```
tailwind.css (源文件, @apply)
    ↓ npx tailwindcss
main.css (编译产物, ~10KB)
    ↓ Hugo 直接引用
layouts/partials/head/link.html → 加载 css/main.css
```

**Tailwind 不经过 Hugo Pipes 处理**，是预编译后直接作为静态文件加载。

---

## 三、轻量化部署评估

### 结论：可以不依赖 npm 部署

| 组件 | 是否需要 npm | 说明 |
|------|-------------|------|
| Hugo 构建 | **不需要** | `hugo` 命令直接生成站点 |
| Tailwind CSS | **不需要** | 编译产物 `assets/css/main.css` 已提交到 Git |
| SCSS 编译 | **不需要** | Hugo Extended 内置支持 SCSS |
| 第三方 JS 库 | **不需要** | `assets/lib/` 和 `static/lib/` 已包含预编译文件 |
| NPM 包 | **不需要** | 仅用于开发时同步更新 `assets/lib/` |

### 最小部署依赖

```
hugo-extended (>= 0.83.0)    → 构建静态站点
OpenResty (Nginx + LuaJIT)   → 运行 Lua 脚本
Redis                         → 用户数据存储
```

### 部署步骤

```bash
# 1. 构建 Hugo 站点（无需 npm）
hugo --minify

# 2. 将 public/ 目录部署到 Nginx

# 3. 将 lua/ 目录部署到 OpenResty 可访问路径
#    例如: /www/server/nginx/waf/
#    并在 Nginx 配置中引用:
#    rewrite_by_lua_file /www/server/nginx/waf/game_user.lua;

# 4. 启动 Redis
redis-server

# 5. 确保 nginx.conf 中配置了:
#    - lua_shared_dict limit 10m;
#    - location /user { rewrite_by_lua_file ...; }
#    - location /url  { rewrite_by_lua_file ...; }
```

### 何时需要 npm

| 场景 | 命令 |
|------|------|
| 修改 Tailwind 源文件后重新编译 | `npm run build:tailwind` |
| 开发时热重载 Tailwind | `npm run server:tailwind` |
| 开发模式（Hugo + Tailwind 同时 watch） | `npm run dev` |
| 更新 `assets/lib/` 中的第三方库 | `npm run update-dependencies` |
| JS 代码检查 | `npx eslint assets/js/` |

### 生产部署建议

对于生产环境，建议使用预编译的 `main.css` 直接部署，**跳过 npm**，以减少部署复杂度和依赖。仅在需要修改 Tailwind 样式时才使用 npm 重新编译。
