# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/controls/editors/coloreditor.py
# Compiled at: 2013-04-11 17:47:52
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtCore import Qt
from customeditor import CustomEditor

class ColorEditor(CustomEditor):

    def __init__(self, parent=None, editable=True, field_name='color', **kwargs):
        CustomEditor.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        self.setObjectName(field_name)
        layout = QtGui.QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.color_button = QtGui.QPushButton(parent)
        self.color_button.setMaximumSize(QtCore.QSize(20, 20))
        layout.addWidget(self.color_button)
        if editable:
            self.color_button.clicked.connect(self.buttonClicked)
        self.setLayout(layout)
        self._color = None
        return

    def get_value(self):
        color = self.getColor()
        if color:
            value = (
             color.red(), color.green(), color.blue(), color.alpha())
        else:
            value = None
        return CustomEditor.get_value(self) or value

    def set_value(self, value):
        value = CustomEditor.set_value(self, value)
        if value:
            color = QtGui.QColor()
            color.setRgb(*value)
            self.setColor(color)
        else:
            self.setColor(value)

    def getColor(self):
        return self._color

    def set_enabled(self, editable=True):
        self.color_button.setEnabled(editable)

    def setColor(self, color):
        pixmap = QtGui.QPixmap(16, 16)
        if color:
            pixmap.fill(color)
        else:
            pixmap.fill(Qt.transparent)
        self.color_button.setIcon(QtGui.QIcon(pixmap))
        self._color = color

    def buttonClicked(self, raised):
        if self._color:
            color = QtGui.QColorDialog.getColor(self._color)
        else:
            color = QtGui.QColorDialog.getColor()
        if color.isValid() and color != self._color:
            self.setColor(color)
            self.editingFinished.emit()