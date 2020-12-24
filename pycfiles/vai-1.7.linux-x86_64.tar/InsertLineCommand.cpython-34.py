# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/InsertLineCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 870 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertLineCommand(BufferCommand):

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
        document.insertLine(pos[0], self._text)
        document.lineMetaInfo('Change').setData('added', pos[0])
        cursor.toCharFirstNonBlankForLine(pos[0])
        document.documentMetaInfo('Modified').setData(True)
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLine(self.savedCursorPos()[0])
        self.restoreCursorPos()
        self.restoreModifiedState()