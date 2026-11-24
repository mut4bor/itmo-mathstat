import matplotlib.pyplot as plt
import numpy as np
from estimates import ESTIMATORS, N, generateSamples

sampleSizes = np.arange(10, 101, 10)

# means[i, j], variances[i, j]: sample size i, estimator j
means = np.empty((len(sampleSizes), len(ESTIMATORS)))
variances = np.empty((len(sampleSizes), len(ESTIMATORS)))
for i, n in enumerate(sampleSizes):
    samples = generateSamples(n)
    for j, (_, estimate, _) in enumerate(ESTIMATORS):
        values = estimate(samples)
        means[i, j] = values.mean()
        variances[i, j] = values.var(ddof=1)

for j, (name, _, distribution) in enumerate(ESTIMATORS):
    theory = [distribution(n) for n in sampleSizes]

    fig, (axMean, axVariance) = plt.subplots(1, 2, figsize=(12, 5))
    axMean.plot(sampleSizes, means[:, j], marker=".", label=f"M[{name}], N = {N}")
    axMean.plot(
        sampleSizes,
        [d.mean() for d in theory],
        color="red",
        linestyle="--",
        label="theory",
    )
    axMean.set_xlabel("n")
    axMean.set_ylabel("M")
    axMean.set_title(f"M[{name}]")
    axMean.legend()

    axVariance.plot(
        sampleSizes, variances[:, j], marker=".", label=f"D[{name}], N = {N}"
    )
    axVariance.plot(
        sampleSizes,
        [d.var() for d in theory],
        color="red",
        linestyle="--",
        label="theory",
    )
    axVariance.set_xlabel("n")
    axVariance.set_ylabel("D")
    axVariance.set_title(f"D[{name}]")
    axVariance.legend()

    fig.suptitle(name)
    fig.tight_layout()
    plt.show()
