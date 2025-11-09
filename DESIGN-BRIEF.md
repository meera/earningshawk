# MarketHawk Design System

**Version:** 2.0
**Last Updated:** November 9, 2025
**Brand:** MarketHawk (formerly EarningLens)
**Domain:** market-hawk.com

## Design Philosophy

MarketHawk transforms drab earnings calls into visually engaging content. Like a hawk spotting opportunities from above, we provide sharp, focused insights through compelling visual storytelling.

Our design system prioritizes:

1. **Professional credibility** - Financial data requires trust
2. **Visual clarity** - Complex data must be instantly comprehensible
3. **Seamless experience** - YouTube videos → Website should feel unified
4. **Engagement over aesthetics** - Boring data presented beautifully
5. **Mobile-first excellence** - Monitor anywhere, anytime

---

## Brand Colors

### Primary Colors

**Hawk Blue - Primary Brand Color**
```
hawk-50:   #EFF6FF  // Lightest - backgrounds
hawk-100:  #DBEAFE  // Light - hover states
hawk-500:  #3B82F6  // PRIMARY - main brand color
hawk-600:  #2563EB  // Darker - primary hover/active
hawk-700:  #1D4ED8  // Dark - emphasis
hawk-800:  #1E40AF  // Darker - headings
hawk-900:  #1E3A8A  // Darkest
```

**Usage:**
- Primary CTAs (Subscribe, Sign In, Watch Now)
- Links and interactive elements
- Chart primary lines
- Brand accents in videos
- Focus rings and active states

**Why Hawk Blue:**
- Industry standard for financial/data applications
- High trust association (credibility is critical)
- Excellent contrast for accessibility (WCAG AAA)
- Sharp and focused like a hawk's gaze
- Complements YouTube without competing

---

### Secondary Colors

**Accent Purple - Tech & Innovation**
```
Accent Purple:    #667EEA (rgb(102, 126, 234))
Accent Dark:      #764BA2 (rgb(118, 75, 162))
```

**Usage:**
- Video overlays and graphics
- Gradient backgrounds
- Emphasis elements
- Lower thirds in videos

**Example gradient:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

---

### Semantic Colors

**Success (Positive Metrics)**
```
success-50:   #ECFDF5  // Light backgrounds
success-500:  #10B981  // Primary green - +15% growth
success-600:  #059669  // Hover state
success-700:  #047857  // Dark backgrounds
```

**Error (Negative Metrics)**
```
error-50:   #FFF1F2  // Light backgrounds
error-500:  #F43F5E  // Primary red - -8% decline
error-600:  #E11D48  // Hover state
error-700:  #BE123C  // Dark backgrounds
```

**Warning (Caution)**
```
warning-50:   #FFFBEB  // Light backgrounds
warning-500:  #F59E0B  // Primary amber - mixed signals
warning-600:  #D97706  // Hover state
```

**Usage:**
- **Success:** Revenue beat, positive growth, exceeded expectations
- **Error:** Revenue miss, declining metrics, errors
- **Warning:** Guidance changes, mixed signals, caution areas
- **Neutral (Slate-500):** Informational data, no trend

**Data Visualization Palette (Multi-line charts):**
```
Chart Line 1:  #3B82F6  (Hawk Blue)
Chart Line 2:  #10B981  (Success Green)
Chart Line 3:  #667EEA  (Purple)
Chart Line 4:  #F59E0B  (Warning Amber)
Chart Line 5:  #EC4899  (Pink)
Chart Line 6:  #14B8A6  (Teal)
Chart Line 7:  #F43F5E  (Error Rose)
Chart Line 8:  #8B5CF6  (Violet)
```

---

### Neutral Colors

**Grayscale Palette**

```
Gray 50:          #F9FAFB (rgb(249, 250, 251))  /* Backgrounds */
Gray 100:         #F3F4F6 (rgb(243, 244, 246))  /* Subtle backgrounds */
Gray 200:         #E5E7EB (rgb(229, 231, 235))  /* Borders */
Gray 300:         #D1D5DB (rgb(209, 213, 219))  /* Dividers */
Gray 400:         #9CA3AF (rgb(156, 163, 175))  /* Disabled */
Gray 500:         #6B7280 (rgb(107, 114, 128))  /* Secondary text */
Gray 600:         #4B5563 (rgb(75, 85, 99))     /* Body text */
Gray 700:         #374151 (rgb(55, 65, 81))     /* Headings */
Gray 800:         #1F2937 (rgb(31, 41, 55))     /* Dark headings */
Gray 900:         #111827 (rgb(17, 24, 39))     /* Near black */

White:            #FFFFFF (rgb(255, 255, 255))
Black:            #000000 (rgb(0, 0, 0))
```

