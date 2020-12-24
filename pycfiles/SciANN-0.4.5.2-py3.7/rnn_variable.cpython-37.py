# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/functionals/rnn_variable.py
# Compiled at: 2020-04-12 04:31:31
# Size of source mod 2**32: 1546 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from keras.layers import InputLayer
from ..utils import to_list, floatx, set_floatx
from .rnn_functional import RNNFunctional

class RNNVariable(RNNFunctional):
    __doc__ = " Configures the `LSTMVariable` object for the network's input.\n\n    # Arguments\n        units: Int.\n            number of time units in an recurrent architecture.\n            A minimum of 2 is needed.\n        name: String.\n            Required as derivatives work only with layer names.\n        tensor: Tensorflow `Tensor`.\n            Can be pass as the input path.\n        dtype: data-type of the network parameters, can be\n            ('float16', 'float32', 'float64').\n\n    # Raises\n\n    "

    def __init__(self, units, name=None, tensor=None, dtype=None):
        if not dtype:
            dtype = floatx()
        else:
            if not dtype == floatx():
                set_floatx(dtype)
            else:
                raise isinstance(units, int) and units >= 2 or AssertionError('RNN needs a minimum of 2 time units. ')
            layer = InputLayer(batch_input_shape=(
             None, units, 1),
              input_tensor=tensor,
              name=name,
              dtype=dtype)
            super(RNNVariable, self).__init__(layers=(to_list(layer)),
              inputs=(to_list(layer.input)),
              outputs=(to_list(layer.output)))

    @classmethod
    def get_class(cls):
        return RNNFunctional