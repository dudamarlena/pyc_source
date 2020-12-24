# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/activation.py
# Compiled at: 2016-04-20 00:05:45
from . import NeuralLayer
from deepy.utils import build_activation

class Activation(NeuralLayer):
    """
    Activation layer.
    """

    def __init__(self, activation_type):
        super(Activation, self).__init__(activation_type)
        self._activation = build_activation(activation_type)

    def compute_tensor(self, x):
        return self._activation(x)