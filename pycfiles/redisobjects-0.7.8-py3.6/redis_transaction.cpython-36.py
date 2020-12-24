# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redisobjects/redis_transaction.py
# Compiled at: 2019-09-28 15:18:33
# Size of source mod 2**32: 664 bytes


class RedisTransaction:

    def __init__(self, connection):
        self.connection = connection
        self.commands = []

    async def execute(self, command, *params):
        self.commands.append((command, *params))

    async def commit(self):
        if len(self.commands) == 0:
            return True
        else:
            if len(self.commands) == 1:
                return await (self.connection.execute)(*self.commands[0])
            await self.connection.execute('multi')
            for command in self.commands:
                await (self.connection.execute)(*command)

            return await self.connection.execute('exec')

    async def discard(self):
        self.commands.clear()