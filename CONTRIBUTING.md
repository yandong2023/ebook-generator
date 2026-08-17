# Contributing

Contributions are welcome.

Please keep the project portable and conservative about dependencies:

1. Keep `SKILL.md` focused; move detailed material into `references/`.
2. Do not hard-code publishing platform rules that can change; document the need for current verification.
3. Add or update tests for script changes.
4. Do not add copied third-party prose or source code without compatible licensing and attribution.
5. Run:

```bash
python scripts/validate_skill.py .
pytest -q
```

For EPUB changes, also run the official `epubcheck` before claiming release-grade validity.
