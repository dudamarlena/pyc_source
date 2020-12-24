# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/vb_ihmm/model/common_sensors.py
# Compiled at: 2014-03-13 01:37:07
"""
Created on Nov 6, 2013

@author: James McInerney
"""
from numpy import *
from sensors import Sensor, MVGaussianSensor
from accuracy_sensors import ReportedGaussian
from numpy.linalg.linalg import inv
from util import inv0, inv00

class CommonMeanSensor(Sensor):

    def __init__(self, sensors, sensorTypes, hyperparams, setM=None):
        self._sensors = sensors
        m0 = hyperparams['m0']
        g0 = hyperparams['g0']
        self._hyperparams = {'m0': m0, 'g0': g0}
        self._sensorTypes = sensorTypes
        self._setM = setM

    def loglik(self):
        return array([ s.loglik() for s in self._sensors ]).sum(axis=0)

    def m(self, exp_z_slotted):
        Zs = [ s.m(exp_z_slotted) for s in self._sensors ]
        m0, g0 = self._hyperparams['m0'], self._hyperparams['g0']
        NS, K = shape(exp_z_slotted)
        XDim = 2
        numer, denom_inv = [ zeros(2) for _ in range(K) ], [ zeros((2, 2)) for _ in range(K) ]
        for s1, t, exp_z in zip(self._sensors, self._sensorTypes, Zs):
            s = s1._sensor
            X = s.X()
            Nk = exp_z.sum(axis=0)
            N, XDim = shape(X)
            N1, K = shape(exp_z)
            assert N == N1, 'N=%i, N1=%i' % (N, N1)
            if t == 'unreported':
                C = s.expC()
                for k in range(K):
                    Pk = inv(C[k, :, :])
                    denom_inv[k] += Nk[k] * Pk
                    for n in range(N):
                        x_n = reshape(X[n, :], (XDim, 1))
                        numer[k] += exp_z[(n, k)] * dot(Pk, x_n).flatten()

            elif t == 'reported':
                Cn = s.expC()
                for k in range(K):
                    for n in range(N):
                        Pn = inv(Cn[n])
                        x_n = reshape(X[n, :], (XDim, 1))
                        numer[k] += exp_z[(n, k)] * dot(Pn, x_n).flatten()
                        denom_inv[k] += exp_z[(n, k)] * Pn

            else:
                raise Exception('Unknown sensor type ' + t)

        m = zeros((K, XDim))
        for k in range(K):
            m[k, :] = dot(inv00(denom_inv[k]), numer[k])

        if self._setM is not None:
            m[K - 1, :] = self._setM
        for s1 in self._sensors:
            s = s1._sensor
            s._m = m

        return

    def diff(self):
        return array([ s.diff() for s in self._sensors ]).sum()

    def means(self):
        return self._sensors[0]._sensor._m