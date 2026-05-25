import fs from 'node:fs'
import path from 'node:path'
import matter from 'gray-matter'
import Unocss from 'unocss/vite'
import { defineConfig } from 'vitepress'
import { version } from '../../package.json'

export default defineConfig({
  base: '/my-blog/',
  description: '记录10年Java工程经验、AI实践与每日技术资讯的个人博客。',
  ignoreDeadLinks: true,
  markdown: {
    headers: {
      level: [0, 0],
    },
  },
  themeConfig: {
    footer: {
      message: '10年Java工程实践 · AI Blog',
      copyright: 'Copyright © 2026 AI Blog',
    },
    search: {
      provider: 'local',
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/wuxw2569/my-blog' },
    ],
    editLink: {
      pattern: 'https://github.com/sfxcode/vitepress-blog-starter/edit/main/docs/:path',
      text: 'Edit this page on GitHub',
    },
    nav: nav(),
    sidebar: {
      '/guide/': sidebarGuide(),
      '/config/': sidebarConfig(),
      '/blog/': sidebarBlog(),
    },
    blog: {
      title: 'My Blog',
      description: 'Java架构、网络、数据与工具实践笔记',
    },

  },
  title: 'Java AI Blog',
  vite: {
    plugins: [
      Unocss({
        configFile: '../../unocss.config.ts',
      }),
    ],
  },
})

function nav() {
  return [
    { text: '指南', link: '/guide/', activeMatch: '/guide/' },
    { text: '配置', link: '/config/', activeMatch: '/config/' },
    { text: '博客', link: '/blog/', activeMatch: '/blog/' },
    { text: 'AI 日报', link: '/daily', activeMatch: '/daily' },
    {
      text: '外部文档',
      items: [
        {
          text: 'Vitepress',
          link: 'https://vitepress.vuejs.org',
        },
        {
          text: 'UnoCSS',
          link: 'https://uno.antfu.me',
        },
      ],
    },
    {
      text: version,
      items: [
        {
          text: '变更日志',
          link: 'https://github.com/sfxcode/vitepress-blog-starter/blob/main/CHANGELOG.md',
        },
      ],
    },
  ]
}

function sidebarGuide() {
  return [
    {
      text: '开始',
      collapsible: true,
      items: [
        { text: '博客指南', link: '/guide/' },
      ],
    },
    {
      text: '核心特性',
      collapsible: true,
      items: [
        { text: '博客文章系统', link: '/guide/' },
        { text: 'AI 每日日报', link: '/daily' },
        { text: '多作者支持', link: '/guide/' },
        { text: '内置搜索', link: '/guide/' },
      ],
    },
    {
      text: '技术栈',
      collapsible: true,
      items: [
        { text: 'UnoCSS 使用指南', link: '/guide/features/unocss' },
        { text: 'VitePress 配置', link: '/config/' },
        { text: 'UnoCSS 配置详情', link: '/config/unocss' },
      ],
    },
    {
      text: '快速导航',
      collapsible: true,
      items: [
        { text: '浏览博客文章', link: '/blog/' },
        { text: '查看 AI 日报', link: '/daily' },
      ],
    },
  ]
}

function sidebarConfig() {
  return [
    {
      text: '基础配置',
      items: [
        { text: '配置指南', link: '/config/' },
        { text: 'UnoCSS', link: '/config/unocss' },
      ],
    },
    {
      text: '站点功能',
      collapsible: true,
      items: [
        { text: '导航栏配置', link: '/config/#导航栏配置' },
        { text: '侧边栏配置', link: '/config/#侧边栏配置' },
        { text: '搜索功能', link: '/config/#搜索功能配置' },
        { text: '部署（Netlify）', link: '/config/#部署配置netlify' },
      ],
    },
    {
      text: '主题定制',
      collapsible: true,
      items: [
        { text: '主题色定制', link: '/config/unocss/#主题色定制' },
        { text: '自定义规则', link: '/config/unocss/#如何添加新的预设或规则' },
        { text: '工具类速查', link: '/config/unocss/#常用工具类速查' },
      ],
    },
  ]
}

