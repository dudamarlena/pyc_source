# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/bias.py
# Compiled at: 2016-04-20 00:05:45
from . import NeuralLayer

class Bias(NeuralLayer):
    """
    Bias layer.
    """

    def __init__(self):
        super(Bias, self).__init__('bias')

    def prepare(self):
        self.output_dim = self.input_dim
        self.B = self.create_bias(self.output_dim, 'bias')
        self.register_parameters(self.B)

    def compute_tensor(self, x):
        return x + self.B