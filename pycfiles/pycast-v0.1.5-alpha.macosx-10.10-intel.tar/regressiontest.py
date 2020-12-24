# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/regressiontest.py
# Compiled at: 2015-05-28 03:51:29
import unittest
from mock import patch
from pycast.common.timeseries import TimeSeries
from pycast.common.matrix import Matrix
from pycast.methods import Regression, LinearRegression

class RegressionTest(unittest.TestCase):
    """Test class for the Regression method."""

    def calculate_parameters_two_empty_list_test(self):
        """Test for ValueError if both Timeseries are empty"""
        tsOne = TimeSeries.from_twodim_list([])
        tsTwo = TimeSeries.from_twodim_list([])
        reg = Regression()
        self.assertRaises(ValueError, reg.calculate_parameters, tsOne, tsTwo)

    def calculate_parameters_one_empty_list_test(self):
        """Test for ValueError if one Timeseries are empty"""
        tsOne = TimeSeries.from_twodim_list([[1, 12.34]])
        tsTwo = TimeSeries.from_twodim_list([])
        reg = Regression()
        self.assertRaises(ValueError, reg.calculate_parameters, tsOne, tsTwo)

    def calculate_parameters_test(self):
        """Test the calculation of the parameters for the regression line."""
        data1 = [
         [
          1, 10.0], [7, 22.01], [2, 12.4], [3, 17.38], [4, 16.66],
         [
          5, 20.12], [6, 23.45], [8, 24.34], [9, 12.12]]
        data2 = [
         [
          1, 13.0], [2, 15.4], [3, 15.38], [4, 16.32], [10, 10.12],
         [
          5, 18.14], [6, 20.05], [7, 21.01], [8, 25.34]]
        tsSrc1 = TimeSeries.from_twodim_list(data1)
        tsSrc2 = TimeSeries.from_twodim_list(data2)
        expRes = (5.546941864140029, 0.6850537379535376)
        reg = Regression()
        res = reg.calculate_parameters(tsSrc1, tsSrc2)
        self.assertEquals(res, expRes)

    def calculate_parameters_without_match_test(self):
        """Test for ValueError, if the input timeseries have no macthing dates"""
        data1 = [
         [
          1, 12.42], [6, 12.32], [8, 12.45]]
        data2 = [[2, 32.45], [4, 23.12], [7, 65.34]]
        tsOne = TimeSeries.from_twodim_list(data1)
        tsTwo = TimeSeries.from_twodim_list(data2)
        reg = Regression()
        self.assertRaises(ValueError, reg.calculate_parameters, tsOne, tsTwo)

    def calculate_parameter_duplicate_dates_test(self):
        """Test for ValueError if dates in timeseries are not distinct"""
        data1 = [
         [
          1, 12.23], [4, 23.34]]
        data2 = [[1, 34.23], [1, 16.23]]
        tsSrc1 = TimeSeries.from_twodim_list(data1)
        tsSrc2 = TimeSeries.from_twodim_list(data2)
        reg = Regression()
        self.assertRaises(ValueError, reg.calculate_parameters, tsSrc1, tsSrc2)

    def calculate_parameter_with_short_timeseries_test(self):
        """Test for ValueError if Timeseries has only one matching date"""
        data1 = [
         [
          1, 12.23], [4, 23.34]]
        data2 = [[1, 34.23]]
        tsSrc1 = TimeSeries.from_twodim_list(data1)
        tsSrc2 = TimeSeries.from_twodim_list(data2)
        reg = Regression()
        self.assertRaises(ValueError, reg.calculate_parameters, tsSrc1, tsSrc2)

    def match_time_series_test(self):
        """Test if two timeseries are matched correctly"""
        data1 = [
         [
          1, 12.42], [4, 34.23], [7, 12.32], [8, 12.45]]
        data2 = [[2, 32.45], [7, 65.34], [4, 23.12], [5, 32.45]]
        tsSrc1 = TimeSeries.from_twodim_list(data1)
        tsSrc2 = TimeSeries.from_twodim_list(data2)
        dstX = [
         [
          4, 34.23], [7, 12.32]]
        dstY = [[4, 23.12], [7, 65.34]]
        reg = Regression()
        tsX, tsY = reg.match_time_series(tsSrc1, tsSrc2)
        self.assertEqual(tsX, dstX)
        self.assertEqual(tsY, dstY)

    def predict_test(self):
        """Test if given an independent timeseries and parameters the
        right prediction is done"""
        data1 = [
         [
          1, 1], [2, 2], [3, 3]]
        data2 = [[1, 3], [2, 5], [3, 7]]
        ts1 = TimeSeries.from_twodim_list(data1)
        ts2 = TimeSeries.from_twodim_list(data2)
        reg = Regression()
        result = reg.predict(ts1, 1, 2)
        self.assertEquals(ts2, result)

    def test_confidence_interval(self):
        """
        Test if given two timeseries and a desired confidence interval,
        regression gives us the correct over and underestimation.
        """
        data_x = zip(range(100), range(100))
        overestimations = [[90, 89], [91, 88], [92, 91], [93, 53], [94, 93]]
        underestimations = [[95, 100], [96, 97], [97, 101], [98, 101], [99, 100]]
        data_y = data_x[:90] + overestimations + underestimations
        ts_x = TimeSeries.from_twodim_list(data_x)
        ts_y = TimeSeries.from_twodim_list(data_y)
        with patch('pycast.common.timeseries.random.sample') as (sample_mock):
            sample_mock.return_value = underestimations + overestimations
            reg = Regression()
            n, m, error = reg.calculate_parameters_with_confidence(ts_x, ts_y, 0.6)
            self.assertEquals(0, n)
            self.assertEquals(1, m)
            self.assertEquals(error[0], -1)
            self.assertEquals(error[1], 3)


