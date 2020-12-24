# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\function.py
# Compiled at: 2020-02-18 02:02:10
# Size of source mod 2**32: 936 bytes
import math, numpy as np, random

class function:

    def __int__(self):
        self.Tau = 10
        self.dt = 0.01
        self.random_del = 1

    def def_parameter(self, Tau, dt, random_del):
        self.Tau = Tau
        self.dt = dt
        self.random_del = random_del

    def sigmoid(self, x):
        y = 1 / (1 + np.exp(-5 * (x - 0.5)))
        return y

    def f_V(self, x, RI):
        sum = 0
        sum = -x + RI
        return sum / self.Tau

    def eular_V(self, x, i):
        x += self.dt * self.f_V(x, i)
        return x

    def noise(self):
        noise = self.random_del * (random.random() - 0.5)
        return noise