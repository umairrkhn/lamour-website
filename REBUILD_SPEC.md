# Lamour Shopify Theme — Rebuild Specification

> Drop this file into a new empty repo. Everything needed to rebuild the storefront from a blank Shopify theme and connect it to the live store is documented here.

**Design reference:** `/Users/umair/Documents/GitHub/lamour-prototype` — a working HTML/React prototype containing the exact visual language for this theme. All CSS patterns below (grain, glass, mesh, keyframes, cursor) are extracted directly from `Lamour.html` and `app.jsx` in that repo. When making any design decision, open the prototype in a browser first and match it.

---

## 1. Store Identity

| Field | Value |
|---|---|
| Store domain | `xn--lmour-xqa.de` |
| Shopify store | `0b8499-39.myshopify.com` |
| Brand name | **L'Amour** |
| Brand language | German (primary), English (Shopify default locale) |
| Brand colors | Black `#000000`, White `#ffffff`, Signature pink `#f597b1` |

---

## 2. Scaffolding a New Theme from Scratch

### Research summary (verified May 2026)

| Theme | GitHub | Stars | Best for |
|---|---|---|---|
| **Skeleton** (⭐ recommended) | `github.com/Shopify/skeleton-theme` | 700+ | Full custom builds — minimal, no opinions |
| **Dawn** | `github.com/Shopify/dawn` | 3,000+ | Learning best practices, then stripping down |
| Community starters | various | low | Not recommended — unmaintained or opinionated |

**Use Skeleton.** Dawn is a complete reference theme with ~100 pre-built sections — great for studying patterns but adds bloat when building from scratch. Skeleton (launched May 2025 by Shopify) is the official minimal OS 2.0 starter: full blocks/sections/JSON templates structure, no design opinions, MIT licensed.

### Scaffold with Skeleton

```bash
# Install Shopify CLI
npm install -g @shopify/cli

# Option 1 — CLI init (defaults to Skeleton in 2025+)
shopify theme init lamour-theme

# Option 2 — clone directly
git clone https://github.com/Shopify/skeleton-theme.git lamour-theme
cd lamour-theme
rm -rf .git
git init
git add .
git commit -m "init: Shopify Skeleton base"
```

Connect to the store:

```bash
# Authenticate (opens browser)
shopify auth login --store=0b8499-39.myshopify.com

# Push as a new unpublished draft theme for QA
shopify theme push --unpublished --store=0b8499-39.myshopify.com

# Live dev server with hot reload
shopify theme dev --store=0b8499-39.myshopify.com
```

### Option B — Completely blank (minimal file structure)

If you want zero assumptions, create only the required files Shopify needs:

```
layout/
  theme.liquid          ← required
config/
  settings_schema.json  ← required (can be empty array [])
  settings_data.json    ← required (can be {})
templates/
  index.json            ← homepage template
locales/
  en.default.json       ← required (can be {})
```

Minimum `layout/theme.liquid`:

```liquid
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {{ content_for_header }}
  {{ 'theme.css' | asset_url | stylesheet_tag }}
</head>
<body>
  {{ content_for_layout }}
  {{ content_for_footer }}
</body>
</html>
```

### Linking a GitHub repo to Shopify

In the Shopify Admin:
1. **Online Store → Themes → Add theme → Connect from GitHub**
2. Authorize the GitHub app
3. Select your repo and branch (`main`)
4. Shopify will pull from that branch on every push

> The GitHub↔Shopify sync means every `git push origin main` deploys to the draft theme automatically. The live theme is only swapped when you click "Publish" in the Shopify Admin.

---

## 3. Required Shopify Admin Setup

These must exist in the Shopify Admin before the theme can render correctly. Create them at `Admin → Products / Navigation / Files` before pushing the theme.

### 3.1 Collections

Create these collection handles exactly (the handle is set in the URL slug field):

| Collection | Handle | Purpose |
|---|---|---|
| Neuheiten | `neuheiten` | "New Arrivals" — featured on homepage |
| Unsere Empfehlung | `unsere-empfehlung` | "Our Recommendation" — second homepage feature |
| Alle Produkte | `all` | Default catch-all (auto-created by Shopify) |
| Chanel | `chanel` | Brand collection, linked in promotion cards |

### 3.2 Products (hardcoded in homepage promotion cards)

These product handles are referenced directly in homepage JSON. The products must exist with these exact handles, or you must update the template JSON to match whatever handles you create:

| Product | Handle |
|---|---|
| Dior Sauvage Eau de Parfum 200 ml | `dior-sauvage-eau-de-parfum-200-ml` |
| Chanel Bleu Eau de Parfum 3×20 ml | `chanel-bleu-eau-de-parfum-3-x-20-ml` |
| Black Opium Eau de Parfum 30 ml | `black-opium-eau-de-parfum-30-ml` |
| La Vie Est Belle EDP Spray Refillable 100 ml | `la-vie-est-belle-eau-de-parfum-spray-refillable-100-ml` |
| Hugo Boss The Scent EDT 100 ml | `hugo-boss-the-scent-eau-de-toilette-100-ml` |

