# kurtz Editorial Reference v2

Canonical website direction · 28 October 2026. This is the production contract
for all six public pages and future additions. Read it before changing a visual.
Implementation: `docs/reference.css`; compact canonical captures: `screens/`.

## Source and authority

Derived from the owner's approved homepage, the owner's 28 October 2026
reference image, and the original KURTZ Reference Design System
`1.0.0-reference` (package SHA-256
`18df421e38083c40e7b3ca8e77322d795f33dbad6363f93aea706400a7df3193`).
The owner's image guides composition, scale and print rhythm; its photographs
are not licensed website assets. This v2 resolves earlier ambiguities: mono
body text replaces the earlier sans body face; the rail follows the document rather than the
viewport; mobile hides the rail; no ink-bleed blur; no mascot; texture is original
SVG code only. The homepage is approved. Door pages must have the same visual
intensity, while legal pages retain a quiet reading rhythm.

## Principles

Editorial / zine, not SaaS. Make a printed issue with three doors: a dominant
headline, unequal color fields, strong rules, structural numbers and evidence.
Deliberately break the usual AI look. Whitespace alone is not an identity.
Use the mosaic to explain relationships, not a succession of floating features.
The page should remain recognisable in silhouette before its text is read.

Keep evidence readable: full product actions/results, real aspect ratios, captions,
mobile alternatives and accessible controls. Do not recolor or crop product UI to
make it fit a decorative field. Never imply availability with a slogan or diagram.

## Tokens

Use these exact hex values (case insensitive), preferably through variables.
No extra colors, approximate grays or alpha color variants. `transparent` and
`currentColor` are the only extra color keywords; inherited colors are fine.
Opacity may soften decorative SVG layers, never essential text.

| Name / variable suffix | Value | Use / foreground |
| --- | --- | --- |
| Paper / paper | `#f3ebdd` | Page, cards / Ink |
| Ink / ink | `#171b1a` | Rules, dark fields / Cream |
| Cream / cream | `#fff8ed` | Reverse text, clean image backing / Ink |
| Rust / rust | `#c8442b` | Stickers, editorial emphasis / Cream |
| Tangerine / tangerine | `#eea23a` | Gassi, diagonal band / Ink |
| Sage / sage | `#aab7a2` | Player / Ink |
| Teal / teal | `#2b5756` | Ownership, texture / Cream |
| Blue / blue | `#204a59` | Manual, foundation / Cream |
| Focus / focus | `#0065ff` | Focus on light Paper or Ink fields |

CSS names are `--k-color-paper`, etc. Pairings: Ink/Paper 14.68:1,
Cream/Ink 16.47:1, Ink/Sage 8.28:1, Ink/Tangerine 8.17:1,
Cream/Rust 4.61:1, Cream/Teal 7.65:1, Cream/Blue 9.11:1.
Never Cream on Sage/Tangerine, or small Ink on Rust. Focus is 3px solid,
4px offset; use Ink on Sage/Tangerine and Cream on Rust/Teal/Blue/Ink.
Inset focus inside an index cell prevents clipping. Status also has visible words.

Spacing scale (`--k-space-N`, base 16px): 1=4, 2=8, 3=12, 4=16, 6=24,
8=32, 12=48, 16=64, 24=96, 32=128px. Gutter:
`clamp(1rem,3vw,3rem)`. Small labels may use 6px inset; print offsets may
use 7px. Rules: 1px annotations, 2px components/index, 3px mosaic/rail,
4px chapter boundaries. All rules use Ink unless a reverse surface needs
`currentColor`. Radius always 0. Shadows only hard, zero-blur offset blocks.

## Typography

Locally hosted Barlow Condensed **800**, display in ALL CAPS. IBM Plex Mono
**400** for body, controls and labels. No runtime font service. Use only generic
`sans-serif` / `monospace` fallbacks; no third family, including in retired CSS.
Existing binaries and OFL provenance live in `docs/assets/fonts/`.

| Role | Size | Line height | Tracking |
| --- | --- | --- | --- |
| Door title | `clamp(4.5rem,8vw,10rem)` | .85 | -.035em |
| Home manifesto | `clamp(4rem,5.8vw,7rem)` | .88 | -.035em |
| Chapter h2 | `clamp(3rem,6vw,6.5rem)` | .95 | -.025em |
| Subheading h3 | `clamp(2rem,3vw,3rem)` | 1.02 | -.025em |
| Structural numeral | `clamp(6rem,13vw,14rem)` | .8 | -.05em |
| Sticker | 24–40px | 1.05–1.1 | 0 |
| Body | 16px | 1.65 | 0 |
| Lead | 20–28px | 1.35–1.45 | 0 |
| CTA | 14px | 1.5 | 0; uppercase |
| Kicker / issue / caption | 12px minimum | 1.5–1.7 | .06em / .12–.22em / 0 |

