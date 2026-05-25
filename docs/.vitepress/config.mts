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

function sidebarConfig() {
  return [
    {
      text: '配置',
      items: [
        { text: '介绍', link: '/config/' },
        { text: 'UnoCSS', link: '/config/unocss' },
      ],
    },
  ]
}
