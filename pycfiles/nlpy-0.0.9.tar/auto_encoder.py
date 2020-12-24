# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/deep/networks/auto_encoder.py
# Compiled at: 2014-11-18 04:04:39
import theano, theano.tensor as T
from basic_nn import NeuralNetwork

class AutoEncoder(NeuralNetwork):

    @property
    def cost(self):
        err = self.vars.y - self.vars.x
        return T.mean((err * err).sum(axis=1))