import numpy as np
from scipy.stats import t as student

mathExpect = 0
dispersion = 1

rng = np.random.default_rng(2026)

# (title, draw(size), true mathematical expectation)
DISTRIBUTIONS = [
    (
        "Normal",
        lambda size: rng.normal(mathExpect, np.sqrt(dispersion), size),
        mathExpect,
    ),
    ("Uniform", lambda size: rng.uniform(-1, 1, size), 0),
]


# x̄ ∓ t((1 + Q) / 2, n - 1) * s / sqrt(n), over the last axis of samples
def studentInterval(samples, Q):
    samples = np.asarray(samples)
    n = samples.shape[-1]
    mean = samples.mean(axis=-1)
    halfWidth = (
        student.ppf((1 + np.asarray(Q)) / 2, n - 1)
        * samples.std(axis=-1, ddof=1)
        / np.sqrt(n)
    )
    return mean - halfWidth, mean + halfWidth
