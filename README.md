# Ebook Generator — Agent Skill

A portable Agent Skill for turning an idea, research bundle, transcripts, notes, Markdown, DOCX, or a finished manuscript into a structured ebook workflow with export and publishing preparation.

It combines four jobs that are usually split across separate tools:

1. **Plan and write** a coherent book, chapter by chapter.
2. **Transform source material** into original, reader-first synthesis.
3. **Package** Markdown chapters into EPUB3, DOCX, standalone HTML, and optional PDF.
4. **Prepare publication** metadata, cover briefs, validation, and release checklists.

The skill follows the open Agent Skills `SKILL.md` format and keeps detailed guidance in `references/` for progressive disclosure.

## What it can do

- Topic → book brief → outline → chapters → ebook
- Notes / articles / transcripts → deduplicated thematic handbook
- Existing Markdown manuscript → EPUB / DOCX / HTML / PDF
- Local images embedded into EPUB and standalone HTML
- Chapter/heading/image/placeholder checks
- EPUB structural validation plus official `epubcheck` when installed
- Cover brief and store metadata preparation
- Kindle/KDP and other store workflows with current-rule verification rather than hard-coded stale limits

## Repository structure

```text
ebook-generator/
├── SKILL.md
├── README.md
├── LICENSE
├── requirements.txt
├── requirements-pdf.txt
├── scripts/
│   ├── init_book.py
│   ├── check_manuscript.py
│   ├── build_book.py
│   └── validate_epub.py
├── references/
│   ├── research.md
│   ├── quality-gates.md
│   ├── formats.md
│   └── publishing.md
├── assets/
│   ├── book.yaml
│   ├── brief-template.md
│   ├── chapter-template.md
│   └── epub.css
└── examples/
    └── sample-book/
```

## Install dependencies

```bash
python -m pip install -r requirements.txt
```

Optional PDF export:

```bash
python -m pip install -r requirements-pdf.txt
```

For release-grade EPUB validation, install the official `epubcheck` CLI or set `EPUBCHECK_JAR` to an epubcheck JAR and ensure Java is available.

## Quick start

Initialize a project:

```bash
python scripts/init_book.py ./my-book
```

Edit `my-book/book.yaml`, `brief.md`, `outline.md`, and `chapters/*.md`.

Check the manuscript:

```bash
python scripts/check_manuscript.py ./my-book
```

Build all available formats:

```bash
python scripts/build_book.py ./my-book --format all
```

Validate the EPUB:

```bash
python scripts/validate_epub.py ./my-book/dist/book.epub
```

## Example `book.yaml`

```yaml
title: "Practical AI Research"
subtitle: "A Field Guide for Literature Review Workflows"
author: "Your Name"
language: "en"
publisher: ""
description: "A practical guide to reproducible AI-assisted research workflows."
cover: "assets/cover.jpg"
output_name: "practical-ai-research"
```

Chapter files are sorted lexically, so use numbered names:

```text
chapters/
├── 01-introduction.md
├── 02-research-question.md
├── 03-search-strategy.md
└── 04-evidence-synthesis.md
```

## Using it as an Agent Skill

Use this repository as the `ebook-generator` skill directory in any client that supports the open Agent Skills format. The required entry point is `SKILL.md`; scripts and references are loaded or executed only when needed.

Validate the skill metadata/structure with the current Agent Skills reference validator if you have it installed:

```bash
skills-ref validate .
```

## Design principles

- **Reader-first, not source-first.** Twenty inputs do not automatically become twenty chapters.
- **Editable source stays primary.** Generated EPUB/PDF are outputs, not the canonical manuscript.
- **Evidence is traceable.** Nonfiction research keeps a source ledger and never invents citations.
- **Publishing rules are verified at use time.** Store requirements change too often to hard-code as eternal truth.
- **No black-box validity claims.** A structural EPUB check is explicitly distinguished from a full `epubcheck` pass.
- **Original synthesis.** The workflow uses other material as factual/idea input rather than stitching copyrighted passages together.

## 中文说明

这是一个通用“电子书生成”Skill，不只是 Markdown 转 EPUB。

它可以把：

**主题 / 资料 / 网页 / 视频转录 / 笔记 / Markdown / 已完成书稿**

一路处理成：

**书籍 Brief → 大纲 → 分章写作 → 质量检查 → EPUB / DOCX / HTML / PDF → EPUB 校验 → 封面 Brief → 出版 Metadata**。

如果只是已有书稿，也可以跳过写作阶段，直接做排版、导出和校验。

## Acknowledgements

This project is an original implementation inspired by patterns and lessons from several open-source ebook/Agent Skill projects, including:

- `smerchek/claude-epub-skill` — Markdown-to-EPUB skill structure and EPUB-focused workflow
- `ThomasHoussin/Claude-Book` — chapter-by-chapter planning, review gates, continuity/state concepts
- `jessl2juice/kindlepub` — release validation and publishing preparation workflow
- `arturseo-geo/ebook-publishing-skill` — broader self-publishing workflow coverage
- `zarazhangrui/youtube-to-ebook` — source/transcript-to-publication pipeline concept

No source code from those projects is copied into this repository. Their repositories should be consulted under their own licenses when reusing their code.

## License

MIT
