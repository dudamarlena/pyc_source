# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_fit_result.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 5842 bytes
import warnings
from unittest import TestCase
import numpy as np
from eddington_core import FitResult

class FitResultBaseTestCase:
    decimal = 5

    def setUp(self):
        self.fit_result = FitResult(a0=(self.a0),
          a=(self.a),
          aerr=(self.aerr),
          acov=(self.acov),
          chi2=(self.chi2),
          degrees_of_freedom=(self.degrees_of_freedom))

    def test_a0(self):
        np.testing.assert_almost_equal((self.fit_result.a0),
          (self.a0),
          decimal=(self.decimal),
          err_msg='Initial Guess is different than expected')

    def test_a(self):
        np.testing.assert_almost_equal((self.fit_result.a),
          (self.a),
          decimal=(self.decimal),
          err_msg='Calculated parameters are different than expected')

    def test_aerr(self):
        np.testing.assert_almost_equal((self.fit_result.aerr),
          (self.aerr),
          decimal=(self.decimal),
          err_msg='Parameters errors are different than expected')

    def test_arerr(self):
        np.testing.assert_almost_equal((self.fit_result.arerr),
          (self.arerr),
          decimal=(self.decimal),
          err_msg='Parameters relative errors are different than expected')

    def test_acov(self):
        np.testing.assert_almost_equal((self.fit_result.acov),
          (self.acov),
          decimal=(self.decimal),
          err_msg='Parameters covariance is different than expected')

    def test_chi2(self):
        self.assertAlmostEqual((self.fit_result.chi2),
          (self.chi2),
          places=(self.decimal),
          msg='Chi2 is different than expected')

    def test_chi2_reduced(self):
        self.assertAlmostEqual((self.fit_result.chi2_reduced),
          (self.chi2_reduced),
          places=(self.decimal),
          msg='Chi2 reduced is different than expected')

    def test_degrees_of_freedom(self):
        self.assertEqual((self.fit_result.degrees_of_freedom),
          (self.degrees_of_freedom),
          msg='Degrees of freedom are different than expected')

    def test_p_probability(self):
        self.assertAlmostEqual((self.fit_result.p_probability),
          (self.p_probability),
          places=(self.decimal),
          msg='Chi2 reduced is different than expected')

    def test_representation(self):
        self.assertEqual((self.repr_string),
          (str(self.fit_result)),
          msg='Representation is different than expected')


class TestStandardFitResult(TestCase, FitResultBaseTestCase):
    a0 = np.array([1.0, 3.0])
    a = np.array([1.1, 2.98])
    aerr = np.array([0.1, 0.76])
    acov = np.array([[0.01, 2.3], [2.3, 0.988]])
    chi2 = 8.276
    degrees_of_freedom = 5
    chi2_reduced = 1.6552
    p_probability = 0.14167
    arerr = np.array([9.09091, 25.50336])
    repr_string = "Results:\n========\n\nInitial parameters' values:\n\t1.0 3.0\nFitted parameters' values:\n\ta[0] = 1.100 ± 0.1000 (9.091% error)\n\ta[1] = 2.980 ± 0.7600 (25.503% error)\nFitted parameters covariance:\n[[0.01  2.3  ]\n [2.3   0.988]]\nChi squared: 8.276\nDegrees of freedom: 5\nChi squared reduced: 1.655\nP-probability: 0.1417\n"

    def setUp(self):
        FitResultBaseTestCase.setUp(self)


class TestFitResultWithZeroError(TestCase, FitResultBaseTestCase):
    a0 = np.array([1.0, 3.0])
    a = np.array([1.1, 2.98])
    aerr = np.array([0.0, 0.0])
    acov = np.array([[0.0, 0.0], [0.0, 0.0]])
    chi2 = 8.276
    degrees_of_freedom = 5
    chi2_reduced = 1.6552
    p_probability = 0.14167
    arerr = np.array([0.0, 0.0])
    repr_string = "Results:\n========\n\nInitial parameters' values:\n\t1.0 3.0\nFitted parameters' values:\n\ta[0] = 1.100 ± 0.000 (0.000% error)\n\ta[1] = 2.980 ± 0.000 (0.000% error)\nFitted parameters covariance:\n[[0. 0.]\n [0. 0.]]\nChi squared: 8.276\nDegrees of freedom: 5\nChi squared reduced: 1.655\nP-probability: 0.1417\n"

    def setUp(self):
        FitResultBaseTestCase.setUp(self)


class TestFitResultWithZeroValue(TestCase, FitResultBaseTestCase):
    a0 = np.array([1.0, 3.0])
    a = np.array([0.0, 0.0])
    aerr = np.array([0.1, 0.76])
    acov = np.array([[0.01, 2.3], [2.3, 0.988]])
    chi2 = 8.276
    degrees_of_freedom = 5
    chi2_reduced = 1.6552
    p_probability = 0.14167
    arerr = np.array([np.inf, np.inf])
    repr_string = "Results:\n========\n\nInitial parameters' values:\n\t1.0 3.0\nFitted parameters' values:\n\ta[0] = 0.000 ± 0.1000 (inf% error)\n\ta[1] = 0.000 ± 0.7600 (inf% error)\nFitted parameters covariance:\n[[0.01  2.3  ]\n [2.3   0.988]]\nChi squared: 8.276\nDegrees of freedom: 5\nChi squared reduced: 1.655\nP-probability: 0.1417\n"

    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=RuntimeWarning)
            FitResultBaseTestCase.setUp(self)


class TestFitResultWithSmallPProbability(TestCase, FitResultBaseTestCase):
    a0 = np.array([1.0, 3.0])
    a = np.array([1.1, 2.98])
    aerr = np.array([0.1, 0.76])
    acov = np.array([[0.01, 2.3], [2.3, 0.988]])
    chi2 = 43.726
    degrees_of_freedom = 5
    chi2_reduced = 8.7452
    p_probability = 2.63263e-08
    arerr = np.array([9.09091, 25.50336])
    repr_string = "Results:\n========\n\nInitial parameters' values:\n\t1.0 3.0\nFitted parameters' values:\n\ta[0] = 1.100 ± 0.1000 (9.091% error)\n\ta[1] = 2.980 ± 0.7600 (25.503% error)\nFitted parameters covariance:\n[[0.01  2.3  ]\n [2.3   0.988]]\nChi squared: 43.726\nDegrees of freedom: 5\nChi squared reduced: 8.745\nP-probability: 2.633e-08\n"

    def setUp(self):
        FitResultBaseTestCase.setUp(self)