Do not squeeze long words to preserve a desktop composition. At 768px and
below stack title, explanation, then evidence; at 320px allow natural wraps.
Body lines usually 35–65ch. Never rotate paragraphs. Short stickers: -4° to
-8°; paper cards: -1° to -1.5°. Keep at least 8px clear of unrelated content.

## Grid and shared furniture

Home: 68/32 masthead split; complete original wordmark and issue line on the
left, Rust NO DEFAULTS field with a flat diagonal Tangerine band on the right.
Five mosaic tracks: **36 / 29 / 6 / 11 / 18%**. Manifest occupies left two rows;
Player spans tracks 2–3; platform spans 4–5; Gassi, texture and manual form the
second row. Borders are real shared rules, no gutters pretending to be cards.
At 1100px switch to an unequal two-column reading sequence; at 600px stack.

Edition rail: 3.5rem wide, Ink with Tangerine 3px rule, absolute to the document,
full document height, vertical mono edition / chapter / ownership labels. Hide
at <=768px; complete navigation remains. Do not pin it over scrolling content.

Every door and legal page has the same issue line, a complete home-linked
wordmark, navigation and product index. Door layouts use 3:2 or 5:4 unequal
splits with heavy rules and full-bleed chapter fields. Numerals are structural,
not invented run IDs. A texture/sticker area must carry orientation or status.
The four-cell index links Player, Preview, Gassi and public documentation.
Footer: Ink manual panel, source/privacy/credits links, real attribution.
The unchanged light wordmark may use `filter:brightness(0)` in the Paper home
masthead for a monochrome print. This is the only page-content filter; it
does not change the vector geometry.
No generic centered hero or floating global toolbar.

## Components

Snippets show minimal structure; use the production CSS classes and tokens.
Do not paste new inline styles. Components must reflow in source order.

### Door tile with big numeral

Use once to identify a destination or chapter; include honest status and one action.

```html
<article class="destination cinema">
  <div class="door-heading"><span class="door-number" aria-hidden="true">01</span>
    <h2>Video player</h2></div>
  <p class="door-description">Mac beta available.</p>
  <a class="door-label" href="player/">PRESS PLAY <span aria-hidden="true">↗</span></a>
</article>
```
```css
.destination { padding:1.5rem; border-right:3px solid var(--k-color-ink); }
.door-number { font:800 6rem/.85 var(--k-font-display); letter-spacing:-.05em; }
```

### Sticker

Use for a brief truthful status or ownership statement, once per spread.
Rust/Cream, slightly rotated, hard offset Ink shadow block. Never obscure UI.

```html
<p class="sticker">MAC / PUBLIC BETA</p>
```
```css
.sticker { background:var(--k-color-rust); color:var(--k-color-cream);
  padding:.75rem; transform:rotate(-6deg); border:2px solid var(--k-color-ink);
  box-shadow:6px 6px 0 var(--k-color-ink); font:800 2rem/1.1 var(--k-font-display); }
```

### Paper card

Use for a short qualifier, exact status or useful reading instruction, not every paragraph.

```html
<div class="paper-card"><p>No public release date announced.</p></div>
```
```css
.paper-card { background:var(--k-color-paper); color:var(--k-color-ink);
  padding:.75rem 1rem; border-right:7px solid var(--k-color-rust);
  border-bottom:6px solid var(--k-color-rust); transform:rotate(-1.5deg); }
```

### Diagonal band

One flat stripe crossing a graphic field, never a shaded gradient. The only
“gradient exception” is this visual band; implement it as a rotated solid plane.
No CSS gradient function is allowed, including here.

```html
<div class="no-defaults"><p>NO DEFAULTS.</p></div>
```
```css
.no-defaults { position:relative; isolation:isolate; overflow:hidden; }
.no-defaults::after { content:''; position:absolute; z-index:-1;
  left:-5%; width:110%; bottom:0; height:3.5rem;
  background:var(--k-color-tangerine); transform:rotate(-10deg); }
```

### CTA with arrow and underline

Use a native link for navigation and a button for state. Minimum 44px target,
48px preferred. Arrow is decorative; link text names the action.

```html
<a class="door-label" href="#platforms">PLATFORM STATUS <span aria-hidden="true">↓</span></a>
```
```css
.door-label { display:inline-flex; gap:1rem; min-height:44px; padding-block:.5rem;
  border-bottom:2px solid currentColor; text-decoration:none; text-transform:uppercase; }
.door-label:hover { text-decoration:underline; }
```

### Kicker

Use for chapter context and explicit status, never as the only heading.

```html
<p class="eyebrow">02 / PRIVATE DEVELOPMENT PREVIEW</p>
```
```css
.eyebrow { font:400 .75rem/1.7 var(--k-font-mono);
  letter-spacing:.06em; text-transform:uppercase; }
```

### Product figure

Use actual existing assets, full frame and useful alt text. Captions must distinguish
real, staged, translated, scripted and illustrative content. Preserve mobile sources.

