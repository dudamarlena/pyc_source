# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/display/test/test_tauruslabel.py
# Compiled at: 2019-08-19 15:09:29
"""Unit tests for Taurus Label"""
import unittest
from taurus.external.qt import Qt
from taurus.test import insertTest
from taurus.qt.qtgui.test import GenericWidgetTestCase, BaseWidgetTestCase
from taurus.qt.qtgui.display import TaurusLabel
from taurus.qt.qtgui.container import TaurusWidget
from taurus.core.tango.test import TangoSchemeTestLauncher
import functools
from taurus.core.util.colors import ATTRIBUTE_QUALITY_DATA, DEVICE_STATE_DATA
from pint import UnitRegistry as ur
import numpy
DEV_NAME = TangoSchemeTestLauncher.DEV_NAME

class TaurusLabelTest(GenericWidgetTestCase, unittest.TestCase):
    """
    Generic tests for TaurusLabel.

    .. seealso: :class:`taurus.qt.qtgui.test.base.GenericWidgetTestCase`
    """
    _klass = TaurusLabel
    modelnames = ['sys/tg_test/1/wave', '', 'eval:1', None]


class Bug169_Test(BaseWidgetTestCase, unittest.TestCase):
    """
    Test bug169:  See: http://sf.net/p/tauruslib/tickets/65/
                  (aka, Sradana's bug169)

    .. seealso: :class:`taurus.qt.qtgui.test.base.BaseWidgetTestCase`
    """
    _klass = TaurusLabel

    def setUp(self):
        BaseWidgetTestCase.setUp(self)
        self._widget.setModel('sys/tg_test/1/double_scalar#label')
        self._expectedModelClass = self._widget.getModelClass()
        self._parent = TaurusWidget()
        self._parent.setModel('sys/tg_test/1')
        self._widget.setUseParentModel(True)
        self._widget.setParent(self._parent)

    def test_bug169(self):
        """Check if setModel works when using parent model"""
        self._widget.setModel('/double_scalar#label')
        self.assertMaxDeprecations(1)

    def test_relativemodelclass(self):
        """Check consistency in modelClass when using parent model (re: bug169)
        """
        try:
            self._widget.setModel('/double_scalar#label')
        finally:
            mc = self._widget.getModelClass()
            msg = 'getModelClass() inconsistency:\n expected: %s\n got: %s' % (
             self._expectedModelClass, mc)
            self.assertEqual(self._expectedModelClass, mc, msg)

        self.assertMaxDeprecations(1)


testOldFgroles = functools.partial(insertTest, helper_name='text', maxdepr=1, model='tango:' + DEV_NAME + '/double_scalar')

@testOldFgroles(fgRole='value', expected='1.23 mm')
@testOldFgroles(fgRole='w_value', expected='0.00 mm')
@testOldFgroles(fgRole='state', expected='Ready')
@testOldFgroles(fgRole='quality', expected='ATTR_VALID')
@testOldFgroles(fgRole='none', expected='')
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_image#rvalue[1,::2]', expected=('{:~}').format(numpy.array([1.23, 1.23]) * ur().mm))
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_spectrum#rvalue[1]', expected='1.23 mm')
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_image', modelIndex=(1,
                                                                                         1), expected='1.23 mm')
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_spectrum', modelIndex=1, expected='1.23 mm')
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_scalar#state', expected='Ready')
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_scalar#rvalue', fgRole='label', expected='double_scalar')
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_scalar', fgRole='label', expected='double_scalar')
@insertTest(helper_name='text', model='tango:' + DEV_NAME + '/double_scalar#label', expected='double_scalar')
@insertTest(helper_name='bgRole', model='tango:' + DEV_NAME + '/float_scalar_ro', bgRole='none', expected=Qt.QColor(Qt.Qt.transparent).getRgb()[:3])
@insertTest(helper_name='bgRole', model='tango:' + DEV_NAME + '/float_scalar_ro', bgRole='state', expected=DEVICE_STATE_DATA['TaurusDevState.Ready'][1:4])
@insertTest(helper_name='bgRole', model='tango:' + DEV_NAME + '/float_scalar_ro', bgRole='quality', expected=ATTRIBUTE_QUALITY_DATA['ATTR_VALID'][1:4])
@insertTest(helper_name='bgRole', model='tango:' + DEV_NAME + '/float_scalar_ro', expected=ATTRIBUTE_QUALITY_DATA['ATTR_VALID'][1:4])
class TaurusLabelTest2(TangoSchemeTestLauncher, BaseWidgetTestCase, unittest.TestCase):
    """
    Specific tests for TaurusLabel
    """
    _klass = TaurusLabel

    def text(self, model=None, expected=None, fgRole=None, maxdepr=0, modelIndex=None):
        """Check that the label text"""
        self._widget.setModel(model)
        if fgRole is not None:
            self._widget.setFgRole(fgRole)
        if modelIndex is not None:
            self._widget.setModelIndex(modelIndex)
        self.processEvents(repetitions=10, sleep=0.1)
        got = str(self._widget.text())
        msg = 'wrong text for "%s":\n expected: %s\n got: %s' % (
         model, expected, got)
        self.assertEqual(got, expected, msg)
        self.assertMaxDeprecations(maxdepr)
        return

    def bgRole(self, model=None, expected=None, bgRole=None, maxdepr=0):
        """Check that the label text"""
        self._widget.setModel(model)
        self.processEvents(repetitions=50, sleep=0.1)
        if bgRole is not None:
            self._widget.setBgRole(bgRole)
        p = self._widget.palette()
        got = p.color(p.Background).getRgb()[:3]
        msg = 'wrong background RGB for "%s":\n expected: %s\n got: %s' % (
         model, expected, got)
        self.assertEqual(got, expected, msg)
        self.assertMaxDeprecations(maxdepr)
        return


