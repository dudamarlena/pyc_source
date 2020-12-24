# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/helpertest.py
# Compiled at: 2015-05-28 05:24:46
import unittest
from pycast.common.helper import *

class HelperTest(unittest.TestCase):
    """Test class containing all tests for pycasts helper module."""

    def linear_interpolation_test(self):
        """Testing linear interpolation."""
        val1 = 1.0
        val2 = 3.0
        result = linear_interpolation(val1, val2, 1)
        assert result == [2.0]
        val2 = 4.0
        result = linear_interpolation(val1, val2, 2)
        assert result == [2.0, 3.0]