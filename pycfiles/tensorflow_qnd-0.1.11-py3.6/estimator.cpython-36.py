# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/estimator.py
# Compiled at: 2017-05-17 13:39:44
# Size of source mod 2**32: 1728 bytes
import functools, inspect, typing, tensorflow as tf, tensorflow.contrib.learn as learn
from . import util
from .config import def_config

def def_estimator(distributed=False):
    config = def_config(distributed)

    @util.func_scope
    def estimator(model_fn, model_dir):
        return tf.contrib.learn.Estimator((_wrap_model_fn(model_fn)), config=(config()),
          model_dir=model_dir)

    return estimator


def _wrap_model_fn(original_model_fn):

    @util.func_scope
    def model(features, targets, mode):
        are_args = functools.partial(util.are_instances, [features, targets])
        def_model_fn = functools.partial(functools.partial, original_model_fn)
        if are_args(tf.Tensor):
            model_fn = def_model_fn(features, targets)
        else:
            if are_args(dict):
                model_fn = def_model_fn(**features, **targets)
            elif isinstance(features, tf.Tensor):
                if targets is None:
                    model_fn = def_model_fn(features)
            elif isinstance(features, dict):
                if targets is None:
                    model_fn = def_model_fn(**features)
            else:
                raise ValueError('features and targets should be both tf.Tensor or dict.')
        results = model_fn(mode=mode) if 'mode' in inspect.signature(model_fn).parameters.keys() else model_fn()
        if isinstance(results, learn.ModelFnOps):
            return results
        else:
            return (learn.ModelFnOps)(mode, *results if isinstance(results, typing.Sequence) else (
             results,))

    return model