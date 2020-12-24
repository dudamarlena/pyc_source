# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dafne/SalientRegions/SalientDetector-python/tests/test_helpers.py
# Compiled at: 2016-07-15 03:43:36
"""
Testing the helper functions.
"""
from __future__ import absolute_import
from __future__ import print_function
from .context import salientregions as sr
import unittest, cv2, os, numpy as np

class HelpersEllipseTester(unittest.TestCase):
    """
    Tests for the helper functions related to ellipses
    """

    def setUp(self):
        """
        Load the binary masks to make ellipses from, and create the ground truths.
        """
        self.half_major_axis_len = 15
        self.half_minor_axis_len = 9
        self.theta = 0.52
        self.standard_coeff = [
         0.006395179230685,
         -0.0034070290459,
         0.010394944226105]
        testdata_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images/Binary/'))
        self.ellipse1_mask = np.array(cv2.imread(os.path.join(testdata_path, 'Binary_ellipse1.png'), cv2.IMREAD_GRAYSCALE))
        self.features_standard_ellipse1 = np.array([200, 175, 34, 14, 0, 2])
        self.features_poly_ellipse1 = 100.0 * np.array([
         2.0,
         1.75,
         8.650519031e-06,
         -0.0,
         5.1020408163e-05,
         0.02])
        self.ellipse2_mask = np.array(cv2.imread(os.path.join(testdata_path, 'Binary_ellipse2.png'), cv2.IMREAD_GRAYSCALE))
        self.features_standard_ellipse2 = np.array([187, 38.5, 10, 5, 90, 2])
        self.features_poly_ellipse2 = 100.0 * np.array([1.87,
         0.385,
         0.0004,
         0.0,
         0.0001,
         0.02])
        self.ellipse3_mask = np.array(cv2.imread(os.path.join(testdata_path, 'Binary_ellipse3.png'), cv2.IMREAD_GRAYSCALE))
        self.features_standard_ellipse3 = np.array([
         101.9, 90.4, 24, 21, -9.9, 2])
        self.features_poly_ellipse3 = 100.0 * np.array([
         1.019717800289436,
         0.904095513748191,
         1.7518811785e-05,
         -9.01804067e-07,
         2.2518036288e-05,
         0.02])
        self.ellipse4_mask = np.array(cv2.imread(os.path.join(testdata_path, 'Binary_ellipse4.png'), cv2.IMREAD_GRAYSCALE))
        self.features_standard_ellipse4 = np.array([
         65.3, 186, 28, 13, 50.8, 2])
        self.features_poly_ellipse4 = 100.0 * np.array([0.653333333333333,
         1.860687093779016,
         4.0675758984e-05,
         2.2724787475e-05,
         3.125094069e-05,
         0.02])
        self.connectivty = 4
        self.rtol = 2
        self.atol = 0.01
        self.num_regions = 7
        self.num_holes = 1
        self.num_islands = 2
        self.num_indent = 3
        self.num_protr = 1
        self.features = {}
        features_testpath = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'features/'))
        self.features_filename = os.path.join(features_testpath, 'ellipse_features.txt')

    def test_standard2poly_ellipse(self):
        """
        Test the function `standard2poly_ellipse`.
        """
        A, B, C = sr.helpers.standard2poly_ellipse(self.half_major_axis_len, self.half_minor_axis_len, self.theta)
        coeff = [A, B, C]
        assert sr.helpers.array_diff(self.standard_coeff, coeff)

    def test_poly2standard_ellipse(self):
        """
        Test the function `poly2standard_ellipse`.
        """
        params = sr.helpers.poly2standard_ellipse(self.standard_coeff[0], self.standard_coeff[1], self.standard_coeff[2])
        print('Parameters:', params)
        true_params = [
         self.half_major_axis_len,
         self.half_minor_axis_len,
         self.theta]
        print('True parameters:', true_params)
        assert sr.helpers.array_diff(params, true_params, 1e-05, 1e-08)

    def test_mask2features_poly_ellipse1(self):
        """
        Test the function `binary_mask2ellipse_features_single` for test image 1.
        """
        _, _, features = sr.helpers.binary_mask2ellipse_features_single(self.ellipse1_mask, self.connectivty, 2, True)
        print('MATLAB features:', self.features_poly_ellipse1)
        print('Python features:', features)
        print('Difference: ', features - self.features_poly_ellipse1)
        print('Max abs. difference: ', np.max(np.max(np.abs(features - self.features_poly_ellipse1))))
        assert sr.helpers.array_diff(self.features_poly_ellipse1, features, self.rtol, self.atol)

    def test_mask2features_poly_ellipse2(self):
        """
        Test the function `binary_mask2ellipse_features_single` for test image 2.
        """
        _, _, features = sr.helpers.binary_mask2ellipse_features_single(self.ellipse2_mask, self.connectivty, 2, True)
        print('MATLAB features:', self.features_poly_ellipse2)
        print('Python features:', features)
        print('Difference: ', features - self.features_poly_ellipse2)
        print('Max abs.difference: ', np.max(np.max(np.abs(features - self.features_poly_ellipse2))))
        assert sr.helpers.array_diff(self.features_poly_ellipse2, features, self.rtol, self.atol)

    def test_mask2features_poly_ellipse3(self):
        """
        Test the function `binary_mask2ellipse_features_single` for test image 3.
        """
        _, _, features_poly = sr.helpers.binary_mask2ellipse_features_single(self.ellipse3_mask, self.connectivty, 2)
        assert sr.helpers.array_diff(self.features_poly_ellipse3, features_poly, self.rtol, self.atol)

    def test_mask2features_poly_ellipse4(self):
        """
        Test the function `binary_mask2ellipse_features_single` for test image 4.
        """
        _, _, features = sr.helpers.binary_mask2ellipse_features_single(self.ellipse4_mask, self.connectivty, 2)
        assert sr.helpers.array_diff(self.features_poly_ellipse4, features, self.rtol, self.atol)