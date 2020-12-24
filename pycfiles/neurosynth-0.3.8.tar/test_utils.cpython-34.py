# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/tests/test_utils.py
# Compiled at: 2015-01-24 15:30:45
# Size of source mod 2**32: 855 bytes
import unittest
from neurosynth.utils import *
import warnings

class TestUtils(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('always', DeprecationWarning)

    def test_deprecated_decorator(self):

        @deprecated
        def add_three_without_args(val):
            return val + 3

        @deprecated('111')
        def add_five_with_args(val):
            return val + 5

        with warnings.catch_warnings(record=True) as (w):
            i = add_three_without_args(5)
            self.assertEqual(i, 8)
            self.assertTrue(issubclass(w[(-1)].category, DeprecationWarning))
            self.assertTrue(str(w[(-1)].message).startswith('Function'))
            i = add_five_with_args(5)
            self.assertEqual(i, 10)
            self.assertEqual(len(w), 2)
            self.assertEqual(str(w[(-1)].message), '111')