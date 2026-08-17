#!/usr/bin/env python3
"""Initialize a new ebook-generator book project."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def copy_if_missing(src: Path, dst: Path, force: bool = False) -> None:
    if dst.exists() and not force:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize an ebook project")
    parser.add_argument("project", help="Destination project directory")
    parser.add_argument("--force", action="store_true", help="Overwrite template files")
    args = parser.parse_args()

    root = Path(args.project).expanduser().resolve()
    skill_root = Path(__file__).resolve().parents[1]
    assets = skill_root / "assets"

    for directory in ("chapters", "assets/images", "dist"):
        (root / directory).mkdir(parents=True, exist_ok=True)

    copy_if_missing(assets / "book.yaml", root / "book.yaml", args.force)
    copy_if_missing(assets / "brief-template.md", root / "brief.md", args.force)
    copy_if_missing(assets / "chapter-template.md", root / "chapters/01-introduction.md", args.force)

    for name, content in {
        "outline.md": "# Outline\n\n## Chapter 1 — Introduction\n\n- Promise:\n- Key points:\n- Evidence/assets:\n",
        "sources.md": "# Sources\n\nRecord source title, author/organization, date, URL/file, claims used, and chapter references.\n",
        "style-guide.md": "# Style Guide\n\n- Audience:\n- Tone:\n- Voice:\n- Terminology:\n- Citation style:\n- Formatting conventions:\n",
    }.items():
        path = root / name
        if args.force or not path.exists():
            path.write_text(content, encoding="utf-8")

    print(f"Initialized ebook project: {root}")
    print("Next: edit book.yaml, brief.md, outline.md, and chapters/*.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
