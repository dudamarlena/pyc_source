# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/discord/ext/timers/utils.py
# Compiled at: 2019-08-14 10:47:57
# Size of source mod 2**32: 616 bytes
import asyncio
MAX_ASYNCIO_SECONDS = 3456000

class ListBasedQueue(asyncio.LifoQueue):

    def _get(self):
        return self._queue.pop(0)


async def chunked_sleep(time):
    for k in _chunk_sleep(time):
        await asyncio.sleep(k)


def _chunk_sleep(sleep_time):
    while sleep_time > 0:
        new = sleep_time - MAX_ASYNCIO_SECONDS
        if new < 0:
            yield sleep_time
            break
        elif new > MAX_ASYNCIO_SECONDS:
            yield MAX_ASYNCIO_SECONDS
            sleep_time -= MAX_ASYNCIO_SECONDS
        else:
            yield new
            break