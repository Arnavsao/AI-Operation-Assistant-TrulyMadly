# 🍎 macOS Setup Guide

## Important: Use `python3` not `python`

On macOS, Python 3 is accessed via `python3` command, not `python`.

**Your system**: Python 3.13.7 ✅

---

## Quick Setup Commands (Copy & Paste)

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
```bash
# Copy example
cp .env.example .env

# Edit with your API keys
nano .env
# or
open -e .env
```

### 4. Test Setup
```bash
python test_setup.py
```

### 5. Run Server
```bash
uvicorn main:app --reload
```

### 6. Test with Example Client
```bash
# In another terminal
python example_client.py
```

---

## All Commands Use `python3`

Replace any `python` with `python3` in the documentation:

| Documentation Says | You Should Run |
|-------------------|----------------|
| `python test_setup.py` | `python3 test_setup.py` |
| `python example_client.py` | `python3 example_client.py` |
| `python -m venv venv` | `python3 -m venv venv` |

**OR** activate the virtual environment first, then use `python`:
```bash
source venv/bin/activate
python test_setup.py  # Works after activation!
```

---

## Ready to Start?

Run these commands now:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Test setup (after adding API keys to .env)
python test_setup.py

# 5. Run server
uvicorn main:app --reload
```

---

**Note**: Once virtual environment is activated, you can use `python` instead of `python3`!
