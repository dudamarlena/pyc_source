# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/tests/decoratorstest.py
# Compiled at: 2015-05-28 03:51:36
import unittest
from mock import Mock
from pycast.common.decorators import optimized
from pycast.common.timeseries import TimeSeries
from pycast.errors.baseerrormeasure import BaseErrorMeasure
import pycastC.errors.baseerrormeasure.BaseErrorMeasure as cerror

class OptimizedDecoratorTest(unittest.TestCase):

    def test_optimization_enabled(self):
        error = BaseErrorMeasure()
        error._enable_instance_optimization()
        cerror.initialize = Mock()
        error.initialize(None, None)
        assert cerror.initialize.called, 'If optimization is enabled the c method should be called'
        return

    def test_optimization_disabled(self):
        error = BaseErrorMeasure()
        error._disable_instance_optimization()
        cerror.initialize = Mock()
        try:
            error.initialize(None, None)
        except:
            pass

        assert not cerror.initialize.called, 'If optimization is disabled the c method should not be called'
        return

    def test_function_call_is_transparent(self):
        """
        With and without optimization the method
        should be called with the same parameters.
        """
        oldError = BaseErrorMeasure.local_error
        BaseErrorMeasure.local_error = Mock()
        ts = TimeSeries.from_twodim_list([[1, 1]])
        error = BaseErrorMeasure()
        error._enable_instance_optimization()
        error.initialize(ts, ts)
        error = BaseErrorMeasure()
        error._disable_instance_optimization()
        error.initialize(ts, ts)
        BaseErrorMeasure.local_error = oldError

    def test_import_fail(self):
        """
        If the import of the cmodules 
        fails the original method should be used
        """

        class Foo:

            def __init__(self):
                self.optimizationEnabled = True
                self.called = False

            @optimized
            def foo(self):
                self.called = True

        test_obj = Foo()
        test_obj.foo()
        assert test_obj.called, 'If no cmodule exists, original method should be called'