# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/DeleteSingleCharCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2392 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
from .JoinWithNextLineCommand import JoinWithNextLineCommand
TAB_SPACE = 4

class DeleteSingleCharCommand(BufferCommand):

    def execute(self):
        document = self._document
        cursor = self._cursor
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        cursor.toPos(pos)
        if pos == (1, 1):
            return CommandResult(success=False, info=None)
        if pos[1] == 1:
            cursor.toPos((pos[0] - 1, document.lineLength(pos[0] - 1)))
            command = JoinWithNextLineCommand(self._buffer)
            result = command.execute()
            if result.success:
                self._sub_command = command
                return CommandResult(True, '\n')
            else:
                return CommandResult(False, None)
        self.saveModifiedState()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        line_meta = document.lineMetaInfo('Change')
        changed = line_meta.data(pos[0])
        if changed is None:
            line_meta.setData('modified', pos[0])
        last_tab_pos = 1 + int((pos[1] - 1) / TAB_SPACE) * TAB_SPACE
        how_many = pos[1] - last_tab_pos
        if last_tab_pos > 1:
            if how_many == 0:
                how_many = TAB_SPACE
                last_tab_pos = last_tab_pos - TAB_SPACE
        text = document.lineText(pos[0])
        if len(text[last_tab_pos - 1:last_tab_pos - 1 + how_many].strip(' ')) != 0:
            how_many = 1
        deleted = document.deleteChars((pos[0], pos[1] - how_many), how_many)
        cursor.toPos((pos[0], pos[1] - how_many))
        document.documentMetaInfo('Modified').setData(True)
        return CommandResult(success=True, info=deleted)