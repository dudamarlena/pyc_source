# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/booleditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from customeditor import AbstractCustomEditor
from camelot.core import constants
from camelot.core.utils import ugettext

class BoolEditor(QtGui.QCheckBox, AbstractCustomEditor):
    """Widget for editing a boolean field"""
    editingFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None, minimum=constants.camelot_minint, maximum=constants.camelot_maxint, nullable=True, field_name='boolean', **kwargs):
        QtGui.QCheckBox.__init__(self, parent)
        AbstractCustomEditor.__init__(self)
        self.setObjectName(field_name)
        self._nullable = nullable
        self.clicked.connect(self._state_changed)

    def set_value(self, value):
        value = AbstractCustomEditor.set_value(self, value)
        if value:
            self.setCheckState(Qt.Checked)
        else:
            self.setCheckState(Qt.Unchecked)

    def get_value(self):
        value_loading = AbstractCustomEditor.get_value(self)
        if value_loading is not None:
            return value_loading
        else:
            state = self.checkState()
            if state == Qt.Unchecked:
                return False
            return True

    def set_field_attributes(self, editable=True, **kwargs):
        AbstractCustomEditor.set_field_attributes(self, **kwargs)
        self.setDisabled(not editable)

    @QtCore.pyqtSlot(bool)
    def _state_changed(self, value=None):
        self.editingFinished.emit()

    def sizeHint(self):
        size = QtGui.QComboBox().sizeHint()
        return size


class TextBoolEditor(QtGui.QLabel, AbstractCustomEditor):
    """
    :Parameter:
        color_yes: string
            text-color of the True representation
        color_no: string
            text-color of the False representation
    """
    editingFinished = QtCore.pyqtSignal()

    def __init__(self, parent=None, yes='Yes', no='No', color_yes=None, color_no=None, **kwargs):
        QtGui.QLabel.__init__(self, parent)
        AbstractCustomEditor.__init__(self)
        self.setEnabled(False)
        self.yes = ugettext(yes)
        self.no = ugettext(no)
        self.color_yes = color_yes
        self.color_no = color_no

    def set_value(self, value):
        value = AbstractCustomEditor.set_value(self, value)
        if value:
            self.setText(self.yes)
            if self.color_yes:
                selfpalette = self.palette()
                selfpalette.setColor(QtGui.QPalette.WindowText, self.color_yes)
                self.setPalette(selfpalette)
        else:
            self.setText(self.no)
            if self.color_no:
                selfpalette = self.palette()
                selfpalette.setColor(QtGui.QPalette.WindowText, self.color_no)
                self.setPalette(selfpalette)