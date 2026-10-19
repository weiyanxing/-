# Poster Selection Guide

Use this guide to select the composition internally, recommend visual styles to the user, and choose an aspect ratio. Layout is an implementation detail in the default workflow and must not appear as a user-facing choice.

## Resolution Priority

Resolve exactly one internal layout in this order:

1. An explicit `--layout <id>` override.
2. A legacy layout preference from `EXTEND.md`.
3. The automatic selection rules below.
4. `centered-hero` as the fallback when no rule produces a clear result.

An override must exactly match the basename of one definition file in `references/layouts/` (for example, `modular-grid` matches `modular-grid.md`; do not include `.md`). The same validation applies to a legacy EXTEND.md layout preference. An explicit override skips automatic selection and does not change style, aspect ratio, language, renderer, or backend. If a valid override conflicts with the content, warn once and continue with it. If an explicit or legacy value is invalid, stop before rendering and list the valid IDs.

Record the resolved layout, source (`cli-override`, `legacy-extend`, `auto`, or `fallback`), and selection signals in `analysis.md` for reproducibility. Do not show layout IDs or candidates in the normal user confirmation or output summary; an explicit advanced override may be reported for auditability.

## Automatic Composition Selection

Apply the following rules in order. Once a structural hard signal matches, use it unless an explicit or legacy override has already resolved the layout. If the brief directly requests a recognized structure, such as a grid, timeline, full-bleed image, or badge-led composition, treat that intent as a hard signal after explicit and legacy overrides. Map natural-language requests to the closest built-in layout definition without exposing the internal ID to the user.

### 1. Structural Hard Signals

| Content signal | Internal layout |
|----------------|-----------------|
| Three or more ordered steps, times, sessions, or agenda items | `timeline-sequence` |
| Multiple products, SKUs, packages, or items that must be compared | `product-shelf` |
| Three or more peer modules, metrics, categories, or non-sequential information groups | `modular-grid` |
| A slogan or headline is the only meaningful content and typography is the subject | `big-type-only` |

### 2. Goal Candidates

When no hard signal matches, build an ordered candidate list from the poster goal:

| Goal | Ordered internal candidates |
|------|-----------------------------|
| Premium single-message key visual | `centered-hero`, `frame-within-frame`, `poster-card` |
| Announcement with clear details | `top-headline-stack`, `split-horizontal`, `poster-card` |
| Single-product promotion | `centered-hero`, `split-vertical`, `poster-card` |
| Culture, event, or editorial poster | `editorial-column`, `collage-montage`, `full-bleed-image-overlay` |
| Youth, music, or sports energy | `diagonal-dynamic`, `collage-montage`, `big-type-only` |
| Report or thought leadership | `modular-grid`, `editorial-column`, `split-horizontal` |
| Badge, anniversary, award, or certification | `badge-seal-system`, `centered-hero`, `poster-card` |
| Typography-led slogan | `big-type-only`, `top-headline-stack`, `diagonal-dynamic` |

### 3. Information Density

Use required poster copy, not the source document length, to determine density:

| Density | Signal | Prefer |
|---------|--------|--------|
| Low | Headline, optional subheadline, and no more than two details | `centered-hero`, `frame-within-frame`, `full-bleed-image-overlay`, `big-type-only` |
| Medium | Three to five details or one clear CTA plus metadata | `top-headline-stack`, `editorial-column`, `split-vertical`, `split-horizontal`, `poster-card`, `collage-montage` |
| High | More than five must-show details, multiple peer groups, or three or more agenda items | `timeline-sequence`, `modular-grid`, `split-horizontal`, `editorial-column` |

Remove candidates that cannot support the density. If filtering removes every goal candidate, use the first suitable candidate from `timeline-sequence`, `modular-grid`, `editorial-column`, or `split-horizontal` according to the content structure. Never force dense content into a sparse hero structure solely because it was first in the goal table.

### 4. Visual Subject

Reorder the remaining candidates from the available visual material:

- One dominant person or object: prefer `centered-hero` or `frame-within-frame`.
- One strong image with little copy: prefer `full-bleed-image-overlay`.
- Multiple images or a cutout relationship: prefer `collage-montage`.
- No usable image and text must carry the poster: prefer `big-type-only` or `top-headline-stack`.
- A seal, emblem, or symbolic mark is central: prefer `badge-seal-system`.
- The subject has clear movement or directional energy: prefer `diagonal-dynamic`.

