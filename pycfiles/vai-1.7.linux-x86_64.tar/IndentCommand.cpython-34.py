# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/IndentCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 935 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class IndentCommand(BufferCommand):
    __doc__ = '\n    Indent the line at the current cursor position.\n    '

    def __init__(self, buffer):
        super().__init__(buffer)

    def execute(self):
        cursor = self._cursor
        document = self._document
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        self.saveModifiedState()
        line_meta = document.lineMetaInfo('Change')
        changed = line_meta.data(pos[0])
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        if changed is None:
            line_meta.setData('modified', pos[0])
        document.insertChars((pos[0], 1), '    ')
        cursor.toPos((pos[0], pos[1] + 4))
        document.documentMetaInfo('Modified').setData(True)
        return CommandResult(success=True, info=None)