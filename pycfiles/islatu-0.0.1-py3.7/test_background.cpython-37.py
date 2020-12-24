# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/islatu/tests/test_background.py
# Compiled at: 2020-04-22 03:20:28
# Size of source mod 2**32: 1840 bytes
"""
Tests for background module
"""
from unittest import TestCase
import numpy as np
from numpy.testing import assert_equal, assert_almost_equal
from uncertainties import unumpy as unp
from islatu import background

class TestBackground(TestCase):
    __doc__ = '\n    Unit tests for background module\n    '

    def test_bivariate_normal(self):
        """
        A simple test for the generation of a bivariate normal distribution.
        """
        x_1 = np.linspace(-1, 1, 100)
        x_2 = np.linspace(-1, 1, 100)
        input_x = np.array([x_1, x_2])
        abscissa = np.array(np.mgrid[0:len(input_x[0]):1, 0:len(input_x[1]):1])
        output = background.bivariate_normal(abscissa, 0, 0, 1, 1, 1, 10)
        assert_equal(10000, output.size)
        output = output.reshape((100, 100))
        max_inten = np.unravel_index(np.argmax(output, axis=None), output.shape)
        assert_equal([0, 0], max_inten)

    def test_fit_gaussian_2d(self):
        """
        Test the fitting of a 2-d gaussian function.
        """
        x_1 = np.linspace(-1, 1, 10)
        x_2 = np.linspace(-1, 1, 10)
        input_x = np.array([x_1, x_2])
        abscissa = np.array(np.mgrid[0:len(input_x[0]):1, 0:len(input_x[1]):1])
        to_fit = background.bivariate_normal(abscissa, 0, 0, 1, 1, 15, 10)
        to_fit = to_fit.reshape((10, 10))
        to_fit_e = to_fit * 0.1
        result = background.fit_gaussian_2d(to_fit, to_fit_e)
        assert_almost_equal(unp.nominal_values(result[0]), [0, 0, 1, 1, 15, 10])
        assert_equal(4, result[1])
        assert_equal(2, result[2])