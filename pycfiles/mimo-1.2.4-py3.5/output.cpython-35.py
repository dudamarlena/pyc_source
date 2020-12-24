# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimo/io/output.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 631 bytes
import asyncio

class Output:

    def __init__(self, name, *, stream=None):
        self.name = name
        self.stream = stream
        self._connections = []

    async def push(self, item):
        try:
            await asyncio.gather(*[connection.push(item) for connection in self._connections])
        except RuntimeError:
            raise RuntimeError('Event loop closed while waiting for push to {} output: {}'.format(self.stream, self.name))

    def pipe(self, connection):
        self._connections.append(connection)

    def close(self):
        for connection in self._connections:
            connection.close()