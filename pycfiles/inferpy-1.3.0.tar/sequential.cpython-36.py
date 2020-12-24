# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/layers/sequential.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 504 bytes
import tensorflow as tf
from inferpy import contextmanager

def Sequential(*args, **kwargs):
    model = (tf.keras.Sequential)(*args, **kwargs)
    contextmanager.layer_registry.add_sequential(model)
    return model