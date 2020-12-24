# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/coloredfloateditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from customeditor import CustomEditor, set_background_color_palette
from camelot.core import constants
from camelot.view.art import Icon
from camelot.view.controls.editors.floateditor import CustomDoubleSpinBox

class ColoredFloatEditor(CustomEditor):
    """Widget for editing a float field, with a calculator"""
    calculator_icon = Icon('tango/16x16/apps/accessories-calculator.png')
    zero = Icon('tango/16x16/actions/zero.png')
    go_down_red = Icon('tango/16x16/actions/go-down-red.png')
    go_up = Icon('tango/16x16/actions/go-up.png')
    go_down_blue = Icon('tango/16x16/actions/go-down-blue.png')
    go_up_blue = Icon('tango/16x16/actions/go-up-blue.png')

    def __init__(self, parent, precision=2, reverse=False, neutral=False, option=None, field_name='float', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        action = QtGui.QAction(self)
        action.setShortcut(QtGui.QKeySequence(Qt.Key_F4))
        self.setFocusPolicy(Qt.StrongFocus)
        self.spinBox = CustomDoubleSpinBox(option, parent)
        self.spinBox.setDecimals(precision)
        self.spinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.spinBox.addAction(action)
        self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.arrow = QtGui.QLabel()
        self.arrow.setPixmap(self.go_up.getQPixmap())
        self.arrow.setFixedHeight(self.get_height())
        self.arrow.setAutoFillBackground(False)
        self.arrow.setMaximumWidth(19)
        self.calculatorButton = QtGui.QToolButton()
        self.calculatorButton.setIcon(self.calculator_icon.getQIcon())
        self.calculatorButton.setAutoRaise(True)
        self.calculatorButton.setFixedHeight(self.get_height())
        self.calculatorButton.clicked.connect(lambda : self.popupCalculator(self.spinBox.value()))
        action.triggered.connect(lambda : self.popupCalculator(self.spinBox.value()))
        self.spinBox.editingFinished.connect(self.spinbox_editing_finished)
        self.releaseKeyboard()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addSpacing(3.5)
        layout.addWidget(self.arrow)
        layout.addWidget(self.spinBox)
        layout.addWidget(self.calculatorButton)
        self.reverse = reverse
        self.neutral = neutral
        self.setFocusProxy(self.spinBox)
        self.setLayout(layout)
        if not self.reverse:
            if not self.neutral:
                self.icons = {-1: self.go_down_red, 1: self.go_up, 
                   0: self.zero}
            else:
                self.icons = {-1: self.go_down_blue, 1: self.go_up_blue, 
                   0: self.zero}
        else:
            self.icons = {1: self.go_down_red, 
               -1: self.go_up, 
               0: self.zero}

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, prefix='', suffix='', minimum=constants.camelot_minfloat, maximum=constants.camelot_maxfloat, single_step=1.0, **kwargs):
        self.set_enabled(editable)
        self.set_background_color(background_color)
        self.setToolTip(unicode(tooltip or ''))
        self.spinBox.setPrefix('%s ' % unicode(prefix).lstrip())
        self.spinBox.setSuffix(' %s' % unicode(suffix).rstrip())
        self.spinBox.setRange(minimum, maximum)
        self.spinBox.setSingleStep(single_step)

    def set_enabled(self, editable=True):
        self.spinBox.setReadOnly(not editable)
        self.spinBox.setEnabled(editable)
        self.calculatorButton.setShown(editable)
        if editable:
            self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        else:
            self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

    def set_value(self, value):
        value = CustomEditor.set_value(self, value) or 0.0
        self.spinBox.setValue(value)
        self.arrow.setPixmap(self.icons[cmp(value, 0)].getQPixmap())

    def get_value(self):
        self.spinBox.interpretText()
        value = self.spinBox.value()
        return CustomEditor.get_value(self) or value

    def popupCalculator(self, value):
        from camelot.view.controls.calculator import Calculator
        calculator = Calculator()
        calculator.setValue(value)
        calculator.calculation_finished_signal.connect(self.calculation_finished)
        calculator.exec_()

    def calculation_finished(self, value):
        self.spinBox.setValue(float(unicode(value)))
        self.editingFinished.emit()

    @QtCore.pyqtSlot()
    def spinbox_editing_finished(self):
        self.editingFinished.emit()

    def set_background_color(self, background_color):
        set_background_color_palette(self.spinBox.lineEdit(), background_color)