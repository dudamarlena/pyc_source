# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hadoop/nlpy/nlpy/deep/networks/classifier_runner.py
# Compiled at: 2014-11-26 00:42:04
from basic_nn import NeuralNetwork
import theano, theano.tensor as T

class NeuralClassifierRunner(NeuralNetwork):
    """A classifier attempts to match a 1-hot target output."""

    def __init__(self, config):
        super(NeuralClassifierRunner, self).__init__(config)

    def setup_vars(self):
        super(NeuralClassifierRunner, self).setup_vars()
        self.vars.k = T.ivector('k')
        self.inputs.append(self.vars.k)

    @property
    def cost(self):
        return T.constant(0)

    @property
    def errors(self):
        return T.constant(0)

    @property
    def monitors(self):
        return []

    def classify(self, x):
        return self.predict(x).argmax(axis=1)