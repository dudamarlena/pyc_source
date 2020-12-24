# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/meanabsolutescalederrortest.py
# Compiled at: 2015-05-28 03:51:33
import unittest
from pycast.errors import MeanAbsoluteScaledError
from pycast.common.timeseries import TimeSeries

class MeanAbsoluteScaledErrorTest(unittest.TestCase):

    def initialization_error_test(self):
        """Test for the exceptions raised during initialization."""
        MeanAbsoluteScaledError(minimalErrorCalculationPercentage=60.0, historyLength=20.0)
        try:
            MeanAbsoluteScaledError(60.0, 0.0)
        except ValueError:
            pass
        else:
            assert False

        try:
            MeanAbsoluteScaledError(60.0, -12.0)
        except ValueError:
            pass
        else:
            assert False

        try:
            MeanAbsoluteScaledError(60.0, 120.0)
        except ValueError:
            pass
        else:
            assert False

        try:
            MeanAbsoluteScaledError(60.0, 60.0)
        except ValueError:
            pass
        else:
            assert False

    def calculate_historic_means_test(self):
        """Test the calculation of the historic means."""
        dataOrg = [
         [
          1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        correctResult = [
         2.4, 2.6, 2.8, 3.2, 2.8, 3.2, 3.6, 3.6, 3.8, 3.6, 3.8, 3.8, 4.0, 3.6]
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        mase = MeanAbsoluteScaledError(historyLength=5)
        result = mase._get_historic_means(tsOrg)
        assert result == correctResult

    def local_error_calculation_test(self):
        """Testing the mean absolute error calculation of the MASE."""
        dataOrg = [
         [
          1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        dataFor = [[1.0, 11], [2.0, 13], [3.0, 14], [4.0, 11], [5.0, 13], [6.0, 18], [7.0, 20], [8.0, 26], [9.0, 21], [10.0, 34], [11.0, 23], [12.0, 23], [13.0, 15], [14.0, 12], [15.0, 14], [16.0, 17], [17.0, 25], [18.0, 22], [19.0, 14], [20.0, 30]]
        historyLength = 5
        em = MeanAbsoluteScaledError(historyLength=historyLength)
        historyLength += 1
        dataOrg = dataOrg[historyLength:]
        dataFor = dataFor[historyLength:]
        for orgValue, forValue in zip(dataOrg, dataFor):
            difference = orgValue[1] - forValue[1]
            difference = abs(difference)
            assert difference == em.local_error([orgValue[1]], [forValue[1]])

    def initialization_test(self):
        """Test for MASE initialization."""
        dataOrg = [
         [
          1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        dataFor = [[1.0, 11], [2.0, 13], [3.0, 14], [4.0, 11], [5.0, 13], [6.0, 18], [7.0, 20], [8.0, 26], [9.0, 21], [10.0, 34], [11.0, 23], [12.0, 23], [13.0, 15], [14.0, 12], [15.0, 14], [16.0, 17], [17.0, 25], [18.0, 22], [19.0, 14], [20.0, 30]]
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsFor = TimeSeries.from_twodim_list(dataFor)
        em = MeanAbsoluteScaledError(historyLength=5)
        em.initialize(tsOrg, tsFor)
        assert len(em._errorValues) == len(em._historicMeans), 'For each error value an historic mean has to exsist.'
        try:
            em.initialize(tsOrg, tsFor)
        except StandardError:
            pass
        else:
            assert False

        em = MeanAbsoluteScaledError(historyLength=20.0)
        em.initialize(tsOrg, tsFor)
        assert len(em._errorValues) == len(em._historicMeans), 'For each error value an historic mean has to exsist.'
        assert em._historyLength == 4, 'The history is %s entries long. 4 were expected.' % em._historyLength
        em = MeanAbsoluteScaledError(historyLength=40.0)
        em.initialize(tsOrg, tsFor)
        assert len(em._errorValues) == len(em._historicMeans), 'For each error value an historic mean has to exsist.'
        assert em._historyLength == 8, 'The history is %s entries long. 8 were expected.' % em._historyLength

    def error_calculation_test(self):
        """Testing for the correct MASE calculation.

        History length is 5 in this test.
        """
        dataOrg = [
         [
          1.0, 10], [2.0, 12], [3.0, 14], [4.0, 13], [5.0, 17], [6.0, 20], [7.0, 23], [8.0, 26], [9.0, 29], [10.0, 31], [11.0, 26], [12.0, 21], [13.0, 18], [14.0, 14], [15.0, 13], [16.0, 19], [17.0, 24], [18.0, 28], [19.0, 30], [20.0, 32]]
        dataFor = [[1.0, 11], [2.0, 13], [3.0, 14], [4.0, 11], [5.0, 13], [6.0, 18], [7.0, 20], [8.0, 26], [9.0, 21], [10.0, 34], [11.0, 23], [12.0, 23], [13.0, 15], [14.0, 12], [15.0, 14], [16.0, 17], [17.0, 25], [18.0, 22], [19.0, 14], [20.0, 30]]
        tsOrg = TimeSeries.from_twodim_list(dataOrg)
        tsFor = TimeSeries.from_twodim_list(dataFor)
        historyLength = 5
        em = MeanAbsoluteScaledError(historyLength=historyLength)
        em.initialize(tsOrg, tsFor)
        correctResult = [
         1.25, 0.625, 1.527, 1.458, 1.416, 1.319, 1.309, 1.25, 1.157, 1.125, '1.060', '1.180', 1.602, 1.547]
        percentage = 100.0 / len(correctResult) + 0.2
        for errVal in xrange(14):
            endPercentage = percentage * (errVal + 1)
            if endPercentage > 100.0:
                endPercentage = 100.0
            calcErr = str(em.get_error(endPercentage=endPercentage))[:5]
            correctRes = str(correctResult[errVal])[:5]
            assert calcErr == correctRes

        for errVal in xrange(14):
            endDate = dataOrg[(errVal + 6)][0]
            calcErr = str(em.get_error(endDate=endDate))[:5]
            correctRes = str(correctResult[errVal])[:5]
            assert calcErr == correctRes, '%s != %s' % (calcErr, correctRes)

        em.get_error(startDate=7.0)
        try:
            em.get_error(startDate=42.23)
        except ValueError:
            pass
        else:
            assert False