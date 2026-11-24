import numpy as np
from scipy.stats import binom


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
