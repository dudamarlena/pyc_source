# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimo/asynctools/range.py
# Compiled at: 2016-10-13 12:43:28
# Size of source mod 2**32: 405 bytes


class AsynchronousRange:

    def __init__(self, fr, to=None, step=1):
        if to is None:
            self._iterator = iter(range(fr))
        else:
            self._iterator = iter(range(fr, to, step))

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._iterator)
        except StopIteration:
            raise StopAsyncIteration