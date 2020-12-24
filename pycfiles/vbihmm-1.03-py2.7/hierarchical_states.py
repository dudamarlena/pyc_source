# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/hierarchical_states.py
# Compiled at: 2014-03-13 02:27:32
"""
Created on 29 Oct 2013

@author: James McInereny
"""
from states import HMM, DiscreteStates
from numpy import *
from scipy.special.basic import digamma

class HHMM(HMM):

    def __init__(self, sensors, N, K, parent_hmm, hyperparams=None):
        self._parent_hmm = parent_hmm
        P = parent_hmm._K
        self._P = P
        self._prevKs = zeros(K)
        if hyperparams is None:
            hyperparams = {'alpha_tau_pi0': ones(K), 'alpha_tau_pi1': ones(K), 'alpha_tau_a0': ones((K, K, P)), 
               'alpha_tau_a1': ones((K, K, P)), 
               'c': 1e-06 * ones((K, K, P)), 
               'd': 0.001 * ones((K, K, P))}
        self._alpha_tau_a0 = hyperparams['alpha_tau_a0']
        DiscreteStates.__init__(self, sensors, N, K, hyperparams=hyperparams)
        return

    def m(self, parent_exp_z):
        HMM.m(self)

    def loglik(self):
        self.e()
        N, K, P = self._N, self._K, self._P
        loglik = zeros((N, P))
        for p in range(P):
            loglik[1:, p] = (self._exp_s[:, :, :, :].sum(axis=3) * reshape(self._exp_ln_a[:, :, p], (1, K, K))).sum(axis=1).sum(axis=1)

        return loglik

    def expA(self):
        tau_a0, tau_a1, K = self._tau_a0, self._tau_a1, self._K
        P = self._P
        exp_a = zeros((K, K, P))
        acc = zeros((K, K, P))
        for p in range(P):
            acc[:, :, p] = tau_a0[:, :, p] / (tau_a0[:, :, p] + tau_a1[:, :, p])
            for i in range(K):
                for j in range(K - 1):
                    exp_a[(i, j, p)] = acc[i, :j, p].prod() * tau_a1[(i, j, p)] / (tau_a0[(i, j, p)] + tau_a1[(i, j, p)])

                exp_a[(i, K - 1, p)] = acc[i, :K - 1, p].prod()
                assert exp_a[i, :, p].sum() - 1.0 < 0.001, 'sum=%f i=%i p=%i' % (exp_a[i, :, p].sum(), i, p)

        return exp_a

    def _mPi(self, alpha_tau_pi0, alpha_tau_pi1, exp_z, K):
        tau_pi0, tau_pi1 = zeros(K), zeros(K)
        for k in range(K):
            tau_pi0[k] += alpha_tau_pi0[k] + exp_z[0, k + 1:].sum()
            tau_pi1[k] += alpha_tau_pi1[k] + exp_z[(0, k)]

        return (
         tau_pi0, tau_pi1)

    def _mA(self, alpha_tau_a0, alpha_tau_a1, exp_s, K):
        P = self._P
        tau_a0, tau_a1 = zeros((K, K, P)), zeros((K, K, P))
        for p in range(P):
            for i in range(K):
                for j in range(K):
                    tau_a0[(i, j, p)] = alpha_tau_a0[(i, j, p)] + exp_s[:, i, j + 1:, p].sum()
                    tau_a1[(i, j, p)] = alpha_tau_a1[(i, j, p)] + exp_s[:, i, j, p].sum()

        return (
         tau_a0, tau_a1)

    def _eFowardsZ(self, exp_ln_pi, exp_ln_a, ln_obs_lik, N, K):
        parent_exp_z = self._parent_hmm._exp_z
        P = self._P
        ln_alpha_exp_z = zeros((N, K)) - inf
        ln_alpha_exp_z[0, :] = exp_ln_pi + ln_obs_lik[0, :]
        for n in range(1, N):
            for i in range(K):
                for p in range(P):
                    ln_alpha_exp_z[n, :] = logaddexp(ln_alpha_exp_z[n, :], log(parent_exp_z[(n, p)]) + ln_alpha_exp_z[(n - 1, i)] + exp_ln_a[i, :, p] + ln_obs_lik[n, :])

        return ln_alpha_exp_z

    def _eBackwardsZ(self, exp_ln_pi, exp_ln_a, ln_obs_lik, N, K):
        parent_exp_z = self._parent_hmm._exp_z
        P = self._P
        ln_beta_exp_z = zeros((N, K)) - inf
        ln_beta_exp_z[N - 1, :] = zeros(K)
        for n in range(N - 2, -1, -1):
            for j in range(K):
                for p in range(P):
                    ln_beta_exp_z[n, :] = logaddexp(ln_beta_exp_z[n, :], log(parent_exp_z[(n + 1, p)]) + ln_beta_exp_z[(n + 1, j)] + exp_ln_a[:, j, p] + ln_obs_lik[(n + 1, j)])

        return ln_beta_exp_z

    def _eA(self, tau_a0, tau_a1, K):
        P = self._P
        exp_ln_a = zeros((K, K, P))
        for p in range(P):
            acc = digamma(tau_a0[:, :, p]) - digamma(tau_a0[:, :, p] + tau_a1[:, :, p])
            for i in range(K):
                for j in range(K - 1):
                    exp_ln_a[(i, j, p)] = digamma(tau_a1[(i, j, p)]) - digamma(tau_a0[(i, j, p)] + tau_a1[(i, j, p)]) + acc[i, :j].sum()

                exp_ln_a[(i, K - 1, p)] = acc[i, :K - 1].sum()

        return exp_ln_a

    def _eS(self, exp_ln_a, ln_alpha_exp_z, ln_beta_exp_z, ln_obs_lik, N, K):
        parent_exp_z = self._parent_hmm._exp_z
        P = self._P
        ln_exp_s = zeros((N - 1, K, K, P))
        exp_s = zeros((N - 1, K, K, P))
        for p in range(P):
            for n in range(N - 1):
                for i in range(K):
                    ln_exp_s[n, i, :, p] = log(parent_exp_z[(n + 1, p)]) + ln_alpha_exp_z[(n, i)] + ln_beta_exp_z[n + 1, :] + ln_obs_lik[n + 1, :] + exp_ln_a[i, :, p]

                ln_exp_s[n, :, :, :] -= ln_exp_s[n, :, :, :].max()
                exp_s[n, :, :, :] = exp(ln_exp_s[n, :, :, :]) / exp(ln_exp_s[n, :, :, :]).sum()

        return exp_s

    def randomInit(self, N, K):
        P = self._P
        self._N = N
        DiscreteStates.randomInit(self, N, K)
        self._exp_s = zeros((N, K, K, P))
        for n in range(1, N):
            z1, z2 = reshape(self._exp_z[n - 1, :], (K, 1)), reshape(self._exp_z[n, :], (1, K))
            pz = random.dirichlet(ones(P))
            t_n = dot(z1, z2)
            self._exp_s[n, :, :, :] = array([ [ [ t_n[(k1, k2)] * pz[p] for p in range(P) ] for k2 in range(K) ] for k1 in range(K) ])

    def initComponents(self, init_zs, holdBack=0.0):
        N, K, P = self._N, self._K, self._P
        self._exp_z = zeros((N, K))
        for n in range(N):
            self._exp_z[n, :] = holdBack / float(K - 1)
            self._exp_z[(n, init_zs[n])] = 1.0 - holdBack

        self._exp_s = zeros((N, K, K, P))
        for p in range(P):
            for n in range(1, N):
                z1, z2 = reshape(self._exp_z[n - 1, :], (K, 1)), reshape(self._exp_z[n, :], (1, K))
                self._exp_s[n, :, :, p] = dot(z1, z2)