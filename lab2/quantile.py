import math

import numpy as np
from sample import generateSample
from scipy.stats import gaussian_kde


def ecdfQuantile(sample, p):
    xs = np.sort(sample)
    F = np.arange(1, len(xs) + 1) / len(xs)
    return xs[np.searchsorted(F, p)]


def histogramQuantile(sample, p):
    bins = round(1 + 1.59 * math.log(len(sample)))
    heights, edges = np.histogram(sample, bins=bins, density=True)
    cdf = np.concatenate([[0], np.cumsum(heights * np.diff(edges))])
    k = np.searchsorted(cdf, p) - 1
    return edges[k] + (p - cdf[k]) / heights[k]


def kdeQuantile(sample, p):
    kde = gaussian_kde(sample, bw_method="silverman")
    h = kde.factor * np.std(sample, ddof=1)
    x = np.linspace(min(sample) - 5 * h, max(sample) + 5 * h, 2000)
    f = kde(x)
    cdf = np.concatenate([[0], np.cumsum((f[1:] + f[:-1]) / 2 * np.diff(x))])
    cdf /= cdf[-1]
    return np.interp(p, cdf, x)


def printQuantiles(population, sampleSize, trueDistribution, title):
    sample = np.array(generateSample(population, sampleSize))
    print(f"{title}, n = {sampleSize}")
    print(f"{'p':>6} {'true':>9} {'ECDF':>9} {'hist':>9} {'KDE':>9}")
    for p in [0.01, 0.05, 0.5]:
        print(
            f"{p:>6} {trueDistribution.ppf(p):>9.4f} {ecdfQuantile(sample, p):>9.4f} "
            f"{histogramQuantile(sample, p):>9.4f} {kdeQuantile(sample, p):>9.4f}"
        )
    print()
