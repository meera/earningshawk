# MarketHawk Design Quick Reference

**Quick cheat sheet for developers**

---

## Colors

### Primary
```tsx
className="bg-hawk-600 hover:bg-hawk-700"  // Buttons
className="text-hawk-600"                   // Links
className="border-hawk-600"                 // Borders
```

### Semantic
```tsx
// Positive metrics
className="text-success-600 bg-success-50"

// Negative metrics  
className="text-error-600 bg-error-50"

// Warning
className="text-warning-600 bg-warning-50"

// Neutral
className="text-slate-600"
```

### Company Brands
```tsx
className="bg-robinhood-green"  // #00C805
className="bg-palantir-blue"    // #0033A0
className="bg-apple-blue"       // #0071E3
```

---

## Typography

### Font Families
```tsx
className="font-sans"   // Inter (default)
className="font-mono"   // JetBrains Mono (tickers, data)
```

### Sizes
```tsx
// Display (Hero sections)
className="text-display-xl"  // 64px, bold
className="text-display-lg"  // 56px, bold
className="text-display-md"  // 48px, bold

// Headings
className="text-4xl"  // H1 (36px)
className="text-3xl"  // H2 (30px)
className="text-2xl"  // H3 (24px)
className="text-xl"   // H4 (20px)

// Body
className="text-lg"    // Large body (18px)
className="text-base"  // Normal body (16px)
className="text-sm"    // Small text (14px)
className="text-xs"    // Captions (12px)

// Video overlays
className="text-video-title"    // 64px
className="text-video-subtitle" // 32px
className="text-video-metric"   // 48px
```

### Weights
```tsx
className="font-light"     // 300 - Large numbers
className="font-normal"    // 400 - Body text
className="font-medium"    // 500 - Emphasis
className="font-semibold"  // 600 - Headings
className="font-bold"      // 700 - Strong emphasis
className="font-extrabold" // 800 - Hero headings
className="font-black"     // 900 - Metrics
```

---

## Components

### Button - Primary
```tsx
<button className="
  px-6 py-3
  bg-hawk-600 hover:bg-hawk-700
  text-white font-semibold
  rounded-lg
  transition-colors duration-200
  focus:outline-none focus:ring-2 focus:ring-hawk-500 focus:ring-offset-2
">
  Watch Now
</button>
```

### Button - Secondary
```tsx
<button className="
  px-6 py-3
  bg-slate-100 hover:bg-slate-200
  text-slate-900 font-semibold
  rounded-lg
  transition-colors duration-200
">
  Learn More
</button>
```

### Button - Outline
```tsx
<button className="
  px-6 py-3
  border-2 border-hawk-600
  text-hawk-600 hover:bg-hawk-50
  font-semibold rounded-lg
  transition-colors duration-200
">
  Sign In
</button>
```

### Card - Standard
```tsx
<div className="
  bg-white
  rounded-xl
  border border-slate-200
  p-6
  shadow-card hover:shadow-card-hover
  transition-shadow duration-200
">
  {/* Card content */}
</div>
```

### Card - Metric
```tsx
<div className="bg-white rounded-xl border border-slate-200 p-6">
  <dt className="text-sm font-medium text-slate-600 uppercase tracking-wide">
    Revenue
  </dt>
  <dd className="mt-2 text-3xl font-black text-slate-900 font-mono">
    $94.9B
  </dd>
  <div className="mt-2 flex items-center text-sm font-semibold text-success-600">
    <ArrowUpIcon className="w-4 h-4 mr-1" />
    +6.0%
  </div>
</div>
```

### Input Field
```tsx
<div>
  <label className="block text-sm font-medium text-slate-700 mb-2">
    Email
  </label>
  <input
    type="email"
    className="
      w-full px-4 py-3
      border border-slate-300
      rounded-lg
      focus:ring-2 focus:ring-hawk-500 focus:border-transparent
      placeholder:text-slate-400
    "
    placeholder="you@company.com"
  />
</div>
```

### Badge - Status
```tsx
// Positive
<span className="
  inline-flex items-center
  px-2.5 py-0.5
  rounded-full
  text-xs font-medium
  bg-success-50 text-success-700
">
  Beat Expectations
</span>

// Negative
<span className="bg-error-50 text-error-700 ...">
  Missed Guidance
</span>

// Neutral
<span className="bg-slate-100 text-slate-700 ...">
  In Line
</span>
```

---

## Layout

