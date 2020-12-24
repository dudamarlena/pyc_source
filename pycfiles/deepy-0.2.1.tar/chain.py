# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/chain.py
# Compiled at: 2016-04-20 00:05:45
from layer import NeuralLayer

class Chain(NeuralLayer):
    """
    Stack many layers to form a chain.
    This is useful to reuse layers in a customized layer.
    Usage:
        As part of the main pipe line:
            chain = Chain(layer1, layer2)
            model.stack(chain)
        As part of the computational graph:
            chain = Chain(layer1, layer2)
            y = chain.compute(x)
    """

    def __init__(self, *layers):
        super(Chain, self).__init__('chain')
        self.layers = []
        self._layers_to_stack = []
        if len(layers) == 1 and type(layers[0]) == int:
            self.input_dim = layers[0]
        else:
            self.stack(*layers)

    def stack(self, *layers):
        if self.input_dim is None or self.input_dim == 0:
            self._layers_to_stack.extend(layers)
        else:
            self._register_layers(*layers)
        return self

    def _register_layers(self, *layers):
        for layer in layers:
            if not self.layers:
                layer.initialize(self.input_dim)
            else:
                layer.initialize(self.layers[(-1)].output_dim)
            self.layers.append(layer)
            self.output_dim = layer.output_dim

        self.register_inner_layers(*self.layers)

    def prepare(self, *layers):
        if self._layers_to_stack:
            self._register_layers(*self._layers_to_stack)
            self._layers_to_stack = []

    def compute_tensor(self, x):
        return self._output(x, False)

    def compute_test_tesnor(self, x):
        return self._output(x, True)

    def _output(self, x, test):
        y = x
        for layer in self.layers:
            y = layer.compute_flexible_tensor(y, test=test)

        return y