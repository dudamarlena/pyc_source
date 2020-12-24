# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\rnn_layer_unit.py
# Compiled at: 2020-02-08 04:22:59
# Size of source mod 2**32: 1336 bytes
import numpy as np, rnn_neuron as nu, function
W = np.array([[0, 1], [0.917, 0]])

class rnn_layer_unit:

    def __init__(self):
        self.random_del = 1
        self.dt = 0.01
        self.Tau = 10
        self.W = None
        self.Wr = None
        self.b = None
        self.V = None
        self.S = None
        self.one_layer = nu.neuron()
        self.one_layer.def_parameter(self.Tau, self.dt, self.random_del)
        self.function = function.function()
        self.function.def_parameter(self.Tau, self.dt, self.random_del)
        self.mode = None

    def def_parameter(self, Tau, dt, random_del):
        self.random_del = random_del
        self.dt = dt
        self.Tau = Tau
        self.one_layer.def_parameter(self.Tau, self.dt, self.random_del)

    def initiate(self, v, b, w, wr, mode=None):
        self.W = w
        self.Wr = wr
        self.V = v
        self.S = self.function.sigmoid(v)
        self.b = b
        self.mode = mode

    def forward(self, si):
        self.V, self.S = self.one_layer.forward(self.V, si, self.S, self.W, self.Wr, self.b, self.mode)
        return (self.V, self.S)