### 3.3 Navigation Menus

Create these menus in **Admin → Online Store → Navigation**:

| Menu handle | Label (shown in Admin) | Purpose |
|---|---|---|
| `main-menu` | Hauptmenü | Primary desktop navigation |
| `marken` | Marken | Mega menu dropdown for brands |
| `customer-account-main-menu` | Kundenkonto | Customer account sidebar nav |
| `footer` | Informationen | Footer column 1 |
| `weitere-informationen` | Weitere Fragen? | Footer column 2 |
| `ber-lamour` | Über Lamour | Footer column 3 |
| `backlinks` | Top Marken | Footer brand links |
| `top-produkte` | Top Produkte | Footer product links |

**Main menu suggested structure** (German copy, preserve exactly):

```
PARFUM          → /collections/all
  Damen         → /collections/damen-parfum
  Herren        → /collections/herren-parfum
  Unisex        → /collections/unisex-parfum
MARKEN          → /collections/all
  Chanel        → /collections/chanel
  Dior          → /collections/dior
  Hugo Boss     → /collections/hugo-boss
  ...
GESICHT         → /collections/gesicht
HAARE           → /collections/haare
KÖRPER          → /collections/korper
MAKE-UP         → /collections/make-up
```

### 3.4 Shop Images (Files)

Upload these to **Admin → Content → Files** before pushing the new theme. The theme references them via `shopify://shop_images/[filename]`:

| File name | Used in |
|---|---|
| `logo.png` | Header logo, header promotion image |
| `output-onlinepngtools_1.png` | Browser favicon |
| `hero_H1_primary.png` | Homepage hero slide 1 |
| `hero_H2_atmosphere.png` | Homepage hero slide 2 |
| `hero_H3_lifestyle.png` | Homepage hero slide 3 |
| `brand-statement_BS1_rose.png` | Brand statement section image |
| `about-1.png` | Media/text overlay section |
| `about-2.jpg` | Media/text overlay section |
| `prod2_4c233e08-bf96-4885-a3fb-22272fd1aaf6.png` | Promotion card |
| `prod3_c54ae2c8-96e5-4020-a0ae-0a4fceb3391e.png` | Promotion card |
| `image_29258.jpg` | Content block |
| `image_86248.jpg` | Content block |

---

## 4. Design Tokens + Light/Dark Mode

### 4.1 Light/Dark mode architecture

The theme supports both modes via a `data-theme` attribute on `<html>`. Light is the default. The user can toggle; the choice is persisted to `localStorage`. The system preference (`prefers-color-scheme`) is respected on first visit.

**How it works:**
- CSS custom properties are defined per-theme under `[data-theme="light"]` and `[data-theme="dark"]`
- All colours in sections and components reference the tokens — never hardcoded hex values
- A vanilla Web Component `<lamour-theme-toggle>` handles the button + state
- Shopify theme settings expose a "Default theme" option (light / dark / system)

**CSS token structure** — paste into `assets/theme.css`:

```css
/* ── Shared tokens (never change between modes) ────────────────────────── */
:root {
  --color-pink:      #f597b1;
  --color-pink-dim:  rgba(245, 151, 177, 0.15);

  --font-display: 'Fraunces', 'Times New Roman', serif;
  --font-body:    'Inter', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', ui-monospace, monospace;

  --text-hero:    clamp(3.5rem, 8vw, 7.5rem);
  --text-display: clamp(2.5rem, 5vw, 5rem);
  --text-heading: clamp(2rem, 4vw, 3.5rem);
  --text-sub:     clamp(1.5rem, 3vw, 2.25rem);
  --text-body:    1rem;
  --text-small:   0.875rem;
  --text-micro:   0.75rem;

  --space-section: clamp(5rem, 10vw, 9rem);
  --space-gap:     clamp(3rem, 6vw, 7rem);
  --container:     1400px;

  --ease-out:    cubic-bezier(0.16, 1, 0.3, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --dur-fast:  150ms;
  --dur-base:  300ms;
  --dur-slow:  600ms;
  --dur-reveal: 800ms;
}

/* ── Light mode (default) ──────────────────────────────────────────────── */
[data-theme="light"],
:root {
  --color-bg:       #faf9f7;
  --color-bg-soft:  #f4f2ef;
  --color-bg-card:  #ffffff;
  --color-surface:  #eeebe7;
  --color-border:   rgba(0,0,0,0.10);

  --color-text:     #0e0e0e;
  --color-text-70:  rgba(14,14,14,0.70);
  --color-text-40:  rgba(14,14,14,0.40);
  --color-text-10:  rgba(14,14,14,0.10);

  --color-glass:        rgba(255,255,255,0.60);
  --color-glass-strong: rgba(255,255,255,0.85);
  --blur-glass:        blur(18px) saturate(140%);
  --blur-glass-strong: blur(24px) saturate(160%);

  --color-nav-bg:    rgba(250,249,247,0.72);
  --color-nav-border: rgba(0,0,0,0.08);
}

/* ── Dark mode ─────────────────────────────────────────────────────────── */
[data-theme="dark"] {
  --color-bg:       #000000;
  --color-bg-soft:  #0a0a0a;
  --color-bg-card:  #111111;
  --color-surface:  #1a1a1a;
  --color-border:   rgba(255,255,255,0.10);

  --color-text:     #ffffff;
  --color-text-70:  rgba(255,255,255,0.70);
  --color-text-40:  rgba(255,255,255,0.40);
  --color-text-10:  rgba(255,255,255,0.10);

  --color-glass:        rgba(255,255,255,0.05);
  --color-glass-strong: rgba(255,255,255,0.10);
  --blur-glass:        blur(18px) saturate(140%);
  --blur-glass-strong: blur(24px) saturate(160%);

  --color-nav-bg:    rgba(12,12,12,0.72);
  --color-nav-border: rgba(255,255,255,0.08);
}

/* ── System preference fallback (first visit, no localStorage) ─────────── */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    --color-bg:       #000000;
    --color-bg-soft:  #0a0a0a;
    --color-bg-card:  #111111;
    --color-surface:  #1a1a1a;
    --color-border:   rgba(255,255,255,0.10);
    --color-text:     #ffffff;
    --color-text-70:  rgba(255,255,255,0.70);
    --color-text-40:  rgba(255,255,255,0.40);
    --color-text-10:  rgba(255,255,255,0.10);
    --color-glass:        rgba(255,255,255,0.05);
    --color-glass-strong: rgba(255,255,255,0.10);
    --color-nav-bg:    rgba(12,12,12,0.72);
    --color-nav-border: rgba(255,255,255,0.08);
  }
}
```

