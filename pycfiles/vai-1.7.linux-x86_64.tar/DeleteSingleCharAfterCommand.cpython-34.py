# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/DeleteSingleCharAfterCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 889 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DeleteSingleCharAfterCommand(BufferCommand):

    def execute(self):
        document = self._document
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        self.saveModifiedState()
        pos = self.savedCursorPos()
        self._cursor.toPos(pos)
        if pos[1] == document.lineLength(pos[0]):
            return CommandResult(success=False, info=None)
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        line_meta = document.lineMetaInfo('Change')
        changed = line_meta.data(pos[0])
        if changed is None:
            line_meta.setData('modified', pos[0])
        deleted = document.deleteChars(pos, 1)
        document.documentMetaInfo('Modified').setData(True)
        return CommandResult(success=True, info=deleted)