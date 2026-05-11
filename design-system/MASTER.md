# L'Amour Design System — MASTER

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that page file exists, its rules **override** this Master. Otherwise, follow the Master exclusively.

---

**Project:** L'Amour (`lämour.de` / `0b8499-39.myshopify.com`)
**Stack:** Shopify OS 2.0, Liquid, Vanilla CSS + JS (Web Components), no build step
**Language:** German primary (`de`), English fallback (`en`)
**Last updated:** 2026-05-11

---

## 1. Brand Identity

| Attribute | Value |
|-----------|-------|
| Category | Luxury beauty e-commerce |
| Personality | Refined, editorial, intimate, modern German luxury |
| Tone | Confident whisper — never shouts |
| Style | Minimal glassmorphism meets organic editorial |
| Audience | German-speaking beauty enthusiasts, 22–45, premium-conscious |

---

## 2. Color System

All colors are CSS custom properties on `<html data-theme="light|dark">`.
**Never hardcode hex values in sections — always reference tokens.**

### Light Mode (default) — Background: Cream `#EBE7DE`

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-bg` | `#EBE7DE` | Page background (warm cream) |
| `--color-bg-soft` | `#E2DCD2` | Alternate section bg (brand-statement, etc.) |
| `--color-bg-card` | `#EBE7DE` | Card backgrounds |
| `--color-surface` | `#D8D0C4` | Elevated surfaces, input fills |
| `--color-border` | `rgba(0,0,0,0.10)` | Hairlines, card borders |
| `--color-text` | `#0E0E0E` | Primary text |
| `--color-text-70` | `rgba(14,14,14,0.70)` | Secondary text, subtitles |
| `--color-text-40` | `rgba(14,14,14,0.40)` | Muted text, placeholders |
| `--color-text-10` | `rgba(14,14,14,0.10)` | Decorative text overlays |
| `--color-glass` | `rgba(244,242,239,0.70)` | Glass panels, overlays |
| `--color-glass-strong` | `rgba(244,242,239,0.92)` | Solid glass (nav, modals) |
| `--color-nav-bg` | `rgba(244,242,239,0.78)` | Sticky header backdrop |
| `--color-nav-border` | `rgba(0,0,0,0.08)` | Header bottom border |

### Dark Mode — Background: Noir `#000000`

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-bg` | `#000000` | Page background |
| `--color-bg-soft` | `#0A0A0A` | Alternate section bg |
| `--color-bg-card` | `#111111` | Card backgrounds |
| `--color-surface` | `#1A1A1A` | Elevated surfaces |
| `--color-border` | `rgba(255,255,255,0.10)` | Hairlines, borders |
| `--color-text` | `#EBE7DE` | Primary text (cream on dark) |
| `--color-text-70` | `rgba(235,231,222,0.70)` | Secondary text |
| `--color-text-40` | `rgba(235,231,222,0.40)` | Muted text |
| `--color-text-10` | `rgba(235,231,222,0.10)` | Decorative overlays |
| `--color-glass` | `rgba(255,255,255,0.05)` | Glass panels |
| `--color-glass-strong` | `rgba(255,255,255,0.10)` | Strong glass |
| `--color-nav-bg` | `rgba(12,12,12,0.72)` | Sticky header |
| `--color-nav-border` | `rgba(255,255,255,0.08)` | Header border |

### Brand & Accent Colors (both modes)

| Token | Hex | Usage |
|-------|-----|-------|
| `--color-pink` | `#F597B1` | Primary accent, CTA borders, hover fills, cursor |
| `--color-pink-dim` | `rgba(245,151,177,0.15)` | Soft pink backgrounds, glass tints |

### Blur / Glass Utilities

| Token | Value |
|-------|-------|
| `--blur-glass` | `blur(18px) saturate(140%)` |
| `--blur-glass-strong` | `blur(24px) saturate(160%)` |

---

## 3. Typography

### Typefaces

| Role | Font | Fallback | Loaded via |
|------|------|----------|-----------|
| Display / Headings | `Fraunces` (variable) | `'Times New Roman', serif` | Google Fonts |
| Body / UI | `Inter` | `system-ui, sans-serif` | Google Fonts |
| Mono / Labels | `JetBrains Mono` | `ui-monospace, monospace` | Google Fonts |

