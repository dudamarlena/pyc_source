# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\non_layer_unit.py
# Compiled at: 2020-02-18 02:18:19
# Size of source mod 2**32: 2412 bytes
import numpy as np, non_neuron as nu, function, random
W = np.array([[0, 1], [0.917, 0]])

class non_layer_unit:

    def __init__(self):
        self.random_del = 1
        self.dt = 0.01
        self.Tau = 10
        self.W = None
        self.b = None
        self.V = None
        self.S = None
        self.si = None
        self.one_layer = nu.neuron()
        self.one_layer.def_parameter(self.Tau, self.dt, self.random_del)
        self.function = function.function()
        self.function.def_parameter(self.Tau, self.dt, self.random_del)
        self.mode = None
        self.Loss = None
        self.dout = None
        self.lr = 0.01

    def set_lr(self, lr):
        self.lr = lr

    def loss(self, t):
        self.Loss = 0.5 * np.sum((self.S - t) ** 2)

    def def_parameter(self, Tau, dt, random_del):
        self.random_del = random_del
        self.dt = dt
        self.Tau = Tau
        self.one_layer.def_parameter(self.Tau, self.dt, self.random_del)

    def initiate(self, v, b, w, mode=None):
        self.W = w
        self.V = v
        self.S = self.function.sigmoid(v)
        self.b = b
        self.mode = mode

    def sgd(self, dW, db):
        self.W -= self.lr * dW
        self.b -= self.lr * db

    def forward(self, si):
        self.si = si
        self.V, self.S = self.one_layer.forward(self.V, si, self.W, self.b)
        return (
         self.V, self.S)

    def forward_dry(self, si):
        self.si = si
        self.V, self.S = self.one_layer.forward_dry(self.V, si, self.W, self.b)
        return (
         self.V, self.S)

    def backward(self, t):
        dy = self.function.sigmoid_back(self.S, self.Loss)
        dW = np.dot(self.si.T, dy)
        dx = np.dot(dy, self.W.T)
        self.sgd(dW, dy)

    def output_loss(self, t):
        self.dout = self.S - t
        return self.dout[0][0]

    def printS(self):
        print(self.S)