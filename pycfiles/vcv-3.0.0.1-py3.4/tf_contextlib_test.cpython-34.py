# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/tf_contextlib_test.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 3075 bytes
"""Unit tests for tf_contextlib."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tensorflow.python.platform import test
from tensorflow.python.util import tf_contextlib
from tensorflow.python.util import tf_decorator
from tensorflow.python.util import tf_inspect

@tf_contextlib.contextmanager
def test_yield_append_before_and_after_yield(x, before, after):
    x.append(before)
    yield
    x.append(after)


@tf_contextlib.contextmanager
def test_yield_return_x_plus_1(x):
    yield x + 1


@tf_contextlib.contextmanager
def test_params_and_defaults(a, b=2, c=True, d='hello'):
    return [a, b, c, d]


class TfContextlibTest(test.TestCase):

    def testRunsCodeBeforeYield(self):
        x = []
        with test_yield_append_before_and_after_yield(x, 'before', ''):
            self.assertEqual('before', x[(-1)])

    def testRunsCodeAfterYield(self):
        x = []
        with test_yield_append_before_and_after_yield(x, '', 'after'):
            pass
        self.assertEqual('after', x[(-1)])

    def testNestedWith(self):
        x = []
        with test_yield_append_before_and_after_yield(x, 'before', 'after'):
            with test_yield_append_before_and_after_yield(x, 'inner', 'outer'):
                with test_yield_return_x_plus_1(1) as (var):
                    x.append(var)
        self.assertEqual(['before', 'inner', 2, 'outer', 'after'], x)

    def testMultipleCallsOfSeparateInstances(self):
        x = []
        with test_yield_append_before_and_after_yield(x, 1, 2):
            pass
        with test_yield_append_before_and_after_yield(x, 3, 4):
            pass
        self.assertEqual([1, 2, 3, 4], x)

    def testReturnsResultFromYield(self):
        with test_yield_return_x_plus_1(3) as (result):
            self.assertEqual(4, result)

    def testUnwrapContextManager(self):
        decorators, target = tf_decorator.unwrap(test_params_and_defaults)
        self.assertEqual(1, len(decorators))
        self.assertTrue(isinstance(decorators[0], tf_decorator.TFDecorator))
        self.assertEqual('contextmanager', decorators[0].decorator_name)
        self.assertFalse(isinstance(target, tf_decorator.TFDecorator))

    def testGetArgSpecReturnsWrappedArgSpec(self):
        argspec = tf_inspect.getargspec(test_params_and_defaults)
        self.assertEqual(['a', 'b', 'c', 'd'], argspec.args)
        self.assertEqual((2, True, 'hello'), argspec.defaults)


if __name__ == '__main__':
    test.main()