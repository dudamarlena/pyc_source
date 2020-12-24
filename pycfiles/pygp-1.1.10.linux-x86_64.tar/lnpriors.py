# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pygp/priors/lnpriors.py
# Compiled at: 2013-04-10 06:45:39
"""
Hyperpriors for log likelihood calculation
------------------------------------------
This module contains a set of commonly used priors for GP models.
Note some priors are available in a log transformed space and non-transformed space
"""
import scipy as SP, numpy as NP, pdb, scipy.special as SPs, itertools

def lnFobgp(x, params):
    """Fobenius norm prior on latent space:
    x: factors [N x Q]
    params: scaling parameter 
    params[0]: prior cost
    Note: this prior only works if the paramter is constraint to be strictly positive
    """
    lng = NP.zeros_like(x)
    dlng = NP.zeros_like(x)
    for i, j in itertools.combinations(xrange(x.shape[1]), 2):
        norm_x_i = NP.sqrt(NP.dot(x[:, i:i + 1].T, x[:, i:i + 1]))
        norm_x_j = NP.sqrt(NP.dot(x[:, j:j + 1].T, x[:, j:j + 1]))
        vect_dot = NP.dot(x[:, i:i + 1].T, x[:, j:j + 1])[(0, 0)]
        inner = NP.sqrt(vect_dot ** 2)
        lng[(0, 0)] += inner / (norm_x_i * norm_x_j)
        dlng[:, i:i + 1] += 1.0 / inner * vect_dot * x[:, j:j + 1] / (norm_x_i * norm_x_j) - inner / (norm_x_i * norm_x_j) ** 2 * x[:, i:i + 1] * norm_x_j / norm_x_i
        dlng[:, j:j + 1] += 1.0 / inner * vect_dot * x[:, i:i + 1] / (norm_x_i * norm_x_j) - inner / (norm_x_i * norm_x_j) ** 2 * x[:, j:j + 1] * norm_x_i / norm_x_j

    lng = lng * params[0]
    dlng = dlng * params[0]
    return [
     lng, dlng]


def lnL1(x, params):
    """L1 type prior defined on the non-log weights
    params[0]: prior cost
    Note: this prior only works if the paramter is constraint to be strictly positive
    """
    l = SP.double(params[0])
    x_ = 1.0 / x
    lng = -l * x_
    dlng = +l * x_ ** 2
    return [lng, dlng]


def lnGamma(x, params):
    """
    Returns the ``log gamma (x,k,t)`` distribution and its derivation with::
    
        lngamma     = (k-1)*log(x) - x/t -gammaln(k) - k*log(t)
        dlngamma    = (k-1)/x - 1/t
    
    
    **Parameters:**
    
    x : [double]
        the interval in which the distribution shall be computed.
    
    params : [k, t]
        the distribution parameters k and t.
    
    """
    k = SP.double(params[0])
    t = SP.double(params[1])
    lng = (k - 1) * SP.log(x) - x / t - SPs.gammaln(k) - k * SP.log(t)
    dlng = (k - 1) / x - 1 / t
    return [lng, dlng]


def lnGammaExp(x, params):
    """
    
    Returns the ``log gamma (exp(x),k,t)`` distribution and its derivation with::
    
        lngamma     = (k-1)*log(x) - x/t -gammaln(k) - k*log(t)
        dlngamma    = (k-1)/x - 1/t
   
    
    **Parameters:**
    
    x : [double]
        the interval in which the distribution shall be computed.
    
    params : [k, t]
        the distribution parameters k and t.
    
    """
    ex = SP.exp(x)
    rv = lnGamma(ex, params)
    rv[1] *= ex
    return rv


def lnGauss(x, params):
    """
    Returns the ``log normal distribution`` and its derivation in interval x,
    given mean mu and variance sigma::

        [N(params), d/dx N(params)] = N(mu,sigma|x).

    **Note**: Give mu and sigma as mean and variance, the result will be logarithmic!

    **Parameters:**

    x : [double]
        the interval in which the distribution shall be computed.

    params : [k, t]
        the distribution parameters k and t.
        
    """
    mu = SP.double(params[0])
    sigma = SP.double(params[1])
    halfLog2Pi = 0.9189385332046727
    N = SP.log(SP.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / sigma) - halfLog2Pi
    dN = -(x - mu) / sigma ** 2
    return [N, dN]


def lnuniformpdf(x, params):
    """
    Implementation of ``lnzeropdf`` for development purpose only. This
    pdf returns always ``[0,0]``.  
    """
    return [
     0, 0]


def _plotPrior(X, prior):
    import pylab as PL
    Y = SP.array(prior[0](X, prior[1]))
    PL.hold(True)
    PL.plot(X, SP.exp(Y[0, :]))
    PL.show()


if __name__ == '__main__':
    prior = [
     lnGammaExp, [4, 2]]
    X = SP.arange(0.01, 10, 0.1)
    _plotPrior(X, prior)