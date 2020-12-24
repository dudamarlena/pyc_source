# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/states_backup.py
# Compiled at: 2014-03-13 01:38:40
"""
Created on Oct 17, 2013

@author: James McInerney
"""
from sensors import Sensor, DiscreteSensor
from numpy import *
from scipy.special.basic import digamma
from viterbi import viterbiLog
import itertools as itt, pickle

class DiscreteStates(DiscreteSensor):

    def __init__(self, sensors, N, K, hyperparams=None):
        self._sensors = sensors
        self.randomInit(N, K)
        self._init_exp_z = self._exp_z.copy()
        self._prevKs = zeros(K)
        self._ln_obs_lik = zeros((N, K))
        DiscreteSensor.__init__(self, zeros((N, K)), K, hyp=hyperparams)

    def e(self):
        raise Exception('not implemented')

    def expPi(self):
        tau_pi0, tau_pi1, K = self._tau_pi0, self._tau_pi1, self._K
        exp_pi = zeros((1, K))
        acc = tau_pi0 / (tau_pi0 + tau_pi1)
        for k in range(K):
            exp_pi[(0, k)] = acc[:k].prod() * tau_pi1[k] / (tau_pi0[k] + tau_pi1[k])

        return exp_pi

    def expZ(self):
        return self._exp_z

    def ln_obs_lik(self):
        return self._ln_obs_lik

    def sigComponents(self, thres=1.0):
        totalKs = self._prevKs + self._exp_z.sum(axis=0)
        ks, = where(totalKs > thres)
        return (self._K, ks)

    def randomInit(self, N, K):
        self._N = N
        concs = ones(K)
        self._exp_z = array([ random.dirichlet(concs) for _ in range(N) ])
        self._ln_obs_lik = zeros((N, K))

    def extendN(self, N0):
        assert N0 > self._N
        N = self._N
        exp_z1 = zeros((N0, self._K))
        exp_z1[:N, :] = self._exp_z
        exp_z1[N:, :] = array([ random.dirichlet(ones(self._K)) for _ in range(N0 - N) ])
        self._exp_z = exp_z1
        self._N = N0

    def estimateTransitions(self):
        exp_z = self._exp_z
        N, K = shape(exp_z)
        exp_s = zeros((N - 1, K, K))
        for n in range(N - 1):
            v1, v2 = reshape(exp_z[n - 1, :], (1, K)), reshape(exp_z[n, :], (K, 1))
            exp_s[n, :, :] = dot(v1, v2)

        return exp_s

    def _ePi(self, tau_pi0, tau_pi1, K):
        exp_ln_pi = zeros(K)
        acc = digamma(tau_pi0) - digamma(tau_pi0 + tau_pi1)
        for k in range(K):
            exp_ln_pi[k] = digamma(tau_pi1[k]) - digamma(tau_pi0[k] + tau_pi1[k]) + acc[:k].sum()

        return exp_ln_pi


