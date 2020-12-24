# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/assertion.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 908 bytes
import collections, numpy, tensorflow as tf
from .util import func_scope
__all__ = [
 'is_int',
 'is_natural_num',
 'is_natural_num_sequence',
 'is_sequence',
 'assert_no_nan']

def is_int(num):
    return isinstance(num, int) or isinstance(num, numpy.integer) or isinstance(num, numpy.ndarray) and num.ndim == 0 and issubclass(num.dtype.type, numpy.integer)


def is_natural_num(num):
    return is_int(num) and num > 0


def is_natural_num_sequence(num_list, length=None):
    return is_sequence(num_list) and all(is_natural_num(num) for num in num_list) and (length == None or len(num_list) == length)


def is_sequence(obj):
    return isinstance(obj, collections.Sequence)


@func_scope()
def assert_no_nan(tensor):
    return tf.assert_equal(tf.reduce_any(tf.is_nan(tensor)), False)