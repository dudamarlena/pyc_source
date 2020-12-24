# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\poda\layers\merge.py
# Compiled at: 2019-09-26 09:27:13
# Size of source mod 2**32: 4375 bytes
import tensorflow as tf

def add(input_tensor_1, input_tensor_2, names=None):
    """[summary]
    
    Arguments:
        input_tensor_1 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 1]
        input_tensor_2 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 2]
        names {[str]} -- [Name of the layer] (default: {None})

    Returns:
        [Tensor] -- [Added tensor]
    """
    if names != None:
        names = str(names)
    else:
        names = 'add'
    add_tensor = tf.math.add(x=input_tensor_1, y=input_tensor_2, name=names)
    return add_tensor


def concatenate(list_tensor, axis=-1, names=None):
    """[summary]
    
    Arguments:
        list_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A list tensor representing prelayer 1]
    
    Keyword Arguments:
        axis {int} -- [Dimension tensor] (default: {-1})
        names {[str]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [Concatenate tensor]
    """
    if names != None:
        names = str(names)
    else:
        names = 'concatenate'
    concat_tensor = tf.concat(values=list_tensor, axis=axis, name=names)
    return concat_tensor


def flatten(input_tensor, names=None):
    """[summary]
    
    Arguments:
        input_tensor {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer]
    
    Keyword Arguments:
        names {[type]} -- [Name of the layer] (default: {None})
    
    Returns:
        [Tensor] -- [Flatten tensor]
    """
    return tf.compat.v2.keras.layers.Flatten()(input_tensor)


def maximum(input_tensor_1, input_tensor_2, names=None):
    """[summary]
    
    Arguments:
        input_tensor_1 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 1]
        input_tensor_2 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 2]
        names {[str]} -- [Name of the layer] (default: {None})

    Returns:
        [Tensor] -- [Maximum tensor]
    """
    if names != None:
        names = str(names)
    else:
        names = 'maximum'
    maximum_tensor = tf.math.maximum(x=input_tensor_1, y=input_tensor_2, name=names)
    return maximum_tensor


def minimum(input_tensor_1, input_tensor_2, names=None):
    """[summary]
    
    Arguments:
        input_tensor_1 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 1]
        input_tensor_2 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 2]
        names {[str]} -- [Name of the layer] (default: {None})

    Returns:
        [Tensor] -- [Minimum tensor]
    """
    if names != None:
        names = str(names)
    else:
        names = 'minimum'
    minimum_tensor = tf.math.minimum(x=input_tensor_1, y=input_tensor_2, name=names)
    return minimum_tensor


def multiply(input_tensor_1, input_tensor_2, names=None):
    """[summary]
    
    Arguments:
        input_tensor_1 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 1]
        input_tensor_2 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 2]
        names {[str]} -- [Name of the layer] (default: {None})

    Returns:
        [Tensor] -- [Multiplied tensor]
    """
    if names != None:
        names = str(names)
    else:
        names = 'multipy'
    multiply_tensor = tf.math.multiply(x=input_tensor_1, y=input_tensor_2, name=names)
    return multiply_tensor


def substract(input_tensor_1, input_tensor_2, names=None):
    """[summary]
    
    Arguments:
        input_tensor_1 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 1]
        input_tensor_2 {[float, double, int32, int64, uint8, int16, or int8]} -- [A Tensor representing prelayer 2]
        names {[str]} -- [Name of the layer] (default: {None})

    Returns:
        [Tensor] -- [Substracted tensor]
    """
    if names != None:
        names = str(names)
    else:
        names = 'subtract'
    substract_tensor = tf.math.subtract(x=input_tensor_1, y=input_tensor_2, name=names)
    return substract_tensor