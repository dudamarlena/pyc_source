# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/variable.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 562 bytes
import functools, tensorflow as tf
from .assertion import is_natural_num_sequence
__all__ = [
 'variable']

def variable(shape_or_initial, name=None):
    create_variable = functools.partial((tf.Variable), name=name)
    if is_natural_num_sequence(shape_or_initial):
        shape = shape_or_initial
        return create_variable(tf.contrib.layers.xavier_initializer() if len(shape) == 2 else tf.truncated_normal_initializer(stddev=0.1)(shape))
    else:
        initial = shape_or_initial
        return create_variable(initial)