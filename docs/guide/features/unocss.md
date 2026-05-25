# UnoCSS 使用指南

本项目使用 [UnoCSS](https://uno.antfu.me/) 作为原子化 CSS 引擎，替代传统的 Tailwind CSS，实现更轻量、更快速的样式开发体验。

## 什么是 UnoCSS

UnoCSS 是由 Anthony Fu 创建的即时原子化 CSS 引擎。与 Tailwind CSS 和 Windi CSS 不同，UnoCSS 没有内置核心工具类，所有功能都通过 Preset（预设）提供，具有极高的灵活性和性能。

核心特点：

- **按需生成**：只生成实际使用到的 CSS，产物体积最小
- **极速运行**：基于 Rust 编写的引擎，比 Tailwind CSS 快 5-100 倍
- **高度可扩展**：通过 Preset 和 Rule 自定义任意工具类
- **兼容模式**：默认预设兼容 Tailwind CSS / Windi CSS / Bootstrap 语法

## 本项目的 UnoCSS 配置

项目的 UnoCSS 配置文件位于 `docs/uno.config.ts`，核心配置如下：

```ts
import {
  defineConfig,
  presetIcons,
  presetUno,
  transformerDirectives,
  transformerVariantGroup,
} from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),           // 默认预设，兼容 Tailwind/Windi 语法
    presetIcons({          // 图标预设，支持任意图标作为类名
      scale: 1.2,
      unit: 'em',
    }),
  ],
  transformers: [
    transformerVariantGroup(),   // 变体组支持 hover:(bg-blue text-white)
    transformerDirectives(),     // 指令支持 @apply
  ],
  content: {
    pipeline: {
      include: ['./**/*.vue', './**/*.md'],  // 扫描 Vue 和 Markdown 文件
    },
  },
})
```

### 使用的预设说明

| 预设 | 作用 |
|------|------|
| `presetUno` | 默认预设，提供 Tailwind CSS / Windi CSS 兼容的工具类 |
| `presetIcons` | 图标预设，支持通过类名直接使用图标（如 `i-mdi-home`） |

### 使用的转换器说明

| 转换器 | 作用 |
|--------|------|
| `transformerVariantGroup` | 支持变体分组语法，如 `hover:(bg-blue-500 text-white)` |
| `transformerDirectives` | 支持在 CSS 中使用 `@apply` 指令复用工具类 |

## 常用工具类示例

### 布局

```html
<div class="flex items-center justify-between">
  <span class="text-lg font-bold">左侧</span>
  <span class="text-sm text-gray-500">右侧</span>
</div>
```

### 间距与尺寸

```html
<div class="p-4 m-2 w-full max-w-4xl mx-auto">
  <div class="h-16 w-16 rounded-full bg-blue-500"></div>
</div>
```

### 文字与颜色

```html
<h1 class="text-2xl font-bold text-gray-800">标题</h1>
<p class="text-base text-gray-600 leading-relaxed">正文内容</p>
<a class="text-blue-500 hover:text-blue-700 underline">链接</a>
```

### 响应式

```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <!-- 移动端单列，平板双列，桌面三列 -->
</div>
```

### 暗色模式

```html
<div class="bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200">
  自适应暗色模式的内容
</div>
```

### 图标使用

配合 `presetIcons`，可直接通过类名使用图标：

```html
<span class="i-mdi-home text-xl"></span>      <!-- Material Design 图标 -->
<span class="i-carbon-search"></span>          <!-- Carbon 图标 -->
<span class="i-logos-vue text-2xl"></span>     <!-- Logo 图标 -->
```

## 如何自定义配置

### 添加自定义规则

在 `uno.config.ts` 中通过 `rules` 添加自定义工具类：

```ts
export default defineConfig({
  rules: [
    // 自定义渐变文字
    ['gradient-text', {
      'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      '-webkit-background-clip': 'text',
      '-webkit-text-fill-color': 'transparent',
    }],
    // 支持动态值的规则
    [/^grid-gap-(\d+)$/, ([, d]) => ({ 'grid-gap': `${d / 4}rem` })],
  ],
})
```

### 添加自定义快捷方式

通过 `shortcuts` 定义常用的组合样式：

```ts
export default defineConfig({
  shortcuts: {
    'btn-primary': 'px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition',
    'card': 'p-4 bg-white rounded-lg shadow-md dark:bg-gray-800',
    'section-title': 'text-xl font-bold text-gray-800 dark:text-gray-100 mb-4',
  },
})
```

使用时只需一个类名：

```html
<button class="btn-primary">提交</button>
<div class="card">卡片内容</div>
```

### 添加更多预设

如果需要 Tailwind CSS 的排版样式，可以添加 `presetTypography`：

```ts
import presetTypography from '@unocss/preset-typography'

export default defineConfig({
  presets: [
    presetUno(),
    presetIcons({ scale: 1.2, unit: 'em' }),
    presetTypography(),  // 添加排版预设
  ],
})
```

## 在 VitePress 中的集成

UnoCSS 通过 Vite 插件方式集成到 VitePress 中，配置位于 `.vitepress/config.mts`：

```ts
import Unocss from 'unocss/vite'

export default defineConfig({
  vite: {
    plugins: [
      Unocss({
        configFile: '../../unocss.config.ts',
      }),
    ],
  },
})
```

这样，在 Markdown 文件和 Vue 组件中都可以直接使用 UnoCSS 的工具类。

---

<Feature/>