class LinearRegressionTest(unittest.TestCase):
    precision = 4

    def lstsq_test(self):
        """Test the least square method"""
        volumes = [
         [
          24], [20], [20], [20], [21], [30],
         [
          40], [20], [20], [20], [19], [35]]
        promoted = [
         [
          1, 0, 0, 0, 1],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 1, 0, 0, 0],
         [
          1, 0, 1, 0, 0],
         [
          1, 0, 0, 1, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 1, 0, 0, 0],
         [
          1, 0, 1, 0, 0]]
        expRes = [
         [
          19.999999999999993],
         [
          8.881784197001252e-15],
         [
          12.50000000000001],
         [
          20.000000000000007],
         [
          4.0]]
        volMatrix = Matrix(1, 12)
        volMatrix.initialize(volumes)
        proMatrix = Matrix(5, 12)
        proMatrix.initialize(promoted)
        resMatrix = LinearRegression.lstsq(proMatrix, volMatrix)
        for row in range(resMatrix.get_height()):
            for col in range(resMatrix.get_width()):
                self.assertAlmostEqual(resMatrix.get_value(col, row), expRes[row][col], self.precision)

    def lstsq_wrong_input_size_test(self):
        """Test for value error in lstsq method, if height of input matrices, does not match"""
        volumes = [
         [
          24], [20], [20], [20], [21], [30]]
        promoted = [
         [
          1, 0, 0, 0, 1],
         [
          1, 0, 0, 0, 0]]
        volMatrix = Matrix(1, 6)
        volMatrix.initialize(volumes)
        proMatrix = Matrix(5, 2)
        proMatrix.initialize(promoted)
        self.assertRaises(ValueError, LinearRegression.lstsq, proMatrix, volMatrix)

    def lstsq_matrix_test(self):
        """Test least square solution using a matrix with zero column"""
        volumes = [
         [
          24], [20], [20], [20], [21], [30],
         [
          40], [20], [20], [20], [19], [35]]
        promoted = [
         [
          1, 0, 0, 0, 1],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 1, 0, 0],
         [
          1, 0, 0, 1, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 1, 0, 0]]
        volMatrix = Matrix(1, 12)
        volMatrix.initialize(volumes)
        proMatrix = Matrix(5, 12)
        proMatrix.initialize(promoted)
        exRes = [
         [
          20.0],
         [
          2.18197426e-16],
         [
          12.5],
         [
          20.0],
         [
          4.0]]
        res = LinearRegression.lstsq(proMatrix, volMatrix)
        for row in xrange(len(exRes)):
            for col in xrange(len(exRes[0])):
                self.assertAlmostEqual(exRes[row][col], res.get_value(col, row), self.precision)

    def lstsq_value_error_test(self):
        """Test for the value error, if Matrix with dependent variable has more than 1 column"""
        volumes = [[23, 34], [12, 34], [14, 54]]
        promoted = [
         [
          1, 0, 0, 0, 1],
         [
          1, 0, 0, 0, 0],
         [
          1, 0, 0, 0, 0]]
        volMatrix = Matrix(2, 3)
        volMatrix.initialize(volumes)
        proMatrix = Matrix(5, 3)
        proMatrix.initialize(promoted)
        self.assertRaises(ValueError, LinearRegression.lstsq, proMatrix, volMatrix)