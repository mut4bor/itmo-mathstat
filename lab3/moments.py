import math

import numpy as np
from scipy.linalg import solve_triangular
from scipy.optimize import least_squares


# E[X] = (a + b) / 2, D[X] = (b - a)^2 / 12  =>  a, b = m ∓ sqrt(3 * s^2)
def uniformMoments(sample):
    sample = np.asarray(sample)
    m1 = sample.mean()
    m2 = (sample**2).mean()
    halfWidth = np.sqrt(3 * (m2 - m1**2))
    return m1 - halfWidth, m1 + halfWidth


# E[X^k] = (b^(k+1) - a^(k+1)) / ((k + 1)(b - a)) = sum a^j b^(k-j) / (k + 1)
def uniformRawMoment(a, b, k):
    return sum(a**j * b ** (k - j) for j in range(k + 1)) / (k + 1)


# E[X] = 1 / lambda  =>  lambda = 1 / m
def exponentialMoments(sample):
    return (1 / np.mean(sample),)


# E[X^k] = k! / lambda^k
def exponentialRawMoment(lam, k):
    return math.factorial(k) / lam**k


# Covariance of (X, X^2, ..., X^K): Cov(X^i, X^j) = E[X^(i+j)] - E[X^i] E[X^j]
def momentCovariance(rawMoment, theta, K):
    m = np.array([rawMoment(*theta, k) for k in range(2 * K + 1)])
    orders = np.arange(1, K + 1)
    return m[orders[:, None] + orders[None, :]] - np.outer(m[orders], m[orders])


# Minimizes g^T W g, where g_k = mean(x^k) - E[X^k], k = 1..K.
# weights="identity": W = I.
# weights="optimal":  W = S^-1, S = covariance of the moment conditions at the
#                     classical estimate (two-step GMM). S is standardized to a
#                     correlation matrix R = D S D = C C^T for numerical stability,
#                     so the objective is ||C^-1 D g||^2.
def gmm(sample, K, rawMoment, start, weights="identity", bounds=(-np.inf, np.inf)):
    sample = np.asarray(sample)
    orders = np.arange(1, K + 1)
    sampleMoments = np.array([(sample**k).mean() for k in orders])

    if weights == "optimal":
        S = momentCovariance(rawMoment, start, K)
        D = 1 / np.sqrt(np.diag(S))
        C = np.linalg.cholesky(D[:, None] * S * D[None, :])
        transform = lambda g: solve_triangular(C, D * g, lower=True)
    else:
        transform = lambda g: g

    def residuals(theta):
        theory = np.array([rawMoment(*theta, k) for k in orders])
        return transform(sampleMoments - theory)

    return tuple(least_squares(residuals, start, bounds=bounds).x)


def uniformGMM(sample, K, weights="identity"):
    return gmm(sample, K, uniformRawMoment, uniformMoments(sample), weights)


def exponentialGMM(sample, K, weights="identity"):
    start = exponentialMoments(sample)
    return gmm(sample, K, exponentialRawMoment, start, weights, bounds=(0, np.inf))
