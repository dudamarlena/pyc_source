# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\source\template_cli\template_cli\Styles\CustomTitlebar\windowdragger.py
# Compiled at: 2019-04-15 07:08:15
# Size of source mod 2**32: 1201 bytes
"""unlessFrameWindow's titlebar"""
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