# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/onehot_embed.py
# Compiled at: 2016-04-20 00:05:45
import numpy as np, theano.tensor as T
from deepy.layers import NeuralLayer
from deepy.layers.var import NeuralVariable
from deepy.utils import onehot_tensor, onehot
from deepy.utils import FLOATX

class OneHotEmbedding(NeuralLayer):
    """
    One-hot embedding layer.
    Computation: [0,1,2]  ---> [[1,0,0],[0,1,0],[0,0,1]]
    """

    def __init__(self, vocab_size, cached=True, zero_index=None, mask=None):
        super(OneHotEmbedding, self).__init__('onehot')
        self.vocab_size = vocab_size
        self.output_dim = vocab_size
        self.cached = cached
        self.zero_index = zero_index
        self.mask = mask.tensor if type(mask) == NeuralVariable else mask

    def prepare(self):
        if not self.cached:
            return
        onehot_matrix = []
        for i in xrange(self.vocab_size):
            onehot_matrix.append(onehot(self.vocab_size, i))

        onehot_matrix = np.array(onehot_matrix, dtype=FLOATX)
        self.onehot_list = self.create_matrix(self.vocab_size, self.vocab_size, 'onehot_list')
        self.onehot_list.set_value(onehot_matrix)

    def compute_tensor(self, x):
        if self.cached:
            if x.ndim == 1:
                ret_tensor = self.onehot_list[x]
            else:
                ret_tensor = self.onehot_list[x.flatten()].reshape((x.shape[0], x.shape[1], self.vocab_size))
        else:
            ret_tensor = onehot_tensor(x, self.vocab_size)
        if self.zero_index != None:
            mask = T.neq(x, self.zero_index)
            if x.ndim == 1:
                ret_tensor *= mask[:, None]
            else:
                ret_tensor *= mask[:, :, None]
        if self.mask:
            if x.ndim == 1:
                ret_tensor *= self.mask[:, None]
            else:
                ret_tensor *= self.mask[:, :, None]
        return ret_tensor