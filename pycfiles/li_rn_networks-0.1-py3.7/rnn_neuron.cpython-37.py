# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\rnn_neuron.py
# Compiled at: 2020-02-08 04:23:12
# Size of source mod 2**32: 1734 bytes
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
        self.dsr_prev = None
        self.function = function.function()
        self.function.def_parameter(self.Tau, self.dt, self.random_del)

    def def_parameter(self, Tau, dt, random_del):
        self.random_del = random_del
        self.dt = dt
        self.Tau = Tau
        self.function.def_parameter(self.Tau, self.dt, self.random_del)

    def forward(self, v, si, sr, W, Wr, b, mode='None'):
        noise = self.random_del * (random.random() - 0.5) * 10
        RI = -noise + np.dot(si, W)
        RI += np.dot(sr, Wr)
        v = self.function.eular_V(v, RI)
        s = self.function.sigmoid(v)
        if mode == 'RI':
            return (
             v, s, RI)
        return (
         v, s)