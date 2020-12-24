# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/kohlrabi/lib/python3.5/site-packages/libkohlrabi/tasks/serverside.py
# Compiled at: 2016-04-01 07:47:41
# Size of source mod 2**32: 912 bytes
"""
Server-side Task.
"""
import asyncio, sys
from .base import TaskBase
PY35 = sys.version_info >= (3, 5, 0)

class ServerTaskBase(TaskBase):
    __doc__ = '\n    Base class for a server-side task.\n    '

    def __call__(self, *args, **kwargs):
        return self.coro(*args, **kwargs)

    @asyncio.coroutine
    def invoke_func(self, ack_id, *args, **kwargs):
        result = yield from self.coro(*args, **kwargs)
        yield from self.kohlrabi.send_msg(result, queue='{}-RESULT'.format(ack_id))