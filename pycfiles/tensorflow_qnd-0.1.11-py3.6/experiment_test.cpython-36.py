# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/experiment_test.py
# Compiled at: 2017-05-17 13:34:19
# Size of source mod 2**32: 583 bytes
import types, tensorflow as tf
from . import test
from . import experiment
from . import inputs_test

def test_def_experiment():
    append_argv()
    def_experiment_fn = experiment.def_def_experiment_fn()
    _assert_is_function(def_experiment_fn)
    experiment_fn = def_experiment_fn(test.oracle_model, test.user_input_fn)
    _assert_is_function(experiment_fn)
    assert isinstance(experiment_fn('output'), tf.contrib.learn.Experiment)


def _assert_is_function(obj):
    assert isinstance(obj, types.FunctionType)


def append_argv():
    inputs_test.append_argv()