# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimo/stream/stream_from_input.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 306 bytes
from .stream import Stream

class StreamFromInput(Stream):
    OUT = [
     'item']

    def __init__(self, input):
        super().__init__()
        self.input = input

    async def run(self, ins, outs):
        async for item in self.input:
                        await outs.item.push(item)

        outs.item.close()