class Mixture(DiscreteStates):

    def __init__(self, sensors, N, K, hyperparams=None):
        self._prevKs = zeros(K)
        self.randomInit(N, K)
        if hyperparams is None:
            hyperparams = {'alpha_tau_pi0': ones(K), 'alpha_tau_pi1': ones(K)}
        DiscreteStates.__init__(self, sensors, N, K, hyperparams=hyperparams)
        return

    def loglik(self):
        pass

    def m(self):
        alpha_tau_pi0, alpha_tau_pi1 = self._hyperparams['alpha_tau_pi0'], self._hyperparams['alpha_tau_pi1']
        exp_z = self._exp_z
        self._tau_pi0, self._tau_pi1 = self._mixMPi(alpha_tau_pi0, alpha_tau_pi1, exp_z, self._K)
        [ s.m(exp_z) for s in self._sensors ]

    def e(self):
        ln_obs_lik = array([ s.loglik() for s in self._sensors ]).sum(axis=0)
        self._ln_obs_lik = ln_obs_lik
        N, K = shape(ln_obs_lik)
        exp_ln_pi = self._ePi(self._tau_pi0, self._tau_pi1, self._K)
        self._exp_z = self._mixEZ(ln_obs_lik, exp_ln_pi, N, K)

    def updateOnline(self, coeff=1.0):
        alpha_tau_pi0, alpha_tau_pi1 = self._hyperparams['alpha_tau_pi0'], self._hyperparams['alpha_tau_pi1']
        hyp = {'alpha_tau_pi0': alpha_tau_pi0 + coeff * (self._tau_pi0 - alpha_tau_pi0), 'alpha_tau_pi1': alpha_tau_pi1 + coeff * (self._tau_pi1 - alpha_tau_pi1)}
        self._hyperparams = hyp
        self._prevKs += coeff * self._exp_z.sum(axis=0)
        DiscreteStates.updateOnline(self)

    def save(self, filepath):
        save(filepath + '_exp_z', self._exp_z)
        save(filepath + '_tau_pi0', self._tau_pi0)
        save(filepath + '_tau_pi1', self._tau_pi1)
        pickle.dump(self._hyperparams, open(filepath + '_hyp.pck', 'w'))

    def load(self, filepath):
        self._exp_z = load(filepath + '_exp_z.npy')
        self._tau_pi0 = load(filepath + '_tau_pi0.npy')
        self._tau_pi1 = load(filepath + '_tau_pi1.npy')
        self._hyperparams = pickle.load(open(filepath + '_hyp.pck', 'r'))

    def _mixMPi(self, alpha_tau_pi0, alpha_tau_pi1, exp_z, K):
        tau_pi0, tau_pi1 = zeros(K), zeros(K)
        for k in range(K):
            tau_pi0[k] = alpha_tau_pi0[k] + exp_z[:, k + 1:].sum()
            tau_pi1[k] = alpha_tau_pi1[k] + exp_z[:, k].sum()

        return (
         tau_pi0, tau_pi1)

    def _mixEZ(self, ln_obs_lik, exp_ln_pi, N, K):
        ln_exp_z = zeros((N, K))
        for k in range(K):
            ln_exp_z[:, k]
            exp_ln_pi[k]
            ln_obs_lik[:, k]
            ln_exp_z[:, k] = exp_ln_pi[k] + ln_obs_lik[:, k]

        ln_exp_z -= reshape(ln_exp_z.max(axis=1), (N, 1))
        exp_z = exp(ln_exp_z) / reshape(exp(ln_exp_z).sum(axis=1), (N, 1))
        return exp_z


