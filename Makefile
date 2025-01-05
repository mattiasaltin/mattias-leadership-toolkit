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

# Help target to display available commands
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make setup    - Set up the virtual environment and install dependencies"
	@echo "  make run      - Run the URLChecker script using Streamlit"
	@echo "  make freeze   - Update requirements.txt with current dependencies"
	@echo "  make clean    - Remove the virtual environment"
	@echo "  make help     - Display this help message"