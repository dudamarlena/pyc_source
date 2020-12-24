# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/batch_norm.py
# Compiled at: 2016-04-20 00:05:45
import theano.tensor as T
from . import NeuralLayer

class BatchNormalization(NeuralLayer):
    """
    Batch normalization.
    http://arxiv.org/pdf/1502.03167v3.pdf
    """

    def __init__(self, epsilon=1e-06, weights=None):
        super(BatchNormalization, self).__init__('norm')
        self.epsilon = epsilon

    def prepare(self):
        self.gamma = self.create_weight(shape=(self.input_dim,), suffix='gamma')
        self.beta = self.create_bias(self.input_dim, suffix='beta')
        self.register_parameters(self.gamma, self.beta)

    def compute_tensor(self, x):
        m = x.mean(axis=0)
        std = T.mean((x - m) ** 2 + self.epsilon, axis=0) ** 0.5
        x_normed = (x - m) / (std + self.epsilon)
        out = self.gamma * x_normed + self.beta
        return out