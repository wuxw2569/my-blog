# UnoCSS 配置

UnoCSS 是一个原子化 CSS 引擎，本项目使用它来处理样式编写。以下是项目实际的 UnoCSS 配置说明和使用指南。

## 项目配置

配置文件位于 `docs/uno.config.ts`：

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
    presetUno(),
    presetIcons({
      scale: 1.2,
      unit: 'em',
    }),
  ],
  transformers: [
    transformerVariantGroup(),
    transformerDirectives(),
  ],
  content: {
    pipeline: {
      include: ['./**/*.vue', './**/*.md'],
    },
  },
})
```

### 已启用的预设

| 预设 | 说明 |
|------|------|
| `presetUno` | 默认预设，兼容 Tailwind CSS / Windi CSS 语法，提供完整的工具类集合 |
| `presetIcons` | 图标预设，支持以 CSS class 方式使用任意图标集，缩放比例 1.2em |

### 已启用的转换器

| 转换器 | 说明 |
|--------|------|
| `transformerVariantGroup` | 支持分组语法，如 `hover:(bg-blue text-white)` 代替 `hover:bg-blue hover:text-white` |
| `transformerDirectives` | 支持在 CSS 中使用 `@apply` 指令引入 UnoCSS 工具类 |

### 内容扫描范围

配置了 `content.pipeline.include`，仅扫描 Vue 组件和 Markdown 文件：

```ts
content: {
  pipeline: {
    include: ['./**/*.vue', './**/*.md'],
  },
},
```

这确保只有实际使用的工具类会被打包，保持产物体积最小。

---

## Vite 集成

在 `docs/.vitepress/config.mts` 中通过 Vite 插件方式加载 UnoCSS：

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

主题入口 `docs/.vitepress/theme/index.ts` 中通过 `import 'uno.css'` 引入生成的样式。

---

## 项目中使用的图标集

项目已安装以下图标集：

| 图标集 | npm 包 | 前缀示例 |
|--------|--------|----------|
| BoxIcons | `@iconify-json/bx` | `i-bx-xxx` |
| Fluent Emoji | `@iconify-json/fluent-emoji` | `i-fluent-emoji-xxx` |
| Heroicons Outline | `@iconify-json/heroicons-outline` | `i-heroicons-outline-xxx` |
| Logos | `@iconify-json/logos` | `i-logos-xxx` |

使用方式：

```html
<!-- BoxIcons -->
<span class="i-bx-home" />
<span class="i-bx-search" />

<!-- Heroicons -->
<span class="i-heroicons-outline-chart-bar" />

