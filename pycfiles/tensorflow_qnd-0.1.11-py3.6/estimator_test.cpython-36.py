# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/estimator_test.py
# Compiled at: 2017-06-19 06:21:17
# Size of source mod 2**32: 451 bytes
import tensorflow as tf
from . import test
from .estimator import *

def test_def_estimator():
    test.append_argv()
    if not isinstance(def_estimator()(test.oracle_model, 'output'), tf.contrib.learn.Estimator):
        raise AssertionError
    elif not isinstance(def_estimator()(lambda x, y: (tf.contrib.learn.ModelFnOps)(*('train', ), *test.oracle_model(x, y)), 'output'), tf.contrib.learn.Estimator):
        raise AssertionError