# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/NewLineAfterCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 842 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class NewLineAfterCommand(BufferCommand):

    def execute(self):
        document = self._document
        cursor = self._cursor
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        current_text = document.lineText(pos[0])
        current_indent = len(current_text) - len(current_text.lstrip(' '))
        document.newLineAfter(pos[0])
        document.insertChars((pos[0] + 1, 1), ' ' * current_indent)
        document.lineMetaInfo('Change').setData('added', pos[0] + 1)
        cursor.toPos((pos[0] + 1, 1))
        cursor.toLineEnd()
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self.savedCursorPos()[0] + 1)
        self.restoreCursorPos()