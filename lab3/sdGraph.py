from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

INPUT = Path(__file__).with_name("sd.md")


def splitRow(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


# Parses sd.md (written by sd.py) into
# {title: [(heading, sampleSizes, {methodName: sd values})]}
def readTables(path):
    distributions = {}
    lines = path.read_text(encoding="utf-8").replace("\\*", "*").splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## "):
            title = line[3:].strip()
            distributions[title] = []
        elif line.startswith("### "):
            heading = line[4:].strip()
            methods = splitRow(lines[i + 2])[1:]
            rows = []
            for row in lines[i + 4 :]:
                if not row.startswith("|"):
                    break
                rows.append([float(v) for v in splitRow(row)])
            rows = np.array(rows)
            sd = {method: rows[:, j + 1] for j, method in enumerate(methods)}
            distributions[title].append((heading, rows[:, 0], sd))
    return distributions


def methodStyle(methodName):
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    if methodName == "MoM":
        return {"color": "black", "linestyle": "-", "marker": ".", "zorder": 3}
    K = int(methodName.split("K = ")[1].split(",")[0])
    return {
        "color": colors[[3, 5, 7].index(K)],
        "linestyle": "--" if "W = I" in methodName else "-",
        "marker": ".",
        "zorder": 2,
    }


def makeGraph(title, tables):
    fig, axes = plt.subplots(
        len(tables), 1, sharex=True, figsize=(8, 4.5 * len(tables)), squeeze=False
    )
    for ax, (heading, n, sd) in zip(axes[:, 0], tables):
        for methodName, values in sd.items():
            ax.plot(n, values, label=methodName, **methodStyle(methodName))
        ax.plot(n, sd["MoM"][0] * np.sqrt(n[0] / n), ":", color="gray", label="~ 1/√n")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylabel(heading.split(",")[0])
        ax.set_title(f"Standard deviation: {heading}")
        ax.grid(True, which="both", alpha=0.3)

    axes[-1, 0].set_xlabel("n")
    axes[0, 0].legend(fontsize="small")
    fig.suptitle(title)
    fig.tight_layout()
    plt.show()


for title, tables in readTables(INPUT).items():
    makeGraph(title, tables)
