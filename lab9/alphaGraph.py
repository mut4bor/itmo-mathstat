import matplotlib.pyplot as plt
from hypothesis import ALPHA, DISTRIBUTIONS, N, plotRates, rejectionRates

fig, axes = plt.subplots(1, len(DISTRIBUTIONS), sharey=True, figsize=(18, 5))
for ax, (title, draw) in zip(axes, DISTRIBUTIONS):
    rates, bounds = rejectionRates(draw)
    plotRates(ax, rates, bounds, f"α*, N = {N}")
    ax.axhline(y=ALPHA, color="red", linestyle="--", label=f"α = {ALPHA}")
    ax.set_ylabel("α*")
    ax.set_title(title)
    ax.legend()

fig.suptitle("H0: M = 0, true M = 0")
fig.tight_layout()
plt.show()
