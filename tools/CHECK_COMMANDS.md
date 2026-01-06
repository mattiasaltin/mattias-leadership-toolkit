# Local Markdown Check Commands

This document provides individual command-line instructions for running markdown checks locally.

## Prerequisites

### Option 1: Using npx (No installation required)

The commands below use `npx` which automatically downloads and runs the tools. No installation needed.

### Option 2: Install tools globally

```bash
npm install -g markdownlint-cli markdown-link-check
```

## Individual Commands

### 1. Lint Markdown Files

Check all markdown files for linting issues:

```bash
npx --yes markdownlint-cli "**/*.md" --ignore node_modules
```

Auto-fix linting issues where possible:

```bash
npx --yes markdownlint-cli "**/*.md" --ignore node_modules --fix
```

Check a specific file:

```bash
npx --yes markdownlint-cli path/to/file.md
```

### 2. Check Markdown Links

Check all links in all markdown files:

```bash
find . -name "*.md" -not -path "./node_modules/*" -not -path "./.venv/*" -exec npx --yes markdown-link-check --config .markdown-link-check.json {} \;
```

Check links in a specific file:

```bash
npx --yes markdown-link-check path/to/file.md --config .markdown-link-check.json
```

Check links without config file:

```bash
npx --yes markdown-link-check path/to/file.md
```

### 3. Using Make Commands

Run all markdown linting:

```bash
make lint-markdown
```

Auto-fix markdown linting issues:

```bash
make lint-markdown-fix
```

Check all links:

```bash
make check-links
```

Run all checks:

```bash
make check-all
```

### 4. Pre-commit Hooks

Install pre-commit hooks (runs automatically on `git commit`):

```bash
make install-pre-commit
# or manually:
pip3 install pre-commit
pre-commit install
```

Run pre-commit hooks on all files:

```bash
make pre-commit
# or manually:
pre-commit run --all-files
```

Run pre-commit hooks on staged files only:

```bash
make pre-commit-hook
# or manually:
pre-commit run
```

## Quick Reference

| Task | Command |
|------|---------|
| Lint all markdown | `npx --yes markdownlint-cli "**/*.md" --ignore node_modules` |
| Fix linting issues | `npx --yes markdownlint-cli "**/*.md" --ignore node_modules --fix` |
| Check all links | `find . -name "*.md" -not -path "./node_modules/*" -exec npx --yes markdown-link-check --config .markdown-link-check.json {} \;` |
| Install pre-commit | `make install-pre-commit` |
| Run all checks | `make check-all` |