def baseFormatter1(dtype, **kwargs):
    return '{:~.1f}'


def baseFormatter2(dtype, **kwargs):
    return dtype.__name__


@insertTest(helper_name='checkClassFormat', model='eval:1.2345', formatter='>>{}<<', expected='>>1.2345<<')
@insertTest(helper_name='checkClassFormat', model='eval:Q(5)#rvalue.magnitude', formatter=baseFormatter2, expected='int')
@insertTest(helper_name='checkClassFormat', model='eval:Q("5m")#rvalue.units', formatter=baseFormatter2, expected='Unit')
@insertTest(helper_name='checkClassFormat', model='eval:1.2345', formatter=baseFormatter1, expected='1.2')
@insertTest(helper_name='checkClassFormat', model='eval:"hello"', formatter=baseFormatter1, expected='hello')
@insertTest(helper_name='checkClassFormat', model='eval:"hello"', formatter=baseFormatter2, expected='str')
@insertTest(helper_name='checkClassFormat', model='eval:"hello"', formatter=None, expected='hello')
@insertTest(helper_name='checkClassFormat', model='eval:1.2345', formatter='{:~.3f}', expected='1.234')
@insertTest(helper_name='checkClassFormat', model='eval:1.2345', formatter='{:.3f}', expected='1.234 dimensionless')
@insertTest(helper_name='checkInstanceFormat', model='eval:1.2345', formatter='>>{}<<', expected='>>1.2345<<')
@insertTest(helper_name='checkInstanceFormat', model='eval:Q(5)#rvalue.magnitude', formatter=baseFormatter2, expected='int')
@insertTest(helper_name='checkInstanceFormat', model='eval:Q("5m")#rvalue.units', formatter=baseFormatter2, expected='Unit')
@insertTest(helper_name='checkInstanceFormat', model='eval:1.2345', formatter=baseFormatter1, expected='1.2')
@insertTest(helper_name='checkInstanceFormat', model='eval:"hello"', formatter=baseFormatter1, expected='hello')
@insertTest(helper_name='checkInstanceFormat', model='eval:"hello"', formatter=baseFormatter2, expected='str')
@insertTest(helper_name='checkInstanceFormat', model='eval:"hello"', formatter=None, expected='hello')
@insertTest(helper_name='checkInstanceFormat', model='eval:1.2345', formatter='{:~.3f}', expected='1.234')
@insertTest(helper_name='checkInstanceFormat', model='eval:1.2345', formatter='{:.3f}', expected='1.234 dimensionless')
class TaurusLabelFormatTest(BaseWidgetTestCase, unittest.TestCase):
    """
    Specific tests for testing the Formatting API with TaurusLabel
    instances
    """
    _klass = TaurusLabel

    def setUp(self):
        BaseWidgetTestCase.setUp(self)
        self._origFormatter = self._klass.FORMAT

    def tearDown(self):
        self._klass.FORMAT = self._origFormatter

    def checkInstanceFormat(self, model, formatter, expected):
        if formatter is not None:
            self._widget.setFormat(formatter)
        self._widget.setModel(model)
        self.processEvents(repetitions=50, sleep=0.1)
        got = self._widget.text()
        msg = 'wrong text for "%s":\n expected: %s\n got: %s' % (
         model, expected, got)
        self.assertEqual(got, expected, msg)
        return

    def checkClassFormat(self, model, formatter, expected):
        self._klass.FORMAT = formatter
        self._widget = self._klass(*self.initargs, **self.initkwargs)
        self._widget.setModel(model)
        self.processEvents(repetitions=50, sleep=0.1)
        got = self._widget.text()
        msg = 'wrong text for "%s":\n expected: %s\n got: %s' % (
         model, expected, got)
        self.assertEqual(got, expected, msg)