### Activate venv (macOS/zsh)

The venv is shared across all labs and lives at the repo root (`ITMO/.venv`).

From the repo root:

```bash
source .venv/bin/activate
```

From inside a lab folder:

```bash
source ../.venv/bin/activate
```

### Run scripts

```bash
python3 script.py
```

### Deactivate venv

```bash
deactivate
```

### Using venv in VS Code

Open the `ITMO` folder as your workspace root and the interpreter at
`.venv/bin/python` is detected automatically — no setup needed.

To set it manually:

1. Open the Command Palette (`Cmd+Shift+P`)
2. Select **Python: Select Interpreter**
3. Choose the interpreter at `.venv/bin/python`

### Installing new packages

```bash
pip install <package-name>
```

Packages installed here are available to every lab.

### Recreating the venv

Run from the repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib
```