class HMM(DiscreteStates):

    def __init__(self, sensors, N, K, hyperparams=None):
        self._prevKs = zeros(K)
        self.randomInit(N, K)
        if hyperparams is None:
            hyperparams = {'alpha_tau_pi0': ones(K), 'alpha_tau_pi1': ones(K), 'alpha_tau_a0': ones((K, K)), 
               'alpha_tau_a1': ones((K, K))}
        DiscreteStates.__init__(self, sensors, N, K, hyperparams=hyperparams)
        return

    def loglik(self):
        pass

    def m(self, parent_exp_z=None):
        alpha_tau_pi0, alpha_tau_pi1 = self._hyperparams['alpha_tau_pi0'], self._hyperparams['alpha_tau_pi1']
        alpha_tau_a0, alpha_tau_a1 = self._hyperparams['alpha_tau_a0'], self._hyperparams['alpha_tau_a1']
        exp_z, exp_s = self._exp_z, self._exp_s
        self._tau_pi0, self._tau_pi1 = self._mPi(alpha_tau_pi0, alpha_tau_pi1, exp_z, parent_exp_z, self._K)
        self._tau_a0, self._tau_a1 = self._mA(alpha_tau_a0, alpha_tau_a1, exp_s, self._K)
        [ s.m(exp_z) for s in self._sensors ]

    def e(self):
        ln_obs_lik = array([ s.loglik() for s in self._sensors ]).sum(axis=0)
        self._ln_obs_lik = ln_obs_lik
        N, K = shape(ln_obs_lik)
        exp_ln_pi = self._ePi(self._tau_pi0, self._tau_pi1, self._K)
        exp_ln_a = self._eA(self._tau_a0, self._tau_a1, K)
        ln_alpha_exp_z = self._eFowardsZ(exp_ln_pi, exp_ln_a, ln_obs_lik, N, K)
        ln_beta_exp_z = self._eBackwardsZ(exp_ln_pi, exp_ln_a, ln_obs_lik, N, K)
        self._exp_z = self._eZ(ln_alpha_exp_z, ln_beta_exp_z, N)
        self._exp_s = self._eS(exp_ln_a, ln_alpha_exp_z, ln_beta_exp_z, ln_obs_lik, N, K)

    def viterbi(self):
        return viterbiLog(self._ln_obs_lik, self.expA(), self.expPi())

    def expA(self):
        tau_a0, tau_a1, K = self._tau_a0, self._tau_a1, self._K
        exp_a = zeros((K, K))
        acc = tau_a0 / (tau_a0 + tau_a1)
        for i in range(K):
            for j in range(K):
                exp_a[(i, j)] = acc[i, :j].prod() * tau_a1[(i, j)] / (tau_a0[(i, j)] + tau_a1[(i, j)])

        return exp_a

    def updateOnline(self):
        hyp = {'alpha_tau_pi0': self._tau_pi0, 'alpha_tau_pi1': self._tau_pi1, 
           'alpha_tau_a0': self._tau_a0, 
           'alpha_tau_a1': self._tau_a1}
        self._hyperparams = hyp
        DiscreteStates.updateOnline(self)

    def randomInit(self, N, K):
        self._N = N
        DiscreteStates.randomInit(self, N, K)
        self._exp_s = zeros((N, K, K))
        for n in range(1, N):
            z1, z2 = reshape(self._exp_z[n - 1, :], (K, 1)), reshape(self._exp_z[n, :], (1, K))
            self._exp_s[n, :, :] = dot(z1, z2)

    def extendN(self, N0, assignLeast=3):
        assert N0 > self._N
        N, K = self._N, self._K
        exp_z1 = zeros((N0, self._K))
        exp_z1[:N, :] = self._init_exp_z
        exp_z1 = array([ random.dirichlet(ones(K)) for _ in range(N0) ])
        self._exp_z = exp_z1
        self._init_exp_z = exp_z1.copy()
        exp_s1 = zeros((N0 - 1, K, K))
        exp_s1[:N - 1, :, :] = self._exp_s
        for n in range(1, N0 - 1):
            z1, z2 = reshape(exp_z1[n - 1, :], (K, 1)), reshape(exp_z1[n, :], (1, K))
            exp_s1[n, :, :] = dot(z1, z2)

        self._exp_s = exp_s1
        self._N = N0

    def save(self, filepath):
        save(filepath + '_exp_z', self._exp_z)
        save(filepath + '_exp_s', self._exp_s)
        save(filepath + '_tau_pi0', self._tau_pi0)
        save(filepath + '_tau_pi1', self._tau_pi1)
        save(filepath + '_tau_a0', self._tau_a0)
        save(filepath + '_tau_a1', self._tau_a1)
        pickle.dump(self._hyperparams, open(filepath + '_hyp.pck', 'w'))

    def load(self, filepath):
        self._exp_z = load(filepath + '_exp_z.npy')
        self._exp_s = load(filepath + '_exp_s.npy')
        self._tau_pi0 = load(filepath + '_tau_pi0.npy')
        self._tau_pi1 = load(filepath + '_tau_pi1.npy')
        self._tau_a0 = load(filepath + '_tau_a0.npy')
        self._tau_a1 = load(filepath + '_tau_a1.npy')
        self._hyperparams = pickle.load(open(filepath + '_hyp.pck', 'r'))

    def _mPi(self, alpha_tau_pi0, alpha_tau_pi1, exp_z, parent_exp_z, K):
        tau_pi0, tau_pi1 = zeros(K), zeros(K)
        for k in range(K):
            tau_pi0[k] = alpha_tau_pi0[k] + exp_z[0, k + 1:].sum()
            tau_pi1[k] = alpha_tau_pi1[k] + exp_z[(0, k)]

        return (
         tau_pi0, tau_pi1)

    def _mA(self, alpha_tau_a0, alpha_tau_a1, exp_s, K):
        tau_a0, tau_a1 = zeros((K, K)), zeros((K, K))
        for i in range(K):
            for j in range(K):
                tau_a0[(i, j)] = alpha_tau_a0[(i, j)] + exp_s[:, i, j + 1:].sum()
                tau_a1[(i, j)] = alpha_tau_a1[(i, j)] + exp_s[:, i, j].sum()

        return (
         tau_a0, tau_a1)

    def _eA(self, tau_a0, tau_a1, K):
        exp_ln_a = zeros((K, K))
        acc = digamma(tau_a0) - digamma(tau_a0 + tau_a1)
        for i in range(K):
            for j in range(K):
                exp_ln_a[(i, j)] = digamma(tau_a1[(i, j)]) - digamma(tau_a0[(i, j)] + tau_a1[(i, j)]) + acc[i, :j].sum()

        return exp_ln_a

    def _eZ(self, ln_alpha_exp_z, ln_beta_exp_z, N):
        ln_exp_z = ln_alpha_exp_z + ln_beta_exp_z
        ln_exp_z -= reshape(ln_exp_z.max(axis=1), (N, 1))
        exp_z = exp(ln_exp_z) / reshape(exp(ln_exp_z).sum(axis=1), (N, 1))
        return exp_z

    def _eFowardsZ(self, exp_ln_pi, exp_ln_a, ln_obs_lik, N, K):
        ln_alpha_exp_z = zeros((N, K)) - inf
        ln_alpha_exp_z[0, :] = exp_ln_pi + ln_obs_lik[0, :]
        for n in range(1, N):
            for i in range(K):
                ln_alpha_exp_z[n, :] = logaddexp(ln_alpha_exp_z[n, :], ln_alpha_exp_z[(n - 1, i)] + exp_ln_a[i, :] + ln_obs_lik[n, :])

        return ln_alpha_exp_z

    def _eBackwardsZ(self, exp_ln_pi, exp_ln_a, ln_obs_lik, N, K):
        ln_beta_exp_z = zeros((N, K)) - inf
        ln_beta_exp_z[N - 1, :] = zeros(K)
        for n in range(N - 2, -1, -1):
            for j in range(K):
                ln_beta_exp_z[n, :] = logaddexp(ln_beta_exp_z[n, :], ln_beta_exp_z[(n + 1, j)] + exp_ln_a[:, j] + ln_obs_lik[(n + 1, j)])

        return ln_beta_exp_z

    def _eS(self, exp_ln_a, ln_alpha_exp_z, ln_beta_exp_z, ln_obs_lik, N, K):
        ln_exp_s = zeros((N - 1, K, K))
        exp_s = zeros((N - 1, K, K))
        for n in range(N - 1):
            for i in range(K):
                ln_exp_s[n, i, :] = ln_alpha_exp_z[(n, i)] + ln_beta_exp_z[n + 1, :] + ln_obs_lik[n + 1, :] + exp_ln_a[i, :]

            ln_exp_s[n, :, :] -= ln_exp_s[n, :, :].max()
            exp_s[n, :, :] = exp(ln_exp_s[n, :, :]) / exp(ln_exp_s[n, :, :]).sum()

        return exp_s