---

### Background Colors

**Light Mode (Default)**
```
Page Background:       #F9FAFB (Gray 50)
Card Background:       #FFFFFF (White)
Elevated Card:         #FFFFFF with shadow
Input Background:      #FFFFFF
Code Background:       #F3F4F6 (Gray 100)
```

**Dark Mode (Future)**
```
Page Background:       #111827 (Gray 900)
Card Background:       #1F2937 (Gray 800)
Elevated Card:         #374151 (Gray 700)
Input Background:      #1F2937 (Gray 800)
Code Background:       #374151 (Gray 700)
```

---

## Typography

### Font Families

**Primary Font Stack (Sans-Serif)**
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto',
             'Helvetica Neue', Arial, sans-serif;
```

**Why Inter:**
- Designed for screens and UI
- Excellent readability at all sizes
- Wide range of weights (100-900)
- Professional, modern appearance
- Used by Stripe, GitHub, Netflix
- Free and open source

**Fallback to system fonts ensures:**
- Fast load times
- Native OS feel
- No FOUT (Flash of Unstyled Text)

**Monospace Font Stack (Code/Data)**
```css
font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', 'Monaco',
             'Courier New', monospace;
```

**Usage:**
- Ticker symbols (AAPL, MSFT)
- Numeric data in tables
- Code snippets
- API documentation

---

### Font Sizes & Hierarchy

**Display Text (Hero Sections)**
```
Display XL:    64px / 4rem     (line-height: 1.1)  font-weight: 700
Display L:     56px / 3.5rem   (line-height: 1.1)  font-weight: 700
Display M:     48px / 3rem     (line-height: 1.2)  font-weight: 700
Display S:     40px / 2.5rem   (line-height: 1.2)  font-weight: 700
```

**Headings**
```
H1:            36px / 2.25rem  (line-height: 1.2)  font-weight: 700
H2:            30px / 1.875rem (line-height: 1.3)  font-weight: 600
H3:            24px / 1.5rem   (line-height: 1.4)  font-weight: 600
H4:            20px / 1.25rem  (line-height: 1.5)  font-weight: 600
H5:            18px / 1.125rem (line-height: 1.5)  font-weight: 600
H6:            16px / 1rem     (line-height: 1.5)  font-weight: 600
```

**Body Text**
```
Body Large:    18px / 1.125rem (line-height: 1.7)  font-weight: 400
Body:          16px / 1rem     (line-height: 1.6)  font-weight: 400
Body Small:    14px / 0.875rem (line-height: 1.5)  font-weight: 400
Caption:       12px / 0.75rem  (line-height: 1.4)  font-weight: 400
```

**Video Typography (Remotion)**
```
Video Title:        64px  font-weight: 700
Video Subtitle:     32px  font-weight: 600
Lower Third:        28px  font-weight: 700
Metric Label:       18px  font-weight: 600  (uppercase, letter-spacing: 1px)
Metric Value:       48px  font-weight: 700
Metric Change:      20px  font-weight: 700
```

---

### Font Weights

**Inter Weight Scale**
```
Thin:          100  (Rarely used)
Extra Light:   200  (Rarely used)
Light:         300  (Subtle text, de-emphasized)
Regular:       400  (Body text, paragraphs) ← DEFAULT
Medium:        500  (Slight emphasis)
Semi Bold:     600  (Headings H2-H6, buttons)
Bold:          700  (H1, Display, strong emphasis)
Extra Bold:    800  (Special emphasis)
Black:         900  (Impact, large numbers)
```

**Usage Guidelines:**
- **Body text:** 400 (Regular)
- **Headings:** 600-700 (Semi Bold to Bold)
- **Buttons/CTAs:** 600 (Semi Bold)
- **Large numbers:** 700-900 (Bold to Black)
- **Labels:** 600 (Semi Bold, uppercase)

---

### Letter Spacing & Line Height

**Letter Spacing (Tracking)**
```
Tight:         -0.025em  (Large display text)
Normal:         0         (Body text)
Wide:          +0.025em  (Small text for readability)
Wider:         +0.05em   (Uppercase labels)
Widest:        +0.1em    (Uppercase headings)
```

**Line Height (Leading)**
```
Tight:         1.2   (Large headings)
Snug:          1.4   (Small headings)
Normal:        1.5   (UI text, buttons)
Relaxed:       1.6   (Body text - PREFERRED)
Loose:         1.7   (Large body, marketing)
```

---

## Spacing System

**8px Base Grid**

```
Space 1:    4px   / 0.25rem   (xs)
Space 2:    8px   / 0.5rem    (sm)
Space 3:    12px  / 0.75rem
Space 4:    16px  / 1rem      (base)
Space 5:    20px  / 1.25rem
Space 6:    24px  / 1.5rem
Space 8:    32px  / 2rem
Space 10:   40px  / 2.5rem
Space 12:   48px  / 3rem
Space 16:   64px  / 4rem
Space 20:   80px  / 5rem
Space 24:   96px  / 6rem
```

**Component Padding**
```
Button:        12px 24px  (vertical horizontal)
Input:         12px 16px
Card:          24px
Section:       64px 0     (vertical horizontal)
Container:     0 24px     (mobile)
Container:     0 48px     (desktop)
```

---

## Shadows & Elevation

**Box Shadows (Z-axis depth)**

```css
/* Subtle */
shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.05);

