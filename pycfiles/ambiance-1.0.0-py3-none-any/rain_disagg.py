# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ambhas/rain_disagg.py
# Compiled at: 2012-04-24 01:18:24
__doc__ = '\nCreated on Tue May 24 18:07:28 2011\n\n@author: Sat Kumar Tomer\n@website: www.ambhas.com\n@email: satkumartomer@gmail.com\n'
from __future__ import division
import numpy as np
from ambhas.errlib import rmse
from scipy.optimize import fmin
from scipy.stats import poisson

class RainDisagg:

    def __init__(self, rf):
        self.rf = rf
        len_rf = len(rf)
        rf_1 = rf[0:len_rf - np.mod(len_rf, 32)]
        rf_2 = np.sum(rf_1.reshape(-1, 2), axis=1)
        rf_4 = np.sum(rf_2.reshape(-1, 2), axis=1)
        rf_8 = np.sum(rf_4.reshape(-1, 2), axis=1)
        rf_16 = np.sum(rf_8.reshape(-1, 2), axis=1)
        rf_32 = np.sum(rf_16.reshape(-1, 2), axis=1)
        M1 = np.zeros((6, 11))
        for i in range(11):
            M1[(0, i)] = np.mean(rf_1 ** (i / 2))
            M1[(1, i)] = np.mean(rf_2 ** (i / 2))
            M1[(2, i)] = np.mean(rf_4 ** (i / 2))
            M1[(3, i)] = np.mean(rf_8 ** (i / 2))
            M1[(4, i)] = np.mean(rf_16 ** (i / 2))
            M1[(5, i)] = np.mean(rf_32 ** (i / 2))

        self.M1 = M1
        self.logM = np.log(M1)
        l = [
         32, 16, 8, 4, 2, 1]
        self.log_lambda = np.log(l)
        tau_obs = np.zeros(10)
        for i in range(10):
            tau_obs[i] = -np.polyfit(np.log(l), np.log(M1[:, i + 1]), 1)[0]

        self.tau_obs = tau_obs
        self.lp = fmin(self.fun_poisson, np.array([0.4, 0.2]))
        self.A = np.exp(self.lp[0] * (1 - self.lp[1]))

    def tau_predict(self):
        q = np.arange(0.5, 5.5, 0.5)
        c = abs(self.lp[0])
        beta = abs(self.lp[1])
        b = 2
        tau_pred = q - c * (q * (1 - beta) + beta ** q - 1) / np.log(b)
        self.tau_pred = tau_pred
        self.q = q

    def fun_poisson(self, par):
        q = np.arange(0.5, 5.5, 0.5)
        c = abs(par[0])
        beta = abs(par[1])
        b = 2
        tau_pred = q - c * (q * (1 - beta) + beta ** q - 1) / np.log(b)
        f = rmse(tau_pred, self.tau_obs)
        return f

    def disaggregate(self, rf):
        len_rf = len(rf)
        rf_pre = np.zeros((1, len_rf * 2))
        for j in range(1):
            for i in xrange(0, len_rf * 2, 2):
                W = self.A * self.lp[1] ** poisson.rvs(1, size=2)
                W[W < 0] = 1e-06
                rf_pre[(j, i)] = rf[int(i / 2)] * W[0] / (W[0] + W[1])
                rf_pre[(j, i + 1)] = rf[int(i / 2)] * W[1] / (W[0] + W[1])

        rf_pre = np.mean(rf_pre, axis=0)
        for i in xrange(0, len_rf * 2, 2):
            if np.mod(rf_pre[i], 0.5) != 0:
                TB = np.mod(rf_pre[i], 0.5)
            else:
                TB = 0
            rf_pre[i] -= TB
            rf_pre[(i + 1)] += TB

        return rf_pre