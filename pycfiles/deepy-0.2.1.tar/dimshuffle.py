# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/layers/dimshuffle.py
# Compiled at: 2016-04-20 00:05:45
from . import NeuralLayer

class DimShuffle(NeuralLayer):
    """
    DimShuffle layer.
    """

    def __init__(self, *pattern):
        super(DimShuffle, self).__init__('dimshuffle')
        if len(pattern) == 1 and type(pattern[0]) == list:
            self.pattern = pattern[0]
        else:
            self.pattern = pattern

    def compute_tensor(self, x):
        return x.dimshuffle(*self.pattern)