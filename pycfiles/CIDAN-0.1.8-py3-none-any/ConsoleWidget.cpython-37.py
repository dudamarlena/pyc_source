# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Console/ConsoleWidget.py
# Compiled at: 2020-03-29 16:43:00
# Size of source mod 2**32: 1405 bytes
from PySide2 import QtCore
from PySide2.QtCore import Slot
from PySide2.QtWidgets import *
from PySide2 import QtGui
import sys

class Stream(QtCore.QObject):
    newText = QtCore.Signal(str)

    def __init__(self):
        super().__init__()

    def write(self, text):
        self.newText.emit(str(text))

    def flush(self):
        pass


class ConsoleWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText('Console:')
        self.layout.addWidget(self.label)
        self.setMinimumHeight(100)
        self.process = QTextBrowser()
        self.process.moveCursor(QtGui.QTextCursor.Start)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.layout.addWidget(self.process)
        self.setLayout(self.layout)
        sys.stdout = Stream()
        sys.stdout.newText.connect(self.onUpdateText)

    def onUpdateText(self, text):
        cursor = self.process.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def __del__(self):
        sys.stdout = sys.__stdout__