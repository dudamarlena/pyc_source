# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/op/basic.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 1336 bytes
from tensorflow import keras

class Operation:
    __doc__ = 'Interface of an operation.\n\n    >>> import tensorflow as tf\n    >>> from deephyper.search.nas.model.space.op.op1d import Operation\n    >>> Operation(layer=tf.keras.layers.Dense(10))\n    Dense\n\n    Args:\n        layer (Layer): a ``tensorflow.keras.layers.Layer``.\n    '

    def __init__(self, layer: keras.layers.Layer):
        assert isinstance(layer, keras.layers.Layer)
        self.from_keras_layer = True
        self._layer = layer

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if hasattr(self, 'from_keras_layer'):
            return type(self._layer).__name__
        return str(self)

    def __call__(self, tensors: list, seed: int=None, **kwargs):
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

    def init(self, current_node):
        """Preprocess the current operation.
        """
        pass


class Tensor(Operation):

    def __init__(self, tensor, *args, **kwargs):
        self.tensor = tensor

    def __call__(self, *args, **kwargs):
        return self.tensor