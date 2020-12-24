# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/viterbi.py
# Compiled at: 2014-02-25 17:06:51
"""
Created on Oct 13, 2013

@author: James McInerney
"""
from numpy import *
seterr(divide='ignore')

def viterbiLog(ln_lik_obs, exp_a, exp_pi, VERBOSE=False):
    N, K = shape(ln_lik_obs)
    T1, T2 = zeros((N, K)), zeros((N, K))
    T1[0, :] = log(exp_pi) + ln_lik_obs[0, :]
    for n in range(1, N):
        for s in range(K):
            v = T1[n - 1, :] + log(exp_a[:, s]) + ln_lik_obs[(n, s)]
            T1[(n, s)] = v.max()
            T2[(n, s)] = v.argmax()

        T1[n, :] -= T1[n, :].max()
        T1[n, :] = log(exp(T1[n, :]) / exp(T1[n, :]).sum())

    S = zeros(N)
    S[N - 1] = T1[N - 1, :].argmax()
    for n in range(N - 1, 0, -1):
        S[n - 1] = T2[(n, S[n])]

    return S