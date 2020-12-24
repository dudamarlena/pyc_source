# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\source\template_cli\template_cli\Styles\CustomTitlebar\windowdragger.py
# Compiled at: 2019-04-15 07:08:15
# Size of source mod 2**32: 1201 bytes
__doc__ = "unlessFrameWindow's titlebar"
from PyQt5.QtCore import QPoint, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget

class WindowDragger(QWidget):
    doubleClicked = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.mousePressed = False
        self.mousePos = QPoint()
        self.wndPos = QPoint()

    def mousePressEvent(self, event):
        self.mousePressed = True
        self.mousePos = event.globalPos()
        parent = self.parentWidget()
        if parent:
            parent = parent.parentWidget()
            self.wndPos = parent.pos()

    def mouseMoveEvent(self, event):
        parent = self.parentWidget()
        if parent:
            parent = parent.parentWidget()
        if parent:
            if self.mousePressed:
                parent.move(self.wndPos + (event.globalPos() - self.mousePos))

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()

    def enterEvent(self, e):
        self.setCursor(Qt.ArrowCursor)