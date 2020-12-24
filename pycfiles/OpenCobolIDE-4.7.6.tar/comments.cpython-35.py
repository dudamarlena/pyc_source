# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.cobol/pyqode/cobol/modes/comments.py
# Compiled at: 2016-12-29 05:32:02
# Size of source mod 2**32: 4548 bytes
"""
This module the commenter mode
"""
import os
from pyqode.core.api import Mode
from pyqode.qt import QtCore, QtGui, QtWidgets

class CommentsMode(Mode):
    __doc__ = '\n    Comments/uncomments a set of lines (Ctrl+/)\n\n    This mode adds a contextual action to the code editor to let the user\n    comment/uncomment the selected lines.\n\n    If no lines were selected, the current line is commented/uncommented and\n    the cursor move to the next line.\n    '

    def on_state_changed(self, state):
        """
        Called when the mode is activated/deactivated
        """
        if state:
            self.action = QtWidgets.QAction(_('Comment/Uncomment'), self.editor)
            self.action.setShortcut('Ctrl+/')
            self.action.triggered.connect(self.comment)
            self.editor.add_action(self.action, sub_menu='COBOL')
            if 'pyqt5' in os.environ['QT_API'].lower():
                self.editor.key_pressed.connect(self.on_key_pressed)
        else:
            self.editor.remove_action(self.action, sub_menu='Python')
        if 'pyqt5' in os.environ['QT_API'].lower():
            self.editor.key_pressed.disconnect(self.on_key_pressed)

    def on_key_pressed(self, key_event):
        ctrl = key_event.modifiers() & QtCore.Qt.ControlModifier == QtCore.Qt.ControlModifier
        if key_event.key() == QtCore.Qt.Key_Slash and ctrl:
            self.comment()
            key_event.accept()

    def _detect_operation(self, comment_symbol, cursor, nb_lines):
        comment = False
        for i in range(nb_lines):
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, cursor.KeepAnchor)
            line = cursor.selectedText()
            if not self.editor.free_format:
                line = line[6:]
            line = line.strip()
            if not line.startswith(comment_symbol):
                comment = True
                break
            cursor.movePosition(QtGui.QTextCursor.EndOfLine)
            cursor.setPosition(cursor.position() + 1)

        return comment

    def comment(self):
        cursor = self.editor.textCursor()
        cursor.beginEditBlock()
        sel_start = cursor.selectionStart()
        has_selection = True
        if not cursor.hasSelection():
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            has_selection = False
        lines = cursor.selection().toPlainText().splitlines()
        nb_lines = len(lines)
        cursor.setPosition(sel_start)
        comment_symbol = self.editor.comment_indicator
        comment = self._detect_operation(comment_symbol, cursor, nb_lines)
        cursor.setPosition(sel_start)
        l = len(comment_symbol)
        for i in range(nb_lines):
            cursor.movePosition(QtGui.QTextCursor.StartOfLine)
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, cursor.KeepAnchor)
            full_line = cursor.selectedText()
            if not self.editor.free_format:
                full_line = '      ' + full_line[6:]
            line = full_line.lstrip()
            indent = len(full_line) - len(line)
            if line != '':
                cursor.movePosition(QtGui.QTextCursor.StartOfLine)
                if not comment:
                    cursor.setPosition(cursor.position() + indent)
                    cursor.movePosition(cursor.Right, cursor.KeepAnchor, l)
                    cursor.insertText('')
                else:
                    if self.editor.free_format:
                        print('indent', indent)
                        cursor.setPosition(cursor.position() + indent)
                    else:
                        cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor, 6)
                    cursor.insertText(comment_symbol)
                cursor.movePosition(cursor.NextBlock)

        cursor.endEditBlock()
        if not has_selection:
            cursor = self.editor.textCursor()
            cursor.movePosition(cursor.Down, cursor.MoveAnchor)
            self.editor.setTextCursor(cursor)