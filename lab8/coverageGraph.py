import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pager import show  # noqa: E402

import matplotlib.pyplot as plt
import numpy as np
from clopperPearson import METHODS, clopperPearson, intervalTable

N = 10**3
Q = 0.95
sampleSizes = [10, 50, 100, 150, 200, 500]
probabilities = [0.1, 0.5, 0.9]

rng = np.random.default_rng(2026)
tables = {n: intervalTable(n, Q) for n in sampleSizes}

for p in probabilities:
    # coverage[i, j]: sample size i, method j; bounds of the interval for Q*
    coverage = np.empty((len(sampleSizes), len(METHODS)))
    bounds = np.empty((len(sampleSizes), len(METHODS), 2))
    for i, n in enumerate(sampleSizes):
        successes = rng.binomial(n, p, N)
        lower, upper = tables[n]
        covered = (lower[:, successes] <= p) & (p <= upper[:, successes])
        for j, count in enumerate(covered.sum(axis=1)):
            coverage[i, j] = count / N
            bounds[i, j] = clopperPearson(count, N, Q)

    fig, axes = plt.subplots(2, 4, sharex=True, sharey=True, figsize=(20, 9))
    for j, ((name, _), ax) in enumerate(zip(METHODS, axes.flat)):
        ax.errorbar(
            sampleSizes,
            coverage[:, j],
            yerr=[coverage[:, j] - bounds[:, j, 0], bounds[:, j, 1] - coverage[:, j]],
            marker=".",
            capsize=4,
            label=f"Q*, N = {N}",
        )
        ax.axhline(y=Q, color="red", linestyle="--", label=f"Q = {Q}")
        ax.set_xscale("log")
        ax.set_xticks(sampleSizes, [str(n) for n in sampleSizes])
        ax.xaxis.set_tick_params(labelbottom=True)
        ax.set_xlabel("n")
        ax.set_ylabel("Q*")
        ax.set_title(name)
        ax.legend()
    for ax in axes.flat[len(METHODS) :]:
        ax.set_visible(False)

    fig.suptitle(f"p = {p}")
    fig.tight_layout()
    show()
