# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/word_embed.py
# Compiled at: 2016-05-16 02:45:03
import numpy as np, theano.tensor as T
from deepy.layers import NeuralLayer
from var import NeuralVariable
from deepy.utils import FLOATX

class WordEmbedding(NeuralLayer):
    """
    Word embedding layer.
    The word embeddings are randomly initialized, and are learned over the time.
    """

    def __init__(self, size, vocab_size, zero_index=None, mask=None, init=None):
        super(WordEmbedding, self).__init__('word_embed')
        self.size = size
        self.vocab_size = vocab_size
        self.output_dim = size
        self.zero_index = zero_index
        self._mask = mask.tensor if type(mask) == NeuralVariable else mask
        self._init = init

    def prepare(self):
        self.embed_matrix = self.create_weight(self.vocab_size, self.size, 'embed', initializer=self._init)
        self.register_parameters(self.embed_matrix)

    def compute_tensor(self, x, mask=None):
        mask_input = mask if mask else self._mask
        if self.zero_index is not None:
            mask = T.neq(x, self.zero_index)
            x = T.cast(x * mask, 'int32')
        elif mask_input:
            mask = self._mask
        else:
            mask = None
        ret_tensor = self.embed_matrix[x.flatten()].reshape(list(x.shape) + [self.size])
        if mask:
            if x.ndim == 2:
                ret_tensor *= mask[:, :, None]
            elif x.ndim == 1:
                ret_tensor *= mask[:, None]
        return ret_tensor