/* Default card */
shadow:     0 1px 3px rgba(0, 0, 0, 0.1),
            0 1px 2px rgba(0, 0, 0, 0.06);

/* Raised card/hover */
shadow-md:  0 4px 6px rgba(0, 0, 0, 0.07),
            0 2px 4px rgba(0, 0, 0, 0.05);

/* Elevated (modals, dropdowns) */
shadow-lg:  0 10px 15px rgba(0, 0, 0, 0.1),
            0 4px 6px rgba(0, 0, 0, 0.05);

/* High elevation (popovers) */
shadow-xl:  0 20px 25px rgba(0, 0, 0, 0.1),
            0 10px 10px rgba(0, 0, 0, 0.04);

/* Maximum elevation */
shadow-2xl: 0 25px 50px rgba(0, 0, 0, 0.15);
```

**Video Overlays**
```css
/* Text readability over video */
text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);

/* Metric cards in video */
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
```

---

## Border Radius

**Rounded Corners**

```
Radius SM:     4px   / 0.25rem   (Subtle, inputs)
Radius Base:   8px   / 0.5rem    (Buttons, badges)
Radius MD:     12px  / 0.75rem   (Cards)
Radius LG:     16px  / 1rem      (Large cards)
Radius XL:     20px  / 1.25rem   (Video thumbnails)
Radius 2XL:    24px  / 1.5rem    (Hero sections)
Radius Full:   9999px            (Pills, avatars)
```

**Usage:**
- Buttons: 8px (Base)
- Input fields: 8px (Base)
- Cards: 12px (MD)
- Video overlays: 16px (LG)
- Profile pictures: Full
- Metric cards: 20px (XL)

---

## YouTube Integration

### Maintaining Visual Continuity

**Challenge:** Videos uploaded to YouTube → users click → land on earninglens.com
**Goal:** Seamless transition (users shouldn't feel like they left the "experience")

**Strategy:**

1. **Consistent Branding in Video**
   - EarningLens logo watermark (top-left or bottom-right)
   - Same color palette in video graphics
   - Consistent typography (Inter font in burned-in text)
   - End card with earninglens.com CTA

2. **Video Thumbnail → Website Consistency**
   - Use same accent colors (#667EEA purple, #2563EB blue)
   - Same typography for company names
   - Similar layout patterns (logo + ticker + title)

3. **Website Design Echoes Video**
   - Metric cards on website match video overlay style
   - Same chart colors and styles
   - Identical trend indicators (↑ green, ↓ red)
   - Consistent speaker name displays

4. **Transition Elements**
   - Video player on website uses same aspect ratio
   - Transcript display matches video subtitle style
   - Interactive charts use same data viz palette

---

### Video-Specific Design

**YouTube Video Overlays (Burned into Video)**

**Lower Third (Speaker Name)**
```
Background:     rgba(0, 0, 0, 0.85) with backdrop blur
Accent Bar:     8px wide, #667EEA (Accent Purple)
Text:           28px, font-weight: 700, white
Position:       Bottom-left, 60px from edge
```

**Metric Cards (Floating)**
```
Background:     rgba(255, 255, 255, 0.95) with backdrop blur
Border Radius:  16px
Box Shadow:     0 8px 32px rgba(0, 0, 0, 0.15)
Padding:        20px 28px
Label:          14px, uppercase, #718096, letter-spacing: 0.5px
Value:          32px, font-weight: 700, #1a202c
Trend:          16px, font-weight: 700, colored (#48bb78 or #f56565)
```

**Animated Title Card**
```
Background:     Gradient (#667eea to #764ba2) or solid #f7fafc
Title:          64px, font-weight: 700, centered
Subtitle:       32px, font-weight: 600, #4a5568
Underline:      Animated, 6px height, #667EEA
Duration:       3-5 seconds
```

**Company Logo Display**
```
Logo:           120px x 120px, rounded corners (12px)
Ticker:         24px, font-weight: 700, monospace
Company Name:   20px, font-weight: 600, #4a5568
Animation:      Float (subtle vertical movement)
```

---

## Component Patterns

### Buttons

**Primary Button**
```css
background: #2563EB;
color: white;
padding: 12px 24px;
border-radius: 8px;
font-size: 16px;
font-weight: 600;
transition: all 150ms;

hover: background: #1D4ED8; transform: translateY(-1px); shadow: md;
active: transform: translateY(0); shadow: sm;
```

**Secondary Button**
```css
background: white;
color: #2563EB;
border: 2px solid #2563EB;
/* same sizing/padding as primary */
```

**Ghost Button**
```css
background: transparent;
color: #2563EB;
border: none;
/* same sizing/padding, hover: background: gray-100 */
```

---

### Cards

**Standard Card**
```css
background: white;
border-radius: 12px;
padding: 24px;
box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
border: 1px solid rgba(0, 0, 0, 0.05);
```

**Metric Card (Video Style)**
```css
background: white;
border-radius: 20px;
padding: 32px;
box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
min-width: 280px;
```

**Hover States**
```css
transition: all 200ms;
hover: transform: translateY(-2px); box-shadow: lg;
```

---

### Forms

**Input Fields**
```css
background: white;
border: 1px solid #D1D5DB (gray-300);
border-radius: 8px;
padding: 12px 16px;
font-size: 16px;

focus: border-color: #2563EB; box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
```

**Labels**
```css
font-size: 14px;
font-weight: 600;
color: #374151 (gray-700);
margin-bottom: 8px;
```

---

## Accessibility

**Contrast Ratios (WCAG AA)**

✅ **Passing combinations:**
- Primary Blue (#2563EB) on White: 7.13:1 (AAA)
- Gray 600 (#4B5563) on White: 8.59:1 (AAA)
- White on Primary Blue: 7.13:1 (AAA)
- Positive Green (#48BB78) on White: 3.35:1 (AA Large)
- Negative Red (#F56565) on White: 3.94:1 (AA Large)

**Focus States**
```css
outline: 2px solid #2563EB;
outline-offset: 2px;
```

**Screen Reader Labels**
- All interactive elements have aria-labels
- Trend indicators include sr-only text ("up 30%")
- Charts include data tables for screen readers

---

## Implementation

### CSS Variables

```css
:root {
  /* Colors */
  --color-primary: #2563EB;
  --color-primary-hover: #1D4ED8;
  --color-accent: #667EEA;
  --color-positive: #48BB78;
  --color-negative: #F56565;
  --color-neutral: #718096;

  /* Typography */
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Shadows */
  --shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1), 0 4px 6px rgba(0, 0, 0, 0.05);

  /* Radius */
  --radius: 0.5rem;
  --radius-lg: 1rem;
}
```

### Tailwind Config

**Full configuration available in `/tailwind.config.ts`**

Key extensions:
```typescript
// Colors
hawk: {
  50: '#EFF6FF',
  500: '#3B82F6',  // Primary
  600: '#2563EB',
  900: '#1E3A8A',
}

success: {
  500: '#10B981',  // Positive metrics
}

error: {
  500: '#F43F5E',  // Negative metrics
}

// Company brands
robinhood: { green: '#00C805' }
palantir: { blue: '#0033A0' }
apple: { blue: '#0071E3' }

// Typography
fontSize: {
  'display-xl': ['4rem', { lineHeight: '1.1', fontWeight: '700' }],
  'video-title': ['4rem', { lineHeight: '1.1' }],
  'video-metric': ['3rem', { lineHeight: '1', fontWeight: '700' }],
}

fontFamily: {
  sans: ['Inter', '-apple-system', ...],
  mono: ['JetBrains Mono', 'Fira Code', ...],
}

// Shadows
boxShadow: {
  'card': '0 1px 3px rgba(0, 0, 0, 0.1), ...',
  'metric': '0 10px 40px rgba(0, 0, 0, 0.1)',
  'video-overlay': '0 8px 32px rgba(0, 0, 0, 0.15)',
}

// Animations
animation: {
  'fade-in': 'fadeIn 0.5s ease-in',
  'slide-up': 'slideUp 0.5s ease-out',
}
```

**Install required plugins:**
```bash
npm install -D @tailwindcss/forms @tailwindcss/typography @tailwindcss/aspect-ratio
```

---

## Examples

### Hero Section
```
Background: White
Heading (H1): 64px, font-weight: 700, #111827
Subheading: 24px, font-weight: 400, #6B7280, line-height: 1.6
CTA Button: Primary Blue, 16px, font-weight: 600
```

### Video Card
```
Thumbnail: 16:9 aspect ratio, border-radius: 12px
Overlay: Gradient from transparent to rgba(0,0,0,0.6)
Title: 20px, font-weight: 600, #111827
Metadata: 14px, font-weight: 400, #6B7280
Ticker Badge: Monospace, 12px, uppercase, #2563EB background
```

### Metric Display
```
Label: 14px, uppercase, #718096, letter-spacing: 1px, font-weight: 600
Value: 48px, font-weight: 700, #1a202c
Change: 20px, font-weight: 700, #48bb78 or #f56565 with arrow
Card: White background, 20px radius, shadow-lg
```

---

## Brand Voice

**Tone:** Professional yet approachable, data-driven but not boring

**Writing Style:**
- Clear and concise
- Active voice
- No jargon (or explain when necessary)
- Confidence without arrogance

**Example Headlines:**
- ✅ "Palantir Q3 2024: Revenue Up 30% YoY"
- ❌ "PLTR CRUSHES EARNINGS!!!" (too hype)
- ❌ "Palantir Technologies Reports Third Quarter Financial Results" (too corporate)

---

## Resources

**Font Downloads:**
- Inter: https://rsms.me/inter/
- JetBrains Mono: https://www.jetbrains.com/lp/mono/

**Design Tools:**
- Figma (design mockups)
- ColorBox (palette generation): https://colorbox.io/
- Coolors (palette testing): https://coolors.co/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

**Inspiration:**
- Stripe (clean SaaS design)
- Linear (modern product design)
- Bloomberg Terminal (data-heavy UI done right)
- Notion (content-focused design)

---

## Quick Start

### 1. Install Fonts

**Inter (Primary Font)**
```html
<!-- Add to <head> in layout.tsx -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
```

**JetBrains Mono (Data/Code Font)**
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 2. Install Dependencies

```bash
# Tailwind CSS and plugins
npm install -D tailwindcss postcss autoprefixer
npm install -D @tailwindcss/forms @tailwindcss/typography @tailwindcss/aspect-ratio

# Initialize Tailwind (if not already done)
npx tailwindcss init -p
```

### 3. Import Tailwind

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom base styles */
@layer base {
  body {
    @apply font-sans antialiased;
    @apply text-slate-600 bg-slate-50;
  }

  h1, h2, h3, h4, h5, h6 {
    @apply font-semibold text-slate-900;
  }

  code {
    @apply font-mono;
  }
}
```

### 4. Example Component

```tsx
// components/MetricCard.tsx
export function MetricCard({
  label,
  value,
  change,
  trend
}: {
  label: string;
  value: string;
  change: string;
  trend: 'positive' | 'negative' | 'neutral';
}) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-card hover:shadow-card-hover transition-shadow">
      <dt className="text-sm font-medium text-slate-600 uppercase tracking-wide">
        {label}
      </dt>
      <dd className="mt-2 text-3xl font-black text-slate-900 font-mono">
        {value}
      </dd>
      <div className={`mt-2 flex items-center text-sm font-semibold ${
        trend === 'positive' ? 'text-success-600' :
        trend === 'negative' ? 'text-error-600' :
        'text-slate-500'
      }`}>
        {trend === 'positive' && <ArrowUpIcon className="w-4 h-4 mr-1" />}
        {trend === 'negative' && <ArrowDownIcon className="w-4 h-4 mr-1" />}
        {change}
      </div>
    </div>
  );
}
```

---

**Version:** 2.0
**Last Updated:** November 9, 2025
**Maintainer:** Development Team
**Status:** Active
**Related Files:**
- `/tailwind.config.ts` - Full Tailwind configuration
- `/web/app/globals.css` - Global styles
- `/CLAUDE.md` - Project documentation
