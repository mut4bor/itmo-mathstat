import matplotlib.pyplot as plt
from sample import generatePopulation, generateSample


def makeHistogram(population, sampleSize, title="Histogram"):
    sample = sorted(generateSample(population, sampleSize))
    plt.hist(
        sample, bins=sampleSize // 10, color="skyblue", edgecolor="black", density=True
    )
    plt.axhline(y=1, color="red", linestyle="--", label="Uniform density")
    plt.legend()
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()


population = generatePopulation(0, 1, 10**6)

makeHistogram(population, 10**1, title="Histogram 1")
makeHistogram(population, 10**2, title="Histogram 2")
makeHistogram(population, 10**3, title="Histogram 3")
makeHistogram(population, 10**4, title="Histogram 4")
