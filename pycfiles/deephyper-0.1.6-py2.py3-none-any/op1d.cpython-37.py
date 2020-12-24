# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/op/op1d.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 5831 bytes
import tensorflow as tf
from tensorflow import keras
from . import Operation

class Dense(Operation):
    __doc__ = 'Multi Layer Perceptron operation.\n\n    Help you to create a perceptron with n layers, m units per layer and an activation function.\n\n    Args:\n        units (int): number of units per layer.\n        activation: an activation function from tensorflow.\n    '

    def __init__(self, units, activation=None, *args, **kwargs):
        self.units = units
        self.activation = activation
        self.kwargs = kwargs
        self._layer = None

    def __str__(self):
        if isinstance(self.activation, str):
            return f"Dense_{self.units}_{self.activation}"
        if self.activation is None:
            return f"Dense_{self.units}"
        return f"Dense_{self.units}_{self.activation.__name__}"

    def __call__(self, inputs, seed=None, **kwargs):
        assert len(inputs) == 1, f"{type(self).__name__} as {len(inputs)} inputs when 1 is required."
        if self._layer is None:
            self._layer = (keras.layers.Dense)(units=self.units, 
             kernel_initializer=tf.keras.initializers.glorot_uniform(seed=seed), **self.kwargs)
        out = self._layer(inputs[0])
        if self.activation is not None:
            out = keras.layers.Activation(activation=(self.activation))(out)
        return out


class Dropout(Operation):
    __doc__ = 'Dropout operation.\n\n    Help you to create a dropout operation.\n\n    Args:\n        rate (float): rate of deactivated inputs.\n    '

    def __init__(self, rate):
        self.rate = rate
        super().__init__(layer=keras.layers.Dropout(rate=(self.rate)))

    def __str__(self):
        return f"Dropout({self.rate})"


class Identity(Operation):

    def __init__(self):
        pass

    def __call__(self, inputs, **kwargs):
        assert len(inputs) == 1, f"{type(self).__name__} as {len(inputs)} inputs when 1 is required."
        return inputs[0]


class Conv1D(Operation):
    __doc__ = "Convolution for one dimension.\n\n    Help you to create a one dimension convolution operation.\n\n    Args:\n        filter_size (int): size kernels/filters\n        num_filters (int): number of kernels/filters\n        strides (int):\n        padding (str): 'same' or 'valid'\n    "

    def __init__(self, filter_size, num_filters=1, strides=1, padding='same'):
        self.filter_size = filter_size
        self.num_filters = num_filters
        self.strides = strides
        self.padding = padding
        self._layer = None

    def __str__(self):
        return f"{type(self).__name__}_{self.filter_size}_{self.num_filters}"

    def __call__(self, inputs, **kwargs):
        if not len(inputs) == 1:
            raise AssertionError(f"{type(self).__name__} as {len(inputs)} inputs when only 1 is required.")
        else:
            inpt = inputs[0]
            if len(inpt.get_shape()) == 2:
                out = keras.layers.Reshape((inpt.get_shape()[1], 1))(inpt)
            else:
                out = inpt
        if self._layer is None:
            self._layer = keras.layers.Conv1D(filters=(self.num_filters),
              kernel_size=(self.filter_size),
              strides=(self.strides),
              padding=(self.padding))
        out = self._layer(out)
        return out


class MaxPooling1D(Operation):
    __doc__ = "MaxPooling over one dimension.\n\n    Args:\n        pool_size ([type]): [description]\n        strides (int, optional): Defaults to 1. [description]\n        padding (str, optional): Defaults to 'valid'. [description]\n        data_format (str, optional): Defaults to 'channels_last'. [description]\n    "

    def __init__(self, pool_size, strides=1, padding='valid', data_format='channels_last'):
        self.pool_size = pool_size
        self.strides = strides
        self.padding = padding
        self.data_format = data_format

    def __str__(self):
        return f"{type(self).__name__}_{self.pool_size}_{self.padding}"

    def __call__(self, inputs, **kwargs):
        if not len(inputs) == 1:
            raise AssertionError(f"{type(self).__name__} as {len(inputs)} inputs when only 1 is required.")
        else:
            inpt = inputs[0]
            if len(inpt.get_shape()) == 2:
                out = keras.layers.Reshape((inpt.get_shape()[1], 1))(inpt)
            else:
                out = inpt
        out = keras.layers.MaxPooling1D(pool_size=(self.pool_size),
          strides=(self.strides),
          padding=(self.padding),
          data_format=(self.data_format))(out)
        return out


class Flatten(Operation):
    __doc__ = 'Flatten operation.\n\n    Args:\n        data_format (str, optional): Defaults to None.\n    '

    def __init__(self, data_format=None):
        self.data_format = data_format

    def __call__(self, inputs, **kwargs):
        if not len(inputs) == 1:
            raise AssertionError(f"{type(self).__name__} as {len(inputs)} inputs when only 1 is required.")
        else:
            inpt = inputs[0]
            if len(inpt.get_shape()) == 2:
                out = inpt
            else:
                out = keras.layers.Flatten(data_format=(self.data_format))(inpt)
        return out


class Activation(Operation):
    __doc__ = 'Activation function operation.\n\n    Args:\n        activation (callable): an activation function\n    '

    def __init__(self, activation=None, *args, **kwargs):
        self.activation = activation
        self._layer = None

    def __str__(self):
        return f"{type(self).__name__}_{self.activation}"

    def __call__(self, inputs, *args, **kwargs):
        inpt = inputs[0]
        if self._layer is None:
            self._layer = keras.layers.Activation(activation=(self.activation))
        out = self._layer(inpt)
        return out