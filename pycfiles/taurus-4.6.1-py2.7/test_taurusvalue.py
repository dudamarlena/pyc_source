# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/panel/test/test_taurusvalue.py
# Compiled at: 2019-08-19 15:09:30
"""Test for taurus.qt.qtgui.panel.taurusvalue"""
import unittest
from taurus.test import insertTest
from taurus.qt.qtgui.test import BaseWidgetTestCase
from taurus.qt.qtgui.panel import TaurusValue
from taurus.core.tango.test import TangoSchemeTestLauncher
DEV_NAME = TangoSchemeTestLauncher.DEV_NAME

@insertTest(helper_name='texts', model='tango:' + DEV_NAME + '/double_scalar', expected=('double_scalar',
                                                                                         '1.23',
                                                                                         '0.00',
                                                                                         'mm'))
class TaurusValueTest(TangoSchemeTestLauncher, BaseWidgetTestCase, unittest.TestCase):
    """
    Specific tests for TaurusValue
    """
    _klass = TaurusValue

    def test_bug126(self):
        """Verify that case is not lost when customizing a label (bug#126)"""
        w = self._widget
        self._widget.setModel('tango:' + DEV_NAME + '/double_scalar')
        label = 'MIXEDcase'
        w.setLabelConfig(label)
        self.processEvents(repetitions=10, sleep=0.1)
        shownLabel = str(w.labelWidget().text())
        msg = 'Shown label ("%s") differs from set label ("%s")' % (shownLabel,
         label)
        self.assertEqual(label, shownLabel, msg)
        self.assertMaxDeprecations(1)

    def texts(self, model=None, expected=None, fgRole=None, maxdepr=0):
        """Checks the texts for scalar attributes"""
        self._widget.setModel(model)
        if fgRole is not None:
            self._widget.setFgRole(fgRole)
        self.processEvents(repetitions=10, sleep=0.1)
        got = (str(self._widget.labelWidget().text()),
         str(self._widget.readWidget().text()),
         str(self._widget.writeWidget().displayText()),
         str(self._widget.unitsWidget().text()))
        msg = 'wrong text for "%s":\n expected: %s\n got: %s' % (
         model, expected, got)
        self.assertEqual(got, expected, msg)
        self.assertMaxDeprecations(maxdepr)
        return

    def test_labelCaseSensitivity(self):
        """Verify that case is respected of in the label widget"""
        w = self._widget
        self._widget.setModel('tango:' + DEV_NAME + '/MIXEDcase')
        label = 'MIXEDcase'
        self.processEvents(repetitions=10, sleep=0.1)
        shownLabel = str(w.labelWidget().text())
        msg = 'Shown label ("%s") differs from set label ("%s")' % (shownLabel,
         label)
        self.assertEqual(label, shownLabel, msg)
        self.assertMaxDeprecations(0)

    def tearDown(self):
        """Set Model to None"""
        self._widget.setModel(None)
        TangoSchemeTestLauncher.tearDown(self)
        unittest.TestCase.tearDown(self)
        return


if __name__ == '__main__':
    pass