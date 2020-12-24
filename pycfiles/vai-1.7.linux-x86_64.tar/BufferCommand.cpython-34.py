# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/commands/BufferCommand.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 2276 bytes


class BufferCommand(object):
    __doc__ = 'A base class for commands modifying a buffer'
    MEMENTO_INSERT, MEMENTO_REPLACE = list(range(2))

    def __init__(self, buffer):
        self._buffer = buffer
        self._document = buffer.document
        self._cursor = buffer.cursor
        self._line_memento_data = []
        self._sub_command = None
        self._saved_cursor_pos = None
        self._saved_modified_state = None

    def saveCursorPos(self):
        self._saved_cursor_pos = self._cursor.pos

    def saveModifiedState(self):
        self._saved_modified_state = self._document.documentMetaInfo('Modified').data()

    def restoreModifiedState(self):
        if self._saved_modified_state is not None:
            self._document.documentMetaInfo('Modified').setData(self._saved_modified_state)

    def restoreCursorPos(self):
        if self._saved_cursor_pos is not None:
            self._cursor.toPos(self._saved_cursor_pos)

    def savedCursorPos(self):
        return self._saved_cursor_pos

    def saveLineMemento(self, line_number, restore_strategy):
        self._line_memento_data.append((line_number, restore_strategy, self._document.lineMemento(line_number)))

    def restoreLineMemento(self):
        line_number, restore_strategy, memento = self._line_memento_data.pop()
        if restore_strategy == BufferCommand.MEMENTO_INSERT:
            self._document.insertFromMemento(line_number, memento)
        else:
            if restore_strategy == BufferCommand.MEMENTO_REPLACE:
                self._document.replaceFromMemento(line_number, memento)
            else:
                raise Exception('Unknown restore mode for memento')

    def lastSavedMemento(self):
        return self._line_memento_data[(-1)]

    def executeSubCommand(self, subcommand_type):
        sub_command = subcommand_type(self._buffer)
        result = sub_command.execute()
        if result.success:
            self._sub_command = sub_command
        return result

    def undo(self):
        if self._sub_command is not None:
            self._sub_command.undo()
            self._sub_command = None
            return
        for i in range(len(self._line_memento_data)):
            self.restoreLineMemento()

        self.restoreCursorPos()
        self.restoreModifiedState()