# itmo-mathstat

Labs for the ITMO mathematical statistics course. Each lab has its own folder (`lab1/`, `lab2/`, …).

## Virtual environment

The whole project uses a single venv at the repo root: `.venv/`. Every lab uses it.

### Create the venv

Run from the repo root:

**Windows (PowerShell)**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install matplotlib
```

**Windows (Git Bash)**

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install matplotlib
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib
```

### Activate the venv

From the repo root:

| Shell              | Command                         |
| ------------------ | ------------------------------- |
| PowerShell         | `.venv\Scripts\Activate.ps1`    |
| cmd                | `.venv\Scripts\activate.bat`    |
| Git Bash           | `source .venv/Scripts/activate` |
| macOS / Linux      | `source .venv/bin/activate`     |

Git Bash uses forward slashes and `Scripts/`: `.venv/bin/activate` doesn't exist on Windows, and backslash paths fail in bash.

From inside a lab folder, prefix the path with `..` (for example, `..\.venv\Scripts\Activate.ps1`).

If PowerShell blocks the script, allow local scripts for your user once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### Run scripts

With the venv active, run a script from the repo root or from inside its lab folder:

```bash
python lab1/graph.py
```

### Deactivate the venv

```bash
deactivate
```

### Install new packages

With the venv active:

```bash
pip install <package-name>
```

Every lab can use packages installed here.

## Using the venv in VS Code

Open the repo root as the workspace folder. VS Code finds the interpreter in `.venv/` on its own.

To pick it by hand:

1. Open the Command Palette (`Ctrl+Shift+P`, or `Cmd+Shift+P` on macOS).
2. Run **Python: Select Interpreter**.
3. Pick `.venv\Scripts\python.exe` on Windows or `.venv/bin/python` on macOS/Linux.
