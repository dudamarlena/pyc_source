# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_widgets/test_attribute_widgets.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, numpy as np
from pyrpl.async_utils import sleep as async_sleep
from qtpy import QtCore, QtWidgets
from pyrpl.test.test_base import TestPyrpl
from pyrpl import APP
from pyrpl.curvedb import CurveDB
from pyrpl.widgets.startup_widget import HostnameSelectorWidget
from pyrpl.async_utils import sleep as async_sleep
from pyrpl.widgets.spinbox import NumberSpinBox
from pyrpl.widgets.attribute_widgets import NumberAttributeWidget
from pyrpl.hardware_modules.iir import IIR
from pyrpl.software_modules import NetworkAnalyzer
from qtpy import QtTest, QtCore

class TestAttributeWidgets(TestPyrpl):

    def teardown(self):
        pass

    def test_spin_box(self):
        for mod in self.pyrpl.modules:
            if not isinstance(mod, (IIR, NetworkAnalyzer)):
                widget = mod._create_widget()
                for name, aw in widget.attribute_widgets.items():
                    if isinstance(aw, NumberAttributeWidget):
                        yield (
                         self.assert_spin_box, mod, widget, name, aw)

    _TEST_SPINBOX_BUTTON_DOWN_TIME = 0.05

    def assert_spin_box(self, mod, widget, name, aw):
        print 'Testing spinbox widget for %s.%s...' % (mod.name, name)
        mod.free()
        APP.processEvents()
        original_m_value = getattr(mod, name)
        maximum = aw.widget.maximum if np.isfinite(aw.widget.maximum) else 10000000
        minimum = aw.widget.minimum if np.isfinite(aw.widget.minimum) else -10000000
        setattr(mod, name, (maximum + minimum) / 2)
        APP.processEvents()
        w_value = aw.widget_value
        m_value = getattr(mod, name)
        norm = 1 if m_value == 0 or w_value == 0 else m_value
        assert abs(w_value - m_value) / norm < 0.001, (
         w_value, m_value, mod.name, name)
        fullname = '%s.%s' % (mod.name, name)
        exclude = ['spectrumanalyzer.center']
        if fullname in exclude:
            print 'Widget %s.%s was not enabled and cannot be tested...' % (
             mod.name, name)
            return
        QtTest.QTest.keyPress(aw, QtCore.Qt.Key_Up)
        async_sleep(self._TEST_SPINBOX_BUTTON_DOWN_TIME)
        QtTest.QTest.keyRelease(aw, QtCore.Qt.Key_Up)
        async_sleep(self._TEST_SPINBOX_BUTTON_DOWN_TIME)
        new_val = getattr(mod, name)
        assert new_val > m_value, (new_val, m_value, mod.name, name)
        QtTest.QTest.keyPress(aw, QtCore.Qt.Key_Down)
        async_sleep(self._TEST_SPINBOX_BUTTON_DOWN_TIME)
        QtTest.QTest.keyRelease(aw, QtCore.Qt.Key_Down)
        async_sleep(self._TEST_SPINBOX_BUTTON_DOWN_TIME)
        new_new_val = getattr(mod, name)
        assert new_new_val < new_val, (new_new_val, new_val, mod.name, name)
        setattr(mod, name, original_m_value)