# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/mlgear/metrics.py
# Compiled at: 2019-12-27 10:20:12
# Size of source mod 2**32: 1188 bytes
import numpy as np
from math import sqrt
from keras import backend as K
from sklearn.metrics import mean_squared_error

def crps_score(actual, predicted):
    return ((predicted - actual) ** 2).sum(axis=1).sum(axis=0) / (199 * actual.shape[0])


def crps_score_(actual, predicted):
    actual = np.clip(np.cumsum(actual, axis=1), 0, 1)
    predicted = np.clip(np.cumsum(predicted, axis=1), 0, 1)
    return crps_score(actual, predicted)


def k_crps(y_true, y_pred):
    y_true = K.clip(K.cumsum(y_true, axis=1), 0, 1)
    y_pred = K.clip(K.cumsum(y_pred, axis=1), 0, 1)
    return K.sum(K.sum((K.square(y_true - y_pred)), axis=1), axis=0) / K.cast(199 * K.shape(y_true)[0], 'float32')


def k_crps_(y_true, y_pred):
    y_true = K.clip(K.cumsum(y_true, axis=1), 0, 1)
    y_pred = K.clip(K.cumsum(y_pred, axis=1), 0, 1)
    return K.sum(K.sum((K.square(y_true - y_pred)), axis=1), axis=0)


def crps_lgb(actual, predicted):
    actual_ = np.zeros((actual.shape[0], 199))
    for idx, target in enumerate(list(actual)):
        actual_[idx][int(target)] = 1

    return crps_score_(actual_, predicted)


def rmse(actual, predicted):
    return sqrt(mean_squared_error(actual, predicted))