# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: distributions/dbg/random.py
# Compiled at: 2017-10-28 18:53:45
from math import log, pi, sqrt, factorial
import numpy as np, numpy.random
from numpy.random.mtrand import dirichlet as sample_dirichlet
from numpy import dot, inner
from numpy.linalg import cholesky, det, inv
from numpy.random import multivariate_normal
from numpy.random import beta as sample_beta
from numpy.random import poisson as sample_poisson
from numpy.random import gamma as sample_gamma
from scipy.stats import norm, chi2, bernoulli, nbinom
from scipy.special import gammaln
from distributions.util import scores_to_probs
import logging
from distributions.vendor.stats import sample_invwishart as _sample_inverse_wishart
LOG = logging.getLogger(__name__)
assert sample_dirichlet and factorial and sample_poisson and sample_gamma

def seed(x):
    numpy.random.seed(x)
    try:
        import distributions.cRandom
        distributions.cRandom.seed(x)
    except ImportError:
        pass


def sample_discrete_log(scores):
    probs = scores_to_probs(scores)
    return sample_discrete(probs, total=1.0)


def sample_bernoulli(prob):
    return bool(bernoulli.rvs(prob))


def sample_discrete(probs, total=None):
    """
    Draws from a discrete distribution with the given (possibly unnormalized)
    probabilities for each outcome.

    Returns an int between 0 and len(probs)-1, inclusive
    """
    if total is None:
        total = float(sum(probs))
    for attempt in xrange(10):
        dart = numpy.random.rand() * total
        for i, prob in enumerate(probs):
            dart -= prob
            if dart <= 0:
                return i

    LOG.error('imprecision in sample_discrete', dict(total=total, dart=dart, probs=probs))
    raise ValueError(('\n  ').join([
     'imprecision in sample_discrete:',
     ('total = {}').format(total),
     ('dart = {}').format(dart),
     ('probs = {}').format(probs)]))
    return


def sample_normal(mu, sigmasq):
    return norm.rvs(mu, sigmasq)


def sample_chi2(nu):
    return chi2.rvs(nu)


def sample_student_t(dof, mu, Sigma):
    p = len(mu)
    x = numpy.random.chisquare(dof, 1)
    z = numpy.random.multivariate_normal(numpy.zeros(p), Sigma, (1, ))
    return (mu + z / numpy.sqrt(x))[0]


def score_student_t(x, nu, mu, sigma):
    r"""
    multivariate score_student_t

    \cite{murphy2007conjugate}, Eq. 313
    """
    p = len(mu)
    z = x - mu
    S = inner(inner(z, inv(sigma)), z)
    score = gammaln(0.5 * (nu + p)) - gammaln(0.5 * nu) - 0.5 * (p * log(nu * pi) + log(det(sigma)) + (nu + p) * log(1 + S / nu))
    return score


def sample_wishart_naive(nu, Lambda):
    """
    From the definition of the Wishart
    Runs in linear time
    """
    d = Lambda.shape[0]
    X = multivariate_normal(mean=numpy.zeros(d), cov=Lambda, size=nu)
    S = numpy.dot(X.T, X)
    return S


def sample_wishart(nu, Lambda):
    ch = cholesky(Lambda)
    d = Lambda.shape[0]
    z = numpy.zeros((d, d))
    for i in xrange(d):
        if i != 0:
            z[i, :i] = numpy.random.normal(size=(i,))
        z[(i, i)] = sqrt(numpy.random.gamma(0.5 * nu - d + 1, 2.0))

    return dot(dot(dot(ch, z), z.T), ch.T)


def sample_wishart_v2(nu, Lambda):
    """
    From Sawyer, et. al. 'Wishart Distributions and Inverse-Wishart Sampling'
    Runs in constant time
    Untested
    """
    d = Lambda.shape[0]
    ch = cholesky(Lambda)
    T = numpy.zeros((d, d))
    for i in xrange(d):
        if i != 0:
            T[i, :i] = numpy.random.normal(size=(i,))
        T[(i, i)] = sqrt(chi2.rvs(nu - i + 1))

    return dot(dot(dot(ch, T), T.T), ch.T)


def sample_inverse_wishart(nu, S):
    return _sample_inverse_wishart(S, nu)


def sample_normal_inverse_wishart(mu0, lambda0, psi0, nu0):
    D, = mu0.shape
    assert psi0.shape == (D, D)
    assert lambda0 > 0.0
    assert nu0 > D - 1
    cov = sample_inverse_wishart(nu0, psi0)
    mu = np.random.multivariate_normal(mean=mu0, cov=1.0 / lambda0 * cov)
    return (mu, cov)


def sample_partition_from_counts(items, counts):
    """
    Sample a partition of a list of items, as a lists of lists that satisfies
    the group sizes in counts.
    """
    assert sum(counts) == len(items), 'counts do not sum to item count'
    order = numpy.random.permutation(len(items))
    i = 0
    partition = []
    for k in range(len(counts)):
        partition.append([])
        for j in range(counts[k]):
            partition[(-1)].append(items[order[i]])
            i += 1

    return partition


def sample_stick(gamma, tol=0.001):
    """
    Truncated sample from a dirichlet process using stick breaking
    """
    betas = []
    Z = 0.0
    while 1 - Z > tol:
        new_beta = (1 - Z) * sample_beta(1.0, gamma)
        betas.append(new_beta)
        Z += new_beta

    return {i:b / Z for i, b in enumerate(betas)}


def sample_negative_binomial(p, r):
    return int(nbinom.rvs(r, p))