### 5. Channel and Aspect-Ratio Tie-Break

Use channel and aspect ratio only after hard signals, goal, density, and visual-subject rules have produced a set of suitable candidates. Select the first remaining candidate in the matching preference list; if none remains, preserve the current candidate order.

| Channel or aspect ratio | Prefer when tied |
|-------------------------|------------------|
| Stage screen, presentation cover, or web banner | `split-vertical`, `full-bleed-image-overlay`, `modular-grid` |
| Social story, Reel, TikTok cover, or lock screen | `top-headline-stack`, `timeline-sequence`, `centered-hero` |
| Social feed or marketplace thumbnail | `centered-hero`, `poster-card`, `badge-seal-system`, `modular-grid` |
| `16:9` | `split-vertical`, `full-bleed-image-overlay`, `modular-grid` |
| `9:16` | `top-headline-stack`, `timeline-sequence`, `centered-hero` |
| `1:1` | `centered-hero`, `frame-within-frame`, `poster-card`, `badge-seal-system`, `modular-grid` |
| `2:3`, `3:4`, `4:5` | Preserve the candidate order and favor a vertical reading path |

If multiple candidates still tie, use their original order in the goal table. This makes the same brief and options resolve consistently.

## Style Selection

Only recommend IDs from `references/styles/`.

| Tone | Recommended Styles |
|------|--------------------|
| Premium / high-end | `luxury-minimal`, `swiss-editorial`, `cinematic-key-art` |
| Modern editorial | `swiss-editorial`, `data-editorial`, `editorial-collage` |
| Bold / disruptive | `neo-brutalist`, `constructivist-impact`, `pop-commercial` |
| Tech / AI / SaaS | `futurist-gradient`, `glassmorphism-ui`, `data-editorial` |
| Product / retail | `hyperreal-product`, `pop-commercial`, `luxury-minimal` |
| Handmade / local / warm | `organic-craft`, `risograph-zine`, `botanical-premium` |
| Design / education / architecture | `bauhaus-modular`, `swiss-editorial`, `data-editorial` |
| Film / podcast / performance | `cinematic-key-art`, `editorial-collage`, `retro-futurism` |
| Fashion / culture / magazine | `editorial-collage`, `swiss-editorial`, `monochrome-typographic` |
| Quiet premium / Japanese restraint | `japanese-ma`, `luxury-minimal`, `botanical-premium` |
| Typography-led impact | `monochrome-typographic`, `constructivist-impact`, `neo-brutalist` |
| Gala / hotel / nightlife luxury | `art-deco-luxe`, `luxury-minimal`, `cinematic-key-art` |
| Art book / indie culture | `risograph-zine`, `editorial-collage`, `organic-craft` |
| Experimental digital / conceptual | `surreal-3d-editorial`, `futurist-gradient`, `retro-futurism` |

## Aspect Ratio Selection

| Aspect ratio | Best for |
|--------------|----------|
| `2:3` | Default classic poster, Pinterest, flexible vertical poster |
| `4:5` | Instagram/Meta feed portrait and mobile-first campaigns |
| `9:16` | Stories, Reels, TikTok cover, phone lock-screen poster |
| `1:1` | Feed thumbnails, marketplace, compact social announcements |
| `3:4` | Print-friendly vertical, tablet poster, balanced editorial poster |
| `16:9` | Web banner, video thumbnail, presentation cover, stage screen |

## User-Facing Recommendation Format

Introduce the options by saying that information organization will be handled automatically from the content and aspect ratio. For each recommended option, include:

1. **Style**: one existing style ID and a readable display name.
2. **Why it fits**: audience, tone, subject, and channel.
3. **Visual outcome**: what the poster will feel like.
4. **Risk**: asset needs, text-rendering risk, or legibility issue if any.

Do not mention the selected layout, layout candidates, or layout/style combinations.

## Defaults

- Default style: `swiss-editorial`.
- Default aspect ratio: `2:3`.
- Layout: automatic; use `centered-hero` only as the final fallback.
- Default language: source language.
