# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/DeleteLineAtCursorCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2163 bytes
from .BufferCommand import BufferCommand
from .CommandResult import CommandResult
import copy

class DeleteLineAtCursorCommand(BufferCommand):

    def execute(self):
        document = self._document
        if document.isEmpty():
            return CommandResult(success=False, info=None)
        cursor = self._cursor
        if self.savedCursorPos() is None:
            self.saveCursorPos()
        pos = self.savedCursorPos()
        cursor.toPos(pos)
        self.saveModifiedState()
        self.saveLineMemento(pos[0], BufferCommand.MEMENTO_INSERT)
        old_line = copy.deepcopy(self.lastSavedMemento()[2])
        self._old_line_meta_info = {}
        if pos[0] == document.numLines():
            cursor.toLinePrev()
            cursor.toLineBeginning()
        if document.lineMetaInfo('Change').data(pos[0]) != 'added':
            if document.hasLine(pos[0] - 1):
                self._old_line_meta_info[-1] = document.lineMetaInfo('Change').data(pos[0] - 1)
                document.lineMetaInfo('Change').setData('deletion_before', pos[0] - 1)
            if document.hasLine(pos[0] + 1):
                self._old_line_meta_info[1] = document.lineMetaInfo('Change').data(pos[0] + 1)
                document.lineMetaInfo('Change').setData('deletion_after', pos[0] + 1)
        document.deleteLine(pos[0])
        document.documentMetaInfo('Modified').setData(True)
        if document.lineLength(cursor.line) < cursor.column:
            cursor.toPos((cursor.line, document.lineLength(cursor.line)))
        return CommandResult(success=True, info=old_line)

    def undo(self):
        super().undo()
        document = self._document
        cursor = self._cursor
        pos = cursor.pos
        if -1 in self._old_line_meta_info:
            document.lineMetaInfo('Change').setData(self._old_line_meta_info[(-1)], pos[0] - 1)
        if 1 in self._old_line_meta_info:
            document.lineMetaInfo('Change').setData(self._old_line_meta_info[1], pos[0] + 1)