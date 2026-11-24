import matplotlib.pyplot as plt
import numpy as np
from estimates import ESTIMATORS, N, generateSamples


def makeGraph(n):
    samples = generateSamples(n)

    fig, axes = plt.subplots(1, len(ESTIMATORS), figsize=(6 * len(ESTIMATORS), 5))
    for ax, (name, estimate, distribution) in zip(axes, ESTIMATORS):
        values = np.sort(estimate(samples))
        ax.step(
            values,
            np.arange(1, N + 1) / N,
            where="post",
            label=f"F*(x), N = {N}",
        )

        x = np.linspace(values[0], values[-1], 400)
        ax.plot(x, distribution(n).cdf(x), color="red", linestyle="--", label="F(x)")
        ax.set_xlabel(name)
        ax.set_ylabel("F(x)")
        ax.set_title(name)
        ax.legend()

    fig.suptitle(f"n = {n}")
    fig.tight_layout()
    plt.show()


makeGraph(10)
makeGraph(100)
