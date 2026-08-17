#!/usr/bin/env python3
"""Validate EPUB with epubcheck when available, otherwise run structural checks."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


def structural_checks(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        return [f"File does not exist: {path}"], warnings
    if not zipfile.is_zipfile(path):
        return ["EPUB is not a valid ZIP container"], warnings

    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        if not names or names[0] != "mimetype":
            warnings.append("mimetype is not the first ZIP entry")
        if "mimetype" not in names:
            errors.append("Missing root mimetype entry")
        else:
            value = zf.read("mimetype")
            if value != b"application/epub+zip":
                errors.append("mimetype entry is not 'application/epub+zip'")
            info = zf.getinfo("mimetype")
            if info.compress_type != zipfile.ZIP_STORED:
                warnings.append("mimetype entry is compressed; EPUB convention requires it stored uncompressed")
        if "META-INF/container.xml" not in names:
            errors.append("Missing META-INF/container.xml")
        if not any(name.endswith(".opf") for name in names):
            errors.append("No OPF package document found")
        if not any(name.endswith((".xhtml", ".html", ".htm")) for name in names):
            errors.append("No HTML/XHTML content documents found")

        xml_like = [name for name in names if name.endswith((".xml", ".opf", ".ncx", ".xhtml"))]
        for name in xml_like:
            try:
                ET.fromstring(zf.read(name))
            except ET.ParseError as exc:
                errors.append(f"Malformed XML/XHTML in {name}: {exc}")
    return errors, warnings


def run_epubcheck(path: Path) -> int | None:
    binary = shutil.which("epubcheck")
    if binary:
        print(f"Running epubcheck: {binary}")
        return subprocess.run([binary, str(path)]).returncode

    jar = os.environ.get("EPUBCHECK_JAR")
    candidates = [Path(jar)] if jar else []
    candidates += [
        Path("/usr/share/java/epubcheck.jar"),
        Path.home() / ".local/share/epubcheck/epubcheck.jar",
    ]
    java = shutil.which("java")
    for candidate in candidates:
        if java and candidate.exists():
            print(f"Running epubcheck JAR: {candidate}")
            return subprocess.run([java, "-jar", str(candidate), str(path)]).returncode
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an EPUB file")
    parser.add_argument("epub")
    parser.add_argument(
        "--require-epubcheck",
        action="store_true",
        help="Fail when official epubcheck is unavailable",
    )
    args = parser.parse_args()

    path = Path(args.epub).expanduser().resolve()
    errors, warnings = structural_checks(path)
    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")
    if errors:
        return 1

    result = run_epubcheck(path)
    if result is not None:
        return result

    message = (
        "Official epubcheck was not found. Structural checks passed, but this is NOT a full EPUB specification validation. "
        "Install epubcheck (and Java if using the JAR) for release validation."
    )
    if args.require_epubcheck:
        print(f"ERROR: {message}")
        return 2
    print(f"WARNING: {message}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
