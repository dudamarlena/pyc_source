# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/input_data/test_random.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 7305 bytes
from unittest import TestCase
from mock import patch, call
import numpy as np
from eddington_core import linear
from eddington.consts import DEFAULT_MIN_COEFF, DEFAULT_MAX_COEFF, DEFAULT_XMIN, DEFAULT_XMAX, DEFAULT_XSIGMA, DEFAULT_YSIGMA
from eddington.input.random import random_parameters, random_data

class RandomsBaseTestCase:

    def setUp(self):
        random_patcher = patch('eddington.input.random.np.random')
        self.np_random = random_patcher.start()
        self.addCleanup(random_patcher.stop)


class TestRandomParameters(TestCase, RandomsBaseTestCase):
    expected = np.array([3, 2])
    size = 2

    def setUp(self):
        RandomsBaseTestCase.setUp(self)
        self.np_random.uniform.return_value = self.expected

    def check_result(self, actual):
        np.testing.assert_equal(actual,
          (self.expected), err_msg='Random parameters returns unexpected result')

    def check_uniform_call(self, min_coeff, max_coeff):
        self.np_random.uniform.assert_called_once_with(min_coeff,
          max_coeff, size=(self.size))

    def test_default_min_and_max(self):
        actual = random_parameters(self.size)
        self.check_result(actual)
        self.check_uniform_call(min_coeff=DEFAULT_MIN_COEFF,
          max_coeff=DEFAULT_MAX_COEFF)

    def test_set_min_coeff(self):
        min_coeff = 4
        actual = random_parameters(2, min_coeff=min_coeff)
        self.check_result(actual)
        self.check_uniform_call(min_coeff=min_coeff, max_coeff=DEFAULT_MAX_COEFF)

    def test_set_max_coeff(self):
        max_coeff = 7
        actual = random_parameters(2, max_coeff=max_coeff)
        self.check_result(actual)
        self.check_uniform_call(min_coeff=DEFAULT_MIN_COEFF, max_coeff=max_coeff)

    def test_set_min_and_max_coeff(self):
        min_coeff = 4
        max_coeff = 7
        actual = random_parameters(2, min_coeff=min_coeff, max_coeff=max_coeff)
        self.check_result(actual)
        self.check_uniform_call(min_coeff=min_coeff, max_coeff=max_coeff)


class RandomDataFrameBaseTestCase(RandomsBaseTestCase):
    decimal = 5
    func = linear
    a = np.array([1, 2])
    x = np.array([3, 5, 9, 20, 25])
    xerr = np.array([0.1, 0.4, 0.8, 0.25, 0.9])
    yerr = np.array([0.24, 0.25, 0.42, 0.01, 0.3])
    actual_xerr = np.array([0.2, 0.35, 0.79, 0.15, 0.7])
    actual_yerr = np.array([0.22, 0.31, 0.4, 0.07, 0.1])
    y = np.array([7.62, 12.01, 20.98, 41.37, 52.5])
    measurements = 5
    xmin = DEFAULT_XMIN
    xmax = DEFAULT_XMAX
    xsigma = DEFAULT_XSIGMA
    ysigma = DEFAULT_YSIGMA

    def setUp(self):
        RandomsBaseTestCase.setUp(self)
        self.np_random.uniform.return_value = self.x
        self.np_random.exponential.side_effect = [self.xerr, self.yerr]
        self.np_random.normal.side_effect = [self.actual_xerr, self.actual_yerr]

    def test_x(self):
        np.testing.assert_equal((self.data['x']),
          (self.x), err_msg='X is different than expected')

    def test_y(self):
        np.testing.assert_almost_equal((self.data['y']),
          (self.y),
          decimal=(self.decimal),
          err_msg='Y is different than expected')

    def test_xerr(self):
        np.testing.assert_equal((self.data['xerr']),
          (self.xerr), err_msg='X error is different than expected')

    def test_yerr(self):
        np.testing.assert_equal((self.data['yerr']),
          (self.yerr), err_msg='Y error is different than expected')

    def test_uniform_mock_callings(self):
        self.np_random.uniform.assert_called_once_with((self.xmin),
          (self.xmax), size=(self.measurements))

    def test_exponential_mock_calling(self):
        self.assertEqual(2,
          (self.np_random.exponential.call_count),
          msg='Exponential call count is different than expected')
        self.assertEqual(call(scale=(self.xsigma), size=(self.measurements)),
          (self.np_random.exponential.call_args_list[0]),
          msg='First exponential call is different than expected')
        self.assertEqual(call(scale=(self.ysigma), size=(self.measurements)),
          (self.np_random.exponential.call_args_list[1]),
          msg='Second exponential call is different than expected')

    def test_normal_mock_calling(self):
        self.assertEqual(2,
          (self.np_random.normal.call_count),
          msg='Normal call count is different than expected')
        self.assertEqual(call(scale=(self.xerr)),
          (self.np_random.normal.call_args_list[0]),
          msg='First normal call is different than expected')
        self.assertEqual(call(scale=(self.yerr)),
          (self.np_random.normal.call_args_list[1]),
          msg='Second normal call is different than expected')

    def test_keys_orders(self):
        self.assertEqual([
         'x', 'xerr', 'y', 'yerr'],
          (list(self.data.keys())),
          msg="Data's keys are different than expected")


class TestRandomDataWithDefaultParameters(TestCase, RandomDataFrameBaseTestCase):

    def setUp(self):
        RandomDataFrameBaseTestCase.setUp(self)
        self.data = random_data(func=(self.func),
          actual_a=(self.a),
          measurements=(self.measurements))


class TestRandomDataWithXMin(TestCase, RandomDataFrameBaseTestCase):
    xmin = 4

    def setUp(self):
        RandomDataFrameBaseTestCase.setUp(self)
        self.data = random_data(func=(self.func),
          actual_a=(self.a),
          measurements=(self.measurements),
          xmin=(self.xmin))


class TestRandomDataWithXMax(TestCase, RandomDataFrameBaseTestCase):
    xmax = 4

    def setUp(self):
        RandomDataFrameBaseTestCase.setUp(self)
        self.data = random_data(func=(self.func),
          actual_a=(self.a),
          measurements=(self.measurements),
          xmax=(self.xmax))


class TestRandomDataWithXSigma(TestCase, RandomDataFrameBaseTestCase):
    xsigma = 0.24

    def setUp(self):
        RandomDataFrameBaseTestCase.setUp(self)
        self.data = random_data(func=(self.func),
          actual_a=(self.a),
          measurements=(self.measurements),
          xsigma=(self.xsigma))


class TestRandomDataWithYSigma(TestCase, RandomDataFrameBaseTestCase):
    ysigma = 0.24

    def setUp(self):
        RandomDataFrameBaseTestCase.setUp(self)
        self.data = random_data(func=(self.func),
          actual_a=(self.a),
          measurements=(self.measurements),
          ysigma=(self.ysigma))


class TestRandomDataWithoutActualA(TestCase, RandomDataFrameBaseTestCase):

    def setUp(self):
        random_parameters_patcher = patch('eddington.input.random.random_parameters')
        random_parameters_mock = random_parameters_patcher.start()
        random_parameters_mock.return_value = self.a
        self.addCleanup(random_parameters_patcher.stop)
        RandomDataFrameBaseTestCase.setUp(self)
        self.data = random_data(func=(self.func),
          measurements=(self.measurements),
          ysigma=(self.ysigma))