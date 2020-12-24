# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/backend/keras_helpers.py
# Compiled at: 2019-08-07 07:03:08
# Size of source mod 2**32: 1323 bytes
from tensorflow.python.keras import Model
from tensorflow.python.keras.layers import Layer
from tensorflow.python.util import nest
__all__ = [
 'to_keras_objective', 'copy_keras_metadata', 'has_keras_meta',
 'add_trainable_weights']

def has_keras_meta(tensor):
    return hasattr(tensor, '_keras_history') and hasattr(tensor, '_keras_mask')


def copy_keras_metadata(keras_tensor, *new_tensors):
    if not hasattr(keras_tensor, '_keras_history') or not hasattr(keras_tensor, '_keras_mask'):
        pass
    else:
        new_tensors = nest.flatten(new_tensors)
        history = keras_tensor._keras_history
        mask = keras_tensor._keras_mask
        for t in new_tensors:
            setattr(t, '_keras_history', history)
            setattr(t, '_keras_mask', mask)

    if len(new_tensors) == 1:
        return new_tensors[0]
    else:
        return new_tensors


def add_trainable_weights(layer, *variables):
    from odin.backend import is_variable
    variables = nest.flatten(variables)
    if not all(is_variable(v) for v in variables):
        raise AssertionError('All objects from variables must be instance of tensorflow.Variable')
    elif not isinstance(layer, Layer):
        raise AssertionError('layer must be instance of tensorflow.python.keras.layers.Layer')
    variables = [v for v in variables if v not in layer._trainable_weights]
    layer._trainable_weights = layer._trainable_weights + variables
    return layer