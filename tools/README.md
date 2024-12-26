# URL Checker

This directory contains the `URLChecker.py` script, designed to verify the accessibility and status of URLs. This tool is useful for ensuring that links within your projects are valid and responsive, and it is run using Streamlit for an interactive user interface.

## Setup

### Prerequisites

- Python 3.10 or later
- pip (for package management)
- Streamlit

### Environment Setup

1. **Install Python**:

   Ensure Python 3.10 or later is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

### Running the URL Checker

To run the `URLChecker.py` script using Streamlit, ensure your virtual environment is activated:

```bash
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

Then execute the script with Streamlit:

```bash
streamlit run URLChecker.py
```

### Development Notes

- Always activate the virtual environment before working:

  ```bash
  source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
  ```

- After installing new packages, update `requirements.txt`:

  ```bash
  pip freeze > requirements.txt
  ```

### Git Management

The repository uses a `.gitignore` file to exclude virtual environments and other unnecessary files. Virtual environments should be created locally and not committed to the repository.

`.gitignore` includes:
- `.venv/`

---

This setup ensures that the `URLChecker.py` script is easy to use and maintain, providing a consistent environment for development and execution with Streamlit. Let me know if you need further adjustments or additional information!
