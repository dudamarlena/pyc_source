# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qnd/inputs_test.py
# Compiled at: 2017-05-17 13:34:19
# Size of source mod 2**32: 1040 bytes
import tensorflow as tf
from . import inputs
from . import test
_FILE_PATTERN = '*.md'

def test_def_input_fn():
    append_argv()
    for def_input_fn in [inputs.def_def_train_input_fn(),
     inputs.def_def_eval_input_fn()]:
        features, labels = def_input_fn(lambda queue: (queue.dequeue(),) * 2)()
        assert isinstance(features, tf.Tensor)
        assert isinstance(labels, tf.Tensor)
        features, labels = def_input_fn(test.user_input_fn)()
        assert isinstance(features, dict)
        assert isinstance(labels, dict)
        _assert_are_instances([*features.keys(), *labels.keys()], str)
        _assert_are_instances([
         *features.values(), *labels.values()], tf.Tensor)


def _assert_are_instances(objects, klass):
    for obj in objects:
        assert isinstance(obj, klass)


def append_argv():
    test.append_argv('--train_file', _FILE_PATTERN, '--eval_file', _FILE_PATTERN)