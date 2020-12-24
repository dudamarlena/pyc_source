# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimo/io/io_set.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 492 bytes


class IOSet:

    def __init__(self, connections):
        self.connections = {connection.name:connection for connection in connections}

    def __iter__(self):
        return iter(self.connections.values())

    def __len__(self):
        return len(self.connections)

    def __getattr__(self, key):
        if key in self.connections:
            return self.connections[key]
        return self.__getattribute__(key)

    def __getitem__(self, key):
        return self.connections[key]