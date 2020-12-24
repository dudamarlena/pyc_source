# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/regularization.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 210 bytes
import tensorflow as tf
from .util import func_scope

@func_scope()
def l2_regularization_loss(scale=1e-08):
    return tf.contrib.layers.apply_regularization(tf.contrib.layers.l2_regularizer(scale))