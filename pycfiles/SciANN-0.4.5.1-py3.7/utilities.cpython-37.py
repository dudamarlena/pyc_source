# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/utils/utilities.py
# Compiled at: 2020-04-12 17:28:07
# Size of source mod 2**32: 2875 bytes
""" Built-in utilities to process inputs.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
from numpy import pi
import tensorflow as tf, keras as k
import keras.backend as K
from keras.backend import is_tensor
from keras.backend import floatx
from keras.backend import set_floatx
from keras.utils.generic_utils import to_list
from keras.utils.generic_utils import unpack_singleton
from keras.utils import plot_model
import keras.initializers as default_bias_initializer
import keras.initializers as default_kernel_initializer
import keras.initializers as default_constant_initializer

def _is_tf_1():
    return tf.__version__.startswith('1.')


def get_activation(activation):
    """ Evaluates the activation function from a string or list of string inputs.

    # Arguments
        activation: A string pointing to the function name.

    # Returns:
        A function handle.
    """
    if isinstance(activation, list):
        return [get_activation(act) for act in activation]
    if isinstance(activation, str):
        if hasattr(k.activations, activation):
            return getattr(k.activations, activation)
        if hasattr(k.backend, activation):
            return getattr(k.backend, activation)
        if hasattr(tf.math, activation):
            return getattr(tf.math, activation)
        raise ValueError('Not a valid function name: ' + activation + ' - Please provide a valid activation function name from Keras or Tensorflow. ')
    else:
        if callable(activation):
            return activation
        raise TypeError('Please provide a valid input: ' + type(activation) + ' - Expecting a function name or function handle. ')


def set_random_seed(val=1234):
    """ Set random seed for reproducibility.

    # Arguments
        val: A seed value..

    """
    np.random.seed(val)
    if _is_tf_1():
        tf.set_random_seed(val)
    else:
        tf.random.set_seed(val)


def clear_tf_session():
    """ Clear keras and tensorflow sessions.
    """
    if _is_tf_1():
        K.clear_session()
    else:
        tf.keras.backend.clear_session()


def is_same_tensor(x, y):
    if len(to_list(x)) != len(to_list(y)):
        return False
    res = []
    for xi, yi in zip(to_list(x), to_list(y)):
        res.append(xi.name == yi.name)

    return all(res)


def unique_tensors(Xs):
    if len(Xs) > 1:
        ux, uids = np.unique([x.name for x in Xs], return_index=True)
        uids = sorted(uids)
        return [Xs[i] for i in uids]
    return Xs