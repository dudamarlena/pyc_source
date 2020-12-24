# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/DeleteToEndOfWordCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2149 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult

class DeleteToEndOfWordCommand(BufferCommand):
    SPACERS = ' {}[]().!@#$%^&*=,'

    def execute(self):
        cursor = self._buffer.cursor
        document = self._buffer.document
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        cursor.toPos(pos)
        self.saveModifiedState()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_REPLACE)
        line_meta = document.lineMetaInfo('Change')
        changed = line_meta.data(pos[0])
        if changed is None:
            line_meta.setData('modified', pos[0])
        text = document.lineText(pos[0])
        cur_index = pos[1] - 1
        char_under_cursor = text[cur_index]
        if text[cur_index] in DeleteToEndOfWordCommand.SPACERS:
            remove_count = len(text[cur_index:]) - len(text[cur_index:].lstrip(char_under_cursor))
            remove_count += len(text[cur_index + remove_count:]) - len(text[cur_index + remove_count:].lstrip(' '))
        else:
            spacer_indexes = [p for p, c in enumerate(text) if p > cur_index and c in DeleteToEndOfWordCommand.SPACERS]
            if len(spacer_indexes) == 0:
                remove_count = document.lineLength(pos[0]) - cur_index + 1
            else:
                remove_count = spacer_indexes[0] - cur_index
                remove_count += len(text[cur_index + remove_count:]) - len(text[cur_index + remove_count:].lstrip(' '))
        deleted = document.deleteChars(pos, remove_count)
        document.documentMetaInfo('Modified').setData(True)
        return CommandResult(success=True, info=deleted)