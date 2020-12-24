# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/flatten.py
# Compiled at: 2016-04-20 00:05:45
from . import NeuralLayer
import theano.tensor as T

class Flatten(NeuralLayer):
    """
    Flatten layer.
    """

    def __init__(self):
        super(Flatten, self).__init__('flatten')

    def compute_tensor(self, x):
        return T.flatten(x, 2)