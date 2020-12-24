# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuguldur/Documents/ml from scratch/build/lib/deepscratch/layers.py
# Compiled at: 2019-06-16 07:17:25
# Size of source mod 2**32: 2331 bytes
import numpy as np
from .activations import *

class Layer:

    def __init__(self):
        self.trainable = False

    def forward(self, x):
        raise NotImplementedError()

    def backward(self, grad):
        raise NotImplementedError()

    def __call__(self, x):
        return self.forward(x)

    def parameters(self):
        raise NotImplementedError()

    def dparameters(self):
        raise NotImplementedError()

    def nparameters(self):
        """ Total number of trainable parameters in the layer """
        return 0

    def repr(self):
        return ''

    def __repr__(self):
        name = self.__class__.__name__
        args = self.repr()
        params = self.nparameters()
        return f"\x1b[01m{name}\x1b[00m({args}), \x1b[1;92m{params}\x1b[00m params"


class Linear(Layer):

    def __init__(self, in_features, out_features):
        super().__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.W = np.random.random((in_features, out_features))
        self.b = np.zeros((1, out_features))
        self.trainable = True

    def forward(self, x):
        self.layer_input = x
        return np.dot(x, self.W) + self.b

    def backward(self, grad):
        self._Linear__dW = np.dot(self.layer_input.T, grad)
        self._Linear__db = np.sum(grad, axis=0, keepdims=True)
        dx = np.dot(grad, self.W.T)
        return dx

    def parameters(self):
        return [
         self.W, self.b]

    def dparameters(self):
        return [
         self._Linear__dW, self._Linear__db]

    def nparameters(self):
        return np.prod(self.W.shape) + np.prod(self.b.shape)

    def repr(self):
        return f"{self.in_features} → {self.out_features}"


class ReLU(Layer):

    def __init__(self):
        super().__init__()
        self.trainable = False

    def forward(self, x):
        self.layer_input = x
        return relu(x)

    def backward(self, grad):
        return grad * relu((self.layer_input), deriv=True)


class Sigmoid(Layer):

    def __init__(self):
        super().__init__()
        self.trainable = False

    def forward(self, x):
        self.layer_input = x
        return sigmoid(x)

    def backward(self, grad):
        return grad * sigmoid((self.layer_input), deriv=True)