**Using tokens in sections** — every colour reference goes through a variable:

```css
/* ✅ correct */
.product-card { background: var(--color-bg-card); color: var(--color-text); }

/* ❌ wrong — breaks dark mode */
.product-card { background: #ffffff; color: #0e0e0e; }
```

### 4.2 Theme toggle Web Component

Add to `assets/theme.js`:

```js
class LamourThemeToggle extends HTMLElement {
  connectedCallback() {
    this.button = this.querySelector('button');
    this.apply(this.current());
    this.button?.addEventListener('click', () => this.toggle());
  }

  current() {
    return localStorage.getItem('lm-theme')
      || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  }

  apply(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('lm-theme', theme);
    if (this.button) {
      this.button.setAttribute('aria-label', theme === 'dark' ? 'Zum hellen Modus wechseln' : 'Zum dunklen Modus wechseln');
      this.button.setAttribute('aria-pressed', theme === 'dark' ? 'true' : 'false');
    }
  }

  toggle() {
    this.apply(document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
  }
}
customElements.define('lamour-theme-toggle', LamourThemeToggle);
```

Add to `layout/theme.liquid` — **before `content_for_header`** to prevent flash of wrong theme:

```html
<script>
  (function(){
    var t = localStorage.getItem('lm-theme')
      || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', t);
  })();
</script>
```

> This inline script runs synchronously before the first paint — the only acceptable reason to have a blocking script in `<head>`. It prevents the "flash of unstyled light mode" when the user has chosen dark.

Toggle button snippet (`snippets/theme-toggle.liquid`):

```liquid
<lamour-theme-toggle>
  <button
    class="lm-theme-btn"
    aria-label="Farbschema wechseln"
    aria-pressed="false"
    type="button"
  >
    <span class="lm-theme-btn__icon lm-theme-btn__icon--sun" aria-hidden="true">
      {%- render 'icon', name: 'sun' -%}
    </span>
    <span class="lm-theme-btn__icon lm-theme-btn__icon--moon" aria-hidden="true">
      {%- render 'icon', name: 'moon' -%}
    </span>
  </button>
</lamour-theme-toggle>
```

CSS for the toggle button:

```css
.lm-theme-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px; height: 36px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-glass);
  backdrop-filter: var(--blur-glass);
  -webkit-backdrop-filter: var(--blur-glass);
  cursor: pointer;
  color: var(--color-text);
  transition: border-color var(--dur-base) ease, background var(--dur-base) ease;
}
.lm-theme-btn__icon--moon { display: none; }

[data-theme="dark"] .lm-theme-btn__icon--sun  { display: none; }
[data-theme="dark"] .lm-theme-btn__icon--moon { display: block; }
```

Render the toggle inside the header nav, next to cart/search icons:

```liquid
{%- render 'theme-toggle' -%}
```

### 4.3 Shopify customizer setting (default mode)

In `config/settings_schema.json`, add a setting so the merchant can choose the default:

```json
{
  "type": "select",
  "id": "default_color_scheme",
  "label": "Default color mode",
  "options": [
    { "value": "light", "label": "Light" },
    { "value": "dark",  "label": "Dark" },
    { "value": "system","label": "Follow system preference" }
  ],
  "default": "light"
}
```

Read it in `layout/theme.liquid` and pass to the inline script:

