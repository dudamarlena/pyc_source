# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/maxout.py
# Compiled at: 2016-04-20 00:05:45
import theano.tensor as T
from . import NeuralLayer
from dense import Dense

class Maxout(NeuralLayer):
    """
    Maxout activation unit.
     - http://arxiv.org/pdf/1302.4389.pdf
    """

    def __init__(self, output_dim=None, num_pieces=4, init=None, linear_transform=True):
        """
        :param num_pieces: pieces of sub maps
        """
        super(Maxout, self).__init__('maxout')
        self.num_pieces = num_pieces
        self.output_dim = output_dim
        self.linear_transform = linear_transform
        self.init = init

    def prepare(self):
        if self.output_dim is None:
            self.output_dim = self.input_dim // self.num_pieces
        if self.linear_transform:
            self.transformer = Dense(self.output_dim * self.num_pieces).initialize(self.input_dim)
            self.register(self.transformer)
        return

    def compute_tensor(self, x):
        if self.linear_transform:
            x = self.transformer.compute_tensor(x)
        new_shape = [ x.shape[i] for i in range(x.ndim - 1) ] + [self.output_dim, self.num_pieces]
        output = T.max(x.reshape(new_shape, ndim=x.ndim + 1), axis=x.ndim)
        return output