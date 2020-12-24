# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/dists.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 5485 bytes
from collections import defaultdict
from itertools import tee
import numpy as np, random, scipy
from scipy.stats import beta, norm

class ProbDist(dict):
    __doc__ = '\n\t\t\tTaken from norvig: http://nbviewer.jupyter.org/url/norvig.com/ipython/Probability.ipynb\n\t\t\tinput: A dict of {<event_id_or_name>: <frequency>}\n\t\t\treturn: A Probability Distribution; an {outcome: probability} mapping.\n    '

    def __init__(self, mapping=(), **kwargs):
        (self.update)(mapping, **kwargs)
        total = sum(self.values())
        for outcome in self:
            self[outcome] = self[outcome] / total
            assert self[outcome] >= 0


def init_board_gauss(N, k):
    """
    Taken from https://datasciencelab.wordpress.com/2013/12/12/clustering-with-k-means-in-python/
    """
    n = float(N) / k
    X = []
    for i in range(k):
        c = (
         random.uniform(-1, 1), random.uniform(-1, 1))
        s = random.uniform(0.05, 0.5)
        x = []
        while len(x) < n:
            a, b = np.array([np.random.normal(c[0], s), np.random.normal(c[1], s)])
            if abs(a) < 1 and abs(b) < 1:
                x.append([a, b])

        X.extend(x)

    X = np.array(X)[:N]
    return X


def measure_skew(val_array):
    return scipy.stats.skewtest(val_array)


def measure_kurtosis(val_array, **kwargs):
    return (scipy.stats.kurtosis)(val_array, **kwargs)


def erf(x):
    sign = 1 if x >= 0 else -1
    x = abs(x)
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    p = 0.3275911
    t = 1.0 / (1.0 + p * x)
    y = 1.0 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * math.exp(-x * x)
    return sign * y


def pairwise(seq):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(seq)
    next(b, None)
    return zip(a, b)


def values_dist(vals, binsize=10):
    """
    Return a simple frequency distribution of a given list
    """
    if not vals:
        vals = [
         0]
    x = np.sort(np.asarray(vals))
    mu, sigma = np.nanmean(x), np.nanstd(x)
    hist, xedges = np.histogram(x, density=False)
    pdf, cdf = (None, None)
    return (
     hist, xedges, pdf, cdf)


def uniform(min_, max_, dims):
    """Return a random number between min_ and max_ ."""
    return mdp.numx_rand.random(dims) * (max_ - min_) + min_


def circumference_distr(center, radius, n):
    """Return n random points uniformly distributed on a circumference."""
    phi = uniform(0, 2 * mdp.numx.pi, (n, 1))
    x = radius * mdp.numx.cos(phi) + center[0]
    y = radius * mdp.numx.sin(phi) + center[1]
    return mdp.numx.concatenate((x, y), axis=1)


def circle_distr(center, radius, n):
    """Return n random points uniformly distributed on a circle."""
    phi = uniform(0, 2 * mdp.numx.pi, (n, 1))
    sqrt_r = mdp.numx.sqrt(uniform(0, radius * radius, (n, 1)))
    x = sqrt_r * mdp.numx.cos(phi) + center[0]
    y = sqrt_r * mdp.numx.sin(phi) + center[1]
    return mdp.numx.concatenate((x, y), axis=1)


def rectangle_distr(center, w, h, n):
    """Return n random points uniformly distributed on a rectangle."""
    x = uniform(-w / 2.0, w / 2.0, (n, 1)) + center[0]
    y = uniform(-h / 2.0, h / 2.0, (n, 1)) + center[1]
    return mdp.numx.concatenate((x, y), axis=1)


def dirichlet_sample_approximation(base_measure, alpha, tol=0.01):
    betas = []
    pis = []
    betas.append(beta(1, alpha).rvs())
    pis.append(betas[0])
    while sum(pis) < 1.0 - tol:
        s = np.sum([np.log(1 - b) for b in betas])
        new_beta = beta(1, alpha).rvs()
        betas.append(new_beta)
        pis.append(new_beta * np.exp(s))

    pis = np.array(pis)
    thetas = np.array([base_measure() for _ in pis])
    return (pis, thetas)


def dirichlet(scale_factor, categories, sample_size=10000):
    from scipy.stats import dirichlet
    return dirichlet(alpha=(scale_factor * categories)).rvs(sample_size)


class DirichletProcessSample:
    __doc__ = '\n    Taken from http://nbviewer.jupyter.org/github/tdhopper/notes-on-dirichlet-processes/blob/master/2015-07-28-dirichlet-distribution-dirichlet-process.ipynb\n    '

    def __init__(self, base_measure, alpha):
        self.base_measure = base_measure
        self.alpha = alpha
        self.cache = []
        self.weights = []
        self.total_stick_used = 0.0

    def __call__(self):
        remaining = 1.0 - self.total_stick_used
        i = DirichletProcessSample.roll_die(self.weights + [remaining])
        if i is not None:
            if i < len(self.weights):
                return self.cache[i]
        stick_piece = beta(1, self.alpha).rvs() * remaining
        self.total_stick_used += stick_piece
        self.weights.append(stick_piece)
        new_value = self.base_measure()
        self.cache.append(new_value)
        return new_value

    @staticmethod
    def roll_die(weights):
        if weights:
            return random.choice((range(len(weights))), p=weights)
        else:
            return