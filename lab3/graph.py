import matplotlib.pyplot as plt
import numpy as np
from moments import exponentialMoments, uniformMoments
from sample import generateExponentialPopulation, generatePopulation, generateSample


def makeGraph(population, sampleSizes, estimate, trueParams, names, title="graph"):
    estimates = np.array([estimate(generateSample(population, n)) for n in sampleSizes])

    for i, (value, name) in enumerate(zip(trueParams, names)):
        line = plt.plot(sampleSizes, estimates[:, i], marker=".", label=f"{name}*")
        plt.axhline(
            y=value, color=line[0].get_color(), linestyle="--", label=f"{name} = {value}"
        )
    plt.xscale("log")
    plt.xlabel("n")
    plt.ylabel("Estimate")
    plt.title(title)
    plt.legend()
    plt.show()


lam = 1

population = generatePopulation(0, 1, 10**6)
exponentialPopulation = generateExponentialPopulation(lam, 10**6)
sampleSizes = np.unique(np.logspace(1, 4, 60).astype(int))

makeGraph(
    population, sampleSizes, uniformMoments, (0, 1), ("a", "b"),
    "Uniform, method of moments",
)
makeGraph(
    exponentialPopulation, sampleSizes, exponentialMoments, (lam,), ("λ",),
    "Exponential, method of moments",
)