```liquid
<script>
  (function(){
    var stored = localStorage.getItem('lm-theme');
    var systemDark = matchMedia('(prefers-color-scheme: dark)').matches;
    var shopDefault = '{{ settings.default_color_scheme }}';
    var t = stored || (shopDefault === 'system' ? (systemDark ? 'dark' : 'light') : shopDefault);
    document.documentElement.setAttribute('data-theme', t);
  })();
</script>
```

### 4.4 Google Fonts import

Load this **before** any other stylesheet (top of `<head>`, before `content_for_header`):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,500;9..144,600;9..144,700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

Fraunces variation settings (from prototype `Lamour.html`):

```css
/* Display headings — editorial, bold */
.font-display {
  font-family: 'Fraunces', 'Times New Roman', serif;
  font-optical-sizing: auto;
  font-variation-settings: 'SOFT' 20, 'WONK' 0;
  font-weight: 700;
  letter-spacing: -0.035em;
}

/* Body serif — softer, lighter */
.font-serif {
  font-family: 'Fraunces', 'Times New Roman', serif;
  font-optical-sizing: auto;
  font-variation-settings: 'SOFT' 30, 'WONK' 0;
}

/* Uppercase label/eyebrow — Inter condensed */
.font-sub {
  font-family: 'Inter', system-ui, sans-serif;
  font-weight: 300;
  letter-spacing: 0.28em;
  text-transform: uppercase;
}
```

---

## 4B. Prototype CSS Patterns

> Source: `/Users/umair/Documents/GitHub/lamour-prototype/Lamour.html`
> Every pattern below is copy-paste ready. Do not deviate from these without a design reason.

### Grain overlay (filmic texture)

Applied to any section needing cinematic depth. Add class `grain` + `position: relative` to the container:

```css
.grain::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.35 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  opacity: 0.06;
  mix-blend-mode: overlay;
}
```

### Glassmorphism variants

Three tiers — use contextually:

```css
/* Nav, floating cards — subtle */
.glass {
  background: rgba(12,12,12,0.55);
  backdrop-filter: blur(18px) saturate(140%);
  -webkit-backdrop-filter: blur(18px) saturate(140%);
  border: 1px solid rgba(255,255,255,0.08);
}

/* Sticky header on scroll, modals — stronger */
.glass-strong {
  background: rgba(20,20,20,0.72);
  backdrop-filter: blur(24px) saturate(160%);
  -webkit-backdrop-filter: blur(24px) saturate(160%);
  border: 1px solid rgba(255,255,255,0.10);
}

/* Pink-tinted — hover states, highlight cards */
.glass-pink {
  background: linear-gradient(135deg, rgba(244,150,176,0.14), rgba(244,150,176,0.04));
  backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid rgba(244,150,176,0.25);
}
```

In **light mode**, glass uses warm white instead:

```css
[data-theme="light"] .glass {
  background: rgba(250,249,247,0.72);
  border-color: rgba(0,0,0,0.08);
}
[data-theme="light"] .glass-strong {
  background: rgba(255,255,255,0.88);
  border-color: rgba(0,0,0,0.10);
}
```

### Gradient mesh hero background

```css
.mesh-hero {
  background:
    radial-gradient(60% 50% at 20% 25%, rgba(244,150,176,0.35), transparent 60%),
    radial-gradient(40% 40% at 85% 75%, rgba(244,150,176,0.25), transparent 60%),
    radial-gradient(35% 45% at 65% 20%, rgba(255,200,214,0.18), transparent 65%),
    radial-gradient(50% 50% at 50% 110%, rgba(244,150,176,0.22), transparent 65%),
    linear-gradient(180deg, #030303 0%, #000 60%, #000 100%);
}
```

### Animation keyframes (copy into `assets/theme.css`)

```css
/* Hero title entrance — scale + blur + letter-spacing */
@keyframes heroIn {
  0%   { opacity: 0; transform: scale(0.94); letter-spacing: 0.04em; filter: blur(14px); }
  100% { opacity: 1; transform: scale(1);    letter-spacing: -0.03em; filter: blur(0); }
}
.hero-title { animation: heroIn 1.6s cubic-bezier(.2,.7,.2,1) both; }
.hero-sub   { animation: heroIn 1.4s 0.5s cubic-bezier(.2,.7,.2,1) both; }

/* Pink shimmer on text */
@keyframes shimmer {
  0%   { background-position: -200% 0; }
  100% { background-position:  200% 0; }
}
.shimmer {
  background: linear-gradient(90deg,
    transparent 0%,
    rgba(244,150,176,0.25) 40%,
    rgba(255,255,255,0.5) 50%,
    rgba(244,150,176,0.25) 60%,
    transparent 100%);
  background-size: 200% 100%;
  animation: shimmer 2.4s linear infinite;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

/* Brand marquee scroll */
@keyframes marquee {
  0%   { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.marquee-track { animation: marquee 40s linear infinite; }

/* Floating element (e.g. product image) */
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50%       { transform: translateY(-14px) rotate(0.5deg); }
}
.float { animation: float 7s ease-in-out infinite; }

/* Pulsing ring (scan / highlight effect) */
@keyframes pulseRing {
  0%   { transform: scale(0.7); opacity: 0.8; }
  100% { transform: scale(2.2); opacity: 0; }
}
.pulse-ring   { animation: pulseRing 2s cubic-bezier(.2,.7,.2,1) infinite; }
.pulse-ring-2 { animation-delay: 0.6s; }
.pulse-ring-3 { animation-delay: 1.2s; }

/* Scroll reveal — JS adds .in class via IntersectionObserver */
.reveal {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 1s cubic-bezier(.2,.7,.2,1), transform 1s cubic-bezier(.2,.7,.2,1);
}
.reveal.in { opacity: 1; transform: none; }
.reveal-delay-1 { transition-delay: 120ms; }
.reveal-delay-2 { transition-delay: 240ms; }
.reveal-delay-3 { transition-delay: 360ms; }

/* Reduce motion kill-switch */
@media (prefers-reduced-motion: reduce) {
  .hero-title, .hero-sub, .shimmer, .marquee-track, .float,
  .pulse-ring, .reveal { animation: none !important; transition: none !important; }
  .reveal { opacity: 1; transform: none; }
}
```

