# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **content repository**, not a software project. It is a curated collection of leadership
resources written in Markdown. The "product" is the Markdown itself. Helper tooling:

- `tools/url_checker.py` — Streamlit UI for validating links
- `tools/check_nav.py` — indexes, prev/next chains, and `mkdocs.yml` coverage
- `tools/check_citations.py` — soft-404 / YouTube oEmbed checks on citation hosts
- MkDocs Material (`mkdocs.yml`; `docs/` via `tools/prepare_docs.sh`) — GitHub Pages

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
  management: staffing, coaching, objectives), plus `product-discovery.md`.

The root `README.md` is the entry point and also defines shared "Key Frameworks Referenced"
(EMPOWERED, GROW, OKR, DORA, BICEPS) that individual content files link back to.

## Commands

All common tasks go through the `Makefile`:

- `make setup` — create `.venv` and install `requirements.txt`
- `make run` — launch the URL checker UI: `streamlit run tools/url_checker.py`
- `make lint-markdown` / `make lint-markdown-fix` — run `markdownlint-cli` (auto-fix variant)
- `make check-nav` — indexes, prev/next chains, and `mkdocs.yml` coverage
- `make check-links` — fail-closed `markdown-link-check` on every `.md`
- `make check-citations` — soft-404 title/final-URL checks on curated hosts + YouTube
- `make check-all` — lint + nav + links + citations
- `make docs-setup` / `make docs-serve` / `make docs-build` — MkDocs Material site
- `make pre-commit` — run all pre-commit hooks on all files
- `make freeze` — regenerate `requirements.txt` (direct tool deps only)
- `make clean` — remove `.venv`

CI (`.github/workflows/markdown.yml`) on push/PR: markdownlint, nav, links, and
`mkdocs build --strict`. Pages deploy is `.github/workflows/pages.yml`. Link-check intentionally
ignores LinkedIn and Substack (bot-blocked from Actions); do not ignore durable citation hosts.

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
- `docs/` is generated (symlink layer) by `tools/prepare_docs.sh` / `make docs-prepare`; git-ignored.
- `site/` is the MkDocs build output and is git-ignored.
- `.venv/` is git-ignored; create it locally via `make setup`.