function sidebarBlog() {
  const postsDir = path.resolve(__dirname, '../blog/posts')

  // 标签到分类的映射
  const categoryMap: Record<string, string[]> = {
    'AI 与智能': ['AI', 'AI基础', 'AI工具', 'Agent', '智能体', 'NLP', 'LLM', 'Spring AI', 'Machine Learning', 'Deep Learning', 'RAG', 'Prompt'],
    '全栈开发': ['全栈开发', '前端', '后端', 'Vue', 'React', 'Spring Boot', 'Java', 'JavaScript', 'TypeScript', 'Node.js', 'Web开发', 'UI设计'],
    'Python': ['Python', '爬虫', 'Flask', 'Django', 'FastAPI'],
    '自动化与测试': ['自动化', '自动化测试', '测试用例生成', '代码注释', 'CI/CD'],
    '数据与可视化': ['数据', 'SQL', '可视化', '报表', '数据库', 'MySQL', 'Redis', 'Elasticsearch'],
    '网络与安全': ['网络', '安全', 'API', 'HTTP', 'WebSocket'],
    'DevOps 与运维': ['部署', '网站监控', 'Docker', 'Kubernetes', 'Linux', '服务器', '云服务'],
    '知识管理': ['知识管理', 'README', '文档编写', '博客发布', '个人网站', '笔记'],
    '项目管理': ['项目管理', '日报', '会议纪要', '周报', '程序员'],
    '架构设计': ['架构', '微服务', '设计模式', '高并发', '分布式'],
  }

  // 按分类收集文章
  const categorized: Record<string, { text: string, link: string, date: string }[]> = {}
  const uncategorized: { text: string, link: string, date: string }[] = []

  try {
    const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.md'))

    for (const file of files) {
      const fullPath = path.join(postsDir, file)
      try {
        const { data } = matter(fs.readFileSync(fullPath, 'utf-8'))
        const title = data.title || file.replace(/\.md$/, '')
        const link = `/blog/posts/${file.replace(/\.md$/, '.html')}`
        const date = data.date ? new Date(data.date).toLocaleDateString('zh-CN') : ''
        const tags: string[] = data.tags
          ? String(data.tags).split(',').map((t: string) => t.trim())
          : []

        let matched = false
        for (const [category, keywords] of Object.entries(categoryMap)) {
          if (tags.some(tag => keywords.includes(tag))) {
            if (!categorized[category]) categorized[category] = []
            categorized[category].push({ text: title, link, date })
            matched = true
            break
          }
        }
        if (!matched) {
          uncategorized.push({ text: title, link, date })
        }
      }
      catch { /* 跳过解析失败的文件 */ }
    }
  }
  catch { /* 目录不存在时返回空 */ }

  // 按分类定义顺序构建侧边栏，每个分类内按日期降序
  const orderedCategories = [
    'AI 与智能', '全栈开发', 'Python', '自动化与测试',
    '数据与可视化', '网络与安全', 'DevOps 与运维',
    '知识管理', '项目管理', '架构设计',
  ]

  const sidebar: { text: string, collapsed: boolean, items: { text: string, link: string }[] }[] = []

  for (const cat of orderedCategories) {
    if (categorized[cat]?.length) {
      const sorted = categorized[cat].sort((a, b) => b.date.localeCompare(a.date))
      sidebar.push({
        text: `${cat}（${sorted.length}）`,
        collapsed: true,
        items: sorted.map(p => ({ text: p.text, link: p.link })),
      })
    }
  }

  if (uncategorized.length) {
    const sorted = uncategorized.sort((a, b) => b.date.localeCompare(a.date))
    sidebar.push({
      text: `其他（${sorted.length}）`,
      collapsed: true,
      items: sorted.map(p => ({ text: p.text, link: p.link })),
    })
  }

  return sidebar
}
