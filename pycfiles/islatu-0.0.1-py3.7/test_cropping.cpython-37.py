# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/islatu/tests/test_cropping.py
# Compiled at: 2020-04-22 02:40:45
# Size of source mod 2**32: 2816 bytes
"""
Tests for corrections module
"""
import unittest, numpy as np
from numpy.testing import assert_almost_equal
from islatu import cropping

class TestCropping(unittest.TestCase):
    __doc__ = '\n    Unit tests for cropping module\n    '

    def test_crop_2d_a(self):
        """
        Test crop_2d.
        """
        initial_array = np.ones((50, 50))
        expected_array = np.ones((20, 20))
        result = cropping.crop_2d(initial_array, 20, 40, 10, 30)
        assert_almost_equal(result, expected_array)

    def test_crop_2d_b(self):
        """
        Test crop_2d with rectanglar crop.
        """
        initial_array = np.ones((50, 50))
        expected_array = np.ones((20, 10))
        result = cropping.crop_2d(initial_array, 20, 40, 10, 20)
        assert_almost_equal(result, expected_array)

    def test_crop_around_peak_2d_a(self):
        """
        Test crop_around_peak_2d with custom.
        """
        initial_array = np.ones((50, 50))
        initial_array[(25, 25)] = 100
        expected_array = np.ones((10, 10))
        expected_array[(5, 5)] = 100
        result = cropping.crop_around_peak_2d(initial_array, x_size=10, y_size=10)
        assert_almost_equal(result, expected_array)

    def test_crop_around_peak_2d_b(self):
        """
        Test crop_around_peak_2d with defaults.
        """
        initial_array = np.ones((50, 50))
        initial_array[(25, 25)] = 100
        expected_array = np.ones((20, 20))
        expected_array[(10, 10)] = 100
        result = cropping.crop_around_peak_2d(initial_array)
        assert_almost_equal(result, expected_array)

    def test_crop_around_peak_2d_c(self):
        """
        Test crop_around_peak_2d with asymmetry.
        """
        initial_array = np.ones((50, 50))
        initial_array[(25, 25)] = 100
        expected_array = np.ones((10, 20))
        expected_array[(5, 10)] = 100
        result = cropping.crop_around_peak_2d(initial_array,
          x_size=10, y_size=20)
        assert_almost_equal(result, expected_array)

    def test_crop_around_peak_2d_error(self):
        """
        Test crop_around_peak_2d with uncertainty.
        """
        initial_array = np.ones((50, 50))
        initial_array[(25, 25)] = 100
        initial_array_e = initial_array * 0.1
        expected_array = np.ones((10, 10))
        expected_array[(5, 5)] = 100
        expected_array_e = expected_array * 0.1
        result = cropping.crop_around_peak_2d(initial_array, initial_array_e, x_size=10, y_size=10)
        assert_almost_equal(result[0], expected_array)
        assert_almost_equal(result[1], expected_array_e)