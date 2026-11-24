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


def decadeLimits(values):
    return 10 ** np.floor(np.log10(np.min(values))), 10 ** np.ceil(
        np.log10(np.max(values))
    )


# 1-2-5 ticks covering [low, high], e.g. 0.001, 0.002, 0.005, 0.01, ..., 1
def oneTwoFiveTicks(low, high):
    decades = range(int(np.log10(low)), int(np.log10(high)))
    return np.array([m * 10.0**d for d in decades for m in (1, 2, 5)] + [high])


# Places the 1-2-5 ticks at equal distances, interpolating log10 linearly
# between neighbouring ticks.
def equalTickScale(ax, ticks):
    logTicks = np.log10(ticks)
    index = np.arange(len(ticks))

    def forward(y):
        with np.errstate(divide="ignore", invalid="ignore"):
            return np.interp(np.log10(y), logTicks, index)

    def inverse(i):
        return 10 ** np.interp(i, index, logTicks)

    ax.set_yscale("function", functions=(forward, inverse))
    ax.set_yticks(ticks, [f"{v:g}" for v in ticks])
    ax.set_ylim(ticks[0], ticks[-1])


def makeGraph(title, tables):
    fig, axes = plt.subplots(
        1, len(tables), sharex=True, figsize=(6 * len(tables), 6), squeeze=False
    )
    for ax, (heading, n, sd) in zip(axes[0], tables):
        for methodName, values in sd.items():
            ax.plot(n, values, marker=".", label=methodName)
        ax.set_xticks(np.linspace(0, n[-1], 11))
        ax.set_xlim(0, n[-1])
        values = np.concatenate(list(sd.values()))
        equalTickScale(ax, oneTwoFiveTicks(*decadeLimits(values)))
        ax.set_box_aspect(1)
        ax.set_xlabel("n")
        ax.set_ylabel(heading.split(",")[0])
        ax.set_title(f"Standard deviation: {heading}")
        ax.grid(True, which="major", alpha=0.3)

    axes[0, 0].legend(fontsize="small")
    fig.suptitle(title)
    fig.tight_layout()
    plt.show()


for title, tables in readTables(INPUT).items():
    makeGraph(title, tables)
