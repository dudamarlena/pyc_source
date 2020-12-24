# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\li_rn_networks\rnnclass.py
# Compiled at: 2019-05-07 23:21:38
# Size of source mod 2**32: 6158 bytes
from optimizer import optimizer_SGD, AdaGrad, NormGrad, SGD
import numpy as np
from functions import sigmoid, sigmoid_back, clip_grads

class Loss:

    def __init__(self):
        self.Loss = None
        self.dout = None

    def forward(self, out, t):
        self.Loss = 0.5 * np.sum((out - t) ** 2)
        self.dout = out - t
        return self.Loss

    def backward(self):
        return self.dout


class RNNneuron:

    def __init__(self, W, Wh, b):
        self.params = [
         W, Wh, b]
        self.grads = [
         np.zeros_like(W), np.zeros_like(Wh), np.zeros_like(b)]
        self.F_container = np.empty(0)
        self.B_container = np.empty(0)
        self.dh_prev = None
        self.lr = 0.01
        self.optimizer = SGD(self.lr)
        self.clipper = 0
        self.NormGrad = 0.02

    def forward(self, x, h_prev):
        W, Wh, b = self.params
        if h_prev is None:
            y = np.dot(x, W) + b
        else:
            y = np.dot(h_prev, Wh) + np.dot(x, W) + b
        z = sigmoid(y)
        self.h_prev = z
        self.F_container = [W, Wh, b, x, y, z]
        return (z, self.F_container)

    def backward(self, dz, h_prev):
        W, Wh, b, x, y, z = self.F_container
        dh_prev = self.dh_prev
        if dh_prev is None:
            dz = dz
        else:
            dz = dh_prev + dz
        dy = sigmoid_back(z, dz)
        db = dy
        dW = np.dot(x.T, dy)
        dx = np.dot(dy, W.T)
        dWh = np.dot(h_prev.T, dy)
        dh_prev = np.dot(dy, Wh.T)
        self.drads, self.clipper = clip_grads(self.grads, self.NormGrad)
        self.dh_prev = dh_prev
        self.grads[0][...] = dW
        self.grads[1][...] = dWh
        self.grads[2][...] = db
        self.params = self.optimizer.update(self.params, self.grads)
        self.container = [
         dy, db, dW, dWh, dx]
        return (
         dx, self.container)

    def setlr(self, lr, model=0):
        self.lr = lr
        if model == 0:
            self.optimizer = SGD(self.lr)
        else:
            if model == 1:
                self.optimizer = AdaGrad(self.lr)
            else:
                if model == 2:
                    self.optimizer = NormGrad(self.lr)

    def viewlr(self):
        return self.optimizer.viewlr()

    def change_lr(self, New_lr):
        self.optimizer.change_lr(New_lr)

    def reset(self):
        self.h_prev = None
        self.dh_prev = None

    def clipper_Chech(self):
        return self.clipper

    def change_NormGrad(self, NormGrad):
        self.NormGrad = NormGrad


class BPneuron:

    def __init__(self, W, b):
        self.params = [
         W, b]
        self.grads = [
         np.zeros_like(W), np.zeros_like(b)]
        self.container = np.empty(0)
        self.lr = 0.01
        self.optimizer = AdaGrad(self.lr)

    def forward(self, x):
        W, b = self.params
        y = np.dot(x, W) + b
        z = sigmoid(y)
        self.container = [W, b, x, y, z]
        return (z, self.container)

    def backward(self, dz):
        W, b, x, y, z = self.container
        dy = sigmoid_back(z, dz)
        db = dy
        dW = np.dot(x.T, dy)
        dx = np.dot(dy, W.T)
        self.grads[0][...] = dW
        self.grads[1][...] = db
        self.params = self.optimizer.update(self.params, self.grads)
        self.container = [
         dy, db, dW, dx]
        return (
         dx, self.container)

    def setlr(self, lr, model=0):
        self.lr = lr
        if model == 0:
            self.optimizer = SGD(self.lr)
        else:
            if model == 1:
                self.optimizer = AdaGrad(self.lr)
            else:
                if model == 2:
                    self.optimizer = NormGrad(self.lr)

    def viewlr(self):
        return self.optimizer.viewlr()

    def change_lr(self, New_lr):
        self.optimizer.change_lr(New_lr)