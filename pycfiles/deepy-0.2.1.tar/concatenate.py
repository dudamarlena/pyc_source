# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/concatenate.py
# Compiled at: 2016-04-20 00:05:45
import theano.tensor as T
from . import NeuralLayer

class Concatenate(NeuralLayer):
    """
    Concatenate two tensors.
    They should have identical dimensions except the last one.
    """

    def __init__(self, axis=2):
        """
        :type layer1: NeuralLayer
        :type layer2: NeuralLayer
        """
        super(Concatenate, self).__init__('concate')
        self.axis = axis
        if axis < 0:
            raise Exception('There are some bugs in T.concatenate, that axis can not lower than 0')

    def prepare(self):
        self.output_dim = sum(self.input_dims)

    def compute_tensor(self, *xs):
        return T.concatenate(xs, axis=self.axis)

    def compute_test_tesnor(self, *xs):
        return T.concatenate(xs, axis=self.axis)