import matplotlib.pyplot as plt
import numpy as np
from sample import generateNormalPopulation, generatePopulation, generateSample
from scipy.stats import gaussian_kde, norm, uniform


def makeGraph(population, sampleSize, trueDensity, xRange, title="graph", h=None):
    sample = np.array(generateSample(population, sampleSize))
    s = np.std(sample, ddof=1)
    kde = gaussian_kde(sample, bw_method="silverman" if h is None else h / s)
    h = kde.factor * s

    x = np.linspace(*xRange, 400)

    plt.plot(x, kde(x), label=f"KDE (h = {h:.4f})")
    plt.plot(x, trueDensity(x), color="red", linestyle="--", label="f(x)")
    plt.xlabel("x")
    plt.ylabel("f*(x)")
    plt.title(title)
    plt.legend()
    plt.show()


mathExpect = 0
dispersion = 1

population = generatePopulation(0, 1, 10**6)
normalPopulation = generateNormalPopulation(mathExpect, dispersion, 10**6)

uniformDensity = uniform(0, 1).pdf
normalDensity = norm(mathExpect, np.sqrt(dispersion)).pdf

makeGraph(population, 10**1, uniformDensity, (-1, 2), f"Uniform, n = {10**1}")
makeGraph(population, 10**2, uniformDensity, (-1, 2), f"Uniform, n = {10**2}")
makeGraph(population, 10**3, uniformDensity, (-1, 2), f"Uniform, n = {10**3}")
makeGraph(population, 10**4, uniformDensity, (-1, 2), f"Uniform, n = {10**4}")

makeGraph(normalPopulation, 10**1, normalDensity, (-5, 5), f"Normal, n = {10**1}")
makeGraph(normalPopulation, 10**2, normalDensity, (-5, 5), f"Normal, n = {10**2}")
makeGraph(normalPopulation, 10**3, normalDensity, (-5, 5), f"Normal, n = {10**3}")
makeGraph(normalPopulation, 10**4, normalDensity, (-5, 5), f"Normal, n = {10**4}")
