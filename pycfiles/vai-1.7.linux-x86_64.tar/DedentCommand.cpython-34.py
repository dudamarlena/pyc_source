# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/DedentCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 1116 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DedentCommand(BufferCommand):
    __doc__ = '\n    Dedent the line at the current cursor position.\n    '

    def __init__(self, buffer):
        super().__init__(buffer)

    def execute(self):
        cursor = self._cursor
        document = self._document
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        text = document.lineText(pos[0])
        if text[0:4] != '    ':
            return CommandResult(success=False, info=None)
        line_meta = document.lineMetaInfo('Change')
        changed = line_meta.data(pos[0])
        self.saveModifiedState()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        document.deleteChars((pos[0], 1), 4)
        if changed is None:
            line_meta.setData('modified', pos[0])
        document.documentMetaInfo('Modified').setData(True)
        cursor.toPos((pos[0], pos[1] - 4))
        return CommandResult(success=True, info=None)