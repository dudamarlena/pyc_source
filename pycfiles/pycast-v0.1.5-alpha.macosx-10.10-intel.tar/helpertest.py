# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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