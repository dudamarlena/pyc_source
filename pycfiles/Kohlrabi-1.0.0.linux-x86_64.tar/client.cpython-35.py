# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/kohlrabi/lib/python3.5/site-packages/libkohlrabi/tasks/client.py
# Compiled at: 2016-04-01 07:47:41
# Size of source mod 2**32: 1288 bytes
"""
Client-side task.
"""
import asyncio
from .base import TaskBase

class ClientTaskResult(object):
    __doc__ = '\n    An object that represents the result of a ClientTask.\n\n    Used to get the result of the coro.\n    '

    def __init__(self, ack_id: int, task_id: str, kh):
        self.ack_id = ack_id
        self.task_id = task_id
        self.kohlrabi = kh

    @asyncio.coroutine
    def _redis_get_func_result(self, timeout=30):
        result = yield from asyncio.wait_for(self.kohlrabi.get_msg(queue='{}-RESULT'.format(self.ack_id)), timeout=timeout)
        return result

    @property
    def result(self):
        return self.kohlrabi._loop.run_until_complete(self._redis_get_func_result())

    def result_with_timeout(self, timeout):
        return self.kohlrabi._loop.run_until_complete(self._redis_get_func_result(timeout=timeout))


class ClientTaskBase(TaskBase):
    __doc__ = '\n    Base class for a client-side task.\n    '

    def invoke_func(self, *args, **kwargs):
        ack_id = self.loop.run_until_complete(self.kohlrabi.apply_task(self, *args, **kwargs))
        return ClientTaskResult(ack_id, self.task_id, self.kohlrabi)