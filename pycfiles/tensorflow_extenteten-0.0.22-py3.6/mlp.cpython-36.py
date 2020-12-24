# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/mlp.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 623 bytes
import functools, tensorflow as tf
from .assertion import is_natural_num_sequence
from .util import func_scope
from . import layer
__all__ = [
 'mlp']

@func_scope()
def mlp(x, *, layer_sizes, dropout_keep_prob=1, activate=tf.nn.elu):
    assert is_natural_num_sequence(layer_sizes)
    return layer.linear(functools.reduce(functools.partial((layer.fully_connected), dropout_keep_prob=dropout_keep_prob,
      activate=activate), layer_sizes[:-1], x), layer_sizes[(-1)])