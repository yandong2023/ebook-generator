#!/usr/bin/env python3
"""Run lightweight structural checks on an ebook-generator project."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)
PLACEHOLDERS = ("TODO", "TBD", "FIXME", "[citation needed]", "[SOURCE]", "XXX")


def load_config(project: Path) -> dict:
    config_path = project / "book.yaml"
    if not config_path.exists():
        return {}
    return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}


def resolve_image(chapter: Path, project: Path, raw: str) -> Path | None:
    src = raw.strip().split()[0].strip("<>")
    if src.startswith(("http://", "https://", "data:")):
        return None
    candidates = [chapter.parent / src, project / src]
    for candidate in candidates:
        candidate = candidate.resolve()
        if candidate.exists():
            return candidate
    return candidates[0].resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description="Check manuscript structure")
    parser.add_argument("project")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    project = Path(args.project).expanduser().resolve()
    config = load_config(project)
    chapters = sorted((project / "chapters").glob("*.md"))

    errors: list[str] = []
    warnings: list[str] = []
    stats: list[dict] = []
    seen_titles: dict[str, str] = {}

    if not (project / "book.yaml").exists():
        errors.append("Missing book.yaml")
    for key in ("title", "author", "language"):
        if not str(config.get(key, "")).strip():
            warnings.append(f"book.yaml: missing or empty '{key}'")

    if not chapters:
        errors.append("No Markdown chapters found in chapters/")

    for chapter in chapters:
        text = chapter.read_text(encoding="utf-8")
        headings = HEADING_RE.findall(text)
        h1s = [title.strip() for marks, title in headings if len(marks) == 1]
        words = len(WORD_RE.findall(re.sub(r"```.*?```", "", text, flags=re.S)))
        stats.append({"file": chapter.name, "words": words, "h1": h1s[0] if h1s else None})

        if not h1s:
            errors.append(f"{chapter.name}: missing H1 chapter title")
        elif len(h1s) > 1:
            warnings.append(f"{chapter.name}: contains {len(h1s)} H1 headings; one chapter title is recommended")

        if h1s:
            normalized = re.sub(r"\s+", " ", h1s[0]).casefold()
            if normalized in seen_titles:
                errors.append(f"Duplicate chapter title: '{h1s[0]}' in {seen_titles[normalized]} and {chapter.name}")
            else:
                seen_titles[normalized] = chapter.name

        if words < 100:
            warnings.append(f"{chapter.name}: only {words} words; verify this chapter is intentional")

        for marker in PLACEHOLDERS:
            if marker.casefold() in text.casefold():
                warnings.append(f"{chapter.name}: unresolved placeholder '{marker}'")

        for raw_src in IMAGE_RE.findall(text):
            resolved = resolve_image(chapter, project, raw_src)
            if resolved is not None and not resolved.exists():
                errors.append(f"{chapter.name}: missing local image '{raw_src}'")

        previous_level = 0
        for marks, title in headings:
            level = len(marks)
            if previous_level and level > previous_level + 1:
                warnings.append(
                    f"{chapter.name}: heading jumps H{previous_level} -> H{level} near '{title.strip()}'"
                )
            previous_level = level

    result = {
        "project": str(project),
        "chapters": len(chapters),
        "words": sum(item["words"] for item in stats),
        "chapter_stats": stats,
        "errors": errors,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Project: {project}")
        print(f"Chapters: {result['chapters']} | Approx. words: {result['words']}")
        for item in stats:
            print(f"  {item['file']}: {item['words']} words")
        if errors:
            print("\nERRORS")
            for message in errors:
                print(f"  - {message}")
        if warnings:
            print("\nWARNINGS")
            for message in warnings:
                print(f"  - {message}")
        if not errors and not warnings:
            print("\nNo issues found.")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
