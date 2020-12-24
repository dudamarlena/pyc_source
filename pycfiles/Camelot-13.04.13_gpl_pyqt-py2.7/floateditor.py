# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/floateditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from customeditor import CustomEditor, set_background_color_palette, draw_tooltip_visualization
from camelot.view.art import Icon
from camelot.core import constants

class CustomDoubleSpinBox(QtGui.QDoubleSpinBox):
    """Spinbox that doesn't accept mouse scrolling as input"""

    def __init__(self, option=None, parent=None):
        super(CustomDoubleSpinBox, self).__init__(parent)
        self._option = option
        self._locale = QtCore.QLocale()

    def wheelEvent(self, wheel_event):
        wheel_event.ignore()

    def keyPressEvent(self, key_event):
        if self._option and self._option.version != 5 and key_event.key() in (Qt.Key_Up, Qt.Key_Down):
            key_event.ignore()
        else:
            decimal_point = QtCore.QLocale.system().decimalPoint()
            if key_event.key() == Qt.Key_Period and decimal_point.unicode() != Qt.Key_Period:
                new_key_event = QtGui.QKeyEvent(key_event.type(), decimal_point.unicode(), key_event.modifiers(), QtCore.QString(decimal_point))
                key_event.accept()
                QtGui.QApplication.sendEvent(self, new_key_event)
            else:
                super(CustomDoubleSpinBox, self).keyPressEvent(key_event)

    def textFromValue(self, value):
        text = unicode(self._locale.toString(float(value), 'f', self.decimals()))
        return text

    def paintEvent(self, event):
        super(CustomDoubleSpinBox, self).paintEvent(event)
        if self.toolTip():
            draw_tooltip_visualization(self)


class FloatEditor(CustomEditor):
    """Widget for editing a float field, with a calculator button.  
    The calculator button can be turned of with the **calculator** field
    attribute.
    """
    calculator_icon = Icon('tango/16x16/apps/accessories-calculator.png')

    def __init__(self, parent, minimum=constants.camelot_minfloat, maximum=constants.camelot_maxfloat, calculator=True, decimal=False, option=None, field_name='float', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setObjectName(field_name)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self._decimal = decimal
        self._calculator = calculator
        action = QtGui.QAction(self)
        action.setShortcut(QtGui.QKeySequence(Qt.Key_F4))
        self.setFocusPolicy(Qt.StrongFocus)
        self.spinBox = CustomDoubleSpinBox(option, parent)
        self.spinBox.setRange(minimum, maximum)
        self.spinBox.setDecimals(2)
        self.spinBox.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.spinBox.addAction(action)
        self.calculatorButton = QtGui.QToolButton()
        self.calculatorButton.setIcon(self.calculator_icon.getQIcon())
        self.calculatorButton.setAutoRaise(True)
        self.calculatorButton.setFixedHeight(self.get_height())
        self.calculatorButton.setToolTip('Calculator F4')
        self.calculatorButton.setFocusPolicy(Qt.ClickFocus)
        self.calculatorButton.clicked.connect(lambda : self.popupCalculator(self.spinBox.value()))
        action.triggered.connect(lambda : self.popupCalculator(self.spinBox.value()))
        self.spinBox.editingFinished.connect(self.spinbox_editing_finished)
        self.releaseKeyboard()
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.spinBox)
        layout.addWidget(self.calculatorButton)
        self.setFocusProxy(self.spinBox)
        self.setLayout(layout)

    def set_field_attributes(self, editable=True, background_color=None, tooltip=None, prefix='', suffix='', precision=2, single_step=1.0, **kwargs):
        self.set_enabled(editable)
        self.set_background_color(background_color)
        self.spinBox.setToolTip(unicode(tooltip or ''))
        self.spinBox.setPrefix('%s ' % unicode(prefix or '').lstrip())
        self.spinBox.setSuffix(' %s' % unicode(suffix or '').rstrip())
        self.spinBox.setSingleStep(single_step)
        if self.spinBox.decimals() != precision:
            self.spinBox.setDecimals(precision)

    def set_value(self, value):
        value = CustomEditor.set_value(self, value)
        if value:
            self.spinBox.setValue(float(value))
        elif value == None:
            self.spinBox.lineEdit().setText('')
        else:
            self.spinBox.setValue(0.0)
        return

    def get_value(self):
        value_loading = CustomEditor.get_value(self)
        if value_loading is not None:
            return value_loading
        else:
            if self.spinBox.text() == '':
                return
            self.spinBox.interpretText()
            value = self.spinBox.value()
            if self._decimal:
                import decimal
                value = decimal.Decimal('%.*f' % (self.spinBox.decimals(), value))
            return value

    def set_enabled(self, editable=True):
        self.spinBox.setReadOnly(not editable)
        self.spinBox.setEnabled(editable)
        self.calculatorButton.setShown(editable and self._calculator)
        if editable:
            self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.UpDownArrows)
        else:
            self.spinBox.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

    def popupCalculator(self, value):
        from camelot.view.controls.calculator import Calculator
        calculator = Calculator(self)
        calculator.setValue(value)
        calculator.calculation_finished_signal.connect(self.calculation_finished)
        calculator.exec_()

    @QtCore.pyqtSlot(QtCore.QString)
    def calculation_finished(self, value):
        self.spinBox.setValue(float(unicode(value)))
        self.editingFinished.emit()

    @QtCore.pyqtSlot()
    def spinbox_editing_finished(self):
        self.editingFinished.emit()

    def set_background_color(self, background_color):
        set_background_color_palette(self.spinBox.lineEdit(), background_color)
        set_background_color_palette(self.spinBox, background_color)