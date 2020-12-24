# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\non_neuron.py
# Compiled at: 2020-02-18 02:19:27
# Size of source mod 2**32: 2291 bytes
import numpy as np, function, random
Tau = 10
dt = 0.01
random_del = 0.5

class neuron:

    def __init__(self):
        self.random_del = 1
        self.dt = 0.01
        self.Tau = 10
        self.V = None
        self.S = None
        self.function = function.function()
        self.function.def_parameter(self.Tau, self.dt, self.random_del)

    def def_parameter(self, Tau, dt, random_del):
        self.random_del = random_del
        self.dt = dt
        self.Tau = Tau
        self.function.def_parameter(self.Tau, self.dt, self.random_del)

    def forward(self, v, si, W, b, mode='None'):
        noise = self.random_del * (random.random() - 0.5)
        RI = -noise + np.dot(si, W) + b
        v = self.function.eular_V(v, RI)
        s = self.function.sigmoid(v)
        if mode == 'RI':
            return (
             v, s, RI)
        return (
         v, s)

    def forward_dry(self, v, si, W, b, mode='None'):
        noise = self.random_del * (random.random() - 0.5)
        RI = -noise + np.dot(si, W) + b
        v += RI
        s = self.function.sigmoid(v)
        if mode == 'RI':
            return (
             v, s, RI)
        return (
         v, s)

    def forward_it(self, v, s, W, b, input, mode='None'):
        noise = self.random_del * (random.random() - 0.5)
        RI = -noise + np.dot(s, W) + input
        v = self.function.eular_V(v, RI)
        s = self.function.sigmoid(v)
        if mode == 'RI':
            return (
             v, s, RI)
        return (
         v, s)