import math

import matplotlib.pyplot as plt
import numpy as np
from sample import generateNormalPopulation, generatePopulation, generateSample
from scipy.stats import norm, uniform


def makeHistogram(population, sampleSize, trueDensity, xRange, title="Histogram"):
    sample = sorted(generateSample(population, sampleSize))
    plt.hist(
        sample,
        bins=round(1 + 1.59 * math.log(sampleSize)),
        color="skyblue",
        edgecolor="black",
        density=True,
        label="Histogram",
    )

    x = np.linspace(*xRange, 400)
    plt.plot(x, trueDensity(x), color="red", linestyle="--", label="f(x)")

    plt.legend()
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.show()


mathExpect = 0
dispersion = 1

population = generatePopulation(0, 1, 10**6)
normalPopulation = generateNormalPopulation(mathExpect, dispersion, 10**6)

uniformDensity = uniform(0, 1).pdf
normalDensity = norm(mathExpect, np.sqrt(dispersion)).pdf

makeHistogram(population, 10**1, uniformDensity, (-0.2, 1.2), title="Histogram 1")
makeHistogram(population, 10**2, uniformDensity, (-0.2, 1.2), title="Histogram 2")
makeHistogram(population, 10**3, uniformDensity, (-0.2, 1.2), title="Histogram 3")
makeHistogram(population, 10**4, uniformDensity, (-0.2, 1.2), title="Histogram 4")

makeHistogram(normalPopulation, 10**1, normalDensity, (-4, 4), title="Histogram 1")
makeHistogram(normalPopulation, 10**2, normalDensity, (-4, 4), title="Histogram 2")
makeHistogram(normalPopulation, 10**3, normalDensity, (-4, 4), title="Histogram 3")
makeHistogram(normalPopulation, 10**4, normalDensity, (-4, 4), title="Histogram 4")
