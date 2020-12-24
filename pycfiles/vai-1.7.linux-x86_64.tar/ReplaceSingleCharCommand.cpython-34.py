# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/ReplaceSingleCharCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 814 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class ReplaceSingleCharCommand(BufferCommand):

    def __init__(self, buffer, char):
        super().__init__(buffer)
        self._char = char

    def execute(self):
        document = self._buffer.document
        cursor = self._buffer.cursor
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        cursor.toPos(pos)
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        meta_info = document.lineMetaInfo('Change')
        if meta_info.data(pos[0]) is None:
            meta_info.setData('modified', pos[0])
        deleted = document.replaceChars(pos, 1, self._char)
        return CommandResult(True, deleted)