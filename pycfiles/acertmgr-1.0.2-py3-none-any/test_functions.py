# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\acerim\tests\test_functions.py
# Compiled at: 2017-09-24 21:08:15
__doc__ = '\nSuite of unittests for functions found in /acerim/acefunctions.py.\n'
from __future__ import division, print_function, absolute_import
import os, unittest, numpy as np, acerim
from acerim import acefunctions as af
from acerim import aceclasses as ac
DATA_PATH = os.path.join(acerim.__path__[0], 'sample')

class Test_compute_stats(unittest.TestCase):
    """Test computeStats function"""
    crater_csv = os.path.join(DATA_PATH, 'craters.csv')
    cdf = ac.CraterDataFrame(crater_csv)
    test_dataset = os.path.join(DATA_PATH, 'moon.tif')
    ads = ac.AceDataset(test_dataset, radius=1737)

    def test_first_mean(self):
        """Test mean on first crater in cdf"""
        pass


class Test_circle_mask(unittest.TestCase):
    """Test ring_mask function"""

    def test_trivial(self):
        """Test radius 0"""
        actual = af.circle_mask(np.ones((3, 3)), 0)
        expected = np.array([[False, False, False],
         [
          False, False, False],
         [
          False, False, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))

    def test_odd(self):
        """Test roi with odd side length"""
        actual = af.circle_mask(np.ones((5, 5)), 2)
        expected = np.array([[False, False, True, False, False],
         [
          False, True, True, True, False],
         [
          True, True, True, True, True],
         [
          False, True, True, True, False],
         [
          False, False, True, False, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))

    def test_even(self):
        """Test roi with even side length"""
        actual = af.circle_mask(np.ones((4, 4)), 2)
        expected = np.array([[False, True, True, False],
         [
          True, True, True, True],
         [
          True, True, True, True],
         [
          False, True, True, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))

    def test_offcenter(self):
        """Test specifying off center location"""
        actual = af.circle_mask(np.ones((5, 5)), 2, center=(3, 2))
        expected = np.array([[False, False, False, True, False],
         [
          False, False, True, True, True],
         [
          False, True, True, True, True],
         [
          False, False, True, True, True],
         [
          False, False, False, True, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))


class Test_ring_mask(unittest.TestCase):
    """Test ring_mask function"""

    def test_trivial(self):
        actual = af.ring_mask(np.ones((3, 3)), 0, 0)
        expected = np.array([[False, False, False],
         [
          False, False, False],
         [
          False, False, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))

    def test_odd(self):
        """Test roi with odd side length"""
        actual = af.ring_mask(np.ones((5, 5)), 1, 2)
        expected = np.array([[False, False, True, False, False],
         [
          False, True, False, True, False],
         [
          True, False, False, False, True],
         [
          False, True, False, True, False],
         [
          False, False, True, False, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))

    def test_even(self):
        """Test roi with even side length"""
        actual = af.ring_mask(np.ones((4, 4)), 1.5, 2)
        expected = np.array([[False, True, True, False],
         [
          True, False, False, True],
         [
          True, False, False, True],
         [
          False, True, True, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))

    def test_offcenter(self):
        """Test specifying off center location"""
        actual = af.ring_mask(np.ones((5, 5)), 1, 2, center=(3, 2))
        expected = np.array([[False, False, False, True, False],
         [
          False, False, True, False, True],
         [
          False, True, False, False, False],
         [
          False, False, True, False, True],
         [
          False, False, False, True, False]])
        self.assertIsNone(np.testing.assert_array_equal(actual, expected))


class Test_m2deg(unittest.TestCase):
    """Test m2deg functions"""

    def test_basic(self):
        """Test simple"""
        actual = af.m2deg(400, 10, 20)
        expected = 2.0
        self.assertEqual(actual, expected)

    def test_float(self):
        """Test float"""
        actual = af.m2deg(1500.0, 4.0, 0.25)
        expected = 1500.0
        self.assertEqual(actual, expected)