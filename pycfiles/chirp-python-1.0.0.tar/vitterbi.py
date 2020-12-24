# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\chirp\pitch\vitterbi.py
# Compiled at: 2013-12-11 23:17:46
__doc__ = '\nreverse vitterbi filter finds MAP path through particle filter output\n\nCopyright (C) 2011 Dan Meliza <dan // meliza.org>\nCreated 2011-08-02\n'
import numpy as nx, _vitterbi

def filter(particles, loglikelihood, proposal, rwalk_scale=0.01, min_loglike=-100, **kwargs):
    """
    Run the Vitterbi reverse filter. This is an O(N^2t) operation that
    finds the MAP path through the posterior density.

    particles: the values of the particles at each time point,
               N particles by K time points
    likelihood: the loglikelihood associated with all valid values, L by K
    proposal:   P(x_i|x_{i-1}), P by K-1
    """
    logprop = nx.log(nx.maximum(proposal, nx.exp(min_loglike)))
    P = logprop.shape[0]
    idx = nx.arange(-P / 2, P / 2)
    lognorm = -0.5 * (nx.log(2 * nx.pi * rwalk_scale ** 2) + (idx.astype('d') / rwalk_scale) ** 2)
    return _vitterbi.filter(particles, loglikelihood, logprop, lognorm, min_loglike)