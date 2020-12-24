# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/composable_states.py
# Compiled at: 2014-03-13 01:37:21
"""
Created on 22 Oct 2013

@author: James McInerney
"""
from numpy import *
from scipy.special.basic import digamma
from states import DiscreteStates, Mixture

class MixtureComp(Mixture):

    def __init__(self, sensors, N, L, K, hyperparams=None):
        self._L = L
        self._prevKs = zeros((L, K))
        if hyperparams is None:
            hyperparams = {'alpha_tau_pi0': ones(K), 'alpha_tau_pi1': ones(K)}
        DiscreteStates.__init__(self, sensors, N, K, hyperparams=hyperparams)
        return

    def m(self, parent_exp_z):
        L = self._L
        K = self._K
        N = self._N
        exp_z = zeros((N, L, K))
        Mixture.m()

    def randomInit(self, N, K):
        L = self._L
        self._N = N
        concs = ones((L, K))
        self._exp_z = array([ [ random.dirichlet(concs[l, :]) for l in range(L) ] for _ in range(N) ])
        self._ln_obs_lik = zeros((N, L, K))

    def _mixMPi(self, alpha_tau_pi0, alpha_tau_pi1, exp_z, K):
        L = self._L
        tau_pi0, tau_pi1 = zeros((L, K)), zeros((L, K))
        for l in range(L):
            tau_pi0[l, :], tau_pi1[l, :] = Mixture._mixMPi(alpha_tau_pi0, alpha_tau_pi1, exp_z[:, l, :], K)

        return (
         tau_pi0, tau_pi1)

    def _mixEZ(self, ln_obs_lik, exp_ln_pi, N, K):
        L = self._L
        exp_z = zeros((N, L, L))
        for l in range(L):
            exp_z[:, l, :] = Mixture._mixEZ(ln_obs_lik, exp_ln_pi[l, :], N, K)

        return exp_z

    def _ePi(self, tau_pi0, tau_pi1, K):
        L = self._L
        exp_ln_pi = zeros((L, K))
        for l in range(L):
            exp_ln_pi[l, :] = Mixture._ePi(tau_pi0, tau_pi1, K)

        return exp_ln_pi