### Type Scale (fluid with `clamp`)

| Token | Value | Usage |
|-------|-------|-------|
| `--text-hero` | `clamp(3.5rem, 8vw, 7.5rem)` | Hero H1 |
| `--text-display` | `clamp(2.5rem, 5vw, 5rem)` | Section headings (h2) |
| `--text-heading` | `clamp(2rem, 4vw, 3.5rem)` | Sub-section headings (h2/h3) |
| `--text-sub` | `clamp(1.5rem, 3vw, 2.25rem)` | Subheadings, lead text |
| `--text-body` | `1rem` | Body copy (16px base) |
| `--text-small` | `0.875rem` | Labels, buttons, captions |
| `--text-micro` | `0.75rem` | Eyebrows, mono tags, footnotes |

### Font Utility Classes

```css
/* Heading / Display — Fraunces variable */
.font-display {
  font-family: 'Fraunces', 'Times New Roman', serif;
  font-optical-sizing: auto;
  font-variation-settings: 'SOFT' 20, 'WONK' 0;
  font-weight: 700;
  letter-spacing: -0.035em;
}

/* Editorial Serif — softer weight */
.font-serif {
  font-family: 'Fraunces', 'Times New Roman', serif;
  font-optical-sizing: auto;
  font-variation-settings: 'SOFT' 30, 'WONK' 0;
}

/* Label / Eyebrow — Inter spaced caps */
.font-sub {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 300;
  letter-spacing: 0.28em;
  text-transform: uppercase;
}

/* Monospaced — section tags, numbers */
.font-mono {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
}
```

### Typography Rules

- Heading lines: `line-height: 1.05` for hero/display, `1.15` for section headings
- Body: `line-height: 1.6`, `font-weight: 300–400`
- Eyebrows: `font-size: var(--text-micro)`, `color: var(--color-pink)`, monospace, uppercase, letter-spacing 0.2–0.3em
- Italic accents in headings use `color: var(--color-pink)`, `font-style: italic`, `font-weight: 400`
- Section `§` symbols prefix eyebrow tags (e.g., `§ Über Lamour`)

---

## 4. Spacing System

| Token | Value | Usage |
|-------|-------|-------|
| `--space-section` | `clamp(5rem, 10vw, 9rem)` | Vertical section padding |
| `--space-gap` | `clamp(3rem, 6vw, 7rem)` | Between major content blocks |
| `--container` | `1400px` | Max content width |

Container padding: `clamp(1rem, 4vw, 3rem)` horizontal via `.lm-container`.

### Component-level spacing (multiples of 4px/8px)

| Step | px | rem | Usage |
|------|----|-----|-------|
| xs | 4px | 0.25rem | Icon gaps, tight inline |
| sm | 8px | 0.5rem | Between inline elements |
| md | 16px | 1rem | Standard padding |
| lg | 24px | 1.5rem | Card/panel padding |
| xl | 32px | 2rem | Section sub-gaps |
| 2xl | 48px | 3rem | Section margins |
| 3xl | 64px | 4rem | Hero internal padding |

---

## 5. Motion & Animation

### Easing Tokens

