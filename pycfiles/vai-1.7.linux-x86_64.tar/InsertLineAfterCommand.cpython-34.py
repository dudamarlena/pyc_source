# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/InsertLineAfterCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1076 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertLineAfterCommand(BufferCommand):
    __doc__ = '\n    Command to perform insertion of a line after the cursor current line\n    Moves the cursor to the first non-blank character of the newly added line\n    '

    def __init__(self, buffer, text):
        super().__init__(buffer)
        self._text = text

    def execute(self):
        document = self._document
        cursor = self._cursor
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        self.saveModifiedState()
        pos = self.savedCursorPos()
        cursor.toPos(pos)
        document.insertLine(pos[0] + 1, self._text)
        document.lineMetaInfo('Change').setData('added', pos[0] + 1)
        document.documentMetaInfo('Modified').setData(True)
        cursor.toCharFirstNonBlankForLine(pos[0] + 1)
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self.savedCursorPos()[0] + 1)
        self.restoreCursorPos()
        self.restoreModifiedState()