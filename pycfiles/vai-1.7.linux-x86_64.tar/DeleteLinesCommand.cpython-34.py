# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/DeleteLinesCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2820 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
import copy

class DeleteLinesCommand(BufferCommand):
    __doc__ = '\n    Deletes a bunch of lines.\n    '

    def __init__(self, buffer, from_line, num_lines):
        super().__init__(buffer)
        self._from_line = from_line
        self._num_lines = num_lines
        self._fragment = None
        self._old_line_meta_info = {}

    def execute(self):
        document = self._document
        cursor = self._cursor
        if document.isEmpty():
            return CommandResult(success=False, info=None)
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        self.saveModifiedState()
        pos = self.savedCursorPos()
        line_above = self._from_line - 1
        line_above = line_above if document.hasLine(line_above) else None
        line_below = self._from_line + self._num_lines + 1
        line_below = line_below if document.hasLine(line_below) else None
        self._fragment = document.extractFragment(self._from_line, self._num_lines)
        if document.lineMetaInfo('Change').data(pos[0]) != 'added':
            if line_above is not None:
                self._old_line_meta_info[-1] = document.lineMetaInfo('Change').data(line_above)
                document.lineMetaInfo('Change').setData('deletion_before', line_above)
            if line_below is not None:
                self._old_line_meta_info[1] = document.lineMetaInfo('Change').data(line_below)
                document.lineMetaInfo('Change').setData('deletion_after', line_below)
        document.deleteLines(self._from_line, self._num_lines)
        document.documentMetaInfo('Modified').setData(True)
        self._repositionCursor(self._from_line, line_above, line_below)
        return CommandResult(success=True, info=self._fragment)

    def _repositionCursor(self, from_line, line_above, line_below):
        cursor = self._cursor
        if line_above is None and line_below is None:
            cursor.toPos((1, 1))
        else:
            if line_above is None and line_below is not None:
                cursor.toPos((from_line, 1))
            else:
                if line_above is not None and line_below is None:
                    cursor.toPos((line_above, 1))
                else:
                    cursor.toPos((from_line, 1))

    def undo(self):
        super().undo()
        document = self._document
        cursor = self._cursor
        pos = cursor.pos
        if -1 in self._old_line_meta_info:
            document.lineMetaInfo('Change').setData(self._old_line_meta_info[(-1)], pos[0] - 1)
        if 1 in self._old_line_meta_info:
            document.lineMetaInfo('Change').setData(self._old_line_meta_info[1], pos[0] + 1)
        document.insertFragment(self._from_line, self._fragment)
        self._fragment = None