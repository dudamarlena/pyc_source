# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/monthseditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4.QtCore import Qt
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QHBoxLayout
from PyQt4.QtGui import QAbstractSpinBox
from camelot.core.utils import ugettext as _
from camelot.view.controls.editors import CustomEditor
from camelot.view.controls.editors.customeditor import ValueLoading
from camelot.view.controls.editors.integereditor import CustomDoubleSpinBox

class MonthsEditor(CustomEditor):
    """MonthsEditor

    composite months and years editor
    """

    def __init__(self, parent=None, editable=True, field_name='months', **kw):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        self.years_spinbox = CustomDoubleSpinBox()
        self.months_spinbox = CustomDoubleSpinBox()
        self.years_spinbox.setMinimum(0)
        self.years_spinbox.setMaximum(10000)
        self.months_spinbox.setMinimum(0)
        self.months_spinbox.setMaximum(12)
        self.years_spinbox.setSuffix(_(' years'))
        self.months_spinbox.setSuffix(_(' months'))
        self.years_spinbox.setDecimals(0)
        self.years_spinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.years_spinbox.setSingleStep(1)
        self.months_spinbox.setDecimals(0)
        self.months_spinbox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.months_spinbox.setSingleStep(1)
        self.years_spinbox.editingFinished.connect(self._spinbox_editing_finished)
        self.months_spinbox.editingFinished.connect(self._spinbox_editing_finished)
        layout = QHBoxLayout()
        layout.addWidget(self.years_spinbox)
        layout.addWidget(self.months_spinbox)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    @QtCore.pyqtSlot()
    def _spinbox_editing_finished(self):
        self.editingFinished.emit()

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, **kwargs):
        self.set_enabled(editable)
        self.set_background_color(background_color)
        self.years_spinbox.setToolTip(unicode(tooltip or ''))

    def set_enabled(self, editable=True):
        self.years_spinbox.setReadOnly(not editable)
        self.years_spinbox.setEnabled(editable)
        self.months_spinbox.setReadOnly(not editable)
        self.months_spinbox.setEnabled(editable)
        if not editable:
            self.years_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.months_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        else:
            self.years_spinbox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
            self.months_spinbox.setButtonSymbols(QAbstractSpinBox.UpDownArrows)

    def set_value(self, value):
        CustomEditor.set_value(self, value)
        if self._value_loading:
            return
        if self.value_is_none:
            value = 0
        years, months = divmod(value, 12)
        self.years_spinbox.setValue(years)
        self.months_spinbox.setValue(months)

    def get_value(self):
        if CustomEditor.get_value(self) is ValueLoading:
            return ValueLoading
        self.years_spinbox.interpretText()
        years = int(self.years_spinbox.value())
        self.months_spinbox.interpretText()
        months = int(self.months_spinbox.value())
        value = years * 12 + months
        return value