```html
<figure class="stage"><a class="capture-link" href="assets/desktop-clean-1152.webp">
  <img src="assets/desktop-clean-1152.webp" width="1152" height="720"
    alt="Real kurtz capture on a staged Mac desktop, controls hidden."></a>
  <figcaption>Real kurtz capture · Staged desktop</figcaption></figure>
```
```css
.capture-link { display:block; border:2px solid var(--k-color-ink); }
.stage img { width:100%; height:auto; object-fit:contain; }
figcaption { font:400 .75rem/1.7 var(--k-font-mono); border-top:1px solid currentColor; }
```

### Texture panel

Use original SVG linework as a graphic counterweight, with a solid opaque sticker
or card for readable text. Decorative pseudo-elements have no accessible content.

```html
<aside class="texture-panel"><p class="sticker">IN DEVELOPMENT</p></aside>
```
```css
.texture-panel { padding:2rem; background:var(--k-color-teal)
  url(assets/textures/independent-lines.svg) center/15rem auto; }
```

## Textures and rights

Only `press-grain.svg` and `independent-lines.svg` are current texture assets.
Grain is procedural noise; the lines are original hatch, nested rules and
abstract circuits. Use a grain layer gently on broad fields; linework is bolder
in a separate panel, or low-opacity behind nonessential decoration. Never make
text contrast depend on a pattern. No blur on page content, no photo textures
without documented rights. Do not extract, trace or recreate mural imagery
from the owner's reference. Do not modify the wordmark paths.

To add a pattern: write original SVG paths from rules / grids / geometry; use
this palette; avoid embedded images, scripts and external URLs; give it a clear
viewBox and tiling seam; document authorship, method and MPL-2.0 terms in
`docs/assets/textures/README.txt` and Credits. Inspect at 320 and 1920px and
AA-check its text backgrounds. Add a canonical capture. No new photo required.

## Copy voice and product truth

Short. Declarative. Precise. ALL CAPS for slogans, sentence case for prose.
Use understatement, not AI superlatives, emoji or faux intimacy. No invented
benchmarks, performance claims, release dates or free-trial language.

Current website source of truth: Player Mac 0.9.7 beta, build 9, free; macOS
15.6+, Universal DMG. Mobile/TV are in development/release preparation with
explicit qualification limits. Preview is private development, date and pricing
unannounced. Gassi is coming soon: no public benchmark or submission service.
These are snapshot facts, not permission to upgrade claims without evidence.
Preserve linked release/status evidence and all preview provenance disclaimers.

## Page templates

**Home:** issue masthead → manifesto/three-door mosaic → product index →
SELF-HOSTED closing line → attribution/legal footer. Do not homogenize the tiles.

**Door (Player / Preview / Gassi):** issue line → home mark + local navigation →
large numeral + title field / contrasting status field → evidence mosaic with
heavy rules → status/action chapter → product index → shared manual footer.
Player uses Sage, Ink capture field, Paper/Teal entry spread, Blue foundation,
Tangerine downloads. Preview uses Paper/Teal title, Ink evidence, Sage question,
Cream mail, Tangerine expandable tour and Teal ownership. Gassi uses
Tangerine title, Blue explanation and an original line panel with a truthful
COMING SOON sticker. Its sparse content must not be padded with fake metrics.

**Legal:** issue line → home mark + useful link → Paper manual with large title,
quiet two-column heading/body rules → product index → shared footer. On mobile
stack heading before paragraph. Preserve dates, sources and licenses. No stickers
inside legal prose, no theatrical texture under long text.

## Do / Don't

| Do | Don't |
| --- | --- |
| Unequal contiguous fields with black rules | Uniform rounded cards or icon-card grids |
| Large condensed uppercase and mono prose | Centered generic hero, display font used as body |
| Hard offset sticker block / flat band | Soft shadows, glow, glassmorphism, blur |
| Flat spot colors, original SVG texture | Gradients, stock-like illustrations, photo textures without rights |
| Rectangular controls and underlined arrows | Rounded pills, emoji, floating glass navigation |
| Full captures with original captions | Cropped results, tinted UI, imaginary product evidence |
| Honest status next to the action | Coming-soon download buttons, invented trial or benchmark |

## Required verification

Every visual change must pass `python3 design-system/style-lint.py` and
`python3 -m unittest discover -s design-system -p 'test_*.py'`.
The linter scans **all** CSS, including compatibility files, plus style blocks
and attributes in all public HTML. There are no radius, blur, font or color
allow-list exceptions. `transparent` / `currentColor`, generic fallback families
and exact token literals are documented syntax, not bypasses.

Inspect all six pages at 320, 390, 768, 1440 and 1920px; open disclosures,
exercise comparison, legacy anchors and keyboard focus; test reduced motion,
200% text and zoom reflow; check AA contrast, resources, JS and preservation.
Capture Home and each door at 390/1440px in compact WebP, after fonts/images
load. Keep local QA evidence outside the served tree. State browser and zoom
method honestly; a reflow emulation is not a native browser-menu zoom test.