### Product card background gradients (dark mode)

Used when no product image is available, or as card underlays:

```css
.prod-bg-1 {
  background:
    radial-gradient(circle at 30% 20%, rgba(244,150,176,0.55), transparent 55%),
    radial-gradient(circle at 70% 80%, rgba(0,0,0,0.6), transparent 60%),
    linear-gradient(135deg, #1a1416 0%, #2a1a1f 50%, #0a0607 100%);
}
.prod-bg-2 {
  background:
    radial-gradient(circle at 80% 10%, rgba(244,150,176,0.4), transparent 55%),
    linear-gradient(180deg, #0a0a0a 0%, #1a0e12 100%);
}
.prod-bg-3 {
  background:
    radial-gradient(circle at 20% 80%, rgba(244,150,176,0.5), transparent 60%),
    linear-gradient(135deg, #0a0a0a, #000);
}
```

### Oversized watermark text

```css
.watermark {
  font-family: 'Fraunces', serif;
  font-weight: 600;
  letter-spacing: -0.04em;
  line-height: 0.82;
  background: linear-gradient(180deg, rgba(244,150,176,0.14) 0%, rgba(244,150,176,0.02) 70%, transparent 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
```

### Thin divider line

```css
.hair {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
}
```

### Custom cursor (desktop only)

HTML in `layout/theme.liquid` before `</body>`:

```html
<div class="cursor-dot" aria-hidden="true"></div>
<div class="cursor-ring" aria-hidden="true"></div>
```

CSS:

```css
@media (hover: hover) and (pointer: fine) {
  html, body { cursor: none; }
  a, button, [data-hover] { cursor: none; }

  .cursor-dot, .cursor-ring {
    position: fixed; top: 0; left: 0;
    pointer-events: none; z-index: 9999;
    transform: translate3d(-100px,-100px,0);
    will-change: transform;
  }
  .cursor-dot {
    width: 6px; height: 6px;
    border-radius: 9999px;
    background: #fff;
    mix-blend-mode: difference;
    transition: width .18s ease, height .18s ease, opacity .2s ease;
  }
  .cursor-ring {
    width: 34px; height: 34px;
    border-radius: 9999px;
    border: 1px solid rgba(255,255,255,0.35);
    margin-left: -17px; margin-top: -17px;
    transition: width .28s cubic-bezier(.2,.7,.2,1), height .28s cubic-bezier(.2,.7,.2,1),
                background .25s ease, border-color .25s ease;
  }
  /* Hover: pink disc */
  .cursor-hover .cursor-dot { opacity: 0; }
  .cursor-hover .cursor-ring {
    width: 40px; height: 40px;
    margin-left: -20px; margin-top: -20px;
    background: rgba(244,150,176,0.55);
    border-color: transparent;
  }
  /* Press: shrink */
  .cursor-press .cursor-ring { transform: translate3d(var(--cx,0), var(--cy,0), 0) scale(0.82); }
}
@media (hover: none), (pointer: coarse) {
  .cursor-dot, .cursor-ring { display: none !important; }
}
```

JS (in `assets/theme.js`):

```js
class LamourCursor extends HTMLElement {
  connectedCallback() {
    const dot  = document.querySelector('.cursor-dot');
    const ring = document.querySelector('.cursor-ring');
    if (!dot || !ring) return;
    let rx = -100, ry = -100, mx = -100, my = -100;
    const lerp = (a, b, t) => a + (b - a) * t;

    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    document.addEventListener('mousedown', () => document.documentElement.classList.add('cursor-press'));
    document.addEventListener('mouseup',   () => document.documentElement.classList.remove('cursor-press'));

    document.querySelectorAll('a,button,[data-hover]').forEach(el => {
      el.addEventListener('mouseenter', () => document.documentElement.classList.add('cursor-hover'));
      el.addEventListener('mouseleave', () => document.documentElement.classList.remove('cursor-hover'));
    });

    const tick = () => {
      rx = lerp(rx, mx, 0.12); ry = lerp(ry, my, 0.12);
      dot.style.transform  = `translate3d(${mx}px,${my}px,0)`;
      ring.style.transform = `translate3d(${rx}px,${ry}px,0)`;
      ring.style.setProperty('--cx', `${rx}px`);
      ring.style.setProperty('--cy', `${ry}px`);
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
}
customElements.define('lamour-cursor', LamourCursor);
```

