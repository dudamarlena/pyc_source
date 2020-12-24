# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimo/stream/stream_from_iterator.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 315 bytes
from .stream import Stream

class StreamFromIterator(Stream):
    OUT = [
     'item']

    def __init__(self, iterator):
        super().__init__()
        self.iterator = iterator

    async def run(self, ins, outs):
        for item in self.iterator:
            await outs.item.push(item)

        outs.item.close()