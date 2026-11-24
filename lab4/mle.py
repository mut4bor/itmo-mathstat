import numpy as np


# L(a, b) = (b - a)^-n if a <= min(x) and max(x) <= b, else 0.
# L grows as b - a shrinks  =>  a* = min(x), b* = max(x)
def uniformMLE(sample):
    sample = np.asarray(sample)
    return sample.min(), sample.max()


# ln L(c, λ) = n ln(λ / 2) - λ * sum |x_i - c|
# d/dc: λ * sum sign(x_i - c) = 0     =>  c* = median(x)
# d/dλ: n / λ - sum |x_i - c| = 0     =>  λ* = n / sum |x_i - c*|
def laplaceMLE(sample):
    sample = np.asarray(sample)
    c = np.median(sample)
    return c, 1 / np.mean(np.abs(sample - c))
