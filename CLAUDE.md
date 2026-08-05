# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **content repository**, not a software project. It is a curated collection of leadership
resources written in Markdown. The "product" is the Markdown itself. Helper tooling:

- `tools/url_checker.py` — Streamlit UI for validating links
- `tools/check_nav.py` — indexes and prev/next chain consistency
- MkDocs Material (`mkdocs.yml` + `docs/` symlinks) — optional site via GitHub Pages

Because the deliverable is prose, the meaningful quality gates are Markdown linting, navigation
consistency, and link validation — not compilation or unit tests.

## Structure

Content is organized into two top-level domains, each a self-contained collection with its own
`README.md` and `CONTRIBUTING.md`:

- `engineering-leadership-resources/` — organized around three areas of accountability plus a
  catch-all: `org-health/`, `tech-health/`, `delivery-execution/`, and `other/`. Each subdirectory
  has its own `README.md` acting as an index.
- `product-leadership-resources/` — flat set of topic files structured around Marty Cagan's
  EMPOWERED framework (leadership: vision, strategy, principles, priorities, evangelism;
  management: staffing, coaching, objectives), plus `product-discovery.md` and `product-other.md`.

The root `README.md` is the entry point and also defines shared "Key Frameworks Referenced"
(EMPOWERED, GROW, OKR, DORA, BICEPS) that individual content files link back to.

## Commands

All common tasks go through the `Makefile`:

- `make setup` — create `.venv` and install `requirements.txt`
- `make run` — launch the URL checker UI: `streamlit run tools/url_checker.py`
- `make lint-markdown` / `make lint-markdown-fix` — run `markdownlint-cli` (auto-fix variant)
- `make check-nav` — indexes + prev/next chains (`tools/check_nav.py`)
- `make check-links` — run `markdown-link-check` on every `.md` (uses `.markdown-link-check.json`)
- `make check-all` — lint + nav + link-check (mirrors CI)
- `make docs-setup` / `make docs-serve` / `make docs-build` — MkDocs Material site
- `make pre-commit` — run all pre-commit hooks on all files
- `make freeze` — regenerate `requirements.txt` (direct tool deps only)
- `make clean` — remove `.venv`

CI (`.github/workflows/markdown.yml`) runs on push/PR to `main`/`master` and enforces markdownlint,
nav consistency, and link validation. Pages deploy is `.github/workflows/pages.yml`. Run
`make check-all` locally before pushing to match CI.

## Conventions when editing content

These are load-bearing — CI and the house style depend on them:

- **Markdown lint rules** (`.markdownlint.json`): line length is capped at **120 chars** (code
  blocks and tables exempt). Inline HTML (MD033) and "first line must be a heading" (MD041) are
  disabled. The pre-commit hook auto-fixes on commit.
- **Resource format icons** — every resource entry is prefixed with a format emoji, used
  consistently across all content: 📘 Book · 🎥 Video/Talk · 📄 Article/Blog · 🎧 Podcast ·
  📊 Research Paper/Whitepaper. Preserve these when adding entries.
- **Section emojis and navigation** — headings and directory sections use consistent emoji
  (🌱 engineering, 🌟 product, 🧠 org-health, ⚙️ tech-health, 🚀 delivery). Match the surrounding
  style rather than introducing new markers.
- **British English** spelling is used throughout the prose ("organised", "optimise", "prioritise").
- **Links to internal files must be valid** — the link checker fails CI on broken links. When
  moving or renaming a file, update the domain `README.md` index and any cross-references.
- When adding a resource file to a domain, add it to the relevant `README.md` index so it is
  discoverable (indexes are maintained by hand, not generated). `make check-nav` enforces this and
  prev/next chain consistency.

## Mermaid diagrams

When asked to create/edit/visualize a diagram, follow `.github/instructions/mermaid.instructions.md`
(referenced by `.github/copilot-instructions.md`).

## Notes

- `tmp/` is excluded from lint/link checks (see the CI `ignore-files` and lint `--ignore`).
- `docs/` is a thin symlink layer over root content (MkDocs requires a child `docs_dir`).
- `site/` is the MkDocs build output and is git-ignored.
- `.venv/` is git-ignored; create it locally via `make setup`.