<!-- Logos -->
<span class="i-logos-vue" />
<span class="i-logos-spring-icon" />
```

---

## 如何添加新的预设或规则

### 添加官方预设

1. 安装预设包：

```bash
pnpm add -D @unocss/preset-xxx
```

2. 在 `docs/uno.config.ts` 中导入并注册：

```ts
import { presetAttributify } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetIcons({ scale: 1.2, unit: 'em' }),
    presetAttributify(),  // 新增
  ],
})
```

### 添加自定义规则

在配置文件中通过 `rules` 字段添加：

```ts
export default defineConfig({
  rules: [
    // 静态规则：class 名 -> CSS
    ['card-shadow', { 'box-shadow': '0 4px 12px rgba(0,0,0,0.08)' }],

    // 动态规则：正则匹配 + 返回函数
    [/^text-gradient-(.+)$/, ([, color]) => ({
      'background': `linear-gradient(135deg, ${color}, #0a7d70)`,
      '-webkit-background-clip': 'text',
      '-webkit-text-fill-color': 'transparent',
    })],
  ],
})
```

### 添加快捷方式（shortcuts）

将多个工具类组合为一个简短 class：

```ts
export default defineConfig({
  shortcuts: {
    'btn-primary': 'bg-[#0a7d70] text-white rounded-full px-6 py-2 font-650 hover:opacity-90 transition',
    'card': 'bg-white border border-[rgba(17,19,21,0.1)] rounded-28px p-7',
    'section-title': 'text-[clamp(34px,5vw,58px)] font-bold tracking-tight',
  },
})
```

使用方式：

```html
<button class="btn-primary">提交</button>
<div class="card">内容</div>
```

### 添加新的图标集

1. 安装对应的 Iconify 包：

```bash
pnpm add -D @iconify-json/carbon    # 例如 Carbon 图标
```

2. 无需修改配置，`presetIcons` 会自动识别已安装的图标集。

3. 直接使用：

```html
<span class="i-carbon-logo-github" />
```

---

## 主题色定制

本项目的主题色定义在 `docs/.vitepress/theme/home.css` 的 CSS 变量中：

```css
:root {
  --home-ink: #111315;           /* 主文字色 */
  --home-muted: #5e646b;         /* 次要文字色 */
  --home-line: rgba(17,19,21,0.1); /* 边框/分割线 */
  --home-panel: rgba(255,255,255,0.78); /* 面板背景 */
  --home-accent: #0a7d70;        /* 主题强调色（绿色） */
  --home-accent-soft: #dff7f2;   /* 强调色浅底 */
}
```

### 修改主题色

直接修改上述 CSS 变量值即可全局生效。例如将主题色改为蓝色系：

```css
:root {
  --home-accent: #2563eb;
  --home-accent-soft: #dbeafe;
}
```

### 在 UnoCSS 中使用主题色

通过任意值语法引用 CSS 变量：

```html
<div class="bg-[var(--home-accent)]">背景</div>
<div class="text-[var(--home-ink)]">文字</div>
<div class="border-[var(--home-line)]">边框</div>
```

或者使用 UnoCSS 的 `theme` 功能，在配置中定义颜色：

```ts
// docs/uno.config.ts
export default defineConfig({
  theme: {
    colors: {
      accent: '#0a7d70',
      'accent-soft': '#dff7f2',
      ink: '#111315',
      muted: '#5e646b',
    },
  },
})
```

之后可以使用语义化的 class：

```html
<div class="bg-accent text-ink border-muted">内容</div>
```

---

## 常用工具类速查

### 布局

| 工具类 | CSS 效果 |
|--------|----------|
| `flex` | `display: flex` |
| `grid` | `display: grid` |
| `items-center` | `align-items: center` |
| `justify-center` | `justify-content: center` |
| `gap-4` | `gap: 1rem` |
| `grid-cols-3` | `grid-template-columns: repeat(3, 1fr)` |

### 间距

| 工具类 | CSS 效果 |
|--------|----------|
| `p-4` | `padding: 1rem` |
| `px-6` | `padding-left: 1.5rem; padding-right: 1.5rem` |
| `mt-8` | `margin-top: 2rem` |
| `mx-auto` | `margin-left: auto; margin-right: auto` |

### 排版

| 工具类 | CSS 效果 |
|--------|----------|
| `text-lg` | `font-size: 1.125rem` |
| `font-bold` | `font-weight: 700` |
| `leading-tight` | `line-height: 1.25` |
| `tracking-tight` | `letter-spacing: -0.025em` |

### 颜色

| 工具类 | CSS 效果 |
|--------|----------|
| `text-white` | `color: #fff` |
| `bg-[#0a7d70]` | `background: #0a7d70`（任意值） |
| `opacity-80` | `opacity: 0.8` |

### 圆角与边框

| 工具类 | CSS 效果 |
|--------|----------|
| `rounded-lg` | `border-radius: 0.5rem` |
| `rounded-full` | `border-radius: 9999px` |
| `border` | `border-width: 1px` |
| `border-gray-200` | `border-color: #e5e7eb` |

### 阴影与过渡

| 工具类 | CSS 效果 |
|--------|----------|
| `shadow-md` | 中等阴影 |
| `transition` | 常用过渡属性 |
| `hover:opacity-90` | 悬停时透明度 |
| `transform` | 启用变换 |
| `translate-y--1px` | 向上偏移 1px |

### 响应式

前缀 `sm:` / `md:` / `lg:` / `xl:` 对应不同断点：

```html
<div class="grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
  <!-- 移动端1列，中等屏幕2列，大屏4列 -->
</div>
```

### 变体分组

借助 `transformerVariantGroup`，可将多个状态组合书写：

```html
<div class="hover:(bg-blue-500 text-white shadow-lg)">
  <!-- 等同于 hover:bg-blue-500 hover:text-white hover:shadow-lg -->
</div>
```

---

## 参考链接

- [UnoCSS 官方文档](https://unocss.dev/)
- [UnoCSS 预设列表](https://unocss.dev/presets/)
- [Tailwind CSS 工具类对照](https://tailwindcss.com/docs)（UnoCSS 兼容大部分语法）
- [Iconify 图标搜索](https://icon-sets.iconify.design/)
