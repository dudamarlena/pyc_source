# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/kohlrabi/lib/python3.5/site-packages/libkohlrabi/util.py
# Compiled at: 2016-04-01 07:48:41
# Size of source mod 2**32: 216 bytes
"""
Utilities.
"""
import asyncio
SIDE_CLIENT = 0
SIDE_SERVER = 1

@asyncio.coroutine
def wraps_future(fut: asyncio.Future, coro):
    result = yield from coro
    fut.set_result(result)