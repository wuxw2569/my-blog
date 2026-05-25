# 博客指南

欢迎来到 **Java AI Blog** -- 一个记录10年Java工程经验、AI实践与每日技术资讯的个人技术博客。

本指南将帮助你快速了解博客的功能、结构和使用方式。

## 博客简介

这是一个基于 VitePress 构建的个人技术博客，专注于以下几个方向：

- **架构设计**：Spring Boot、Spring Cloud、DDD、限流熔断与系统演进
- **网络与数据**：HTTP/TCP 排障、MySQL、Redis、Elasticsearch 实战
- **AI 与智能**：Agent、LLM、RAG、Prompt 工程、Spring AI
- **自动化工具**：Python 脚本、CI/CD、Docker、Linux 运维
- **每日 AI 日报**：自动订阅 AI 行业动态，追踪模型、工具和产品资讯

截至目前，博客已收录 **230+ 篇** 技术文章，持续更新中。

## 核心特性

### 博客文章系统

博客支持 Markdown 格式的文章，每篇文章包含以下元数据：

| 字段 | 说明 |
|------|------|
| `title` | 文章标题 |
| `date` | 发布日期 |
| `tags` | 标签分类（逗号分隔） |
| `summary` | 文章摘要 |
| `author` | 作者标识 |
| `cover` | 封面图片路径 |

文章按标签自动归类到以下分区：

- AI 与智能
- 全栈开发
- Python
- 自动化与测试
- 数据与可视化
- 网络与安全
- DevOps 与运维
- 知识管理
- 项目管理
- 架构设计

### AI 每日日报

博客集成了 AI 日报功能，自动抓取并整理每日 AI 行业热点，涵盖：

- 大模型最新进展
- AI 工具与产品发布
- 行业应用案例
- 开源项目动态

访问导航栏的 **AI 日报** 即可查看最新内容。

### 多作者支持

博客支持多作者系统，每篇文章可通过 `author` 字段指定作者，方便团队协作或记录不同技术方向的内容。

### 内置搜索

博客提供了本地全文搜索功能，可通过页面顶部的搜索框快速查找文章、标签或关键词。

## 快速开始

### 浏览文章

1. 点击导航栏 **博客** 进入文章列表
2. 左侧侧边栏按技术分类组织，点击展开感兴趣的分区
3. 每个分区内文章按日期降序排列，最新的在最上面

### 搜索内容

1. 按 `Ctrl + K`（Mac 为 `Cmd + K`）打开搜索框
2. 输入关键词，支持标题、标签和正文内容搜索
3. 从搜索结果中直接跳转到目标文章

### 查看 AI 日报

1. 点击导航栏 **AI 日报** 进入日报页面
2. 日报内容每日自动更新，追踪最新的 AI 行业动态

## 技术栈

本博客基于以下技术构建：

| 技术 | 用途 |
|------|------|
| [VitePress](https://vitepress.vuejs.org/) | 静态站点生成器，提供 Markdown 驱动的文档体验 |
| [Vue 3](https://vuejs.org/) | 前端框架，支持组合式 API |
| [UnoCSS](https://uno.antfu.me/) | 原子化 CSS 引擎，按需生成样式 |
| [gray-matter](https://github.com/jonschlinkert/gray-matter) | 解析 Markdown 文件的 YAML Frontmatter |
| [Netlify](https://www.netlify.com/) | 静态站点部署与托管 |

### 为什么选择这些技术

- **VitePress**：基于 Vite 构建，开发体验极快；Markdown 原生支持，适合技术写作
- **UnoCSS**：比 Tailwind CSS 更轻量，按需生成，零冗余样式
- **gray-matter**：在构建时解析文章元数据，实现标签分类和侧边栏自动生成

## 目录结构

```
docs/
├── index.md                 # 首页
├── daily.md                 # AI 日报页面
├── guide/                   # 指南
│   ├── index.md             # 指南概览（本页）
│   └── features/            # 功能介绍
│       └── unocss.md        # UnoCSS 使用说明
├── config/                  # 配置说明
│   ├── index.md
│   └── unocss.md            # UnoCSS 配置详情
├── blog/                    # 博客内容
│   └── posts/               # 文章目录（230+ 篇 Markdown）
├── public/                  # 静态资源
├── .vitepress/              # VitePress 配置
│   └── config.mts           # 站点配置（导航、侧边栏、博客设置）
└── uno.config.ts            # UnoCSS 配置文件
```

## 下一步

- 前往 [博客](/blog/) 开始阅读技术文章
- 查看 [AI 日报](/daily) 了解最新行业动态
- 了解 [UnoCSS](/guide/features/unocss) 在本项目中的使用方式
