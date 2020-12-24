# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plover_cat/TextEditor.py
# Compiled at: 2017-10-18 19:32:38
# Size of source mod 2**32: 1163 bytes
import string
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QPlainTextEdit

class PloverCATEditor(QPlainTextEdit):

    def __init__(self, widget):
        super().__init__(widget)
        self._project = None

    def setProject(self, project):
        self._project = project

    def keyPressEvent(self, event):
        modifiers = event.modifiers()
        key = event.key()
        text = event.text()
        cursor = self.textCursor()
        if modifiers == QtCore.Qt.NoModifier or modifiers == QtCore.Qt.ShiftModifier:
            if text != '' and all(c in string.printable for c in text):
                if self._project:
                    self._project.insertText(cursor.position(), text)
                return
            if key == QtCore.Qt.Key_Backspace:
                if self._project:
                    self._project.deleteCharacter(cursor.position() - 1)
                return
            if key == QtCore.Qt.Key_Delete:
                if self._project:
                    self._project.deleteCharacter(cursor.position())
                return
        super().keyPressEvent(event)