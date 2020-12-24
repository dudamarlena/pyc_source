# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/gridsearchtest.py
# Compiled at: 2015-05-28 05:24:51
import unittest
from pycast.errors import SymmetricMeanAbsolutePercentageError as SMAPE
from pycast.common.timeseries import TimeSeries
from pycast.methods import BaseForecastingMethod, ExponentialSmoothing, HoltMethod
from pycast.optimization import GridSearch

class GridSearchTest(unittest.TestCase):
    """Test class for the GridSearch."""

    def setUp(self):
        """Initializes self.forecastingMethod."""
        bfm = BaseForecastingMethod(['parameter_one', 'parameter_two'])
        bfm._parameterIntervals = {}
        bfm._parameterIntervals['parameter_one'] = [0.0, 1.0, False, False]
        bfm._parameterIntervals['parameter_two'] = [0.0, 2.0, True, True]
        self.bfm = bfm
        data = [[0.0, 0.0], [1.1, 0.2], [2.2, 0.6], [3.3, 0.2], [4.4, 0.3], [5.5, 0.5]]
        self.timeSeries = TimeSeries.from_twodim_list(data)
        self.timeSeries.normalize('second')

    def tearDown(self):
        """Deletes the BaseForecastingMethod of the test."""
        del self.bfm
        del self.timeSeries

    def create_generator_test(self):
        """Test the parameter generation function."""
        precision = 0.01
        values_one = [ i * precision for i in xrange(1, 100) ]
        values_two = [ i * precision for i in xrange(201) ]
        generator_one = GridSearch(SMAPE, precision=-2)._generate_next_parameter_value('parameter_one', self.bfm)
        generator_two = GridSearch(SMAPE, precision=-2)._generate_next_parameter_value('parameter_two', self.bfm)
        generated_one = [ val for val in generator_one ]
        generated_two = [ val for val in generator_two ]
        assert len(values_one) == len(generated_one)
        assert len(values_two) == len(generated_two)
        for idx in xrange(len(values_one)):
            value = str(values_one[idx])[:12]
            assert str(value) == str(generated_one[idx])[:len(value)]

        for idx in xrange(len(values_two)):
            value = str(values_two[idx])[:12]
            assert str(value) == str(generated_two[idx])[:len(value)]

    def optimize_exception_test(self):
        """Test for exception while calling GridSearch.optimize."""
        try:
            GridSearch(SMAPE, -2).optimize(self.timeSeries)
        except ValueError:
            pass
        else:
            assert False

        try:
            GridSearch(SMAPE, -1).optimize(self.timeSeries, [self.bfm])
        except NotImplementedError:
            pass
        else:
            assert False

    def optimize_value_creation_test(self):
        """Testing the first part of optimize_forecasting_method."""
        self.bfm._requiredParameters = [
         'param1', 'param2', 'param3', 'param4', 'param5']
        try:
            GridSearch(SMAPE, -1).optimize_forecasting_method(self.timeSeries, self.bfm)
        except NotImplementedError:
            pass
        else:
            assert False

        self.bfm._parameterIntervals = {'param3': [
                    0.0, 1.0, True, True], 
           'param4': [
                    0.0, 1.0, True, True], 
           'param5': [
                    0.0, 1.0, True, True]}
        try:
            GridSearch(SMAPE, -5).optimize_forecasting_method(self.timeSeries, self.bfm)
        except NotImplementedError:
            pass
        else:
            assert False

    def inner_optimization_result_test(self):
        """Test for the correct result of a GridSearch optimization."""
        fm = ExponentialSmoothing()
        startingPercentage = 0.0
        endPercentage = 100.0
        self.timeSeries.normalize('second')
        results = []
        for smoothingFactor in [ alpha / 100.0 for alpha in xrange(1, 100) ]:
            fm.set_parameter('smoothingFactor', smoothingFactor)
            resultTS = self.timeSeries.apply(fm)
            error = SMAPE()
            error.initialize(self.timeSeries, resultTS)
            results.append([error, smoothingFactor])

        bestManualResult = min(results, key=lambda item: item[0].get_error(startingPercentage, endPercentage))
        gridSearch = GridSearch(SMAPE, precision=-2)
        gridSearch._startingPercentage = startingPercentage
        gridSearch._endPercentage = endPercentage
        result = gridSearch.optimize_forecasting_method(self.timeSeries, fm)
        bestManualAlpha = bestManualResult[1]
        errorManualResult = bestManualResult[0].get_error()
        bestGridSearchAlpha = result[1]['smoothingFactor']
        errorGridSearchResult = result[0].get_error()
        assert str(errorManualResult)[:8] >= str(errorGridSearchResult)[:8]
        assert str(bestManualAlpha)[:5] == str(bestGridSearchAlpha)[:5]

    def inner_optimization_result_accuracy_test(self):
        """Test for the correct result of a GridSearch optimization."""
        fm = ExponentialSmoothing()
        startingPercentage = 0.0
        endPercentage = 100.0
        self.timeSeries.normalize('second')
        results = []
        for smoothingFactor in [ alpha / 100.0 for alpha in xrange(1, 100) ]:
            fm.set_parameter('smoothingFactor', smoothingFactor)
            resultTS = self.timeSeries.apply(fm)
            error = SMAPE()
            error.initialize(self.timeSeries, resultTS)
            results.append([error, smoothingFactor])

        bestManualResult = min(results, key=lambda item: item[0].get_error(startingPercentage, endPercentage))
        gridSearch = GridSearch(SMAPE, precision=-4)
        gridSearch._startingPercentage = startingPercentage
        gridSearch._endPercentage = endPercentage
        result = gridSearch.optimize_forecasting_method(self.timeSeries, fm)
        bestManualAlpha = bestManualResult[1]
        errorManualResult = bestManualResult[0].get_error()
        bestGridSearchAlpha = result[1]['smoothingFactor']
        errorGridSearchResult = result[0].get_error()
        assert errorManualResult > errorGridSearchResult

    def outer_optimization_result_test(self):
        """Test the multiple method optimization."""
        fm1 = ExponentialSmoothing()
        fm2 = HoltMethod()
        self.timeSeries.normalize('second')
        gridSearch = GridSearch(SMAPE, precision=-2)
        result = gridSearch.optimize(self.timeSeries, [fm1, fm2])

    def optimization_loop_test(self):
        """Testing the optimozation loop."""
        gridSearch = GridSearch(SMAPE, precision=-2)

        def crap_execute(ignoreMe):
            ts = self.timeSeries.to_twodim_list()
            ts = TimeSeries.from_twodim_list(ts)
            for entry in ts:
                entry[0] += 0.1

            return ts

        self.bfm.execute = crap_execute
        result = gridSearch.optimization_loop(self.timeSeries, self.bfm, [], {})
        assert result == []