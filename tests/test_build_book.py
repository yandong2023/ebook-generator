from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "sample-book"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )


def test_manuscript_check_passes():
    result = run("scripts/check_manuscript.py", str(SAMPLE))
    assert result.returncode == 0, result.stdout + result.stderr


def test_build_epub_docx_html():
    for fmt in ("epub", "docx", "html"):
        result = run("scripts/build_book.py", str(SAMPLE), "--format", fmt)
        assert result.returncode == 0, result.stdout + result.stderr

    dist = SAMPLE / "dist"
    assert (dist / "small-systems-better-work.epub").exists()
    assert (dist / "small-systems-better-work.docx").exists()
    assert (dist / "small-systems-better-work.html").exists()


def test_epub_structural_validation():
    epub_path = SAMPLE / "dist" / "small-systems-better-work.epub"
    if not epub_path.exists():
        build = run("scripts/build_book.py", str(SAMPLE), "--format", "epub")
        assert build.returncode == 0, build.stdout + build.stderr
    result = run("scripts/validate_epub.py", str(epub_path))
    assert result.returncode == 0, result.stdout + result.stderr
