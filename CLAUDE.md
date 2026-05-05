# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Type

This is a **Shopify theme**, not an application. It is the **"Local" theme by KrownThemes (v3.2.1)**, configured for **Lamour**, a German fragrance/beauty brand on the domain `xn--lmour-xqa.de`. There is no `package.json`, no build step, and no test suite — files are deployed as-is to Shopify, which compiles Liquid server-side.

The repo is connected to a Shopify store (`0b8499-39.myshopify.com`) via GitHub integration. `main` was the live theme; `development` mirrored it; `draft-theme` is the v3.2.1 upgrade pulled from the Shopify draft "Updated copy of Lamour Dev" (theme ID `198725534039`).

> **History:** v2.4.0.1 lived on `development` and `main`. The v3.2.1 snapshot landed on `draft-theme` in commit `f7bb86d`. Diff was 221 files, +34,214 / −11,296 lines. The Shopify→GitHub sync is currently disabled while the upgrade is being merged.

## Development Workflow

Standard Shopify CLI 3.92.1 (run from the user's shell, browser auth):

- `shopify theme dev` — local preview against the linked store with hot reload
- `shopify theme list --store=0b8499-39.myshopify.com` — list themes & IDs on the store
- `shopify theme pull --store=0b8499-39.myshopify.com --theme=<id> --path=.` — overwrite working tree from a remote theme
- `shopify theme push --unpublished` — push working copy as a hidden theme for QA
- `shopify theme check` — Liquid linter (Theme Check)

There are no unit tests. "Testing" is visual/manual in the Shopify preview. Type checks and bundlers do not apply.

## Scale & Inventory (v3.2.1)

- **70 sections** (+8 vs v2.4) in `sections/`
- **65 snippets** (+10 vs v2.4) in `snippets/`
- **16 theme blocks** in `blocks/` (new directory in v3.2.1)
- **23 JSON templates** in `templates/` (+ 2 legacy `.liquid` templates), including new `page.faq.json` and `page.stores.json`
- **30 component-*.js files** in `assets/` (+10 new components)
- **54 locale files** (27 language pairs, runtime + schema)

**Largest files (concentrated complexity):**
- `sections/main-product.liquid` — **168 KB / 4,280 lines** (was 81 KB in v2.4 — **doubled**)
- `sections/product-quick-view.liquid` — **138 KB / 3,572 lines** (was 60 KB — doubled)
- `sections/featured-product.liquid` — **135 KB / 3,558 lines** (was 65 KB — doubled)
- `assets/__clspeedapp-jquery.js` — 88 KB (full jQuery 3.6.0 bundle, still present)
- `assets/theme.css` — 72 KB
- `assets/component-product-form.js` — 41 KB

The three product sections together are now ~440 KB. Variant logic was extracted into snippets (good), but the section files were not consolidated — extraction was additive, not subtractive.

## Architecture

### CrazyLoad / clspeedapp performance layer (still load-bearing)

Unchanged from v2.4. `layout/theme.liquid` still wraps the entire output through 11 `__clspeedapp-*` snippets that defer scripts (`<script src>` → `data-src`), inline critical CSS, preload LCP images, and lazy-load iframes. Hardcoded exception list in `__clspeedapp-js-init.liquid` for Shopify analytics / Trekkie / `window.theme`.

**Implication for edits:** raw `<script>`, `<link>`, or `<img>` tags dropped into Liquid bypass this perf layer and may behave differently in production than in preview. Route new assets through the existing `__clspeedapp-*` mechanisms or the helper snippets (`lazy-image`, `lazy-svg`, `video-component`).

### Theme blocks system (NEW in v3.2.1, partially adopted)

`blocks/` directory contains 16 reusable, composable block files using Shopify's modern theme-block primitive:

- **Layout primitives:** `_card.liquid`, `_grid-media.liquid`, `_grid-text.liquid`, `_slide-image.liquid`, `_slide-video.liquid`, `content-group.liquid`, `divider.liquid`, `empty-space.liquid`
- **Content blocks:** `button.liquid`, `caption.liquid`, `heading.liquid`, `image.liquid`, `rich-text.liquid`, `custom-liquid.liquid`
- **Commerce blocks:** `product-add-to-cart-button.liquid`, `star-rating.liquid`

**Adoption depth — partial:**
- Only 4 blocks support nesting via `{% content_for 'blocks' %}`: `_card`, `_grid-text`, `_slide-image`, `content-group`
- Only 3 sections actually consume the new blocks system: `flex-cards` (uses `_card`), `flex-grid` (uses `_grid-text`/`_grid-media`), `flex-slideshow` (uses `_slide-image`/`_slide-video`)
- Most other sections still define inline blocks the v2-era way

**Implication for new work:** Build new sections as `flex-*`-style consumers of the `blocks/` library; don't add inline-block patterns. Old sections can stay until they're touched.

### Page composition

Pages are JSON Online Store 2.0 templates that compose sections. The homepage composition was **preserved** through the upgrade — Lamour's German branding and curated products are intact.

- **`index.json`** — slideshow → Logolicious app block → 2× `featured-collection` (Neuheiten, Unsere Empfehlung) → `promotion-cards` (Dior, Chanel, Hugo Boss) → `media-with-text-overlay` → `content-toggles` → `newsletter`. **No new flex-* sections used here yet.**
- **`product.json`** — `main-product` with blocks (rating, vendor, title, price, variant_picker, buy_buttons, description, share) → `product-recommendations`
- **`collection.json`** — `main-collection-banner` → `main-collection-product-grid` → `content-toggles`
- **`cart.json`** — `main-cart` only (no upsell)
- **`page.faq.json`** (NEW) — `main-page` + `content-toggles` (placeholder shipping/returns FAQ)
- **`page.stores.json`** (NEW) — `main-page` + `stores-map` + `contact-form`
- **`header-group.json`** — `announcement-bar` (free shipping, pink #f597b1) + `header` + helpers
- **`footer-group.json`** — `footer` (3 menu blocks: Informationen, Weitere Fragen?, Services) + social + newsletter

### Variant / product extraction (v3.2.1 work, incomplete)

New snippets extract variant logic for reuse:
- `product-variant-picker.liquid` — renders the `<product-variants>` web component, delegates to `product-variant-options` per option
- `product-variant-options.liquid` — `<select>` or radio swatch rendering, image_url for color swatches
- `product-block.liquid` — reusable product card primitive

But: `main-product.liquid` did **not** shrink — it doubled. The snippets exist as additions; the main sections were not torn down to use them as the single source of truth. Real consolidation is still pending work.

### Section-to-snippet dependency graph

Most-included snippets remain similar:
1. `theme-symbols` — central SVG icon sprite (replaces v2's `theme-icons`, which was renamed → `progress-dots-icons.liquid`)
2. `lazy-image` — primary image renderer (used everywhere including blocks)
3. `section-heading`, `product-icon-label`, `product-price`
4. NEW: `product-variant-picker` / `product-variant-options` / `product-block` consumed by product sections
5. NEW: `pickup-availability-data` + `pickup-availability-widget` (replaces deleted `helper-pickup-availability-extended`)
6. NEW: `lang-dir` (proper RTL/LTR helper extracted into a snippet)
7. NEW: `video-component`, `collection-panel`, `cart-gift-wrapping`, `cart-item-discount`, `product-line-property`

### JS architecture

- **No framework** — vanilla Web Components (`class extends HTMLElement`), event-driven via `dispatchEvent`/`addEventListener`, JS hooks via `data-js-*` attributes
- **30 component-*.js + section-*.js files**
- **New v3.2.1 components** (all small, vanilla, no jQuery):
  - `component-collection-tabs.js` (~2.3 KB) — tab-switcher for filtered collections
  - `component-countdown-clock.js` (~2.5 KB) — countdown timer for new `countdown` section
  - `component-recently-viewed.js` — localStorage product history
  - `component-share-link.js` — social share / copy-link
  - `component-terms-checkbox.js` — terms acceptance toggle
  - `component-video-legacy.js` — fallback for older browsers (paired with `component-video.js`)
- **Legacy components unchanged:** `component-product-form.js` (41 KB) and `component-facets.js` (19 KB) are still likely jQuery-coupled
- **jQuery 3.6.0** bundled (88 KB in `__clspeedapp-jquery.js`) — still present, still load-bearing for the legacy components and probably for Avada SEO

### Image handling

`snippets/lazy-image.liquid` is the centralized renderer. Hybrid pattern:
- Modern: `image_url` filter, native `loading="lazy"`, full responsive `srcset` (15 breakpoints 240w–3820w) + `sizes`
- Legacy: custom `onload` handler that adds a `lazyloaded` class for CSS fade-in animations

Blocks (`blocks/_card.liquid`) use `{%- render 'lazy-image', ... -%}` consistently. The bare `<img>` mix from v2.4 is largely cleaned up.

### Theme settings & customizer surface

`config/settings_schema.json` (1,464 lines) — comprehensive: typography (font pickers for headings/body, size/line-height/letter-spacing ranges), colors per zone (header/main/cards/footer × bg/text/accent/borders/shadows), layout (vertical spacing, grid gap), borders, shadows, product card variants. Lamour's saved values in `settings_data.json` survived the upgrade (pink `#f597b1` accent, DM Sans typography, German copy intact).

### Apps & integrations

- **Avada SEO** — 6 snippets, **still uses deprecated `include`** instead of `render` (e.g., `avada-seo.liquid:2-6`). Not fixed by the v3 upgrade.
- **Logolicious** — Shopify app block on homepage (`shopify://apps/logolicious/blocks/app-block/...`)
- **CrazyLoad / SpeedUP.GURU** — perf wrapper, unchanged from v2.4
- **No** Judge.me / Yotpo / Loox / Klaviyo / Gorgias / Recharge. Newsletter is still a custom form with no backend integration visible.

### Localization

- 27 language pairs (54 files: runtime `*.json` + theme-editor `*.schema.json`)
- `en.default.json` is the technical default; **German is the production display language** ("JETZT SHOPPEN", "Neuheiten", "Versandzeit: 3-6 Werktage")
- RTL: `theme.liquid` sets `dir="rtl"` for `ar,he,ur,fa,pa,sd,ku`. v3 also adds `snippets/lang-dir.liquid` as a reusable RTL/LTR helper.

## Customization level

**~80% stock KrownThemes "Local v3.2.1", ~20% merchant configuration.** No custom sections, no custom JS, no custom CSS files. The merchant's investment is entirely in:
- Customizer settings (colors, typography, layout)
- Hand-curated content (homepage products, German copy)
- Two installed apps (Avada SEO, Logolicious)
- A custom newsletter form

This is good news for modernization: there's almost no bespoke code to preserve.

## Known technical debt (v3.2.1, in priority order)

| Issue | v2.4 | v3.2.1 | Status |
|---|---|---|---|
| `main-product.liquid` size | 81 KB | 168 KB | **WORSENED** (doubled) |
| `featured-product.liquid` size | 65 KB | 135 KB | **WORSENED** (doubled) |
| `product-quick-view.liquid` size | 60 KB | 138 KB | **WORSENED** (doubled) |
| Duplicated variant logic | yes | extracted to snippets | **PARTIAL** (additive, not consolidating) |
| Inline `{% style %}` blocks | ~139 | ~115 | improved (~17%) |
| Orphan sections | ~15 | ~39 | grew (most are new library sections like `flex-*`, `countdown`, `logo-list`) |
| jQuery 88 KB bundle | present | present | **UNCHANGED** |
| CrazyLoad / clspeedapp wrapper | present | present | **UNCHANGED** |
| Avada SEO uses `include` | yes | yes | **UNCHANGED** |
| Mixed image handling | yes | centralized via `lazy-image` | **FIXED** |

**New debt introduced by v3.2.1:**
- The `blocks/` library is half-wired (only 3 sections actually consume it; 12 of 16 blocks don't support nesting)
- Product section files grew despite the snippet extraction — modularization without consolidation

**Top priorities now:**
1. Consolidate `main-product` / `featured-product` / `product-quick-view` to actually use the new `product-variant-picker` / `product-block` snippets as the single source of truth — could reclaim 100+ KB
2. Wire the `blocks/` system into more sections (and onto `index.json`) so the new primitive earns its keep
3. Avada SEO `include` → `render`
4. Remove jQuery if nothing actually depends on it (audit Avada and legacy components first)
5. Decide on CrazyLoad: measure CWV with vs. without before committing

## Online Store 2.0+ compliance (v3.2.1)

- ✅ JSON templates, section groups (`header-group.json`, `footer-group.json`)
- ✅ App blocks consumed (Logolicious; main sections declare `"type": "@app"` in block schemas)
- ✅ Modern image filters (`image_url` + native `loading="lazy"`) used consistently
- ✅ Theme blocks (`blocks/` directory) — but adoption is partial (only 3 sections + 4 nesting-capable blocks)
- ⚠️ No use of `image_tag` filter
- ⚠️ Most sections still define inline-block schemas instead of composing `blocks/`

Estimate: ~70% of the way to fully-modern OS 2.0+.

## Conventions worth knowing

- KrownThemes uses `t:sections.split-extra-words.<key>` translation namespacing — follow the pattern when adding settings.
- Snippets prefixed with `__` (double underscore) are vendor / perf-layer internals — treat as third-party, don't modify unless intentionally working on the speed layer.
- `helper-*` sections are reusable building blocks invoked by other sections, not standalone page sections — don't add them to templates directly.
- New interactive UI: extend `HTMLElement`, register via `customElements.define`, hook via `data-js-*` attributes — match existing component code rather than introducing a framework.
- Build new sections as **consumers of `blocks/`** (the `flex-*` pattern) rather than re-defining inline blocks.

## Modernization approach (revised for v3.2.1)

v3.2.1 already did ~60–70% of the modernization work I would have planned against v2.4:
- Theme blocks library exists
- Variant logic is extracted (just not yet consolidated)
- New components are vanilla / Web Components
- Image handling is centralized
- Modern schemas, app block hooks

The remaining ~30–40% is real work, not cosmetic:

- **Phase 1 — Product section consolidation** (highest leverage). Tear down inline product/variant/pricing logic in `main-product`, `featured-product`, `product-quick-view`; route through `product-variant-picker` + `product-variant-options` + `product-block`. Reclaim ~100 KB.
- **Phase 2 — Wire the blocks system.** Refactor `index.json` and other content sections to consume `blocks/` (compose `_card`, `heading`, `button`, etc. instead of redefining). Adoption is the bottleneck, not capability.
- **Phase 3 — Decide on CrazyLoad + jQuery.** Measure Core Web Vitals with the wrapper, prototype native lazy-loading + Shopify image patterns, drop the wrapper if native is within ~5%. Once gone, jQuery likely follows.
- **Phase 4 — Avada `include` → `render`** (small, mechanical), plus modernize legacy `component-product-form.js` / `component-facets.js` to vanilla JS.

**Hardest pieces to replace** if a full migration is later attempted: the header (sticky + mega menu + mobile sidebar), the product form (custom variant logic), and the CrazyLoad layer itself.