### Container
```tsx
// Full width
<div className="w-full px-4 md:px-6 lg:px-8">

// Max width (1280px)
<div className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8">

// Narrow (articles)
<div className="max-w-3xl mx-auto px-4">
```

### Grid - Video Cards
```tsx
<div className="
  grid
  grid-cols-1
  md:grid-cols-2
  lg:grid-cols-3
  xl:grid-cols-4
  gap-6
">
  {videos.map(...)}
</div>
```

### Grid - Metrics
```tsx
<div className="
  grid
  grid-cols-1
  sm:grid-cols-2
  lg:grid-cols-4
  gap-4
">
  {metrics.map(...)}
</div>
```

---

## Spacing

```tsx
// Padding
className="p-4"    // 16px all sides
className="px-6"   // 24px horizontal
className="py-3"   // 12px vertical

// Margin
className="mt-4"   // 16px top
className="mb-6"   // 24px bottom
className="mx-auto" // Center horizontally

// Gap (Grid/Flex)
className="gap-4"  // 16px gap
className="gap-6"  // 24px gap
className="space-y-4" // 16px vertical spacing
```

---

## Shadows

```tsx
className="shadow-card"          // Default card shadow
className="shadow-card-hover"    // Hover state
className="shadow-metric"        // Large metric cards
className="shadow-video-overlay" // Video overlays
className="shadow-glow-blue"     // Blue glow effect
className="shadow-glow-green"    // Green glow (positive)
className="shadow-glow-red"      // Red glow (negative)
```

---

## Animations

```tsx
className="animate-fade-in"   // Fade in on mount
className="animate-slide-up"  // Slide up from bottom
className="animate-scale-in"  // Scale in from 95%

// Transitions
className="transition-colors duration-200"  // Color changes
className="transition-shadow duration-200"  // Shadow changes
className="transition-transform duration-300" // Transform
```

---

## Responsive Design

```tsx
// Mobile first approach
className="text-2xl md:text-3xl lg:text-4xl"

// Show/hide by breakpoint
className="hidden md:block"  // Hide on mobile
className="block md:hidden"  // Show on mobile only

// Breakpoints
sm:  640px   // Mobile landscape
md:  768px   // Tablet
lg:  1024px  // Desktop
xl:  1280px  // Large desktop
2xl: 1536px  // Extra large
```

---

## Common Patterns

### Video Card
```tsx
<article className="group">
  <div className="aspect-video bg-slate-900 rounded-lg overflow-hidden mb-4">
    <img
      src={thumbnail}
      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
    />
  </div>
  <h3 className="font-semibold text-slate-900 group-hover:text-hawk-600">
    {title}
  </h3>
  <p className="text-sm text-slate-600 mt-1">
    {company} • {quarter}
  </p>
</article>
```

### Navigation Bar
```tsx
<nav className="sticky top-0 z-50 bg-white border-b border-slate-200 backdrop-blur-sm bg-white/95">
  <div className="max-w-7xl mx-auto px-4 md:px-6">
    <div className="flex items-center justify-between h-16">
      <Logo />
      <NavLinks />
      <UserMenu />
    </div>
  </div>
</nav>
```

### Hero Section
```tsx
<section className="py-16 md:py-24">
  <div className="max-w-7xl mx-auto px-4 md:px-6 text-center">
    <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-slate-900 mb-6">
      Transform Earnings Calls
    </h1>
    <p className="text-lg md:text-xl text-slate-600 max-w-3xl mx-auto mb-8">
      Visual storytelling for financial data
    </p>
    <button className="bg-hawk-600 hover:bg-hawk-700 text-white px-8 py-4 rounded-lg font-semibold">
      Get Started
    </button>
  </div>
</section>
```

---

## Accessibility

### Focus States
```tsx
// Always include focus states
className="focus:outline-none focus:ring-2 focus:ring-hawk-500 focus:ring-offset-2"
```

### Screen Reader Text
```tsx
<span className="sr-only">Revenue increased by</span>
<span aria-hidden="true">↑</span>
<span>6%</span>
```

### Semantic HTML
```tsx
// Use proper elements
<nav>      // Navigation
<main>     // Main content
<article>  // Video cards
<section>  // Page sections
<aside>    // Sidebars
```

---

## Files

- **Full config:** `/tailwind.config.ts`
- **Design brief:** `/DESIGN-BRIEF.md`
- **Global styles:** `/web/app/globals.css`
- **Project docs:** `/CLAUDE.md`

---

**Last Updated:** November 9, 2025
