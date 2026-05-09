# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Custom Shopify theme for **L'Amour** (`xn--lmour-xqa.de`, store: `0b8499-39.myshopify.com`). Built on the Shopify Skeleton starter (OS 2.0). German is the primary storefront language.

Full rebuild specification (design tokens, section architecture, Liquid patterns, deployment flow) is in [REBUILD_SPEC.md](REBUILD_SPEC.md) — consult it before making design or architecture decisions.

## CLI Commands

```bash
# Local dev server with hot reload (proxies to the live store)
shopify theme dev --store=0b8499-39.myshopify.com

# Push as new unpublished draft (safe — doesn't go live)
shopify theme push --unpublished --store=0b8499-39.myshopify.com

# Push to a specific existing theme ID
shopify theme push --theme=<theme-id> --store=0b8499-39.myshopify.com

# Pull a theme from the store
shopify theme pull --theme=<theme-id> --store=0b8499-39.myshopify.com

# Lint Liquid files
shopify theme check
```

There is no build step — files are edited directly and synced by the Shopify CLI.

## Architecture

### Theme file roles

| Directory | Purpose |
|-----------|---------|
| `layout/` | Root wrappers. `theme.liquid` is the only layout; it loads fonts, CSS, JS, and wraps all pages. |
| `sections/` | Full-width, merchant-customizable page components with embedded `{% schema %}`. |
| `snippets/` | Reusable fragments rendered via `{%- render 'name' -%}`. Never use `{% include %}`. |
| `blocks/` | OS 2.0 theme blocks consumed by sections via `{% content_for 'blocks' %}`. |
| `templates/` | JSON templates that compose sections into page types. |
| `assets/` | `theme.css` (global tokens + component styles), `theme.js` (Web Components only), `critical.css` (above-fold essentials). |
| `config/` | `settings_schema.json` defines the Shopify Customizer UI; `settings_data.json` stores saved values. |
| `locales/` | `en.default.json` (English), `de.json` (German). All user-facing strings must use the `| t` filter. |

### JavaScript pattern

All JS is vanilla Web Components — no jQuery, no frameworks. Each component is a class extending `HTMLElement`, registered with `customElements.define('lamour-*', ...)`. The file is loaded with `defer` in `theme.liquid`. Current components: `LamourThemeToggle`, `LamourCursor`, `LamourReveal`.

### CSS / design token system

All colours are CSS custom properties defined in `assets/theme.css`. The theme switches between light and dark via `data-theme` on `<html>`. **Never hardcode hex values in sections** — always use tokens (`var(--color-bg)`, `var(--color-text)`, etc.). Section-scoped styles go inside `{% stylesheet %}` blocks, not inline `<style>` tags.

Key shared tokens: `--color-pink: #f597b1`, `--font-display: 'Fraunces'`, `--font-body: 'Inter'`, `--container: 1400px`, `--space-section`.

### Light/dark mode

The theme init script runs synchronously in `<head>` before `content_for_header` to prevent flash. It reads `localStorage['lm-theme']` → falls back to `settings.default_color_scheme` → falls back to `prefers-color-scheme`. The `<lamour-theme-toggle>` Web Component handles the toggle button and state updates.

### Images

Never use a bare `<img>` tag. Always render via `{%- render 'image', image: ..., sizes: '...', ratio: '...' -%}`. The snippet provides lazy loading, explicit dimensions, and a full `srcset`.

### Localization

Primary storefront locale is German (`de`). Add all new strings to both `locales/en.default.json` and `locales/de.json`. Reference them with `{{ 'key.path' | t }}`.

## Key Store Dependencies

The theme references these Shopify Admin resources by exact handle — they must exist before sections will render correctly:

- **Collections**: `neuheiten`, `unsere-empfehlung`, `all`, `chanel`
- **Navigation menus**: `main-menu`, `marken`, `footer`, `weitere-informationen`, `ber-lamour`, `backlinks`, `top-produkte`
- **Shop images** (via `shopify://shop_images/`): `logo.png`, `hero_H1_primary.png`, `hero_H2_atmosphere.png`, `hero_H3_lifestyle.png`, `brand-statement_BS1_rose.png`

## Deployment

`git push origin main` → Shopify auto-syncs to the connected draft theme → preview in Admin → click "Publish" to go live. The GitHub↔Shopify integration must be configured in Admin → Online Store → Themes → Add theme → Connect from GitHub.

## What NOT to touch in the theme

Shopify owns these entirely — do not replicate or intercept them:
- `/checkout` flow and all payment processing
- `/account`, `/login`, `/register` (unless using New Customer Accounts)
- SEO meta injection (handled by Avada SEO app via `{%- render 'avada-seo' -%}`)
- Script deferral (handled by CLS Speed App injected via `content_for_header`)
