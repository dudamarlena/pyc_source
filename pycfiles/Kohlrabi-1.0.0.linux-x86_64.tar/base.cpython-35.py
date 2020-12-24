# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/storage/eyes/virtualenv/kohlrabi/lib/python3.5/site-packages/libkohlrabi/tasks/base.py
# Compiled at: 2016-04-01 07:47:41
# Size of source mod 2**32: 1047 bytes
"""
Base task class.
"""
import asyncio, types

class TaskBase(object):
    __doc__ = '\n    Base task.\n    '

    def __init__(self, kh, func: types.FunctionType, id=None):
        self._func = func
        self.coro = self._wrap_func(func)
        self.loop = asyncio.get_event_loop()
        self.kohlrabi = kh
        self.task_id = id if id else self._func.__module__ + '.' + self._func.__name__

    def __call__(self, *args, **kwargs):
        return self.invoke_func(*args, **kwargs)

    @staticmethod
    def _wrap_func(func_obj: types.FunctionType) -> types.FunctionType:
        if func_obj.__code__.co_flags & 384 or func_obj.__code__.co_flags & 32:
            return func_obj
        else:
            return asyncio.coroutine(func_obj)

    def invoke_func(self, *args, **kwargs):
        """
        Invoke the function.

        This is different on server side and client side.
        """
        raise NotImplementedError