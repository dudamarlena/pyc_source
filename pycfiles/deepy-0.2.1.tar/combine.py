# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/combine.py
# Compiled at: 2016-04-20 00:05:45
from . import NeuralLayer

class Combine(NeuralLayer):
    """
    Combine two variables.
    """

    def __init__(self, func, dim=0):
        """
        :type layer1: NeuralLayer
        :type layer2: NeuralLayer
        """
        super(Combine, self).__init__('combine')
        self.func = func
        if dim > 0:
            self.output_dim = dim

    def prepare(self):
        if self.output_dim == 0:
            self.output_dim = self.input_dim

    def compute_tensor(self, *tensors):
        return self.func(*tensors)

    def compute_test_tesnor(self, *tensors):
        return self.func(*tensors)