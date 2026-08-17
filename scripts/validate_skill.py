#!/usr/bin/env python3
"""Offline validation for the core Agent Skills SKILL.md constraints."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate basic Agent Skills structure offline")
    parser.add_argument("skill", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.skill).expanduser().resolve()
    skill_file = root / "SKILL.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_file.exists():
        print("ERROR: missing SKILL.md")
        return 1

    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter")
        metadata = {}
        body = text
    else:
        parts = text.split("---", 2)
        if len(parts) < 3:
            errors.append("SKILL.md frontmatter is not closed")
            metadata = {}
            body = text
        else:
            try:
                metadata = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError as exc:
                metadata = {}
                errors.append(f"Invalid YAML frontmatter: {exc}")
            body = parts[2]

    name = str(metadata.get("name") or "")
    description = str(metadata.get("description") or "")
    compatibility = metadata.get("compatibility")

    if not name:
        errors.append("Frontmatter requires 'name'")
    elif len(name) > 64:
        errors.append("'name' must be <= 64 characters")
    elif not NAME_RE.fullmatch(name):
        errors.append("'name' must contain lowercase letters/numbers with single hyphens")

    if name and root.name != name:
        errors.append(f"Skill directory '{root.name}' must match name '{name}'")

    if not description:
        errors.append("Frontmatter requires non-empty 'description'")
    elif len(description) > 1024:
        errors.append("'description' must be <= 1024 characters")

    if compatibility is not None and not (1 <= len(str(compatibility)) <= 500):
        errors.append("'compatibility' must be 1-500 characters when present")

    line_count = len(text.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md has {line_count} lines; keeping it under 500 is recommended")

    for target in LINK_RE.findall(body):
        if target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = target.split("#", 1)[0]
        if target and not (root / target).exists():
            errors.append(f"Broken local reference in SKILL.md: {target}")

    print(f"Skill: {root}")
    print(f"name={name!r} | description_chars={len(description)} | lines={line_count}")
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1
    print("Offline Agent Skills checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
