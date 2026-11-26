import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pager import show  # noqa: E402

import matplotlib.pyplot as plt
import numpy as np
from clopperPearson import METHODS, clopperPearson, intervalTable

Q = 0.95
n = 100

lower, upper = intervalTable(n, Q)
m = np.arange(n + 1)

for (name, interval), width in zip(METHODS, upper - lower):
    if interval is clopperPearson:
        plt.plot(m, width, color="black", linestyle="--", zorder=3, label=name)
    else:
        plt.plot(m, width, marker=".", label=name)
plt.xlabel("m")
plt.ylabel("width")
plt.title(f"Interval width, n = {n}, Q = {Q}")
plt.legend()
show()