### Scroll reveal (IntersectionObserver)

JS (in `assets/theme.js`):

```js
class LamourReveal extends HTMLElement {
  connectedCallback() {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));
  }
}
customElements.define('lamour-reveal', LamourReveal);
```

Add to `layout/theme.liquid` before `</body>`:

```html
<lamour-cursor></lamour-cursor>
<lamour-reveal></lamour-reveal>
```

---

## 5. Theme File Structure

Build toward this structure. Files marked ★ are the minimum to get the store running:

```
assets/
  theme.css          ★  main stylesheet
  theme.js           ★  vanilla JS — Web Components only, no jQuery
  component-cart.js      cart drawer
  component-product-form.js  variant selection, add to cart
  component-search.js    predictive search

blocks/
  heading.liquid         reusable heading block
  rich-text.liquid       body text block
  button.liquid          CTA button block
  image.liquid           image block

config/
  settings_schema.json   ★  theme customizer schema
  settings_data.json     ★  saved customizer values

layout/
  theme.liquid           ★  root layout

locales/
  en.default.json        ★  English strings
  de.json                    German strings

sections/
  header.liquid          ★  sticky nav
  footer.liquid          ★  footer with menus + newsletter
  announcement-bar.liquid    top promo bar
  hero.liquid            ★  homepage hero (full-bleed, dark gradient)
  featured-collection.liquid ★  product grid by collection
  brand-marquee.liquid       scrolling brand strip
  brand-statement.liquid     editorial text + image block
  promotion-cards.liquid     3-up product/brand feature cards
  media-text.liquid          image left/right with text
  newsletter.liquid          email signup
  content-toggles.liquid     FAQ accordion
  main-product.liquid    ★  PDP — product detail page
  main-collection.liquid ★  PLP — product listing/grid + filters
  main-cart.liquid       ★  cart page
  main-search.liquid         search results
  main-page.liquid       ★  generic content page
  404.liquid             ★  not found page
  password.liquid            password gate

snippets/
  product-card.liquid    ★  reusable product card (used in all grids)
  price.liquid               formatted price with sale state
  image.liquid           ★  lazy-loading image wrapper
  icon.liquid                SVG icon sprite helper
  breadcrumb.liquid          breadcrumb trail

templates/
  index.json             ★  homepage
  product.json           ★  product detail
  collection.json        ★  collection listing
  cart.json              ★  cart
  search.json                search results
  page.json              ★  generic page
  page.contact.json          contact page
  page.faq.json              FAQ page
  404.json               ★  not found
  password.json              store password gate
  customers/
    login.json
    register.json
    account.json
    addresses.json
    order.json
    reset_password.json
    activate_account.json
    blog.json
    article.json
```

---

## 6. Section Architecture Rules

### 6.1 Every section must have a schema

```liquid
{% schema %}
{
  "name": "Section Name",
  "settings": [],
  "presets": [{ "name": "Section Name" }]
}
{% endschema %}
```

### 6.2 Build sections as block consumers (OS 2.0 pattern)

Don't hardcode content in section Liquid. Use `{% content_for 'blocks' %}` so the merchant can reorder blocks in the customizer:

```liquid
{% schema %}
{
  "name": "Hero",
  "blocks": [
    { "type": "heading" },
    { "type": "rich-text" },
    { "type": "button" }
  ],
  "presets": [...]
}
{% endschema %}
```

### 6.3 All images through the lazy-image snippet

Never use a bare `<img>` tag. Always:

```liquid
{%- render 'image',
  image: section.settings.image,
  sizes: '(max-width: 767px) 100vw, 50vw',
  ratio: '0.75'
-%}
```

The `snippets/image.liquid` snippet should use `image_url` filter + native `loading="lazy"` + full `srcset` across breakpoints.

### 6.4 CSS scoping

Use `{% stylesheet %}` for section-scoped styles that only load when the section is on the page:

```liquid
{% stylesheet %}
  .my-section { ... }
{% endstylesheet %}
```

Use `assets/theme.css` for global tokens and component resets.

### 6.5 JS — Web Components only

```js
class LamourCart extends HTMLElement {
  connectedCallback() { ... }
}
customElements.define('lamour-cart', LamourCart);
```

Load with `defer` in `layout/theme.liquid`. No jQuery. No frameworks.

---

## 7. Cart & Checkout Configuration

### Cart behavior

In `config/settings_data.json`, set:

```json
{
  "cart_action": "overlay",
  "cart_recommendations": true,
  "cart_additional_buttons": false
}
```

`"overlay"` means the cart opens as a sidebar drawer, not a redirect to `/cart`. Your `theme.js` must handle the `cart:open` custom event to show/hide the drawer.

