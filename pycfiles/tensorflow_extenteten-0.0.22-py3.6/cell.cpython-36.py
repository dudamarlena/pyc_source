# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/rnn/cell.py
# Compiled at: 2017-05-19 06:10:34
# Size of source mod 2**32: 355 bytes
import tensorflow as tf
from ..util import func_scope
from ..initializers import identity_initializer
__all__ = [
 'ln_lstm', 'gru']

@func_scope()
def ln_lstm(output_size):
    return tf.contrib.rnn.LayerNormBasicLSTMCell(output_size)


@func_scope(initializer=identity_initializer)
def gru(output_size):
    return tf.contrib.rnn.GRUCell(output_size)