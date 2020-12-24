# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/tf/python/keras/activations.py
# Compiled at: 2019-11-05 02:33:02
# Size of source mod 2**32: 319 bytes
import functools, tensorflow as tf
relu6 = functools.partial((tf.keras.activations.relu), max_value=6)
relu6.__name__ = 'seq2annotation.tf.python.keras.activations.relu6'
tf.keras.utils.get_custom_objects()[relu6.__name__] = relu6