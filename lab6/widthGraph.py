import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pager import show  # noqa: E402

import matplotlib.pyplot as plt
import numpy as np
from interval import DISTRIBUTIONS, studentInterval

Q = 0.95
n = 30
sampleSizes = np.arange(10, 1001, 10)
probabilities = np.arange(0.5, 1, 0.01)

for title, draw, _ in DISTRIBUTIONS:
    fig, (axSize, axQ) = plt.subplots(1, 2, figsize=(12, 5))

    widths = []
    for size in sampleSizes:
        lower, upper = studentInterval(draw(size), Q)
        widths.append(upper - lower)
    axSize.plot(sampleSizes, widths, marker=".")
    axSize.set_xlabel("n")
    axSize.set_ylabel("width")
    axSize.set_title(f"Width vs n, Q = {Q}")

    lower, upper = studentInterval(draw(n), probabilities)
    axQ.plot(probabilities, upper - lower, marker=".")
    axQ.set_xlabel("Q")
    axQ.set_ylabel("width")
    axQ.set_title(f"Width vs Q, n = {n}")

    fig.suptitle(title)
    fig.tight_layout()
    show()
