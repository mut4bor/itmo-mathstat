import numpy as np
from clopperPearson import clopperPearson
from scipy.stats import norm

N = 10**3
ALPHA = 0.05
sampleSizes = [10, 50, 100, 150, 200, 500]
mathExpect = 0
dispersion = 1

rng = np.random.default_rng(2026)

# (title, draw(size)): all with mathematical expectation 0 and dispersion 1
DISTRIBUTIONS = [
    ("Normal", lambda size: rng.normal(0, 1, size)),
    ("Uniform", lambda size: rng.uniform(-np.sqrt(3), np.sqrt(3), size)),
    ("Exponential", lambda size: rng.exponential(1, size) - 1),
]


# H0: M = mathExpect with known dispersion.
# Z = (x̄ - mathExpect) * sqrt(n / dispersion), reject H0 if |Z| > u(1 - α / 2).
# Returns True for every row of samples where H0 is rejected.
def rejectsH0(samples):
    n = samples.shape[-1]
    z = (samples.mean(axis=-1) - mathExpect) * np.sqrt(n / dispersion)
    return np.abs(z) > norm.ppf(1 - ALPHA / 2)


# Share of the N samples where H0 is rejected, and its Clopper-Pearson interval,
# for every n, when the true mathematical expectation is shifted by `shift`.
def rejectionRates(draw, shift=0):
    rates = np.empty(len(sampleSizes))
    bounds = np.empty((len(sampleSizes), 2))
    for i, n in enumerate(sampleSizes):
        rejected = rejectsH0(draw((N, n)) + shift).sum()
        rates[i] = rejected / N
        bounds[i] = clopperPearson(rejected, N, 1 - ALPHA)
    return rates, bounds


def plotRates(ax, rates, bounds, label):
    ax.errorbar(
        sampleSizes,
        rates,
        yerr=[rates - bounds[:, 0], bounds[:, 1] - rates],
        marker=".",
        capsize=4,
        label=label,
    )
    ax.set_xscale("log")
    ax.set_xticks(sampleSizes, [str(n) for n in sampleSizes])
    ax.set_xlabel("n")