### Checkout

Shopify handles all checkout routing. Your theme only needs:
- A cart form that `POST`s to `routes.cart_url`
- A checkout button that links to `routes.checkout_url`
- The standard Liquid `{% form 'cart', cart %}` wrapper

Do **not** intercept or modify the checkout flow — Shopify owns that completely.

### Cart AJAX API

For add-to-cart without page reload, use Shopify's AJAX Cart API:

```js
// Add to cart
fetch('/cart/add.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id: variantId, quantity: 1 })
});

// Get cart state
fetch('/cart.js').then(r => r.json());

// Update quantity
fetch('/cart/change.js', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ id: variantId, quantity: newQty })
});
```

---

## 8. Key Liquid Patterns

### 8.1 Collection product grid

```liquid
{%- assign collection = collections[section.settings.collection] -%}
{%- for product in collection.products limit: section.settings.products_to_show -%}
  {%- render 'product-card', product: product -%}
{%- endfor -%}
```

### 8.2 Product variant selector

```liquid
<product-form>
  {% form 'product', product %}
    <select name="id">
      {%- for variant in product.variants -%}
        <option
          value="{{ variant.id }}"
          {% unless variant.available %}disabled{% endunless %}
        >{{ variant.title }}</option>
      {%- endfor -%}
    </select>
    <button type="submit" name="add">In den Warenkorb</button>
  {% endform %}
</product-form>
```

### 8.3 Navigation rendering

```liquid
<ul>
  {%- for link in linklists[section.settings.menu].links -%}
    <li>
      <a href="{{ link.url }}" {% if link.active %}aria-current="page"{% endif %}>
        {{ link.title }}
      </a>
    </li>
  {%- endfor -%}
</ul>
```

### 8.4 Money formatting

```liquid
{{ product.price | money }}           {# 12,99 € #}
{{ product.price | money_without_currency }}   {# 12,99 #}
{{ product.compare_at_price | money }}
```

### 8.5 Image with srcset

```liquid
{%- if image != blank -%}
  <img
    src="{{ image | image_url: width: 800 }}"
    srcset="
      {{ image | image_url: width: 400 }} 400w,
      {{ image | image_url: width: 800 }} 800w,
      {{ image | image_url: width: 1200 }} 1200w,
      {{ image | image_url: width: 1600 }} 1600w
    "
    sizes="{{ sizes | default: '100vw' }}"
    alt="{{ image.alt | escape }}"
    loading="lazy"
    width="{{ image.width }}"
    height="{{ image.height }}"
  >
{%- endif -%}
```

### 8.6 Translation (t filter)

Always use `t` filter for any user-facing string so German translations work:

```liquid
{{ 'products.product.add_to_cart' | t }}
{{ 'cart.general.title' | t }}
```

Add German strings to `locales/de.json`:

```json
{
  "products": {
    "product": {
      "add_to_cart": "In den Warenkorb"
    }
  },
  "cart": {
    "general": {
      "title": "Warenkorb"
    }
  }
}
```

---

## 9. Homepage Section Order

The `templates/index.json` should compose sections in this order:

```
1. Announcement Bar (header-group)
2. Header / Navigation (header-group)
3. Hero / Slideshow — full-bleed, dark gradient mesh, Fraunces display headline
4. Brand Marquee — scrolling strip: CHANEL · DIOR · HUGO BOSS · ...
5. Brand Statement — editorial text + portrait image
6. Featured Collection — "Neuheiten" grid (collection handle: neuheiten)
7. Promotion Cards — 3 brand/product feature cards (Dior, Chanel, Hugo Boss)
8. Media + Text — lifestyle image with brand copy
9. Featured Collection — "Unsere Empfehlung" grid (collection handle: unsere-empfehlung)
10. Content Toggles / FAQ accordion
11. Newsletter signup
12. Footer (footer-group)
```

### German copy — never change

These strings appear in templates and section presets. Copy them exactly:

```
Hero CTA:            "JETZT SHOPPEN"
New Arrivals:        "Neuheiten"
Our Recommendation:  "Unsere Empfehlung"
Shipping note:       "Versandzeit: 3-6 Werktage"
Free shipping bar:   "Kostenloser Versand ab 50€"
Cart heading:        "Warenkorb"
Cart oft together:   "Oft zusammen gekauft"
Brand statement §:   "Brand Statement"
Top brands §:        "UNSERE TOP MARKEN"
```

---

## 10. App Integrations

### 10.1 Avada SEO

Avada injects its snippets automatically when installed on the store. After installing the app, render its snippets in `layout/theme.liquid`:

```liquid
{%- render 'avada-seo' -%}
{%- render 'avada-seo-meta' -%}
```

Place these inside `<head>` before `</head>`. Avada also needs a custom search template at `templates/search.avada-seo.liquid`.

> Avada uses the deprecated `include` tag instead of `render`. This is an Avada limitation — don't fix it in your theme code.

### 10.2 CLS Speed App (SpeedUP.GURU / CrazyLoad)

