# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/islatu/tests/test_corrections.py
# Compiled at: 2020-04-22 03:20:25
# Size of source mod 2**32: 973 bytes
"""
Tests for corrections module
"""
from unittest import TestCase
import numpy as np
from numpy.testing import assert_almost_equal
from uncertainties import ufloat
from islatu import corrections

class TestCorrections(TestCase):
    __doc__ = '\n    Unit tests for corrections module\n    '

    def test_geometry_correction(self):
        """
        Test the implementation of the geometry correction.
        """
        beam_width = 5e-05
        sample_size = ufloat(0.002, 1e-05)
        theta = np.array([0.01, 0.2])
        result = corrections.footprint_correction(beam_width, sample_size, theta)
        assert_almost_equal(result[0].n, 0.006558435584346212)
        assert_almost_equal(result[1].n, 0.1305814681032167)