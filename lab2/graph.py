import matplotlib.pyplot as plt
from sample import generatePopulation, generateSample


def makeGraph(population, sampleSize, title="graph"):
    x = [0]
    y = [0]

    sample = sorted(generateSample(population, sampleSize))

    for index, value in enumerate(sample):
        x.append(value)
        y.append((index + 1) / sampleSize)

    x.append(1)
    y.append(1)

    plt.step(x, y, where="post")
    plt.plot([0, 1], [0, 1], color="red", linestyle="--")
    plt.xlabel("x(n)")
    plt.ylabel("Fr*(x)")
    plt.title(title)
    plt.show()


population = generatePopulation(0, 1, 10**6)

makeGraph(population, 10**1, "Graph 1")
makeGraph(population, 10**2, "Graph 2")
makeGraph(population, 10**3, "Graph 3")
makeGraph(population, 10**4, "Graph 4")
