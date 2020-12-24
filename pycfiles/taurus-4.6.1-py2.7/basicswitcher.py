# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/compact/basicswitcher.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides some basic usable widgets based on TaurusReadWriteSwitcher
"""
from __future__ import absolute_import
from taurus.qt.qtgui.display import TaurusLabel, TaurusLed
from taurus.qt.qtgui.input import TaurusValueLineEdit, TaurusValueCheckBox
from .abstractswitcher import TaurusReadWriteSwitcher
__all__ = [
 'TaurusLabelEditRW', 'TaurusBoolRW']
__docformat__ = 'restructuredtext'

class TaurusLabelEditRW(TaurusReadWriteSwitcher):
    """A Switcher combining a TaurusLabel and a TaurusValueLineEdit"""
    readWClass = TaurusLabel
    writeWClass = TaurusValueLineEdit


class TaurusBoolRW(TaurusReadWriteSwitcher):
    """A Switcher combining a TaurusLed and a TaurusValueCheckBox"""
    readWClass = TaurusLed
    writeWClass = TaurusValueCheckBox

    def setWriteWidget(self, widget):
        widget.setShowText(False)
        TaurusReadWriteSwitcher.setWriteWidget(self, widget)


def _demo():
    """demo of integrability in a form"""
    import sys
    from taurus.qt.qtgui.panel import TaurusForm
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(cmd_line_parser=None)
    f = TaurusForm()
    f.model = ['sys/tg_test/1/long_scalar', 'sys/tg_test/1/long_scalar',
     'sys/tg_test/1/boolean_scalar', 'sys/tg_test/1/boolean_scalar']
    f[0].setReadWidgetClass(TaurusLabelEditRW)
    f[0].setWriteWidgetClass(None)
    f[2].setReadWidgetClass(TaurusBoolRW)
    f[2].setWriteWidgetClass(None)
    f.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    _demo()