| Token | Value | Use |
|-------|-------|-----|
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | Elements entering view |
| `--ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Playful bouncy interactions |

### Duration Tokens

| Token | Value | Use |
|-------|-------|-----|
| `--dur-fast` | `150ms` | Micro-interactions, hover fills |
| `--dur-base` | `300ms` | Standard transitions |
| `--dur-slow` | `600ms` | Section reveals, modals |
| `--dur-reveal` | `800ms` | Scroll-triggered reveals |

### Animation Keyframes (defined in `assets/theme.css`)

| Name | Effect | Use |
|------|--------|-----|
| `heroIn` | scale + letter-spacing + blur → visible | Hero headline entrance |
| `shimmer` | Pink/white sweep on text | Shimmer text utility |
| `marquee` | Infinite horizontal scroll | Brand logo marquee |
| `float` | 7s vertical bob | Floating product images |
| `pulseRing` | Scale 0.7→2.2, fade out | Pulse ring badges |

### Scroll Reveal Classes

```css
.reveal          { opacity: 0; transform: translateY(28px); transition: opacity 800ms ease-out, transform 800ms ease-out; }
.reveal.in       { opacity: 1; transform: none; }
.reveal-delay-1  { transition-delay: 120ms; }
.reveal-delay-2  { transition-delay: 240ms; }
.reveal-delay-3  { transition-delay: 360ms; }
```

### Rules

- Enter animations: `ease-out`, exit: `ease-in`
- Micro-interactions: 150–300ms max
- Complex transitions: ≤400ms
- Stagger list items: 30–50ms delay increments
- All animations must respect `prefers-reduced-motion` (kill-switch already in `assets/theme.css`)

---

## 6. Glassmorphism System

```css
/* Standard glass panel */
.glass {
  background: var(--color-glass);
  backdrop-filter: var(--blur-glass);
  -webkit-backdrop-filter: var(--blur-glass);
  border: 1px solid var(--color-border);
}

/* Strong glass — nav, modals */
.glass-strong {
  background: var(--color-glass-strong);
  backdrop-filter: var(--blur-glass-strong);
  -webkit-backdrop-filter: var(--blur-glass-strong);
  border: 1px solid var(--color-border);
}

/* Pink-tinted glass */
.glass-pink {
  background: linear-gradient(135deg, rgba(245,151,177,0.14), rgba(245,151,177,0.04));
  backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid rgba(245,151,177,0.25);
}
```

Light mode overrides on glass classes are already handled in `assets/theme.css`.

---

## 7. Component Library

### Buttons

```css
/* Base outline button (default CTA) */
.lm-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 2rem;
  font-family: var(--font-body);
  font-weight: 500;
  font-size: var(--text-small);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  border: 1px solid var(--color-pink);
  color: var(--color-pink);
  background: transparent;
  border-radius: 2px;
  cursor: pointer;
  transition: background var(--dur-base) ease, color var(--dur-base) ease;
}
.lm-btn:hover {
  background: var(--color-pink);
  color: #000;
}

/* Filled variant */
.lm-btn--filled {
  background: var(--color-pink);
  color: #000;
}
.lm-btn--filled:hover {
  background: #F07B9E;
  border-color: #F07B9E;
}
```

**Rules:**
- Border-radius: `2px` — luxury square, never pill
- Letter-spacing: `0.12em` uppercase
- Hover: fill with pink, text goes `#000`
- Navigation CTAs: always include SVG arrow icon (16×16, `stroke-width: 1.5`)
- One primary CTA per section maximum

### Cards

```css
.card-base {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  transition: transform var(--dur-base) var(--ease-out),
              box-shadow var(--dur-base) ease;
}
.card-base:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 32px rgba(0,0,0,0.08);
}
```

### Category Cards (`.lm-catcard`)

- Square image with `object-fit: cover`
- Dark vignette overlay: `linear-gradient(to top, rgba(0,0,0,0.7), transparent)`
- Bottom info bar: number (monospaced `01–08`), title (Fraunces), subtitle (monospaced), arrow
- Hover: image scales 1.04, info bar nudges up 4px

### FAQ Accordion (`.lm-faq__item`)

- Single unified glass card wraps all items — no individual borders
- Hairlines between items: `border-bottom: 1px solid var(--color-border)`
- Plus/minus icon inside circular badge with `--color-pink` border
- Question: Fraunces serif; Answer: Inter
- Expand via `max-height` animation + `aria-expanded` toggle

### Navigation Header

- `position: fixed`, `z-index: 100`, full width
- Background: `var(--color-nav-bg)` + `backdrop-filter: var(--blur-glass)`
- Bottom border: `1px solid var(--color-nav-border)`
- Height: `var(--lm-header-h, 80px)`
- Logo: Fraunces; Nav links: Inter 300, letter-spacing 0.1em

### Inputs

