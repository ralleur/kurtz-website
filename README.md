# kurtz website

Public static website for [kurtz.app](https://kurtz.app/).

- `/`: the editorial product index
- `/player/`: the existing free video player
- `/preview/`: the kurtz product tour
- `/gassi/`: Coming soon

GitHub Pages serves `docs/` from `main`. This repository contains only the
reviewed website snapshot. The application and its development history are
not included. Player downloads and application source remain linked to their
existing public release locations.

Website code retains MPL-2.0 terms. Fonts, artwork and film-derived images
retain their own licenses and credits: see [Credits](docs/credits.html),
[Sora OFL](docs/assets/fonts/Sora-OFL.txt). Adapted Caminandes
compositions remain CC BY-SA 3.0. Brand and third-party marks retain their
respective owners. AI-assisted design and implementation; no exclusive rights
in generated material are asserted.

The product story uses English presentation captures of the development web
interface, with translated labels, the official wordmark, fictional documents
and email, and a scripted assistant answer. These are adapted presentation
views, not unmodified production captures or proof of shipped localization.
See the visible preview notes and credits. No real personal data or fixture
source is included.

Canonical visual rules and screenshots: [design-system/](design-system/REFERENCE.md).

## Reference design system

The presentation layer in `docs/reference.css` adapts the owner’s own KURTZ
Reference Design System, version `1.0.0-reference`, dated 28 October 2026.
Source package: `kurtz-reference-design-system.zip`; SHA-256
`18df421e38083c40e7b3ca8e77322d795f33dbad6363f93aea706400a7df3193`.
The owner supplied and authorized this design for the website. The integration
is AI-assisted and retains the website code’s MPL-2.0 terms (see LICENSE.md).
No exclusive rights in AI-generated material are asserted.

The current presentation also follows the owner’s 28 October image reference:
a large original wordmark, issue line, black edition rail, numbered color-block
mosaic, underlined actions and print-like typography. All six pages load only
`reference.css?v=20261028-editorial-v2`. The previous `style.css`, `portal.css`,
`family.css` and `kurtz.css` remain as compatibility imports at their original
URLs but are not loaded by the pages.

Typography is self-hosted: Barlow Condensed 800 for display and IBM Plex Mono 400
for body and labels. All font families have SIL Open Font License 1.1 files:
[Barlow Condensed OFL](docs/assets/fonts/BarlowCondensed-OFL.txt),
[IBM Plex Mono OFL](docs/assets/fonts/IBMPlexMono-OFL.txt), and the retained
Sora license above.
[Font provenance and SHA-256 hashes](docs/assets/fonts/reference-fonts.json)
record the distribution used. No runtime font service or CDN is used.

The original SVG grain, hatching and rule-derived line patterns in
`docs/assets/textures/` are AI-assisted original code under this repository’s
MPL-2.0 license. They contain no photographs or traced reference-image artwork.
The owner’s photographic collage reference is not distributed here. All existing
wordmark files, product captures, mockups and mobile variants remain byte-identical.
The index reuses the existing real library capture on its staged desktop; its
visible caption and film/production credits identify the source. Product mockups
retain their existing provenance and status disclaimers.

The owner’s 28 October decision removes the former mascot scenes, their assets,
scene-only CSS, playback code and asset-specific attribution from the website.
The legacy player deep-link redirects remain in `family.js`. Other product texts,
links, status statements, captures, media licenses and functionality are preserved.

## Search discoverability

The index, Mac player and development preview use descriptive titles and
metadata while retaining the editorial headlines. Only the available Mac
player is marked as `SoftwareApplication`; the preview remains clearly in
development. `robots.txt` points to the public `sitemap.xml`. Existing captures,
release links and license notices remain unchanged.

The historical `ralleur/kurtz` Pages site has a separate website-only migration
change forwarding the old homepage to `/player/`, preserving deep links, and
forwarding credits/privacy to their new addresses. Publish this website before
the migration. The old application repository is not the source of this site.

Submit `https://kurtz.app/sitemap.xml` in the owner's existing Google Search
Console and Bing Webmaster Tools properties after publication. Those accounts
are needed to verify actual indexing and topic-query impressions.
