# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\optimizer.py
# Compiled at: 2018-11-19 01:41:02
# Size of source mod 2**32: 2363 bytes
import numpy as np

def optimizer_SGD(lr, params, grads):
    for i in range(len(params)):
        params[i] -= lr * grads[i]

    return params


class SGD:

    def __init__(self, lr=0.01):
        self.lr = lr

    def update(self, params, grads):
        for i in range(len(params)):
            params[i] -= self.lr * grads[i]

        return params

    def viewlr(self):
        return self.lr

    def change_lr(self, lr):
        self.lr = lr


class AdaGrad:
    """AdaGrad"""

    def __init__(self, lr=0.01):
        self.lr = lr
        self.h = None
        self.lrs = None

    def update(self, params, grads):
        if self.h is None:
            self.h = {}
            self.lrs = {}
            for i in range(len(params)):
                self.h[i] = np.zeros_like(grads[i])
                self.lrs[i] = np.zeros_like(grads[i])

        for i in range(len(params)):
            self.h[i] += grads[i] * grads[i]
            self.lrs[i] = self.lr / np.sqrt(self.h[i] + 1e-07)
            params[i] -= self.lrs[i] * grads[i]

        return params

    def viewlr(self):
        return self.lrs

    def change_lr(self, lr):
        self.lr = lr


class NormGrad:

    def __init__(self, lr=0.01):
        self.lr = lr
        self.h = None
        self.lrs = None
        self.cont = 0
        self.grads = None

    def update(self, params, grads):
        if self.h is None:
            self.h = {}
            self.lrs = {}
            for i in range(len(params)):
                self.h[i] = abs(grads[i])
                self.lrs[i] = np.zeros_like(grads[i])

        if 0 < self.cont < 100:
            for i in range(len(params)):
                self.h[i] += abs(grads[i])
                self.lrs[i] = self.lr

        if self.cont == 100:
            for i in range(len(params)):
                self.h[i] = self.h[i] / 100
                self.lrs[i] = self.lr

        if self.cont > 100:
            for i in range(len(params)):
                self.lrs[i] = self.lr * abs(grads[i]) / self.h[i]

        for i in range(len(params)):
            params[i] -= self.lrs[i] * grads[i]

        self.grads = grads
        self.cont = self.cont + 1
        return params

    def viewlr(self):
        return self.lrs

    def change_lr(self, lr):
        self.lr = lr