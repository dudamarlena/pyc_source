# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/footprint_tools/stats/bayesian.py
# Compiled at: 2017-07-17 14:13:56
import numpy as np, scipy.stats

def compute_prior_weighted(fdr, w, cutoff=0.05, pseudo=0.5):
    """ Returns prior of whether a TF is bound or not """
    k = np.sum(fdr <= cutoff, axis=0)
    n = np.sum(w, axis=0)
    A = n - k + pseudo
    B = k + pseudo
    pr = A / (A + B)
    res = np.ones(fdr.shape)
    res *= pr[np.newaxis, :]
    res[w == 0] = 1
    return res


def compute_delta_prior(obs, exp, fdr, beta_prior, cutoff=0.05):
    """ Returns a point estimate of exepected cleavage depletion with a footprint per nucleotide """
    n, w = obs.shape
    mus = np.ones((n, w))
    ws = np.ones((n, w))
    for i in range(n):
        k = obs[i, :]
        n = np.max(np.vstack([exp[i, :], obs[i, :]]), axis=0)
        mu, v = scipy.stats.beta.stats(k + beta_prior[i][0], n - k + beta_prior[i][1], loc=0, scale=1, moments='mv')
        mus[i, :] = mu
        ws[i, :] = 1 / np.sqrt(v)

    ws[fdr > cutoff] = 0
    delta = np.sum(ws * mus, axis=0) / np.sum(ws, axis=0)
    delta[np.isnan(delta)] = 1
    return delta


import windowing

def log_likelihood(obs, exp, dm, delta=1, w=3):
    """ 
        :param obs:
        :param exp:
        :param dm:
        :param delta:
        :param w:

        :returns : Array of log likelihood values computed from local window
        """
    res = np.ones((obs.shape[0], obs.shape[1]), order='c')
    n = obs.shape[0]
    for i in range(n):
        res[i, :] = windowing.sum(dm[i].log_pmf_values(exp[i, :] * delta, obs[i, :]), w)

    return res


def posterior(prior, ll_on, ll_off):
    """ """
    prior_on = np.log(1 - prior)
    prior_off = np.log(prior)
    p_off = prior_off + ll_off
    p_on = prior_on + ll_on
    denom = np.logaddexp(p_on, p_off)
    return p_off - denom