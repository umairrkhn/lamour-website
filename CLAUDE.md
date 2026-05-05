# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Type

This is a **Shopify theme**, not an application. It is the **"Local" theme by KrownThemes (v2.4.0.1)**, configured for **Lamour**, a German fragrance/beauty brand on the domain `xn--lmour-xqa.de`. There is no `package.json`, no build step, and no test suite — files are deployed as-is to Shopify, which compiles Liquid server-side.

The repo is connected to a Shopify store via GitHub integration: `main` is the live theme, `development` is the working branch (recent commits are validations of the GitHub → Shopify sync).

## Development Workflow

Standard Shopify CLI (run from the user's shell, not installed in-repo):

- `shopify theme dev` — local preview against the linked store with hot reload
- `shopify theme pull` — pull latest from the store (use before editing if the merchant edited via Shopify admin)
- `shopify theme push --unpublished` — push working copy as a hidden theme for QA
- `shopify theme check` — Liquid linter (Theme Check)

There are no unit tests. "Testing" is visual/manual in the Shopify preview. Type checks and bundlers do not apply.

## Scale & Inventory

- **62 sections** in `sections/`
- **55 snippets** in `snippets/`
- **21 JSON templates** in `templates/` (plus a few legacy `.liquid` templates)
- **73 assets** in `assets/` (33 JS + 39 CSS + 1 PNG)
- **33 locale files** in `locales/` (full translations, default `en.default.json`, but production display language is **German**)
- **~25,000 lines** of Liquid total

**Largest files (concentrated complexity):**
- `sections/main-product.liquid` — ~81 KB
- `sections/featured-product.liquid` — ~65 KB
- `sections/product-quick-view.liquid` — ~60 KB
- `assets/__clspeedapp-jquery.js` — 90 KB (full jQuery 3.6.0 bundle)
- `assets/theme.css` — 52 KB
- `assets/component-product-form.js` — 24 KB
- `assets/component-slider.js` — 21 KB
- `assets/section-header.js` — 17 KB

The three product sections together are ~206 KB of largely duplicated variant/media/pricing logic — the single biggest refactor target.

## Architecture

### CrazyLoad / clspeedapp performance layer (load-bearing)

`layout/theme.liquid` does **not** render HTML directly. It captures the entire document into a `__clspeedapp-html` variable, then runs it through 11 `__clspeedapp-*` snippets that transform the output before sending it to the browser:

- `__clspeedapp-theme-config` — initialization, perf timers, script queues
- `__clspeedapp-js-init` — engine setup, lazySizesConfig, hardcoded exception list
- `__clspeedapp-js-functions`, `__clspeedapp-js-frontend`, `__clspeedapp-js-scripts` — JS utilities, event listeners, third-party loader (Trekkie, reCAPTCHA)
- `__clspeedapp-html-css`, `__clspeedapp-html-css-critical` — non-critical CSS deferred, critical CSS inlined
- `__clspeedapp-html-fonts` — font preloads
- `__clspeedapp-theme-html` — converts `<script src>`/`<iframe src>` to `data-src` for lazy loading; injects LCP image preloads
- `__clspeedapp-theme-preload`, `__clspeedapp-image` — image preload + transformation

**Implication for edits:** raw `<script>`, `<link>`, or `<img>` tags dropped into Liquid bypass this perf layer and may behave differently in production than in preview. Route new assets through the existing `__clspeedapp-*` mechanisms or the helper snippets (`lazy-image`, `lazy-svg`).

The exception list (in `__clspeedapp-js-init.liquid`) is hardcoded — Shopify analytics, `window.theme = window.theme`, `window.asyncLoad`, etc. are explicitly NOT deferred.

### Page composition

Pages are JSON Online Store 2.0 templates that compose sections.

- **`index.json`** — slideshow → Logolicious app block → 2× `featured-collection` (Neuheiten, Unsere Empfehlung) → `promotion-cards` (4 hand-curated: Dior Sauvage, Chanel Bleu, Chanel Misia, Hugo Boss The Scent) → `media-with-text-overlay` → `content-toggles` (4 brand accordions) → `newsletter`
- **`product.json`** — `main-product` (12 blocks: vendor, title, price, variant picker, buy buttons, description, share, custom text) → `product-recommendations` (4 auto-fetched)
- **`collection.json`** — `main-collection-banner` → `main-collection-product-grid` (faceted filtering, 24/page, 4×3 desktop / 3×2 tablet / 2×1 mobile) → `content-toggles`
- **`cart.json`** — only `main-cart` with a `cart-items` block (no upsell/recommendations)
- **`page.json`** — `main-page` → `content-toggles` (FAQ accordion)
- **`header-group.json`** — `announcement-bar` (free shipping, pink #f597b1) + `header` (nav, search, account, cart) + helper sections
- **`footer-group.json`** — `footer` with 3 menu blocks (Informationen, Weitere Fragen?, Services) + social + newsletter

### Section-to-snippet dependency graph

Most-included snippets across the codebase:

1. `theme-symbols` — 53× (SVG icon sprite: search, account, cart, chevron, burger, close)
2. `lazy-image` — 31× (responsive image loader)
3. `section-heading` — 18× (standardized h2/h3 + subheading)
4. `product-icon-label` — 18× (sale/sold-out/custom badges)
5. `product-price` — 14× (price w/ sale strike-through, currency)
6. `lazy-svg` — 12×
7. `form-errors` — 10×
8. `lazy-image-small`, `custom-shadow`, `custom-colors` — 7–9× each

`main-product.liquid` is the central consumer: pulls in `product-media`, `product-variants`, `product-price`, `form-errors`, `section-heading`, `custom-shadow`, `lazy-image`, `lazy-svg`.

### JS architecture

- **No framework** — vanilla Web Components (`class ProductVariants extends HTMLElement`), event-driven via `dispatchEvent`/`addEventListener`, JS hooks via `data-js-*` attributes
- **Component-based naming**:
  - `component-*.js` (16 files): modal, product-form, slider, facets, cart, cart-recommendations, range-slider, pagination, quantity-selector, pickup-availability, shipping-calculator, before-after, interactive-map, store-selector, product-model, toggle
  - `section-*.js` (4 files): header, main-product, footer, announcement-bar
  - `vendor-*.js`: macy.js (masonry layout)
  - `instantpage.js` (link prefetch)
- **jQuery 3.6.0** bundled (90 KB) but the modern component code does not use it. Likely a legacy or third-party app dependency — candidate for removal after audit.
- **No SCSS / no PostCSS** — CSS is hand-written; assets/ contains the shipped artifacts, not sources.
- **Inline `<style>` blocks**: ~139 instances across sections inject dynamic CSS (aspect-ratio padding, shadow offsets, color variables). Render-blocking; consolidation target.

### Theme settings & customizer surface

`config/settings_schema.json` exposes ~120–150 distinct settings:

- **Typography** (~6): heading/body font, sizes, line-heights, menu size, button weight (`font_picker` types, currently DM Sans + Inter)
- **Colors** (~31): per-zone (header, main, cards, buttons, footer) — bg, text, accent, borders, shadows
- **Layout** (~2): vertical spacing 50–150px, grid gap 12–36px
- **Borders** (~6), **shadows** (~11), **product card** (~20), **footer/cart** (~10)

`config/settings_data.json` is the merchant's saved values — treat as data, don't edit by hand. Current state: pink `#f597b1` accent, DM Sans typography, white cards, 10px radius, 26px gap.

### Apps & integrations

- **Avada SEO** — 6 snippets (`avada-seo*.liquid`, `avada-defer-css.liquid`), invoked from `theme.liquid`. Note: uses deprecated `include` instead of `render`.
- **Logolicious** — Shopify app block on homepage (logo carousel; `shopify://apps/logolicious/blocks/app-block/...`)
- **CrazyLoad / SpeedUP.GURU** — not a Shopify app, custom perf layer (see above). Engine 1.00, config timestamp 2025031614, debug mode currently ON.
- **No** Judge.me / Yotpo / Loox / Klaviyo / Gorgias / Recharge detected. Newsletter is a custom form (no backend integration visible).

### Localization

- 33 locale files with full translations (not stub).
- `en.default.json` is the technical default; **German is the production display language** — all visible microcopy on the live site is German ("JETZT SHOPPEN", "Neuheiten", "Versandzeit: 3-6 Werktage").
- Each locale has a paired `*.schema.json` (theme editor strings) alongside the runtime `*.json`.
- RTL: `theme.liquid` sets `dir="rtl"` for `ar,he,ur,fa,pa,sd,ku`. Style changes that depend on left/right need to consider both directions.

## Customization level

**~80% stock KrownThemes "Local", ~20% merchant configuration.**

What the merchant has done:
- Brand colors, typography, and customizer settings tuned
- Hand-curated homepage (specific products, German copy, custom collections)
- Logolicious + Avada SEO installed
- Newsletter form

What the merchant has **NOT** done:
- No custom sections (everything in `sections/` is stock theme)
- No custom JS files
- No custom CSS files
- No `shopify_attributes` / Shopify Plus customizations

This is good news for modernization: there's almost no bespoke code to preserve — improvements made to the theme's own structure benefit the brand directly.

## Known technical debt (in priority order)

1. **Monolithic product sections** (~206 KB across `main-product`, `featured-product`, `product-quick-view`) — heavy duplication of variant/media/pricing logic. Extract `_product-media.liquid`, `_product-form.liquid`, `_product-pricing.liquid` partials.
2. **~139 inline `{% style %}` blocks** — render-blocking, scattered. Consolidate into `<head>` CSS custom properties.
3. **~15 orphan sections** defined but never referenced in any template (announcement-bar variants, blog-posts, contact-form, custom-liquid, exit-intent-popup, several customers-*, helper-*, html-email, popup-age-verification, popups, store-selector, etc.). Safe-deletion candidates.
4. **jQuery 90 KB bundle** with no clear consumer in the modern code — verify no app needs it (Avada? Logolicious?), then remove.
5. **Avada SEO uses deprecated `include`** instead of `render` (e.g., `avada-seo.liquid:2`).
6. **CrazyLoad opacity** — perf wrapper transforms output at render time, debugging perf is hard. Hardcoded exception lists are not transparent.
7. **Image handling inconsistency** — some files use modern `image_url` filter, others use bare `<img>` tags. No systematic `image_tag` adoption.

## Online Store 2.0 compliance

- ✅ JSON templates
- ✅ Section groups (`header-group.json`, `footer-group.json`)
- ✅ App blocks (Logolicious)
- ⚠️ Section schemas are minimal (presets defined, full UI schemas are sparse)
- ⚠️ Limited app-block support inside content sections (only via the dedicated `apps.liquid`)

## Conventions worth knowing

- KrownThemes uses `t:sections.split-extra-words.<key>` translation namespacing — follow the same pattern when adding settings.
- Snippets prefixed with `__` (double underscore) are vendor / perf-layer internals — treat as third-party, don't modify unless intentionally working on the speed layer.
- `helper-*` sections are reusable building blocks invoked by other sections, not standalone page sections — don't add them to templates directly.
- Web Component pattern: new interactive UI should extend `HTMLElement`, register via `customElements.define`, hook via `data-js-*` attributes — match existing component code rather than introducing a framework.

## Modernization approach (recommended)

**Incremental in-place upgrade**, not a full Dawn/Hydrogen rewrite. The theme is already 2.0-compliant, JS already uses Web Components, and the merchant has so little custom code that a rebuild would mostly redo what KrownThemes provides.

- **Phase 1 — Cleanup:** delete orphan sections, remove jQuery if unused, consolidate inline styles, fix Avada `include`→`render`.
- **Phase 2 — Product section refactor:** extract shared partials across the three large product sections.
- **Phase 3 — Decide on CrazyLoad:** measure Core Web Vitals with it, prototype native lazy-loading + Shopify image_tag, drop wrapper if native is within ~5%.
- **Phase 4 — Image & form modernization:** replace `lazy-image` snippet with native `<img loading="lazy">` + `image_url` + `sizes`; move newsletter to Shopify Email or Klaviyo for real list management.

**Hardest pieces to replace** if a full migration is later attempted: the header (sticky + mega menu + mobile sidebar, ~17 KB JS + ~27 KB CSS), the product form (custom variant logic), and the CrazyLoad layer itself.
