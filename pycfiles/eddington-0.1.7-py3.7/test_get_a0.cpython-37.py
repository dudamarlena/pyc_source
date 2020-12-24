# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/input_data/test_get_a0.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 888 bytes
from unittest import TestCase
import numpy as np
from eddington.input.util import get_a0

class TestGetDataReturnsNone(TestCase):
    decimal = 5

    def setUp(self):
        self.a0 = None
        self.size = None

    def check(self):
        a0 = get_a0(self.size, self.a0)
        np.testing.assert_almost_equal(a0,
          (self.expected_a0),
          decimal=(self.decimal),
          err_msg='Initial guess is different than expected')

    def test_get_a0_with_size_2(self):
        self.size = 2
        self.expected_a0 = np.array([1, 1])
        self.check()

    def test_get_a0_with_size_3(self):
        self.size = 3
        self.expected_a0 = np.array([1, 1, 1])
        self.check()

    def test_get_a0_with_actual_a0(self):
        a0 = np.array([1.6, 2, 4.82])
        self.a0 = a0
        self.expected_a0 = a0
        self.check()