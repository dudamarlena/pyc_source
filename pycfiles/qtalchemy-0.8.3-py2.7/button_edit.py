# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qtalchemy/widgets/button_edit.py
# Compiled at: 2012-06-23 09:45:07
from qtalchemy import *
from PySide import QtCore, QtGui

class PBButtonEdit(QtGui.QLineEdit):
    buttonPressed = Signal(name='buttonPressed')

    def __init__(self, parent=None):
        QtGui.QLineEdit.__init__(self, parent)
        self.button = QtGui.QToolButton(self)
        self.button.setCursor(QtCore.Qt.ArrowCursor)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        buttonWidth = self.style().pixelMetric(QtGui.QStyle.PM_ScrollBarExtent)
        self.button.clicked.connect(self.buttonPress)

    def resizeEvent(self, event):
        rect = self.rect()
        frameWidth = self.style().pixelMetric(QtGui.QStyle.PM_DefaultFrameWidth)
        buttonWidth = self.style().pixelMetric(QtGui.QStyle.PM_ScrollBarExtent)
        self.button.resize(buttonWidth, rect.height() - 2 * frameWidth)
        self.button.move(rect.right() - buttonWidth, frameWidth)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F4:
            self.buttonPress()
        else:
            QtGui.QLineEdit.keyPressEvent(self, event)

    def buttonPress(self):
        self.buttonPressed.emit()