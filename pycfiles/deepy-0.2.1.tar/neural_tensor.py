# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/neural_tensor.py
# Compiled at: 2016-04-20 00:05:45
from theano import tensor
from decorations import neural_computation

class NeuralTensor:
    """
    A class for exporting Theano tensor operations to neural variables.
    """

    def __getattr__(self, func_name):

        @neural_computation
        def wrapper(*args, **kwargs):
            return getattr(tensor, func_name)(*args, **kwargs)

        return wrapper


neural_tensor = NeuralTensor()
NT = neural_tensor