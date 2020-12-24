# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/keyword_args_test.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 1804 bytes
"""Keyword args tests."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tensorflow.python.platform import test
from tensorflow.python.util import keyword_args

class KeywordArgsTest(test.TestCase):

    def test_keyword_args_only(self):

        def func_without_decorator(a, b):
            return a + b

        @keyword_args.keyword_args_only
        def func_with_decorator(a, b):
            return func_without_decorator(a, b)

        self.assertEqual(3, func_without_decorator(1, 2))
        self.assertEqual(3, func_without_decorator(a=1, b=2))
        self.assertEqual(3, func_with_decorator(a=1, b=2))
        with self.assertRaisesRegexp(ValueError, 'Must use keyword args to call func_with_decorator.'):
            self.assertEqual(3, func_with_decorator(1, 2))
        with self.assertRaisesRegexp(ValueError, 'Must use keyword args to call func_with_decorator.'):
            self.assertEqual(3, func_with_decorator(1, b=2))


if __name__ == '__main__':
    test.main()