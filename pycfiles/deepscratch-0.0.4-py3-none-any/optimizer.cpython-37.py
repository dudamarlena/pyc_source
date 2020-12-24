# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuguldur/Documents/ml from scratch/build/lib/deepscratch/optimizer.py
# Compiled at: 2019-06-16 06:57:24
# Size of source mod 2**32: 492 bytes
import numpy as np

class Optimizer:

    def __init__(self):
        pass

    def update(self):
        pass


class SGD(Optimizer):

    def __init__(self, layers, lr=0.001, momentum=0.1):
        self.lr = lr
        self.momentum = momentum
        self.layers = list(layers)

    def update(self):
        for layer in self.layers:
            if layer.trainable:
                for param, grad in zip(layer.parameters(), layer.dparameters()):
                    param -= self.lr * grad