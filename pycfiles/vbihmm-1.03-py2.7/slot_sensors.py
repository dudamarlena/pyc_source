# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/slot_sensors.py
# Compiled at: 2014-03-13 01:38:31
"""
Created on 8 Oct 2013

@author: James McInerney
"""
from sensors import MVGaussianSensor, Sensor
from numpy import *

class SlottedSensor(Sensor):

    def __init__(self, NS, T, K, sensor):
        self._sensor = sensor
        self._K = K
        self._T = T
        self._NS = NS
        self._diff = 0.0

    def loglik(self):
        T = self._T
        NS = self._NS
        K = self._K
        ln_obs_uns = self._sensor.loglik()
        ln_obs_lik = zeros((NS, K))
        t = 0
        for n in range(NS):
            while t < len(T) and T[t] == n:
                ln_obs_lik[n, :] += ln_obs_uns[t, :]
                t += 1

        return ln_obs_lik

    def m(self, exp_z):
        T = self._T
        N, XDim = shape(self._sensor._X)
        NS, K = shape(exp_z)
        Z = zeros((N, K))
        t = 0
        for n in range(NS):
            while t < len(T) and T[t] == n:
                Z[t, :] = exp_z[n, :]
                t += 1

        self._sensor.m(Z)
        return Z

    def assignments(self, zs, defaultVal=0.0):
        T = self._T
        NS = self._NS
        K = self._K
        zs_slt = defaultVal + zeros(NS)
        t = 0
        for n in range(NS):
            while t < len(T) and T[t] == n:
                zs_slt[n] = zs[t]
                t += 1

        return zs_slt

    def slotted(self, vs):
        T = self._T
        NS = self._NS
        K = self._K
        vs_slt = zeros((NS, K))
        t = 0
        for n in range(NS):
            while t < len(T) and T[t] == n:
                vs_slt[n, :] = vs[t, :]
                t += 1

        return vs_slt

    def setK(self, K0):
        self._K = K0
        self._sensor.setK(K0)