```css
.lm-input {
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  background: var(--color-bg-card);
  color: var(--color-text);
  font-family: var(--font-body);
  font-size: var(--text-body);
  border-radius: 2px;
  transition: border-color var(--dur-base) ease;
}
.lm-input:focus {
  border-color: var(--color-pink);
  outline: none;
  box-shadow: 0 0 0 3px var(--color-pink-dim);
}
```

---

## 8. Layout System

### Container

```css
.lm-container {
  width: 100%;
  max-width: 1400px; /* var(--container) */
  margin-inline: auto;
  padding-inline: clamp(1rem, 4vw, 3rem);
}
```

### Section Structure Pattern

Every section follows this Liquid structure:
1. `<section class="lm-[name]" aria-labelledby="lm-[name]-heading">` — full bleed, semantic
2. `<div class="lm-[name]__inner lm-container">` — constrained, centered
3. `<div class="lm-[name]__hd">` — eyebrow + h2 + optional right-aligned link
4. Content body

### Grid Patterns

| Pattern | CSS | Use |
|---------|-----|-----|
| 2-col equal | `grid-template-columns: 1fr 1fr` | Brand statement, editorial split |
| 4-col grid | `grid-template-columns: repeat(4, 1fr)` | Category grid (→ 2-col mobile) |
| Auto-fill cards | `grid-template-columns: repeat(auto-fill, minmax(280px, 1fr))` | Product grid |

Mobile collapse breakpoint: `767px` — all multi-column grids go to 1 column.

### Breakpoints

| Name | px | Notes |
|------|----|-------|
| Mobile | `< 768px` | Single column, full-width |
| Tablet | `768px–1023px` | 2-col where needed |
| Desktop | `≥ 1024px` | Full layout |
| Wide | `≥ 1400px` | Container max-width caps here |

---

## 9. Surface & Texture Effects

### Grain Overlay (`.grain::before`)

Adds film-grain texture on hero sections. `opacity: 0.06`, `mix-blend-mode: overlay`. Already defined in `assets/theme.css`.

### Hair Dividers (`.hair`)

```css
.hair {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
}
```

### Watermark Text (`.watermark`)

Large ghosted Fraunces text for editorial background layering. Pink gradient clipped to text, `color: transparent`.

### Product Card Backgrounds

Named gradient classes `.prod-bg-1` through `.prod-bg-6` in `assets/theme.css`. Always use these — never write custom inline product gradients.

---

## 10. Icon System

- **Source:** Lucide (stroke icons)
- **Global stroke:** `stroke-width: 1.5` — `--icon-stroke-width: 1.5` in `:root`
- **Standard sizes:** 16×16 (inline/buttons), 18×18 (nav), 24×24 (feature icons), 32×32 (hero)
- **Color:** Always `currentColor` — inherits from parent
- **Inline SVG only** — no `<img>` for icons, no emoji, no mixed filled/outline styles

Common icon paths:
- Arrow right: `M5 12h14M12 5l7 7-7 7`
- Plus: `M12 5v14M5 12h14`
- Minus: `M5 12h14`

---

## 11. Images

**Rule:** Never use bare `<img>` for product, hero, or editorial images. Use the `image` snippet:

```liquid
{%- render 'image',
  image: section.settings.image,
  sizes: '(max-width: 767px) 100vw, 50vw',
  ratio: '1/1',
  class: 'my-class'
-%}
```

For CDN/external images (category grid, marquee logos): use `<img>` with `loading="lazy"` and explicit `width`/`height` attributes to prevent CLS.

Hero images: `loading="eager" fetchpriority="high"`.

---

## 12. Section Design Patterns (Homepage)

### Hero

- Full viewport: `min-height: 100svh`
- Bleeds behind header: `margin-top: calc(-1 * var(--lm-header-h, 80px))`
- Two swapped `<img>` backgrounds (light/dark modes)
- Bottom marquee band for social proof text
- Grain texture overlay

### Brand Marquee

- Infinite scroll brand logos
- `hair` dividers above/below
- Logos: SVG, 80–120px wide, `opacity: 0.6` boosted on hover

### Brand Statement (Editorial Split)

- 2-column: text left, portrait image right
- Background: `var(--color-bg-soft)`
- CTA: `.lm-btn` outline style

