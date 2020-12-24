# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/resnet/metrics.py
# Compiled at: 2020-04-19 13:55:35
# Size of source mod 2**32: 277 bytes
from tensorflow import keras

def top_1_categorical_error(y_true, y_pred):
    return 1.0 - keras.metrics.top_k_categorical_accuracy(y_true, y_pred, 1)


def top_5_categorical_error(y_true, y_pred):
    return 1.0 - keras.metrics.top_k_categorical_accuracy(y_true, y_pred, 5)