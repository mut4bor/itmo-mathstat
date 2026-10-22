import matplotlib.pyplot as plt
import numpy as np
from moments import exponentialGMM, exponentialMoments, uniformGMM, uniformMoments
from sample import generateExponentialPopulation, generatePopulation, generateSample

MOMENT_COUNTS = [3, 5, 7]


def makeGraph(
    population, sampleSizes, moments, gmm, trueParams, names, weights, title="graph"
):
    samples = [generateSample(population, n) for n in sampleSizes]
    methods = [("MoM", moments)] + [
        (f"GMM, K = {K}", lambda s, K=K: gmm(s, K, weights)) for K in MOMENT_COUNTS
    ]

    fig, axes = plt.subplots(
        len(names), 1, sharex=True, figsize=(8, 4 * len(names)), squeeze=False
    )
    axes = axes[:, 0]
    for name, estimate in methods:
        estimates = np.array([estimate(sample) for sample in samples])
        for i, ax in enumerate(axes):
            ax.plot(sampleSizes, estimates[:, i], marker=".", label=name)

    for ax, value, name in zip(axes, trueParams, names):
        ax.axhline(y=value, color="red", linestyle="--", label=f"{name} = {value}")
        ax.set_ylabel(f"{name}*")
        ax.legend()
    axes[-1].set_xlabel("n")
    axes[-1].set_xscale("log")
    fig.suptitle(title)
    plt.show()


lam = 1

population = generatePopulation(0, 1, 10**6)
exponentialPopulation = generateExponentialPopulation(lam, 10**6)
sampleSizes = np.unique(np.logspace(1, 4, 60).astype(int))

for weights, label in [("identity", "W = I"), ("optimal", "W = S^-1")]:
    makeGraph(
        population,
        sampleSizes,
        uniformMoments,
        uniformGMM,
        (0, 1),
        ("a", "b"),
        weights,
        f"Uniform, GMM, {label}",
    )
    makeGraph(
        exponentialPopulation,
        sampleSizes,
        exponentialMoments,
        exponentialGMM,
        (lam,),
        ("λ",),
        weights,
        f"Exponential, GMM, {label}",
    )
