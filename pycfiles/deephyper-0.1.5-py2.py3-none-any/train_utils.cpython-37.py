# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/train_utils.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 2605 bytes
from collections import OrderedDict
import numpy as np, tensorflow as tf
from sklearn.metrics import mean_absolute_error, mean_squared_error
from ... import util
optimizers_keras = OrderedDict()
optimizers_keras['sgd'] = tf.keras.optimizers.SGD
optimizers_keras['rmsprop'] = tf.keras.optimizers.RMSprop
optimizers_keras['adagrad'] = tf.keras.optimizers.Adagrad
optimizers_keras['adam'] = tf.keras.optimizers.Adam
optimizers_keras['adadelta'] = tf.keras.optimizers.Adadelta
optimizers_keras['adamax'] = tf.keras.optimizers.Adamax
optimizers_keras['nadam'] = tf.keras.optimizers.Nadam

def selectOptimizer_keras(name):
    """Return the optimizer defined by name.
    """
    if optimizers_keras.get(name) == None:
        raise RuntimeError('"{0}" is not a defined optimizer for keras.'.format(name))
    else:
        return optimizers_keras[name]


def check_data_config(data_dict):
    gen_keys = [
     'train_gen', 'train_size',
     'valid_gen', 'valid_size', 'types', 'shapes']
    ndarray_keys = ['train_X', 'train_Y', 'valid_X', 'valid_Y']
    if all([k in data_dict.keys() for k in gen_keys]):
        return 'gen'
    if all([k in data_dict.keys() for k in ndarray_keys]):
        return 'ndarray'
    raise RuntimeError('Wrong data config...')


def r2(y_true, y_pred):
    SS_res = tf.keras.backend.sum(tf.keras.backend.square(y_true - y_pred))
    SS_tot = tf.keras.backend.sum(tf.keras.backend.square(y_true - tf.keras.backend.mean(y_true)))
    return 1 - SS_res / (SS_tot + tf.keras.backend.epsilon())


def mae(y_true, y_pred):
    return tf.keras.metrics.mean_absolute_error(y_true, y_pred)


def mse(y_true, y_pred):
    return tf.keras.metrics.mean_squared_error(y_true, y_pred)


def acc(y_true, y_pred):
    return tf.keras.metrics.categorical_accuracy(y_true, y_pred)


metrics = OrderedDict()
metrics['mean_absolute_error'] = metrics['mae'] = mae
metrics['r2'] = r2
metrics['mean_squared_error'] = metrics['mse'] = mse
metrics['accuracy'] = metrics['acc'] = acc

def selectMetric(name):
    """Return the metric defined by name.

    Args:
        name ([type]): [description]

    Returns:
        [type]: [description]
    """
    if metrics.get(name) == None:
        try:
            return util.load_attr_from(name)
        except:
            return name

    else:
        return metrics[name]