# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimo/stream/stream_to_output.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 305 bytes
from .stream import Stream

class StreamToOutput(Stream):
    IN = [
     'item']

    def __init__(self, output):
        super().__init__()
        self.output = output

    async def run(self, ins, out):
        async for item in ins.item:
                        await self.output.push(item)

        ins.item.close()