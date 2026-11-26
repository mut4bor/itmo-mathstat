import numpy as np
from scipy.stats import chi2, norm

N = 10**3
mathExpect = 0
dispersion = 1

rng = np.random.default_rng(2026)


def generateSamples(n):
    return rng.normal(mathExpect, np.sqrt(dispersion), (N, n))


ESTIMATORS = [
    (
        "c*",
        lambda samples: samples.mean(axis=1),
        lambda n: norm(mathExpect, np.sqrt(dispersion / n)),
    ),
    (
        "D* = 1/n",
        lambda samples: samples.var(axis=1, ddof=0),
        lambda n: chi2(n - 1, scale=dispersion / n),
    ),
    (
        "D* = 1/(n-1)",
        lambda samples: samples.var(axis=1, ddof=1),
        lambda n: chi2(n - 1, scale=dispersion / (n - 1)),
    ),
]
