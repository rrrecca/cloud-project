# Python Setup Guide

## Every Day Before Working

```bash
# Activate venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Pull latest code
git pull origin <branch-you-want-to-get-updates-from>

# Install any new libraries added by teammates
pip install -r requirements.txt
```

---

## If You Install a New Library

```bash
pip install library-name
pip freeze > requirements.txt
git add requirements.txt
git commit -m "updated requirements: added library-name"
git push origin your-branch-name
```

---

## Important

- Never push the `venv` folder to GitHub
- Always activate venv before working
- Always run `pip install -r requirements.txt` after pulling