This app wraps all scripts to defer them. It injects `__clspeedapp-*` snippets via `content_for_header`. **Do not replicate or reimport its behavior** — simply having the app installed on the store is enough. The app manages its own file injection.

If you do NOT install CLS Speed App, add native lazy loading and script deferral yourself:

```liquid
{# In layout/theme.liquid, load non-critical scripts with defer #}
<script src="{{ 'theme.js' | asset_url }}" defer></script>
```

### 10.3 Logolicious (if re-added)

Brand logo carousel installed as an app block. Add `{ "type": "@app" }` to the blocks array of your homepage slideshow section schema, then select it in the customizer.

---

## 11. settings_schema.json — Minimum Color + Typography Settings

Paste this into `config/settings_schema.json` as the base customizer options:

```json
[
  {
    "name": "theme_info",
    "theme_name": "Lamour",
    "theme_version": "1.0.0",
    "theme_author": "Custom",
    "theme_documentation_url": "",
    "theme_support_url": ""
  },
  {
    "name": "Colors",
    "settings": [
      { "type": "color", "id": "color_bg", "label": "Background", "default": "#000000" },
      { "type": "color", "id": "color_text", "label": "Text", "default": "#ffffff" },
      { "type": "color", "id": "color_accent", "label": "Accent (pink)", "default": "#f597b1" }
    ]
  },
  {
    "name": "Typography",
    "settings": [
      { "type": "font_picker", "id": "heading_font", "label": "Heading font", "default": "fraunces_n4" },
      { "type": "font_picker", "id": "body_font", "label": "Body font", "default": "inter_n4" }
    ]
  },
  {
    "name": "Layout",
    "settings": [
      { "type": "range", "id": "container_width", "label": "Max container width (px)", "min": 1000, "max": 1800, "step": 40, "default": 1400 }
    ]
  }
]
```

---

## 12. Shopify CLI Cheatsheet

```bash
# Authenticate
shopify auth login --store=0b8499-39.myshopify.com

# List themes on the store
shopify theme list --store=0b8499-39.myshopify.com

# Push as new unpublished draft (safe — doesn't affect live)
shopify theme push --unpublished --store=0b8499-39.myshopify.com

# Push to a specific existing theme ID
shopify theme push --theme=<theme-id> --store=0b8499-39.myshopify.com

# Pull a theme from the store into working directory
shopify theme pull --theme=<theme-id> --store=0b8499-39.myshopify.com

# Start local dev server with hot reload
shopify theme dev --store=0b8499-39.myshopify.com

# Lint Liquid files
shopify theme check

# Open the store customizer for a theme
shopify theme open --theme=<theme-id> --store=0b8499-39.myshopify.com
```

---

## 13. GitHub → Shopify Deployment Flow

Once you've connected the new repo to Shopify via the GitHub integration:

```
git push origin main
  → Shopify detects the push
  → Shopify pulls and syncs to the connected draft theme
  → Preview the draft at: Admin → Online Store → Themes → [theme] → Preview
  → Click "Publish" in Admin when ready to go live
```

To connect:

1. Shopify Admin → **Online Store → Themes → Add theme → Connect from GitHub**
2. Install the Shopify GitHub app on your GitHub account
3. Select repo and branch (`main`)
4. Shopify creates a new draft theme linked to that branch

**Important:** Only one branch can be connected per theme. If you want staging vs. production, push to separate branches and connect each to a different theme on the store.

---

## 14. What NOT to Build in the Theme

These are handled by Shopify itself or installed apps — do not replicate:

- **Checkout flow** — Shopify owns `/checkout` entirely
- **Customer account pages** — Shopify owns `/account`, `/login`, `/register` (unless using New Customer Accounts, which is a separate Shopify setting)
- **Payment processing** — configured in Admin → Payments, not in theme files
- **Shipping rates** — Admin → Shipping and Delivery
- **Tax calculation** — Shopify-managed
- **Inventory management** — Admin → Products
- **Order fulfillment** — Admin → Orders
- **SEO meta injection** — Avada SEO handles this; theme only needs the `render 'avada-seo'` call

---

## 15. Pre-Launch Checklist

- [ ] All 4 collection handles exist in Shopify Admin with correct slugs
- [ ] All 5 hardcoded product handles exist with correct slugs
- [ ] All 7+ nav menus created with correct handles
- [ ] All shop images uploaded to Admin → Content → Files
- [ ] Google Fonts preconnect + import in `<head>` before `content_for_header`
- [ ] Avada SEO app installed and snippets rendered in `layout/theme.liquid`
- [ ] Cart action set to `overlay` in `settings_data.json`
- [ ] German locale strings in `locales/de.json`
- [ ] `shopify theme check` returns 0 errors on your own files
- [ ] Mobile nav tested at 375px and 428px
- [ ] Cart drawer open/close tested
- [ ] Add-to-cart tested on a real product
- [ ] Checkout flow tested end-to-end (use Shopify's bogus gateway for test orders)
- [ ] `prefers-reduced-motion` kills all animations when enabled
- [ ] All images use `loading="lazy"` and explicit `width`/`height`
