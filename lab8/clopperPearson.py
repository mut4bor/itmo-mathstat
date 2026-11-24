import numpy as np
from scipy.stats import binom
from statsmodels.stats.proportion import proportion_confint


# Root of a monotone f on [low, high], f(low) and f(high) of opposite signs
def bisection(f, low=0.0, high=1.0, tolerance=1e-12):
    lowSign = np.sign(f(low))
    while high - low > tolerance:
        middle = (low + high) / 2
        if np.sign(f(middle)) == lowSign:
            low = middle
        else:
            high = middle
    return (low + high) / 2


# Exact Clopper-Pearson interval for p after m successes in n trials:
# lower: P(X >= m | p) = (1 - Q) / 2,  lower = 0 if m = 0
# upper: P(X <= m | p) = (1 - Q) / 2,  upper = 1 if m = n
def clopperPearson(m, n, Q=0.95):
    alpha = 1 - Q
    lower = 0.0
    if m > 0:
        lower = bisection(lambda p: binom.sf(m - 1, n, p) - alpha / 2)
    upper = 1.0
    if m < n:
        upper = bisection(lambda p: binom.cdf(m, n, p) - alpha / 2)
    return lower, upper


def statsmodelsInterval(method):
    def interval(m, n, Q=0.95):
        return proportion_confint(m, n, alpha=1 - Q, method=method)

    return interval


STATSMODELS_METHODS = [
    "beta",
    "normal",
    "agresti_coull",
    "wilson",
    "jeffreys",
    "binom_test",
]

# (name, interval(m, n, Q))
METHODS = [("exact (bisection)", clopperPearson)] + [
    (method, statsmodelsInterval(method)) for method in STATSMODELS_METHODS
]


# lower[j, m], upper[j, m]: method j, m = 0..n successes
def intervalTable(n, Q=0.95):
    table = np.array(
        [[interval(m, n, Q) for m in range(n + 1)] for _, interval in METHODS]
    )
    return table[:, :, 0], table[:, :, 1]
