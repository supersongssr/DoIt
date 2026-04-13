# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DoIt is a customized Hugo blog theme (forked from [HEIGE-PCloud/DoIt](https://github.com/HEIGE-PCloud/DoIt)) used as a standalone site called "游戏仓库" (Game Repository). It has been extended with a user authentication system, URL shortening service, and invite code system built on Nginx + OpenResty (Lua) + Redis.

## Development Commands

```bash
# Install dependencies
npm install

# Development (Hugo server + Tailwind watch)
npm run dev

# Hugo server only (with drafts)
npm run server

# Build Tailwind CSS
npm run build:tailwind

# Production build
npm run build

# Build with draft content
npm run build:preview

# Lint JS
npx eslint assets/js/
```

Hugo Extended v0.83.0+ is required. The dev server serves from `exampleSite/` with themesDir set to `../..`.

## Architecture

### Hugo Theme Layer
- **`layouts/`** - Hugo Go templates. `partials/` holds reusable components, `shortcodes/` has 18+ custom shortcodes, `_default/` has base layouts.
- **`assets/`** - Source assets: `css/` (SCSS + Tailwind entry), `js/` (theme JS), `lib/` (vendored third-party libs), `svg/` (icons).
- **`config/_default/`** - Hugo config split into multiple TOML files (`config.toml`, `params.toml`, `markup.toml`, etc.).
- **`i18n/`** - 26 language translation files.
- **`static/`** - Static assets served directly.
- **`exampleSite/`** - Example/test site content and config used for development.

### Dynamic Backend Layer (Nginx + Lua + Redis)
- **`lua/`** - OpenResty Lua scripts handling dynamic features that Hugo's static generation cannot:
  - `user.lua` - User login/register with Redis backend
  - `url.lua` - URL shortening and redirection
  - `admin.lua` - Admin operations
  - `util.lua` - Shared utilities (Redis connection, HTTP helpers)
- Redis stores user data, invite codes, URL mappings, and session tokens with key prefix `g_`.
- Custom Hugo layouts in `layouts/user/` and `layouts/login/` render the frontend for auth flows.

### Frontend Stack
- Tailwind CSS with `tw-` prefix (see `tailwind.config.js`)
- Hugo Pipes for asset processing
- Third-party JS libs vendored in `assets/lib/` and via npm

### Internationalization
- Translation files in `i18n/` follow Hugo's standard `.toml` format
- Default language is `zh-cn`

## Key Conventions

- Hugo templates use Go template syntax (`{{ }}`, `{{- -}}`)
- Lua scripts follow OpenResty conventions (`ngx.shared.dict`, `resty.redis`)
- Tailwind classes use `tw-` prefix to avoid conflicts with existing CSS
- All Redis keys use the `g_` prefix
- Site is deployed behind Nginx with OpenResty for Lua script execution
