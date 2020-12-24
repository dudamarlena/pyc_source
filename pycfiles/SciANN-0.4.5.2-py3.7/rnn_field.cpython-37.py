# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/functionals/rnn_field.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 2049 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from keras.layers import Dense, TimeDistributed
from keras.activations import linear
from ..utils import default_bias_initializer, default_kernel_initializer
from ..utils import floatx, set_floatx

class RNNField(TimeDistributed):
    __doc__ = " Configures the `LSTMField` class for the model outputs.\n\n    # Arguments\n        units: Positive integer.\n            Dimension of the output of the network.\n        name: String.\n            Assigns a layer name for the output.\n        activation: Callable.\n            A callable object for the activation.\n        kernel_initializer: Initializer for the kernel.\n            Defaulted to a normal distribution.\n        bias_initializer: Initializer for the bias.\n            Defaulted to a normal distribution.\n        trainable: Boolean to activate parameters of the network.\n        dtype: data-type of the network parameters, can be\n            ('float16', 'float32', 'float64').\n\n    # Raises\n\n    "

    def __init__(self, units=1, name=None, activation=linear, kernel_initializer=default_kernel_initializer(), bias_initializer=default_bias_initializer(), trainable=True, dtype=None):
        if not dtype:
            dtype = floatx()
        else:
            if not dtype == floatx():
                set_floatx(dtype)
        assert isinstance(name, str), 'Please provide a string for field name. '
        assert callable(activation), 'Please provide a function handle for the activation. '
        super(RNNField, self).__init__(Dense(units=units,
          activation=activation,
          kernel_initializer=kernel_initializer,
          bias_initializer=bias_initializer,
          use_bias=True,
          trainable=trainable,
          name=name,
          dtype=dtype))