# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/errormeasuretest.py
# Compiled at: 2015-05-28 05:44:07
import unittest
from pycast.errors import BaseErrorMeasure
from pycast.common.timeseries import TimeSeries
from pycast.common.pycastobject import PyCastObject
from pycast.errors.meansquarederror import MeanSquaredError

class BaseErrorMeasureTest(unittest.TestCase):
    """Test class for the BaseErrorMeasure interface."""

    def initialization_test(self):
        """Test the BaseErrorMeasure initialization."""
        BaseErrorMeasure()
        for percentage in [-1.2, -0.1, 100.1, 123.9]:
            try:
                BaseErrorMeasure(percentage)
            except ValueError:
                pass
            else:
                assert False

        for percentage in [0.0, 12.3, 53.4, 100.0]:
            try:
                BaseErrorMeasure(percentage)
            except ValueError:
                assert False

    def get_error_initialization_test(self):
        """Test the get_error of BaseErrorMeasure for the initialization exception."""
        bem = BaseErrorMeasure()
        try:
            bem.get_error()
        except StandardError:
            pass
        else:
            assert False

    def double_initialize_test(self):
        """Test for the error ocuring when the same error measure is initialized twice."""
        data = [
         [
          0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)
        bem = BaseErrorMeasure()
        bem_calculate = bem._calculate
        bem_local_error = bem.local_error

        def return_zero(ignoreMe, ignoreMeToo):
            return 0

        bem.local_error = return_zero
        bem._calculate = return_zero
        bem.initialize(tsOrg, tsCalc)
        for cnt in xrange(10):
            try:
                bem.initialize(tsOrg, tsCalc)
            except StandardError:
                pass
            else:
                assert False

        bem.local_error = bem_calculate
        bem._calculate = bem_local_error

    def initialize_test(self):
        """Test if calculate throws an error as expected."""
        data = [
         [
          0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)
        bem = BaseErrorMeasure()
        try:
            bem.initialize(tsOrg, tsCalc)
        except NotImplementedError:
            pass
        else:
            assert False

        assert not bem.initialize(tsOrg, TimeSeries())

    def get_error_parameter_test(self):
        """Test for the parameter validity of get_error()."""
        data = [
         [
          0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)
        bem = BaseErrorMeasure()
        bem_calculate = bem._calculate
        bem_local_error = bem.local_error

        def return_zero(ignoreMe, ignoreMeToo, andMe=None, andMeToo=None):
            return 0

        bem.local_error = return_zero
        bem._calculate = return_zero
        bem.initialize(tsOrg, tsCalc)
        bem.local_error = bem_local_error
        bem._calculate = bem_calculate
        try:
            bem.get_error(10.0, 90.0)
        except NotImplementedError:
            pass
        else:
            assert False

        for start in [-1.0, 80.0, 103.0]:
            for end in [-5.0, 10.0, 105.0]:
                try:
                    bem.get_error(start, end)
                except ValueError:
                    pass
                else:
                    assert False

        return

    def local_error_test(self):
        """Test local_error of BaseErrorMeasure."""
        data = [
         [
          0.0, 0.0], [1, 0.1], [2, 0.2], [3, 0.3], [4, 0.4]]
        tsOrg = TimeSeries.from_twodim_list(data)
        tsCalc = TimeSeries.from_twodim_list(data)
        bem = BaseErrorMeasure()
        for idx in xrange(len(tsOrg)):
            try:
                bem.local_error([tsOrg[idx][1]], [tsCalc[idx][1]])
            except NotImplementedError:
                pass
            else:
                assert False

    def optimized_test(self):
        """Check if all tests are passed, using optimized implementations."""
        PyCastObject.enable_global_optimization()
        self.get_error_initialization_test()
        self.initialization_test()
        self.initialize_test()
        self.double_initialize_test()
        PyCastObject.disable_global_optimization()

    def confidence_interval_test(self):
        bem = BaseErrorMeasure()
        bem._errorValues = [
         10, -5, 3, -4, None, 0, 2, -3]
        self.assertRaises(ValueError, bem.confidence_interval, -0.5)
        self.assertRaises(ValueError, bem.confidence_interval, 2)
        self.assertEquals(bem.confidence_interval(0.5), (-3.0, 2.0))
        self.assertEquals(bem.confidence_interval(0.1), (0.0, 0.0))
        return

    def get_error_values_test(self):
        bem = BaseErrorMeasure()
        bem._errorValues = [1, -1, 3, -5, 8]
        bem._errorDates = [1, 2, 3, 4, 5]
        self.assertEquals(bem._get_error_values(0, 100, None, None), [1, -1, 3, -5, 8])
        self.assertEquals(bem._get_error_values(0, 100, 2, None), [-1, 3, -5, 8])
        self.assertEquals(bem._get_error_values(0, 100, None, 4), [1, -1, 3, -5])
        self.assertEquals(bem._get_error_values(0, 100, 2, 4), [-1, 3, -5])
        self.assertRaises(ValueError, bem._get_error_values, 0, 100, None, 0)
        return

    def number_of_comparisons_test(self):
        """ Test BaseErrorMeasure.initialize for behaviour if not enough dates match."""
        dataOrg = [
         [
          0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
        dataCalc = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5.1, 5], [6.1, 6], [7.1, 7], [8.1, 8], [9.1, 9]]
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)
        bem = BaseErrorMeasure(60.0)
        bem.local_error = lambda a, b: 1
        mse = MeanSquaredError(80.0)
        if mse.initialize(tsOrg, tsCalc):
            assert False
            assert mse.initialize(tsOrg, tsOrg) or False

    def error_calculation_test(self):
        """Test for a valid error calculation."""
        dataOrg = [
         [
          0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
        dataCalc = [[0, 1], [1, 3], [2, 5], [3, 0], [4, 3], [5, 5], [6.1, 6], [7, 3], [8.1, 8], [9, 8]]
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsCalc = TimeSeries.from_twodim_list(dataCalc)
        mse = MeanSquaredError(80.0)
        mse.initialize(tsOrg, tsCalc)
        assert str(mse.get_error()) == '5.125'