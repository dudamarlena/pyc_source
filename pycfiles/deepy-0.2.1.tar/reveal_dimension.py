# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/reveal_dimension.py
# Compiled at: 2016-04-20 00:05:45
from . import NeuralLayer

class RevealDimension(NeuralLayer):
    """
    Operation for revealing dimension.
    After some dimension-unclear layers such as convolution, the dimension information will be lost.
    Use this layer to redefine the input dimension.
    """

    def __init__(self, dim):
        super(RevealDimension, self).__init__('reveal_dimension')
        self.dim = dim

    def prepare(self):
        self.output_dim = self.dim

    def compute_tensor(self, x):
        return x