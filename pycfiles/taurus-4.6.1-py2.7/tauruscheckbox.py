# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/input/tauruscheckbox.py
# Compiled at: 2019-08-19 15:09:30
"""This module provides a set of basic taurus widgets based on QCheckBox"""
__all__ = [
 'TaurusValueCheckBox']
__docformat__ = 'restructuredtext'
from taurus.external.qt import Qt
from taurus.qt.qtgui.base import TaurusBaseWritableWidget

class TaurusValueCheckBox(Qt.QCheckBox, TaurusBaseWritableWidget):
    """A QCheckBox connected to a boolean writable attribute model"""

    def __init__(self, qt_parent=None, designMode=False):
        name = 'TaurusValueCheckBox'
        self.call__init__wo_kw(Qt.QCheckBox, qt_parent)
        self.call__init__(TaurusBaseWritableWidget, name, designMode=designMode)
        self.setObjectName(name)
        self.updateStyle()
        self.stateChanged.connect(self.notifyValueChanged)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Qt.Key_Return, Qt.Qt.Key_Enter):
            self.writeValue()
            event.accept()
        else:
            Qt.QCheckBox.keyPressEvent(self, event)
            event.ignore()

    def minimumSizeHint(self):
        return Qt.QSize(20, 20)

    def updateStyle(self):
        TaurusBaseWritableWidget.updateStyle(self)
        if self._showText:
            try:
                self.setText(str(self.getModelObj().getConfig().getLabel()))
            except:
                self.setText('----')

        else:
            self.setText('')
        if self.hasPendingOperations():
            txt = str(self.text()).strip()
            if len(txt) == 0:
                self.setText('!')
            self.setStyleSheet('TaurusValueCheckBox {color: blue;}')
        else:
            if str(self.text()) == '!':
                self.setText(' ')
            self.setStyleSheet('TaurusValueCheckBox {}')
        self.update()

    def setValue(self, v):
        self.setChecked(bool(v))

    def getValue(self):
        return self.isChecked()

    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseWritableWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.input'
        ret['icon'] = 'designer:checkbox.png'
        return ret

    model = Qt.pyqtProperty('QString', TaurusBaseWritableWidget.getModel, TaurusBaseWritableWidget.setModel, TaurusBaseWritableWidget.resetModel)
    showText = Qt.pyqtProperty('bool', TaurusBaseWritableWidget.getShowText, TaurusBaseWritableWidget.setShowText, TaurusBaseWritableWidget.resetShowText)
    useParentModel = Qt.pyqtProperty('bool', TaurusBaseWritableWidget.getUseParentModel, TaurusBaseWritableWidget.setUseParentModel, TaurusBaseWritableWidget.resetUseParentModel)
    autoApply = Qt.pyqtProperty('bool', TaurusBaseWritableWidget.getAutoApply, TaurusBaseWritableWidget.setAutoApply, TaurusBaseWritableWidget.resetAutoApply)
    forcedApply = Qt.pyqtProperty('bool', TaurusBaseWritableWidget.getForcedApply, TaurusBaseWritableWidget.setForcedApply, TaurusBaseWritableWidget.resetForcedApply)