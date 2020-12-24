# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/runtime.py
# Compiled at: 2019-04-01 10:58:04
# Size of source mod 2**32: 3821 bytes
"""
Module focused on evaluating tensors to makes the usage easier, forgetting about tensors and sessions
"""
import tensorflow as tf
from functools import wraps
from contextlib import contextmanager
__tf_run_default = True
runner_context = dict(runner_recursive_depth=0)

@contextmanager
def runner_scope():
    runner_context['runner_recursive_depth'] += 1
    try:
        yield
    finally:
        runner_context['runner_recursive_depth'] -= 1


def tf_run_allowed(f):
    """
    A function might return a tensor or not. In order to decide if the result of this function needs to be evaluated
    in a tf session or not, use the tf_run extra parameter or the tf_run_default value. If True, and this function is
    in the first level of execution depth, use a tf Session to evaluate the tensor or other evaluable object (like dicts)
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        global __tf_run_default
        if 'tf_run' in kwargs:
            tf_run = kwargs.pop('tf_run')
        else:
            tf_run = __tf_run_default
        with runner_scope():
            obj = f(*args, **kwargs)
            if tf_run and runner_context['runner_recursive_depth'] == 1:
                try:
                    with tf.Session() as (sess):
                        sess.run(tf.global_variables_initializer())
                        ev_obj = sess.run(obj)
                    return ev_obj
                except (TypeError, ValueError):
                    return obj

            else:
                return obj

    return wrapper


def tf_run_ignored(f):
    """
    A function might call other functions decorated with tf_run_allowed.
    This decorator is used to avoid that such functions are evaluated.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        with runner_scope():
            return f(*args, **kwargs)

    return wrapper


def set_tf_run(enable):
    global __tf_run_default
    __tf_run_default = enable