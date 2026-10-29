from pathlib import Path

import numpy as np
from moments import exponentialGMM, exponentialMoments, uniformGMM, uniformMoments

MOMENT_COUNTS = [3, 5, 7]
REPEATS = 10**3
OUTPUT = Path(__file__).with_suffix(".md")

rng = np.random.default_rng(2026)
lam = 1
sampleSizes = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]

# (title, draw, moments, gmm, trueParams, names)
DISTRIBUTIONS = [
    (
        "Uniform",
        lambda n: rng.uniform(0, 1, n),
        uniformMoments,
        uniformGMM,
        (0, 1),
        ("a", "b"),
    ),
    (
        "Exponential",
        lambda n: rng.exponential(1 / lam, n),
        exponentialMoments,
        exponentialGMM,
        (lam,),
        ("λ",),
    ),
]


def getMethods(moments, gmm):
    methods = [("MoM", moments)]
    for weights, label in [("identity", "W = I"), ("optimal", "W = S^-1")]:
        methods += [
            (f"GMM, K = {K}, {label}", lambda s, K=K, w=weights: gmm(s, K, w))
            for K in MOMENT_COUNTS
        ]
    return methods


# Samples are drawn directly from the distribution, not resampled from a fixed
# population, so the estimates converge to the true parameters.
# Returns sd[i, j, k]: sample size i, method j, parameter k.
def standardDeviations(draw, sampleSizes, methods, names, title):
    estimates = np.empty((len(sampleSizes), REPEATS, len(methods), len(names)))
    for i, n in enumerate(sampleSizes):
        for r in range(REPEATS):
            sample = draw(n)
            for j, (_, estimate) in enumerate(methods):
                estimates[i, r, j] = estimate(sample)
        print(f"{title}: n = {n} done")
    return estimates.std(axis=1, ddof=1)


def formatFloat(value):
    return np.format_float_positional(value, precision=3, fractional=False)


def makeTables(markdown, sd, sampleSizes, methods, trueParams, names, title):
    markdown.append(f"## {title}")
    markdown.append("")
    for k, name in enumerate(names):
        markdown.append(f"### σ({name}*), {name} = {trueParams[k]}, N = {REPEATS}")
        markdown.append("")
        markdown.append("| n | " + " | ".join(name for name, _ in methods) + " |")
        markdown.append("|" + "---|" * (1 + len(methods)))
        for n, row in zip(sampleSizes, sd[:, :, k]):
            markdown.append(
                f"| {n} | " + " | ".join(formatFloat(v) for v in row) + " |"
            )
        markdown.append("")


if __name__ == "__main__":
    markdown = ["# Standard deviation of the estimates", ""]
    for title, draw, moments, gmm, trueParams, names in DISTRIBUTIONS:
        methods = getMethods(moments, gmm)
        sd = standardDeviations(draw, sampleSizes, methods, names, title)
        makeTables(markdown, sd, sampleSizes, methods, trueParams, names, title)

    OUTPUT.write_text("\n".join(markdown), encoding="utf-8")
    print(f"Saved to {OUTPUT}")
