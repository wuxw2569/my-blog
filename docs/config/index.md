# 配置指南

本博客基于 VitePress 构建，集成了 UnoCSS、Anu-Vue 组件库和 gray-matter 文章解析。以下是核心配置的完整说明。

## 项目架构总览

```
ai-blog/
├── docs/
│   ├── .vitepress/
│   │   ├── config.mts          # VitePress 主配置
│   │   └── theme/
│   │       ├── index.ts         # 主题入口，注册 Vue 组件
│   │       ├── components/      # 自定义 Vue 组件
│   │       └── home.css         # 首页样式
│   ├── blog/posts/              # 博客文章（Markdown）
│   ├── config/                  # 配置文档（当前页面）
│   ├── guide/                   # 使用指南
│   └── daily/                   # AI 日报
├── uno.config.ts → docs/uno.config.ts  # UnoCSS 配置
└── package.json
```

## VitePress 主配置

主配置文件位于 `docs/.vitepress/config.mts`，采用 `defineConfig` 定义，包含以下核心字段：

```ts
export default defineConfig({
  base: '/my-blog/',                    // Netlify 部署的基础路径
  description: '记录10年Java工程经验...', // 站点描述，用于 SEO
  ignoreDeadLinks: true,                // 构建时忽略死链接
  title: 'Java AI Blog',                // 站点标题
  // ...
})
```

### 基础路径

站点部署到 Netlify 的子路径 `/my-blog/`，所有内部链接和资源引用都会自动加上此前缀。如果更换部署方式，修改 `base` 字段即可。

### Markdown 扩展

```ts
markdown: {
  headers: {
    level: [0, 0],  // 不自动生成标题 ID（由主题自行处理）
  },
},
```

---

## 博客功能配置

博客功能通过 `themeConfig.blog` 配置，结合 gray-matter 解析文章 frontmatter 实现。

### 站点信息

```ts
themeConfig: {
  blog: {
    title: 'My Blog',
    description: 'Java架构、网络、数据与工具实践笔记',
  },
}
```

### 文章 frontmatter 规范

每篇博客文章（`docs/blog/posts/*.md`）使用 YAML frontmatter 描述元数据：

```yaml
---
title: 文章标题
date: 2026-05-25
tags: [AI, Spring Boot, Java]
author: 作者名
description: 文章摘要
---
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | 是 | 文章标题，同时用作侧边栏显示名 |
| `date` | 是 | 发布日期，用于排序（新的在前） |
| `tags` | 推荐 | 标签列表，用于分类和搜索 |
| `author` | 否 | 作者名，关联作者系统 |
| `description` | 否 | 文章摘要 |

### 文章分类机制

侧边栏中的文章按标签自动归类到以下分类：

| 分类 | 匹配的标签关键词 |
|------|----------------|
| AI 与智能 | AI, Agent, LLM, RAG, Prompt, NLP 等 |
| 全栈开发 | Vue, React, Spring Boot, Java, TypeScript 等 |
| Python | Python, Flask, Django, FastAPI 等 |
| 自动化与测试 | 自动化, CI/CD, 测试用例生成 等 |
| 数据与可视化 | SQL, MySQL, Redis, Elasticsearch 等 |
| 网络与安全 | API, HTTP, WebSocket, 安全 等 |
| DevOps 与运维 | Docker, Kubernetes, Linux, 云服务 等 |
| 知识管理 | 知识管理, 文档编写, 博客发布 等 |
| 项目管理 | 项目管理, 日报, 周报 等 |
| 架构设计 | 架构, 微服务, 设计模式, 高并发 等 |

未匹配任何分类的文章会归入「其他」分组。

### 自定义 Vue 组件

主题注册了以下全局组件，可在任意 Markdown 中使用：

| 组件 | 用途 |
|------|------|
| `<Feature />` | 首页功能展示卡片 |
| `<Posts />` | 文章列表 |
| `<Post />` | 单篇文章卡片 |
| `<PostDetail />` | 文章详情页 |
| `<PostIcon />` | 文章图标 |
| `<PostAuthor />` | 文章作者信息 |
| `<AuthorDetail />` | 作者详情页 |

---

## 导航栏配置

导航栏通过 `themeConfig.nav` 定义，当前配置如下：

```ts
function nav() {
  return [
    { text: '指南', link: '/guide/', activeMatch: '/guide/' },
    { text: '配置', link: '/config/', activeMatch: '/config/' },
    { text: '博客', link: '/blog/', activeMatch: '/blog/' },
    { text: 'AI 日报', link: '/daily', activeMatch: '/daily' },
    {
      text: '外部文档',
      items: [
        { text: 'Vitepress', link: 'https://vitepress.vuejs.org' },
        { text: 'UnoCSS', link: 'https://uno.antfu.me' },
      ],
    },
    {
      text: version,  // 来自 package.json 的版本号
      items: [
        { text: '变更日志', link: 'https://github.com/...' },
      ],
    },
  ]
}
```

### 添加新的导航项

在 `nav()` 函数中追加对象即可：

```ts
// 简单链接
{ text: '关于', link: '/about/' }

