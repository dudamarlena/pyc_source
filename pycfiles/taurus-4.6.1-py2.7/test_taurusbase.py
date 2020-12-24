# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/base/test/test_taurusbase.py
# Compiled at: 2019-08-19 15:09:29
"""Unit tests for taurusbase"""
import unittest
from taurus.test import insertTest
from taurus.qt.qtgui.test import BaseWidgetTestCase
from taurus.core.tango.test import TangoSchemeTestLauncher
from taurus.qt.qtgui.container import TaurusWidget
DEV_NAME = TangoSchemeTestLauncher.DEV_NAME

@insertTest(helper_name='getDisplayValue', model='eval:1+2#', expected='-----')
@insertTest(helper_name='getDisplayValue', model='eval:1+2#label', expected='1+2')
@insertTest(helper_name='getDisplayValue', model='eval:1+2', expected='3')
@insertTest(helper_name='getDisplayValue', model='tango://' + DEV_NAME + '/double_scalar?configuration', expected='double_scalar?configuration', test_skip="old behaviour which we probably don't want")
@insertTest(helper_name='getDisplayValue', model='tango://' + DEV_NAME + '/float_scalar?configuration=label', expected='float_scalar')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/double_scalar#rvalue.magnitude', expected='1.23')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/float_scalar#label', expected='float_scalar')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/float_scalar#', expected='-----')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/state', expected='ON')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/float_scalar', expected='1.23 mm', test_skip='enc/decode rounding errors for float<-->numpy.float32')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/double_scalar', expected='1.23 mm')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/short_scalar', expected='123 mm')
@insertTest(helper_name='getDisplayValue', model='tango:' + DEV_NAME + '/boolean_scalar', expected='True')
class GetDisplayValueTestCase(TangoSchemeTestLauncher, BaseWidgetTestCase, unittest.TestCase):
    """Check TaurusBaseComponent.getDisplayValue
    """
    _klass = TaurusWidget

    def setUp(self):
        BaseWidgetTestCase.setUp(self)

    def getDisplayValue(self, model=None, expected=None):
        """Check if setModel works when using parent model"""
        self._widget.setModel(model)
        got = self._widget.getDisplayValue()
        msg = 'getDisplayValue for "%s" should be %r (got %r)' % (
         model, expected, got)
        self.assertEqual(expected, got, msg)
        self.assertMaxDeprecations(0)