import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pager import show  # noqa: E402

import matplotlib.pyplot as plt
import numpy as np
from hypothesis import DISTRIBUTIONS, N, plotRates, rejectionRates

shifts = np.round(np.arange(0.1, 1.01, 0.1), 1)

fig, axes = plt.subplots(1, len(DISTRIBUTIONS), sharey=True, figsize=(18, 6))
for ax, (title, draw) in zip(axes, DISTRIBUTIONS):
    for shift in shifts:
        rates, bounds = rejectionRates(draw, shift)
        plotRates(ax, rates, bounds, f"M = {shift}")
    ax.set_ylabel("share of rejected H0")
    ax.set_title(title)
    ax.legend(fontsize="small")

fig.suptitle(f"H0: M = 0, N = {N}")
fig.tight_layout()
show()
