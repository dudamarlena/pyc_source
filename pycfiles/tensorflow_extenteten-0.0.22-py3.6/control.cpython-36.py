# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/control.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 870 bytes
import functools, tensorflow as tf
from .util import func_scope
__all__ = [
 'unpack_to_array', 'with_dependencies', 'sequential']

@func_scope()
def unpack_to_array(tensor):
    return tf.TensorArray(tensor.dtype, tf.shape(tensor)[0]).unpack(tensor)


@func_scope()
def with_dependencies(dependencies, tensor):
    """
    This function is documented partially in tensorflow.org.
    But, it cannot be found in a library.
    """
    with tf.control_dependencies(dependencies):
        if isinstance(tensor, tf.Tensor):
            return tf.identity(tensor)
        if isinstance(tensor, tf.Operation):
            return tf.group(tensor)
        raise ValueError('{} must be tf.Tensor or tf.Operation.'.format(tensor))


@func_scope()
def sequential(*ops):
    return functools.reduce(lambda x, y: with_dependencies([x], y), ops)