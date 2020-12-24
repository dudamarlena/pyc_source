# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/baseoptimizationtest.py
# Compiled at: 2015-05-28 03:51:37
import unittest
from pycast.optimization import BaseOptimizationMethod
from pycast.errors import BaseErrorMeasure
from pycast.methods import BaseMethod
from pycast.common.timeseries import TimeSeries

class BaseOptimizationMethodTest(unittest.TestCase):
    """Test class containing all tests for pycast.optimization.BaseOptimizationMethod."""

    def initialization_errormeasure_test(self):
        """Test optimization methods error measure initialization."""
        BaseOptimizationMethod(BaseErrorMeasure, -1)
        try:
            BaseOptimizationMethod(None, -1)
        except TypeError:
            pass
        else:
            assert False

        try:
            BaseOptimizationMethod(BaseOptimizationMethodTest, -1)
        except TypeError:
            pass
        else:
            assert False

        return

    def initialization_precision_test(self):
        """Test the parameter range durign the initialization."""
        for precision in xrange(-7, 1, 1):
            BaseOptimizationMethod(BaseErrorMeasure, precision=precision)

        for precision in [-1020, -324, -11, 1, 42, 123, 2341]:
            try:
                BaseOptimizationMethod(BaseErrorMeasure, precision=precision)
            except ValueError:
                pass
            else:
                assert False

    def optimize_value_error_test(self):
        """Test the optimize call."""
        bom = BaseOptimizationMethod(BaseErrorMeasure, precision=-3)
        bm = BaseMethod()
        bom.optimize(TimeSeries(), [bm])
        try:
            bom.optimize(TimeSeries(), [])
        except ValueError:
            pass
        else:
            assert False