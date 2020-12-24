# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/inference.py
# Compiled at: 2014-03-13 00:26:42
"""
Created on 3 Oct 2013

@author: James McInerney
"""
from numpy import *
from matplotlib.pyplot import *
from numpy.linalg.linalg import inv, det
from scipy.special.basic import digamma
import time
from scipy.stats import vonmises
import sys
from model.util import lnNorm, log0
ROOT = '/media/8A8823BF8823A921/Dropbox/variational/'
set_printoptions(threshold=nan, suppress=1)

def infer(X, K, hyperparams=None, VERBOSE=0, Z_grnd=None):
    N, XDim = shape(X)
    if hyperparams is None:
        hyperparams = {'alpha_pi': 1.0, 'alpha_a': 1.0, 'beta0': 1e-20, 
           'v0': XDim + 1.0, 
           'm0': zeros(XDim), 
           'W0': 1.0 * eye(XDim)}
    alpha_pi = hyperparams['alpha_pi']
    alpha_a = hyperparams['alpha_a']
    beta0 = hyperparams['beta0']
    v0 = hyperparams['v0']
    m0 = hyperparams['m0']
    W0 = hyperparams['W0']
    exp_s = array([ [ random.dirichlet(ones(K)) for _ in range(K) ] for _ in range(N) ])
    if Z_grnd is None:
        exp_z = array([ random.dirichlet(ones(K)) for _ in range(N) ])
    else:
        exp_z = Z_grnd
    itr, max_itr = (0, 200)
    diff, min_diff, prev_exp_ln_a = 1, 0.001, zeros((K, K))
    while itr < max_itr and diff > min_diff:
        tau_pi0, tau_pi1 = mPi(alpha_pi, exp_z, K)
        tau_a0, tau_a1 = mA(alpha_a, exp_s, K)
        NK = exp_z.sum(axis=0)
        vk = v0 + NK + 1.0
        xd = mXd(exp_z, X)
        S = mS(exp_z, X, xd, NK)
        betak = beta0 + NK
        m = mM(K, XDim, beta0, m0, NK, xd, betak)
        W = mW(K, W0, xd, NK, m0, XDim, beta0, S)
        exp_ln_pi = ePi(tau_pi0, tau_pi1, K)
        exp_ln_a = eA(tau_a0, tau_a1, K)
        exp_diff_mu = eDiffMu(X, XDim, NK, betak, m, W, xd, vk, N, K)
        exp_invc = eInvc(W, vk, XDim, K)
        ln_alpha_exp_z = eFowardsZ(exp_ln_pi, exp_ln_a, XDim, exp_invc, exp_diff_mu, vk, betak, N, K)
        ln_beta_exp_z = eBackwardsZ(exp_ln_pi, exp_ln_a, XDim, exp_invc, exp_diff_mu, vk, betak, N, K)
        if Z_grnd is None:
            exp_z = eZ(ln_alpha_exp_z, ln_beta_exp_z, N)
        exp_s = eS(exp_ln_a, ln_alpha_exp_z, ln_beta_exp_z, (XDim, exp_invc, exp_diff_mu, vk, betak), N, K)
        itr += 1
        diff = abs(exp_ln_a - prev_exp_ln_a).sum() / float(K ** 2)
        prev_exp_ln_a = exp_ln_a.copy()
        print 'itr,diff', itr, diff
        if VERBOSE:
            print 'exp_z', exp_z.argmax(axis=1)

    print 'completed inference.'
    return (
     exp_z, m, S, expA(tau_a0, tau_a1, K))


def mPi(alpha_pi, exp_z, K):
    tau_pi0, tau_pi1 = zeros(K), zeros(K)
    for k in range(K):
        tau_pi0[k] = alpha_pi + exp_z[0, k + 1:].sum()
        tau_pi1[k] = 1.0 + exp_z[(0, k)]

    return (
     tau_pi0, tau_pi1)


def mA(alpha_a, exp_s, K):
    tau_a0, tau_a1 = zeros((K, K)), zeros((K, K))
    for i in range(K):
        for j in range(K):
            tau_a0[(i, j)] = alpha_a + exp_s[:, i, j + 1:].sum()
            tau_a1[(i, j)] = 1.0 + exp_s[:, i, j].sum()

    return (
     tau_a0, tau_a1)


def mXd(Z, X):
    N, XDim = shape(X)
    N1, K = shape(Z)
    NK = Z.sum(axis=0)
    assert N == N1
    xd = zeros((K, XDim))
    for n in range(N):
        for k in range(K):
            xd[k, :] += Z[(n, k)] * X[n, :]

    for k in range(K):
        if NK[k] > 0:
            xd[k, :] = xd[k, :] / NK[k]

    return xd


def mS(Z, X, xd, NK):
    N, K = shape(Z)
    N1, XDim = shape(X)
    assert N == N1
    S = [ zeros((XDim, XDim)) for _ in range(K) ]
    for n in range(N):
        for k in range(K):
            B0 = reshape(X[n, :] - xd[k, :], (XDim, 1))
            L = dot(B0, B0.T)
            assert shape(L) == shape(S[k]), shape(L)
            S[k] += Z[(n, k)] * L

    for k in range(K):
        if NK[k] > 0:
            S[k] = S[k] / NK[k]

    return S


def mW(K, W0, xd, NK, m0, XDim, beta0, S):
    Winv = [ None for _ in range(K) ]
    for k in range(K):
        Winv[k] = inv(W0) + NK[k] * S[k]
        Q0 = reshape(xd[k, :] - m0, (XDim, 1))
        q = dot(Q0, Q0.T)
        Winv[k] += beta0 * NK[k] / (beta0 + NK[k]) * q
        assert shape(q) == (XDim, XDim)

    W = []
    for k in range(K):
        try:
            W.append(inv(Winv[k]))
        except linalg.linalg.LinAlgError:
            raise linalg.linalg.LinAlgError()

    return W


