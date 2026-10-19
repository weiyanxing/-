# Poster Content Analysis

Use this reference to turn any source text into `analysis.md`. The goal is not to summarize everything; it is to extract the information that can become a clear poster.

## 1. Identify the Input

Classify the source before extracting content:

- **Type**: event, product, promotion, course, recruitment, report, brand, public-interest, quote, announcement, multi-topic, messy text, long-form text.
- **Purpose**: inform, promote, sell, invite, recruit, announce, educate, persuade, or express brand mood.
- **Audience**: who the poster needs to speak to.
- **Channel**: social feed, story, print poster, banner, internal notice, product ad, event invite.
- **Language**: source language and requested output language.
- **Constraints**: required copy, brand rules, visual assets, aspect ratio, backend, user design instructions.

## 2. Choose the Poster Mainline

A poster needs one mainline. If the source has multiple topics, choose the one most aligned with the user's request.

Use this priority order:

1. Explicit user instruction.
2. Clear CTA or conversion goal.
3. Event/product/campaign title.
4. Most repeated or most specific theme.
5. Best single-message poster angle.

If two mainlines are equally valid and the choice changes the poster meaning, ask the user before generating.

## 3. Extract Poster Fields

Extract only fields that help the poster communicate.

### Must Consider

- **Main headline**: shortest accurate title or offer.
- **Subheadline**: one supporting line when useful.
- **Key points**: up to 3-5 concise benefits, facts, or details.
- **Lineup / speakers / guests**: for events, concerts, conferences, and festivals — the performer or speaker list is core content, not secondary detail. Include all named performers/speakers unless the list exceeds 30 entries.
- **CTA**: an exact action phrase explicitly present in the source, such as register, buy, attend, scan, download, or apply. Record its exact source quote when translating it. Otherwise leave CTA empty.
- **Metadata**: date, time, location, price, speaker, brand, product, URL.
- **Visual subject**: product, person, venue, object, mood, symbol, or abstract concept.
- **Tone**: premium, energetic, calm, playful, technical, editorial, urgent, warm.
- **Missing fields**: important information not present in the source.

### Exclude by Default

- Repeated boilerplate.
- Legal or operational details unless required.
- Long paragraphs that cannot fit on a poster.
- Multiple CTAs competing with each other.
- Internal notes, chat noise, signatures, timestamps, navigation text.
- Organizational affiliations or parenthetical annotations (e.g., company/school names after performer names) — unless the user explicitly requires them or they are the poster's selling point.

## 4. Control Information Density

### Step A: Assess Input Structure

Before applying density limits, determine the compression level from the input's structural characteristics — not word count:

- **Structured input** (bullet points, schedule, lineup, table, or clearly segmented sections with named entities): Apply light filtering only — remove obvious noise (boilerplate, internal notes) but preserve all named entities, facts, and structured items. Do not artificially cap key points.
- **Semi-structured input** (mix of prose paragraphs and key facts, or a brief with some narrative explanation): Apply moderate compression — keep all named entities (people, brands, places) and key facts; trim explanatory prose and redundant descriptions.
- **Unstructured long-form input** (articles, essays, reports, meeting transcripts, multi-paragraph descriptions): Apply the long-text compression rules in Step D below.

### Step B: Classify by Content Type

Different content types have different "core information":

| Content type | Must show (in addition to headline/CTA/metadata) |
|---|---|
| Music festival / concert / performance | Full performer/band lineup per session/day |
| Conference / summit / workshop | Speaker names and talk titles |
| Product launch | Product name, key specs, price |
| Recruitment | Role title, key requirements, compensation highlights |
| Promotion / sale | Offer details, discount amount, valid period |
| Course / training | Instructor, schedule, key topics |

If the content type has a "Must show" rule above, that content cannot be moved to "Can show" or "Do not show" regardless of density.

### Step C: Three-Bucket Classification

Classify extracted content into three buckets:

- **Must show**: headline, key offer/message, required time/place/CTA, AND content-type-specific must-show items from Step B.
- **Can show**: secondary benefits, short context, supporting labels, organizational affiliations.
- **Do not show**: background explanation, redundant details, low-priority paragraphs, content that adds no decision value for the audience.

### Step D: Long-Text Compression (only for long input > 2000 chars)

- Use 1 main headline.
- Use 0-1 subheadline.
- Use at most 5-8 key points (raised from 3-5 to avoid losing named entities).
- Move details to footer-style metadata.
- Prefer a concept poster if exact copy would overload the layout.
- Even for long text: named performers, speakers, or guests are key points, not details.

## 5. Missing Information Policy

Do not invent facts.

- If missing fields are not essential, continue and mark them as omitted.
- If the poster goal depends on a missing field, ask the user.
- CTA is extractive-only. If no exact CTA wording exists in the source, leave CTA empty; never add a neutral fallback such as "Learn more", "Coming soon", "Shop now", "了解更多", "敬请期待", or "立即选购".
- A source-supplied CTA remains ordinary static poster copy. It must not imply a clickable button, pill, chip, tab, or other interactive control.
- If exact text rendering matters, keep required copy short and flag post-editing risk.

## 6. `analysis.md` Output Format

```markdown
# Analysis

## Input

- Type:
- Purpose:
- Audience:
- Channel:
- Source language:
- Output language:
- User instructions:

## Poster Mainline

- Mainline:
- Reason:
- Desired action:

## Extracted Fields

- Main headline:
- Subheadline:
- Key points:
- CTA:
- Metadata:
- Visual subject:
- Tone:

## Information Priority

- Must show:
- Can show:
- Do not show:

## Missing / Ambiguous

- Missing fields:
- Ambiguities:
- Ask user before proceeding: yes/no

## Recommended Direction

- Composition needs:
- Style candidates:
- Aspect ratio candidates:

## Internal Production Record

- Composition reference:
- Resolution source: cli-override / legacy-extend / auto / fallback
- Selection signals:
```
