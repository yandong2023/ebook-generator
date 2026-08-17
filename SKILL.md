---
name: ebook-generator
description: Create, transform, package, validate, and prepare professional ebooks from a topic, outline, notes, URLs, transcripts, Markdown, DOCX, or an existing manuscript. Use when the user wants to write a book, turn source material into an ebook, compile chapters, export EPUB/DOCX/PDF/HTML, generate book metadata or cover briefs, validate an EPUB, or prepare a finished book for Kindle/KDP and other ebook stores.
license: MIT
compatibility: Requires Python 3.10+ for bundled scripts. Core EPUB/DOCX/HTML export uses pip packages from requirements.txt; EPUB packaging itself uses Python standard-library ZIP/XML generation. PDF export optionally uses WeasyPrint. Research/source retrieval depends on tools available to the host agent.
metadata:
  author: yandong2023
  version: "1.0.0"
  standard: agentskills.io
---

# Ebook Generator

Turn an idea or a pile of source material into a coherent, editable, validated ebook. This skill covers the full workflow from planning and writing through export and publishing preparation.

## Choose the operating mode

Infer the mode from the request. Do not force the user through every stage.

1. **Create** — start from a topic, audience, goal, rough notes, or research material.
2. **Transform** — turn existing URLs, transcripts, notes, articles, Markdown, DOCX, or other user-supplied material into a book.
3. **Package** — compile an already-finished manuscript into EPUB/DOCX/HTML/PDF.
4. **Publish prep** — produce store metadata, cover brief, validation results, and a final release checklist.

If the user already supplied enough information, proceed without repeating questions. When details are missing, make conservative defaults and record them in `book.yaml` so they are easy to change.

## Non-negotiable rules

- Preserve the user's meaning and factual claims unless explicitly asked to rewrite them.
- For nonfiction, separate sourced facts from inference and maintain a source/citation ledger when research is used.
- Do not fabricate citations, quotations, statistics, endorsements, reviews, ISBNs, store approvals, or publication status.
- Do not copy long passages from source material. Synthesize and rewrite unless the user owns the text or explicitly provided it for transformation.
- Do not imitate a living author's style. Derive neutral craft attributes instead (for example: concise sentences, high dialogue density, restrained tone).
- Treat publishing platform rules, prices, royalties, metadata limits, and submission requirements as changeable. Verify current rules before giving platform-specific instructions.
- Never claim an EPUB is valid until validation has actually run. Prefer `epubcheck` when available.
- Do not perform irreversible publishing actions without explicit user authorization.

## Canonical project layout

Use this layout for book projects:

```text
book-project/
├── book.yaml
├── brief.md
├── outline.md
├── sources.md
├── style-guide.md
├── chapters/
│   ├── 01-introduction.md
│   └── 02-....md
├── assets/
│   ├── cover.jpg
│   └── images/
└── dist/
```

Initialize it with:

```bash
python scripts/init_book.py path/to/book-project
```

## End-to-end workflow

### 1. Intake and rights boundary

Classify each input as one of: user-authored, public-domain, licensed, factual reference, or third-party copyrighted source. For third-party sources, extract ideas/facts and write original prose rather than reproducing the source.

For source-heavy projects, read [references/research.md](references/research.md).

### 2. Build the book brief

Create or update `brief.md` with:

- working title and subtitle
- target reader
- reader problem / desired outcome
- scope and exclusions
- format: nonfiction, guide, report, fiction, anthology, magazine, etc.
- approximate chapter count and target length
- language and tone
- evidence/citation policy
- desired outputs

Use [assets/brief-template.md](assets/brief-template.md) when useful.

### 3. Build a book bible and outline

Create `style-guide.md` and `outline.md` before long-form drafting. The outline should define the promise of each chapter, its key points, dependencies on previous chapters, and evidence/assets needed.

For long projects, maintain continuity state between chapters: terminology, people/entities, claims already introduced, unresolved promises, examples used, and cross-references.

### 4. Draft chapter by chapter

For each chapter:

1. read the brief, style guide, outline entry, prior chapter summary, and relevant sources;
2. create a short beat/section plan;
3. draft the chapter;
4. run a self-review for structure, repetition, unsupported claims, continuity, and reader usefulness;
5. revise once before marking the chapter ready;
6. save the final chapter under `chapters/NN-slug.md`.

Do not regenerate good sections merely to make them different. Prefer targeted edits.

Use the quality gates in [references/quality-gates.md](references/quality-gates.md).

### 5. Compile and export

The bundled builder expects `book.yaml` plus Markdown chapters.

```bash
python scripts/build_book.py path/to/book-project --format all
```

Supported outputs:

- EPUB3 (`.epub`)
- Microsoft Word (`.docx`)
- standalone HTML (`.html`)
- PDF (`.pdf`) when WeasyPrint is installed

Run manuscript checks first for substantial books:

```bash
python scripts/check_manuscript.py path/to/book-project
```

Then validate EPUB:

```bash
python scripts/validate_epub.py path/to/book-project/dist/book.epub
```

See [references/formats.md](references/formats.md) for details and fallbacks.

### 6. Cover and visual assets

Create a cover **brief** before generating cover art. Specify audience, genre/category cues, emotional promise, composition, typography intent, colors only if requested, and what must not appear.

Keep AI-generated cover art free of accidental title text when the final title will be added by a publishing tool or designer. Verify store-specific dimensions at the time of publication.

### 7. Publishing preparation

For a finished book, prepare:

- title / subtitle / author / publisher or imprint
- short and long description
- category suggestions
- keyword candidates
- audience / age range when applicable
- edition and language
- price hypothesis (clearly labeled as a hypothesis)
- AI-content disclosure notes where relevant
- cover and interior asset checklist
- release checklist

Read [references/publishing.md](references/publishing.md) before platform-specific work. Verify current platform requirements online when possible.

## Output contract

When the user asks for a finished ebook workflow, leave them with:

1. the editable source project (`book.yaml`, outline, chapters, assets);
2. requested export files in `dist/`;
3. validation/check results with any remaining warnings;
4. a concise publication-readiness summary.

If only part of the workflow was requested, return only that part and do not invent completion of later stages.

## Examples

**Topic to ebook**

> Create a practical 10-chapter ebook about using AI for literature reviews, with citations, and export EPUB + DOCX.

Expected: research plan → brief → outline → chapters → checks → EPUB/DOCX → validation summary.

**Sources to ebook**

> Turn these 20 articles and 8 YouTube transcripts into a concise handbook. Avoid repetition and preserve source links.

Expected: source ledger → thematic clustering → original synthesis → chapter plan → manuscript → source appendix → exports.

**Existing manuscript**

> Package this Markdown folder into a professional EPUB for Kindle and Apple Books.

Expected: normalize headings/assets → build EPUB → run validation → report issues; do not unnecessarily rewrite prose.

## References

- Research and source handling: [references/research.md](references/research.md)
- Writing and QA gates: [references/quality-gates.md](references/quality-gates.md)
- Export formats: [references/formats.md](references/formats.md)
- Publishing preparation: [references/publishing.md](references/publishing.md)
