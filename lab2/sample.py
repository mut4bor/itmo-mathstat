import math
import random


def generatePopulation(min, max, size):
    return [random.uniform(min, max) for _ in range(size)]


def generateNormalPopulation(mathExpect, dispersion, size):
    return [
        random.gauss(mu=mathExpect, sigma=math.sqrt(dispersion)) for _ in range(size)
    ]


def generateSample(population, size):
    sample = []
    for _ in range(size):
        sample.append(population[random.randrange(len(population))])
    return sample
