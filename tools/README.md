# Tools

Helper scripts for maintaining this content repository. Prefer the root `Makefile` for day-to-day
checks; this directory holds the implementations.

| Script | Purpose | Make target |
| --- | --- | --- |
| `url_checker.py` | Interactive Streamlit UI for validating links | `make run` |
| `check_nav.py` | Indexes, prev/next chains, and `mkdocs.yml` coverage | `make check-nav` |
| `check_citations.py` | Soft-404 / YouTube oEmbed checks on citation hosts | `make check-citations` |
| `prepare_docs.sh` | Symlink layer for MkDocs (`docs/`) | `make docs-prepare` |

See [CHECK_COMMANDS.md](CHECK_COMMANDS.md) for lint/link commands and the full Make checklist.

## Setup

```bash
make setup          # create .venv and install requirements.txt
source .venv/bin/activate
```

Python 3.10+ required.

## URL checker

```bash
make run            # streamlit run tools/url_checker.py
```

## Freezing dependencies

Do **not** dump the whole venv. Only pin the direct deps the URL checker needs:

```bash
make freeze
```

That rewrites `requirements.txt` with `beautifulsoup4`, `rapidfuzz`, `requests`, and `streamlit`.

## Notes

- `.venv/` is git-ignored; create it locally via `make setup`.
- `docs/` and `site/` are generated/git-ignored MkDocs paths.
- CI runs lint, nav, links, and citations; pre-commit currently runs markdownlint only.
