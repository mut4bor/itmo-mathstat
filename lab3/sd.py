from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from moments import exponentialGMM, exponentialMoments, uniformGMM, uniformMoments
from sample import generateExponentialPopulation, generatePopulation, generateSample

MOMENT_COUNTS = [3, 5, 7]
OUTPUT = Path(__file__).with_suffix(".md")

markdown = ["# Среднеквадратическое отклонение оценок", ""]


def formatFloat(value):
    return np.format_float_positional(value, precision=3, fractional=False)


def getMethods(moments, gmm):
    methods = [("MoM", moments)]
    for weights, label in [("identity", "W = I"), ("optimal", "W = S^-1")]:
        methods += [
            (f"GMM, K = {K}, {label}", lambda s, K=K, w=weights: gmm(s, K, w))
            for K in MOMENT_COUNTS
        ]
    return methods


def makeGraph(
    population, sampleSizes, moments, gmm, trueParams, names, title, repeats=10**3
):
    methods = getMethods(moments, gmm)
    estimates = np.empty((len(sampleSizes), repeats, len(methods), len(names)))
    for i, n in enumerate(sampleSizes):
        for r in range(repeats):
            sample = generateSample(population, n)
            for j, (_, estimate) in enumerate(methods):
                estimates[i, r, j] = estimate(sample)
        print(f"{title}: n = {n} done")

    sd = estimates.std(axis=1, ddof=1)
    bias = estimates.mean(axis=1) - np.array(trueParams)

    fig, axes = plt.subplots(
        len(names), 1, sharex=True, figsize=(8, 5 * len(names)), squeeze=False
    )
    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    for k, (ax, name) in enumerate(zip(axes[:, 0], names)):
        for j, (methodName, _) in enumerate(methods):
            color = colors[0] if j == 0 else colors[1 + (j - 1) % len(MOMENT_COUNTS)]
            style = "--" if "W = I" in methodName else "-"
            ax.plot(sampleSizes, sd[:, j, k], style, color=color, marker=".", label=methodName)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_ylabel(f"σ({name}*)")
        ax.legend(fontsize="small")
    axes[-1, 0].set_xlabel("n")
    fig.suptitle(f"{title}, N = {repeats}")
    plt.show()

    for k, name in enumerate(names):
        markdown.append(f"## {title}, {name} = {trueParams[k]}, N = {repeats}")
        markdown.append("")
        markdown.append(
            "| n | " + " | ".join(f"σ {methodName}" for methodName, _ in methods) + " |"
        )
        markdown.append("|" + "---|" * (1 + len(methods)))
        for i, n in enumerate(sampleSizes):
            markdown.append(
                f"| {n} | " + " | ".join(formatFloat(v) for v in sd[i, :, k]) + " |"
            )
        markdown.append("")
        markdown.append(f"Смещение {name}*:")
        markdown.append("")
        markdown.append(
            "| n | " + " | ".join(f"{methodName}" for methodName, _ in methods) + " |"
        )
        markdown.append("|" + "---|" * (1 + len(methods)))
        for i, n in enumerate(sampleSizes):
            markdown.append(
                f"| {n} | " + " | ".join(formatFloat(v) for v in bias[i, :, k]) + " |"
            )
        markdown.append("")


lam = 1

population = generatePopulation(0, 1, 10**6)
exponentialPopulation = generateExponentialPopulation(lam, 10**6)
sampleSizes = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

makeGraph(
    population, sampleSizes, uniformMoments, uniformGMM, (0, 1), ("a", "b"), "Uniform"
)
makeGraph(
    exponentialPopulation, sampleSizes, exponentialMoments, exponentialGMM,
    (lam,), ("λ",), "Exponential",
)

OUTPUT.write_text("\n".join(markdown), encoding="utf-8")
print(f"Saved to {OUTPUT}")
