# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/est_venv/lib/python3.7/site-packages/est/gui/larch/utils.py
# Compiled at: 2020-03-05 02:52:24
# Size of source mod 2**32: 4556 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/30/2019'
from silx.gui import qt

class _OptionalQDoubleSpinBox(qt.QWidget):
    __doc__ = '\n    Simple widget allowing to activate or tnoe the spin box\n    '
    sigChanged = qt.Signal()

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self._checkbox = qt.QCheckBox(parent=self)
        self.layout().addWidget(self._checkbox)
        self._spinBox = qt.QDoubleSpinBox(parent=self)
        self.layout().addWidget(self._spinBox)
        self._checkbox.setChecked(True)
        self._spinBox.setMinimum(-999999)
        self._spinBox.setMaximum(999999)
        self._lastValue = None
        self.setMinimum = self._spinBox.setMinimum
        self.setMaximum = self._spinBox.setMaximum
        self._checkbox.toggled.connect(self._updateSpinBoxStatus)
        self._spinBox.editingFinished.connect(self._valueChanged)

    def getValue(self):
        if self._checkbox.isChecked():
            return self._spinBox.value()
        return

    def setValue(self, value):
        self._checkbox.setChecked(value is not None)
        if value is not None:
            self._spinBox.setValue(value)

    def _updateSpinBoxStatus(self, *arg, **kwargs):
        self._spinBox.setEnabled(self._checkbox.isChecked())
        self._valueChanged()

    def _valueChanged(self, *arg, **kwargs):
        if self._lastValue != self.getValue():
            self._lastValue = self.getValue()
            self.sigChanged.emit()


class _OptionalQIntSpinBox(qt.QWidget):
    __doc__ = '\n    Simple widget allowing to activate or tnoe the spin box\n    '
    sigChanged = qt.Signal()

    def __init__(self, parent):
        qt.QWidget.__init__(self, parent)
        self.setLayout(qt.QHBoxLayout())
        self._checkbox = qt.QCheckBox(parent=self)
        self.layout().addWidget(self._checkbox)
        self._spinBox = qt.QSpinBox(parent=self)
        self.layout().addWidget(self._spinBox)
        self._checkbox.setChecked(True)
        self._lastValue = None
        self.setMinimum = self._spinBox.setMinimum
        self.setMaximum = self._spinBox.setMaximum
        self.setRange = self._spinBox.setRange
        self._checkbox.toggled.connect(self._updateSpinBoxStatus)
        self._spinBox.valueChanged.connect(self._valueChanged)

    def getValue(self):
        if self._checkbox.isChecked():
            return self._spinBox.value()
        return

    def setValue(self, value):
        self._checkbox.setChecked(value is not None)
        if value is not None:
            self._spinBox.setValue(value)

    def _updateSpinBoxStatus(self, *arg, **kwargs):
        self._spinBox.setEnabled(self._checkbox.isChecked())
        self._valueChanged()

    def _valueChanged(self, *arg, **kwargs):
        if self._lastValue != self.getValue():
            self._lastValue = self.getValue()
            self.sigChanged.emit()