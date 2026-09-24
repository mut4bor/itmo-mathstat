from pathlib import Path

import numpy as np
from quantile import ecdfQuantile, histogramQuantile, kdeQuantile
from sample import generateNormalPopulation, generatePopulation, generateSample
from scipy.stats import norm, uniform

P = np.array([0.01, 0.05, 0.5])
METHODS = [("ECDF", ecdfQuantile), ("hist", histogramQuantile), ("KDE", kdeQuantile)]
OUTPUT = Path(__file__).with_suffix(".md")

markdown = ["# Дисперсия оценок квантилей", ""]


def formatFloat(value):
    return np.format_float_positional(value, precision=3, fractional=False)


def printVariances(population, sampleSize, trueDistribution, title, repeats=10**3):
    estimates = np.empty((repeats, len(METHODS), len(P)))
    for i in range(repeats):
        sample = np.array(generateSample(population, sampleSize))
        for j, (_, quantile) in enumerate(METHODS):
            estimates[i, j] = quantile(sample, P)

    trueQuantiles = trueDistribution.ppf(P)
    theory = P * (1 - P) / (sampleSize * trueDistribution.pdf(trueQuantiles) ** 2)
    variances = estimates.var(axis=0, ddof=1)
    biases = estimates.mean(axis=0) - trueQuantiles

    print(f"{title}, n = {sampleSize}, N = {repeats}")
    print(
        f"{'p':>6} {'theory':>12} "
        + " ".join(f"{'Var ' + name:>12}" for name, _ in METHODS)
        + " "
        + " ".join(f"{'bias ' + name:>10}" for name, _ in METHODS)
    )
    for k, p in enumerate(P):
        print(
            f"{p:>6} {formatFloat(theory[k]):>12} "
            + " ".join(f"{formatFloat(v):>12}" for v in variances[:, k])
            + " "
            + " ".join(f"{b:>+10.4f}" for b in biases[:, k])
        )
    print()

    markdown.append(f"## {title}, n = {sampleSize}, N = {repeats}")
    markdown.append("")
    markdown.append(
        "| p | theory | "
        + " | ".join(f"Var {name}" for name, _ in METHODS)
        + " | "
        + " | ".join(f"bias {name}" for name, _ in METHODS)
        + " |"
    )
    markdown.append("|" + "---|" * (2 + 2 * len(METHODS)))
    for k, p in enumerate(P):
        markdown.append(
            f"| {p} | {formatFloat(theory[k])} | "
            + " | ".join(f"{formatFloat(v)}" for v in variances[:, k])
            + " | "
            + " | ".join(f"{b:+.4f}" for b in biases[:, k])
            + " |"
        )
    markdown.append("")


mathExpect = 0
dispersion = 1

population = generatePopulation(0, 1, 10**6)
normalPopulation = generateNormalPopulation(mathExpect, dispersion, 10**6)

uniformDistribution = uniform(0, 1)
normalDistribution = norm(mathExpect, np.sqrt(dispersion))

printVariances(population, 10**1, uniformDistribution, "Uniform")
printVariances(population, 10**2, uniformDistribution, "Uniform")
printVariances(population, 10**3, uniformDistribution, "Uniform")
printVariances(population, 10**4, uniformDistribution, "Uniform")

printVariances(normalPopulation, 10**1, normalDistribution, "Normal")
printVariances(normalPopulation, 10**2, normalDistribution, "Normal")
printVariances(normalPopulation, 10**3, normalDistribution, "Normal")
printVariances(normalPopulation, 10**4, normalDistribution, "Normal")

OUTPUT.write_text("\n".join(markdown), encoding="utf-8")
print(f"Saved to {OUTPUT}")
