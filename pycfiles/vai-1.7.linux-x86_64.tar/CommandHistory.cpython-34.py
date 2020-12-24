# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/models/CommandHistory.py
# Compiled at: 2014-10-07 11:33:38
# Size of source mod 2**32: 560 bytes


class CommandHistory:

    def __init__(self):
        self._past = []
        self._future = []

    def add(self, command):
        self._past.append(command)
        self._future = []

    def prev(self):
        command = self._past.pop(-1)
        self._future.insert(0, command)
        return command

    def next(self):
        command = self._future.pop(0)
        self._past.append(command)
        return command

    def numUndoableCommands(self):
        return len(self._past)

    def numRedoableCommands(self):
        return len(self._future)