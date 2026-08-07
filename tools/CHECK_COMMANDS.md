# Local Markdown Check Commands

Prefer Make targets. Raw `npx` / `python3` commands are listed for one-off debugging.

## Prerequisites

- Node.js (for `npx` markdownlint / markdown-link-check)
- Python 3.10+ (for nav and citation scripts; `make setup` for the URL-checker venv)

Optional global install:

```bash
npm install -g markdownlint-cli markdown-link-check
```

## Make targets (preferred)

```bash
make lint-markdown       # markdownlint (ignores node_modules, tmp, docs, site)
make lint-markdown-fix  # auto-fix where possible
make check-nav           # indexes, prev/next, mkdocs.yml coverage
make check-links         # fail-closed link check on every .md
make check-citations     # soft-404 / YouTube checks on watched hosts
make check-all           # lint + nav + links + citations
```

Docs site:

```bash
make docs-setup
make docs-serve
make docs-build
```

## Individual commands

### Lint

```bash
npx --yes markdownlint-cli "**/*.md" --ignore node_modules --ignore tmp --ignore docs --ignore site
npx --yes markdownlint-cli "**/*.md" --ignore node_modules --ignore tmp --ignore docs --ignore site --fix
npx --yes markdownlint-cli path/to/file.md
```

### Links

```bash
npx --yes markdown-link-check path/to/file.md --config .markdown-link-check.json
```

Full-tree check matches `make check-links` (skips `node_modules`, `.venv`, `tmp`, `docs`, `site`).
LinkedIn and Substack are ignored in `.markdown-link-check.json` (bot-blocked from CI).

### Nav and citations

```bash
python3 tools/check_nav.py
python3 tools/check_citations.py
```

### Pre-commit

```bash
make install-pre-commit
make pre-commit          # all files
make pre-commit-hook     # staged only
```

Pre-commit runs markdownlint; nav, links, and citations are Make/CI gates.

## Quick reference

| Task | Command |
| --- | --- |
| Lint | `make lint-markdown` |
| Fix lint | `make lint-markdown-fix` |
| Nav | `make check-nav` |
| Links | `make check-links` |
| Citations | `make check-citations` |
| Everything | `make check-all` |
| URL checker UI | `make run` |
| Pre-commit (all) | `make pre-commit` |