def mM(K, XDim, beta0, m0, NK, xd, betak):
    m = zeros((K, XDim))
    for k in range(K):
        m[k, :] = (beta0 * m0 + NK[k] * xd[k, :]) / betak[k]

    return m


def eInvc(W, vk, XDim, K):
    invc = [ None for _ in range(K) ]
    for k in range(K):
        dW = det(W[k])
        if dW > 1e-30:
            ld = log(dW)
        else:
            ld = 0.0
        invc[k] = sum([ digamma((vk[k] + 1 - i) / 2.0) for i in range(XDim) ]) + XDim * log(2) + ld

    return array(invc)


def eDiffMu(X, XDim, NK, betak, m, W, xd, vk, N, K):
    Mu = zeros((N, K))
    for n in range(N):
        for k in range(K):
            A = XDim / betak[k]
            B0 = reshape(X[n, :] - m[k, :], (XDim, 1))
            B1 = dot(W[k], B0)
            l = dot(B0.T, B1)
            assert shape(l) == (1, 1), shape(l)
            Mu[(n, k)] = A + vk[k] * l

    return Mu


def ePi(tau_pi0, tau_pi1, K):
    exp_ln_pi = zeros(K)
    acc = digamma(tau_pi0) - digamma(tau_pi0 + tau_pi1)
    for k in range(K):
        exp_ln_pi[k] = digamma(tau_pi1[k]) - digamma(tau_pi0[k] + tau_pi1[k]) + acc[:k].sum()

    return exp_ln_pi


def eA(tau_a0, tau_a1, K):
    exp_ln_a = zeros((K, K))
    acc = digamma(tau_a0) - digamma(tau_a0 + tau_a1)
    for i in range(K):
        for j in range(K):
            exp_ln_a[(i, j)] = digamma(tau_a1[(i, j)]) - digamma(tau_a0[(i, j)] + tau_a1[(i, j)]) + acc[i, :j].sum()

    return exp_ln_a


def expA(tau_a0, tau_a1, K):
    exp_a = zeros((K, K))
    acc = tau_a0 / (tau_a0 + tau_a1)
    for i in range(K):
        for j in range(K):
            exp_a[(i, j)] = acc[i, :j].prod() * tau_a1[(i, j)] / (tau_a0[(i, j)] + tau_a1[(i, j)])

    return exp_a


def eZ(ln_alpha_exp_z, ln_beta_exp_z, N):
    ln_exp_z = ln_alpha_exp_z + ln_beta_exp_z
    ln_exp_z -= reshape(ln_exp_z.max(axis=1), (N, 1))
    exp_z = exp(ln_exp_z) / reshape(exp(ln_exp_z).sum(axis=1), (N, 1))
    return exp_z


def eFowardsZ(exp_ln_pi, exp_ln_a, XDim, exp_invc, exp_diff_mu, vk, betak, N, K):
    ln_alpha_exp_z = zeros((N, K)) - inf
    ln_alpha_exp_z[0, :] = exp_ln_pi + 0.5 * exp_invc - 0.5 * vk * exp_diff_mu[0, :] - XDim / (2.0 * betak)
    for n in range(1, N):
        for i in range(K):
            ln_alpha_exp_z[n, :] = logaddexp(ln_alpha_exp_z[n, :], ln_alpha_exp_z[(n - 1, i)] + exp_ln_a[i, :] + 0.5 * exp_invc - XDim / (2.0 * betak) - 0.5 * vk * exp_diff_mu[n, :])

    return ln_alpha_exp_z


def eBackwardsZ(exp_ln_pi, exp_ln_a, XDim, exp_invc, exp_diff_mu, vk, betak, N, K):
    ln_beta_exp_z = zeros((N, K)) - inf
    ln_beta_exp_z[N - 1, :] = zeros(K)
    for n in range(N - 2, -1, -1):
        for j in range(K):
            ln_beta_exp_z[n, :] = logaddexp(ln_beta_exp_z[n, :], ln_beta_exp_z[(n + 1, j)] + exp_ln_a[:, j] + 0.5 * exp_invc - XDim / (2.0 * betak) - 0.5 * vk * exp_diff_mu[(n + 1, j)])

    return ln_beta_exp_z


def eS(exp_ln_a, ln_alpha_exp_z, ln_beta_exp_z, (XDim, exp_invc, exp_diff_mu, vk, betak), N, K):
    alpha_exp_z = lnNorm(ln_alpha_exp_z, axis=1)
    beta_exp_z = lnNorm(ln_beta_exp_z, axis=1)
    ln_exp_s = zeros((N - 1, K, K))
    for n in range(N - 1):
        n1 = n + 1
        for i in range(K):
            for j in range(K):
                ln_exp_s[(n, i, j)] = exp_ln_a[(i, j)] + ln_alpha_exp_z[(n1 - 1, i)] + ln_beta_exp_z[(n1, j)] + 0.5 * exp_invc[j] - XDim / (2.0 * betak[j]) - 0.5 * vk[j] * exp_diff_mu[(n1, j)]

    exp_s = lnNorm(ln_exp_s, axis=2)
    print 'ln_exp_s[10,:,:]', ln_exp_s[10, :, :]
    print 'exp_s[10,:,:]', exp_s[10, :, :]
    exp_s10 = ln_exp_s[10, :, :].copy()
    exp_s10 -= reshape(exp_s10.max(axis=1), (K, 1))
    exp_s10 = exp(exp_s10) / reshape(exp(exp_s10).sum(axis=1), (K, 1))
    print 'normal exp_s1[10,:,:]', exp_s10
    return exp_s