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

# Update requirements.txt with current dependencies
.PHONY: freeze
freeze: $(VENV_DIR)/bin/activate
	$(PIP) freeze > requirements.txt

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
	npx --yes markdownlint-cli "**/*.md" --ignore node_modules

.PHONY: lint-markdown-fix
lint-markdown-fix:
	npx --yes markdownlint-cli "**/*.md" --ignore node_modules --fix

.PHONY: check-links
check-links:
	find . -name "*.md" -not -path "./node_modules/*" -not -path "./.venv/*" -exec npx --yes markdown-link-check --config .markdown-link-check.json {} \;

.PHONY: check-all
check-all: lint-markdown check-links

# Help target to display available commands
.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make setup              - Set up the virtual environment and install dependencies"
	@echo "  make install-pre-commit - Install and set up pre-commit hooks"
	@echo ""
	@echo "Pre-commit:"
	@echo "  make pre-commit        - Run all pre-commit hooks on all files"
	@echo "  make pre-commit-hook   - Run pre-commit hooks on staged files"
	@echo ""
	@echo "Markdown checks:"
	@echo "  make lint-markdown     - Lint all markdown files"
	@echo "  make lint-markdown-fix - Lint and auto-fix markdown files"
	@echo "  make check-links       - Check all links in markdown files"
	@echo "  make check-all         - Run all markdown checks"
	@echo ""
	@echo "Other:"
	@echo "  make run               - Run the URLChecker script using Streamlit"
	@echo "  make freeze            - Update requirements.txt with current dependencies"
	@echo "  make clean             - Remove the virtual environment"
	@echo "  make help              - Display this help message"