# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/pyqtgraph/widgets/ColorButton.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 3755 bytes
from ..Qt import QtGui, QtCore
from .. import functions
__all__ = [
 'ColorButton']

class ColorButton(QtGui.QPushButton):
    __doc__ = '\n    **Bases:** QtGui.QPushButton\n    \n    Button displaying a color and allowing the user to select a new color.\n    \n    ====================== ============================================================\n    **Signals:**\n    sigColorChanging(self) emitted whenever a new color is picked in the color dialog\n    sigColorChanged(self)  emitted when the selected color is accepted (user clicks OK)\n    ====================== ============================================================\n    '
    sigColorChanging = QtCore.Signal(object)
    sigColorChanged = QtCore.Signal(object)

    def __init__(self, parent=None, color=(128, 128, 128)):
        QtGui.QPushButton.__init__(self, parent)
        self.setColor(color)
        self.colorDialog = QtGui.QColorDialog()
        self.colorDialog.setOption(QtGui.QColorDialog.ShowAlphaChannel, True)
        self.colorDialog.setOption(QtGui.QColorDialog.DontUseNativeDialog, True)
        self.colorDialog.currentColorChanged.connect(self.dialogColorChanged)
        self.colorDialog.rejected.connect(self.colorRejected)
        self.colorDialog.colorSelected.connect(self.colorSelected)
        self.clicked.connect(self.selectColor)
        self.setMinimumHeight(15)
        self.setMinimumWidth(15)

    def paintEvent(self, ev):
        QtGui.QPushButton.paintEvent(self, ev)
        p = QtGui.QPainter(self)
        rect = self.rect().adjusted(6, 6, -6, -6)
        p.setBrush(functions.mkBrush('w'))
        p.drawRect(rect)
        p.setBrush(QtGui.QBrush(QtCore.Qt.DiagCrossPattern))
        p.drawRect(rect)
        p.setBrush(functions.mkBrush(self._color))
        p.drawRect(rect)
        p.end()

    def setColor(self, color, finished=True):
        """Sets the button's color and emits both sigColorChanged and sigColorChanging."""
        self._color = functions.mkColor(color)
        if finished:
            self.sigColorChanged.emit(self)
        else:
            self.sigColorChanging.emit(self)
        self.update()

    def selectColor(self):
        self.origColor = self.color()
        self.colorDialog.setCurrentColor(self.color())
        self.colorDialog.open()

    def dialogColorChanged(self, color):
        if color.isValid():
            self.setColor(color, finished=False)

    def colorRejected(self):
        self.setColor((self.origColor), finished=False)

    def colorSelected(self, color):
        self.setColor((self._color), finished=True)

    def saveState(self):
        return functions.colorTuple(self._color)

    def restoreState(self, state):
        self.setColor(state)

    def color(self, mode='qcolor'):
        color = functions.mkColor(self._color)
        if mode == 'qcolor':
            return color
        if mode == 'byte':
            return (
             color.red(), color.green(), color.blue(), color.alpha())
        if mode == 'float':
            return (
             color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0, color.alpha() / 255.0)

    def widgetGroupInterface(self):
        return (self.sigColorChanged, ColorButton.saveState, ColorButton.restoreState)