### Category Grid

- 4×2 grid, section header with `§` eyebrow + h2 italic accent + "Alle anzeigen" right-aligned
- Cards: square ratio, vignette overlay, indexed with `01–08` monospaced numbers
- Mobile: 2-col grid

### FAQ Accordion

- Unified glass card, hairline-divided items
- `§` eyebrow + h2 with italic pink accent
- Expand/collapse with `aria-expanded`

---

## 13. Light/Dark Mode Implementation

Theme is set on `<html data-theme="light|dark">` before paint (synchronous script in `<head>`).

Priority order:
1. `localStorage['lm-theme']`
2. Shopify `settings.default_color_scheme`
3. `prefers-color-scheme` media query

Toggle: `<lamour-theme-toggle>` Web Component.

**Light mode note:** The cream background `#EBE7DE` is warm, not white. All "white" surfaces in designs should map to cream or `--color-bg-soft`, never `#FFFFFF`.

---

## 14. Custom Cursor

Desktop only (`@media (hover: hover) and (pointer: fine)`):

- `.cursor-dot`: 6px, `mix-blend-mode: difference`, white
- `.cursor-ring`: 34px ring, `1px solid rgba(255,255,255,0.35)`
- Hover state: dot hides, ring fills `rgba(245,151,177,0.55)` (pink)
- Touch devices: both elements `display: none !important`

---

## 15. Web Components

| Component | Tag | Purpose |
|-----------|-----|---------|
| `LamourThemeToggle` | `<lamour-theme-toggle>` | Light/dark toggle |
| `LamourCursor` | (implicit via JS) | Custom cursor |
| `LamourReveal` | `.reveal` + IntersectionObserver | Scroll reveal |

All extend `HTMLElement`, registered with `customElements.define('lamour-*', ...)`, loaded `defer` in `theme.liquid`.

---

## 16. Anti-Patterns

- ❌ Hardcoded hex in section CSS — use tokens
- ❌ `#FFFFFF` as a background — use `--color-bg` or `--color-bg-soft` (cream)
- ❌ Bare `<img>` for editorial/product images — use `image` snippet
- ❌ `{% include %}` — use `{%- render -%}` only
- ❌ `<style>` tags in sections — use `{% stylesheet %}` blocks
- ❌ Emoji as icons — use Lucide SVG stroke icons
- ❌ Border-radius > 4px on primary UI elements (luxury = square, not pill)
- ❌ Multiple primary CTAs per section
- ❌ Any JS framework — Web Components only
- ❌ Layout-shifting hover transforms (translateY(-2px) max)
- ❌ Pink text on pink background
- ❌ Missing `aria-label` on icon-only buttons
- ❌ Missing `prefers-reduced-motion` support
- ❌ Strings not added to both locale files

---

## 17. Pre-Delivery Checklist

- [ ] All colors reference CSS tokens — no hardcoded hex
- [ ] New strings in both `locales/en.default.json` and `locales/de.json` with `| t` filter
- [ ] Images: `{%- render 'image' -%}` snippet, or `loading="lazy"` + `width`/`height` for CDN
- [ ] Section CSS in `{% stylesheet %}` block only
- [ ] Hover transitions at `var(--dur-base)` (300ms)
- [ ] Focus states visible (2px pink outline or box-shadow equivalent)
- [ ] Interactive elements ≥ 44×44px touch target
- [ ] `prefers-reduced-motion` respected
- [ ] Tested: 375px (mobile), 768px (tablet), 1440px (desktop)
- [ ] No horizontal scroll on mobile
- [ ] Dark mode: `#EBE7DE` cream text on `#000000` — contrast ≥ 7:1 ✓
- [ ] Light mode: `#0E0E0E` near-black on `#EBE7DE` cream — contrast ≥ 7:1 ✓

---

## 18. Page-Specific Overrides

Overrides live in `design-system/pages/[page].md` and take precedence over this Master.

Current overrides: _(none — all pages use Master)_

To create a page override, add a file at `design-system/pages/[page-name].md` and document only the deviations from Master. Example: product page might override card grid columns or add a sticky ATC bar specification.
