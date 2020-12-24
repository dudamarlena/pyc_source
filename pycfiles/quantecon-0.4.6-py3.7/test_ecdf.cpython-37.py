# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/tests/test_ecdf.py
# Compiled at: 2018-11-25 18:01:46
# Size of source mod 2**32: 856 bytes
"""
Tests for ecdf.py

"""
import unittest, numpy as np
from quantecon import ECDF

class TestECDF(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.obs = np.random.rand(40)
        cls.ecdf = ECDF(cls.obs)

    def test_call_high(self):
        """ecdf: x above all obs give 1.0"""
        self.assertAlmostEqual(self.ecdf(1.1), 1.0)

    def test_call_low(self):
        """ecdf: x below all obs give 0.0"""
        self.assertAlmostEqual(self.ecdf(-0.1), 0.0)

    def test_ascending(self):
        """ecdf: larger values should return F(x) at least as big"""
        x = np.random.rand()
        F_1 = self.ecdf(x)
        F_2 = self.ecdf(1.1 * x)
        self.assertGreaterEqual(F_2, F_1)