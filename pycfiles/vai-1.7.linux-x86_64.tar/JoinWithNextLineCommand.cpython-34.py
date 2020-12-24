# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/JoinWithNextLineCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 911 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class JoinWithNextLineCommand(BufferCommand):

    def execute(self):
        document = self._document
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        if pos[0] == document.numLines():
            return CommandResult(success=False, info=None)
        self._cursor.toPos(pos)
        line_meta = document.lineMetaInfo('Change')
        self.saveModifiedState()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        self.saveLineMemento(pos[0] + 1, BufferCommand.MEMENTO_INSERT)
        document.joinWithNextLine(pos[0])
        if line_meta.data(pos[0]) == None:
            line_meta.setData('modified', pos[0])
        document.documentMetaInfo('Modified').setData(True)
        return CommandResult(success=True, info=None)