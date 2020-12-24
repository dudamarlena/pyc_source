# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/op/basic.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 1379 bytes
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Layer
import deephyper.search.nas.model.space.layers as deeplayers

class Operation:
    __doc__ = 'Interface of an operation.\n\n    >>> import tensorflow as tf\n    >>> from deephyper.search.nas.model.space.op.op1d import Operation\n    >>> Operation(layer=tf.keras.layers.Dense(10))\n    Dense\n\n    Args:\n        layer (Layer): a ``tensorflow.keras.layers.Layer``.\n    '

    def __init__(self, layer: Layer):
        assert isinstance(layer, Layer)
        self._layer = layer

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if hasattr(self, '_layer'):
            return type(self._layer).__name__
        else:
            return type(self).__name__

    def __call__(self, tensors: list, *args, **kwargs):
        """
        Args:
            tensors (list): a list of incoming tensors.

        Returns:
            tensor: an output tensor.
        """
        if len(tensors) == 1:
            out = self._layer(tensors[0])
        else:
            out = self._layer(tensors)
        return out

    def init(self):
        """Preprocess the current operation.
        """
        pass


class Tensor(Operation):

    def __init__(self, tensor, *args, **kwargs):
        self.tensor = tensor

    def __call__(self, *args, **kwargs):
        return self.tensor