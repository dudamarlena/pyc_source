# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/dense.py
# Compiled at: 2016-04-20 00:05:45
from deepy.utils import build_activation, FLOATX
import theano.tensor as T
from . import NeuralLayer

class Dense(NeuralLayer):
    """
    Fully connected layer.
    """

    def __init__(self, size, activation='linear', init=None, disable_bias=False, random_bias=False):
        super(Dense, self).__init__('dense')
        self.activation = activation
        self.output_dim = size
        self.disable_bias = disable_bias
        self.random_bias = random_bias
        self.initializer = init

    def prepare(self):
        self._setup_params()
        self._setup_functions()

    def compute_tensor(self, x):
        return self._activation(T.dot(x, self.W) + self.B)

    def _setup_functions(self):
        self._activation = build_activation(self.activation)

    def _setup_params(self):
        self.W = self.create_weight(self.input_dim, self.output_dim, self.name, initializer=self.initializer)
        self.register_parameters(self.W)
        if self.disable_bias:
            self.B = T.constant(0, dtype=FLOATX)
        elif self.random_bias:
            self.B = self.create_weight(suffix=self.name + '_bias', initializer=self.initializer, shape=(
             self.output_dim,))
            self.register_parameters(self.B)
        else:
            self.B = self.create_bias(self.output_dim, self.name)
            self.register_parameters(self.B)