// 下拉菜单
{
  text: '工具',
  items: [
    { text: '在线工具', link: '/tools/online' },
    { text: '开发助手', link: '/tools/dev' },
  ],
}
```

`activeMatch` 用于控制导航项的高亮状态，匹配当前 URL 路径。

---

## 侧边栏配置

侧边栏按路由前缀分组，不同路径使用不同的侧边栏函数：

```ts
sidebar: {
  '/guide/': sidebarGuide(),    // 指南页面侧边栏
  '/config/': sidebarConfig(),  // 配置页面侧边栏
  '/blog/': sidebarBlog(),      // 博客文章侧边栏（动态生成）
}
```

### 指南侧边栏

手动定义，适合内容相对固定的页面：

```ts
function sidebarGuide() {
  return [
    {
      text: '介绍',
      collapsible: true,
      items: [
        { text: '什么是这个?', link: '/guide/' },
      ],
    },
    {
      text: '功能',
      collapsible: true,
      items: [
        { text: 'UnoCSS', link: '/guide/features/unocss' },
      ],
    },
  ]
}
```

### 博客侧边栏

动态生成，扫描 `docs/blog/posts/` 目录下所有 `.md` 文件，按 frontmatter 中的 `tags` 自动分类并按日期降序排列。

关键逻辑：
1. 读取所有文章的 frontmatter（title, date, tags）
2. 根据标签匹配分类关键词，分配到对应分类
3. 同一分类内按日期降序排序
4. 未匹配的文章归入「其他」分组

### 添加新的配置页面侧边栏项

在 `sidebarConfig()` 函数中添加条目：

```ts
function sidebarConfig() {
  return [
    {
      text: '配置',
      items: [
        { text: '介绍', link: '/config/' },
        { text: 'UnoCSS', link: '/config/unocss' },
        // 新增页面
        { text: '新页面', link: '/config/new-page' },
      ],
    },
  ]
}
```

---

## 搜索功能配置

站点使用 VitePress 内置的本地搜索，无需外部服务：

```ts
themeConfig: {
  search: {
    provider: 'local',
  },
}
```

本地搜索会在构建时生成索引，支持标题和正文内容的全文搜索。如需切换为 Algolia 搜索，可修改 `provider` 为 `'algolia'` 并配置相应的 API Key。

---

## 部署配置（Netlify）

### 构建命令

在 Netlify 的站点设置中配置：

| 设置项 | 值 |
|--------|-----|
| Build command | `pnpm build` |
| Publish directory | `docs/.vitepress/dist` |
| Node version | 18+ |

### 基础路径

由于站点部署在 `/my-blog/` 子路径下，`config.mts` 中已设置 `base: '/my-blog/'`。VitePress 会自动为所有内部链接和静态资源添加此前缀。

### Netlify 配置文件

如果需要自定义重定向或 Headers，可以在项目根目录创建 `netlify.toml`：

```toml
[build]
  command = "pnpm build"
  publish = "docs/.vitepress/dist"

[[redirects]]
  from = "/*"
  to = "/my-blog/index.html"
  status = 200
```

---

## 社交链接与页脚

### 社交链接

```ts
themeConfig: {
  socialLinks: [
    { icon: 'github', link: 'https://github.com/wuxw2569/my-blog' },
  ],
}
```

支持的图标类型：`github`、`twitter`、`discord`、`slack` 等，也可使用 SVG 自定义。

### 页脚

```ts
themeConfig: {
  footer: {
    message: '10年Java工程实践 · AI Blog',
    copyright: 'Copyright © 2026 AI Blog',
  },
}
```

---

## 页内编辑链接

```ts
themeConfig: {
  editLink: {
    pattern: 'https://github.com/.../edit/main/docs/:path',
    text: 'Edit this page on GitHub',
  },
}
```

点击页面底部的编辑链接可直接跳转到 GitHub 对应的源文件。`pattern` 中的 `:path` 会被替换为当前页面的相对路径。
