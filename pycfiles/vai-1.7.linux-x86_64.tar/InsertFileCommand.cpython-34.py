# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/InsertFileCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1115 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class InsertFileCommand(BufferCommand):

    def __init__(self, buffer, filename):
        super().__init__(buffer)
        self._filename = filename
        self._how_many = None

    def execute(self):
        document = self._document
        cursor = self._cursor
        try:
            with open(self._filename, 'r') as (f):
                lines = f.readlines()
        except:
            return CommandResult(False, None)

        if self.savedCursorPos() is None:
            self.saveCursorPos()
        self.saveModifiedState()
        pos = self.savedCursorPos()
        line_pos = pos[0]
        cursor.toPos((line_pos, 1))
        self._how_many = len(lines)
        document.insertLines(line_pos, lines)
        document.lineMetaInfo('Change').setData(['added'] * self._how_many, line_pos)
        document.documentMetaInfo('Modified').setData(True)
        return CommandResult(True, None)

    def undo(self):
        self._document.deleteLines(self.savedCursorPos()[0], self._how_many)
        super().undo()