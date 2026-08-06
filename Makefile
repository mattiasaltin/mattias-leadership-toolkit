# Define variables
VENV_DIR = .venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
STREAMLIT = $(VENV_DIR)/bin/streamlit

# Default target
.PHONY: all
all: setup

# Create and activate virtual environment
.PHONY: setup
setup: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate: requirements.txt
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	touch $(VENV_DIR)/bin/activate

# Run the URL Checker script using Streamlit
.PHONY: run
run: $(VENV_DIR)/bin/activate
	$(STREAMLIT) run tools/url_checker.py

# Freeze only the direct deps needed by tools/url_checker.py (never dump the whole venv)
.PHONY: freeze
freeze: $(VENV_DIR)/bin/activate
	$(PIP) freeze | grep -E '^(beautifulsoup4|rapidfuzz|requests|streamlit)==' > requirements.txt

# Clean up the virtual environment
.PHONY: clean
clean:
	if [ -f "$(VENV_DIR)/bin/activate" ]; then \
		. $(VENV_DIR)/bin/activate && deactivate; \
	fi
	rm -rf $(VENV_DIR)

# Pre-commit hooks
.PHONY: install-pre-commit
install-pre-commit:
	pip3 install pre-commit || python3 -m pip install pre-commit
	pre-commit install

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: pre-commit-hook
pre-commit-hook:
	pre-commit run

# Markdown checks
.PHONY: lint-markdown
lint-markdown:
	npx --yes markdownlint-cli "**/*.md" --ignore node_modules --ignore tmp --ignore docs --ignore site

.PHONY: lint-markdown-fix
lint-markdown-fix:
	npx --yes markdownlint-cli "**/*.md" --ignore node_modules --ignore tmp --ignore docs --ignore site --fix

.PHONY: check-links
check-links:
	@failed=0; \
	while IFS= read -r -d '' f; do \
		npx --yes markdown-link-check --config .markdown-link-check.json "$$f" || failed=1; \
	done < <(find . -name "*.md" -not -path "./node_modules/*" -not -path "./.venv/*" -not -path "./tmp/*" -not -path "./docs/*" -not -path "./site/*" -print0); \
	if [ "$$failed" -ne 0 ]; then echo "check-links: one or more files had dead links"; exit 1; fi

.PHONY: check-nav
check-nav:
	python3 tools/check_nav.py

.PHONY: check-all
check-all: lint-markdown check-nav check-links

.PHONY: docs-setup
docs-setup: $(VENV_DIR)/bin/activate
	$(PIP) install -r requirements-docs.txt

.PHONY: docs-prepare
docs-prepare:
	bash tools/prepare_docs.sh

.PHONY: docs-serve
docs-serve: docs-setup docs-prepare
	$(VENV_DIR)/bin/mkdocs serve

.PHONY: docs-build
docs-build: docs-setup docs-prepare
	$(VENV_DIR)/bin/mkdocs build --strict

# Help target to display available commands
.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make setup              - Set up the virtual environment and install dependencies"
	@echo "  make install-pre-commit - Install and set up pre-commit hooks"
	@echo "  make docs-setup         - Install MkDocs Material (docs dependencies)"
	@echo ""
	@echo "Pre-commit:"
	@echo "  make pre-commit        - Run all pre-commit hooks on all files"
	@echo "  make pre-commit-hook   - Run pre-commit hooks on staged files"
	@echo ""
	@echo "Markdown checks:"
	@echo "  make lint-markdown     - Lint all markdown files"
	@echo "  make lint-markdown-fix - Lint and auto-fix markdown files"
	@echo "  make check-links       - Check all links in markdown files"
	@echo "  make check-nav         - Check indexes and prev/next chains"
	@echo "  make check-all         - Lint + nav + link checks"
	@echo ""
	@echo "Docs site:"
	@echo "  make docs-serve        - Serve MkDocs Material locally"
	@echo "  make docs-build        - Build the static site into site/"
	@echo ""
	@echo "Other:"
	@echo "  make run               - Run the URLChecker script using Streamlit"
	@echo "  make freeze            - Update requirements.txt with direct tool deps only"
	@echo "  make clean             - Remove the virtual environment"
	@echo "  make help              - Display this help message"