# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/pangu_task/task.py
# Compiled at: 2020-03-09 11:30:37
# Size of source mod 2**32: 1118 bytes
import threading

class Proxy:

    def __init__(self, method, *args, **kwargs):
        assert callable(method), 'method must be a function'
        self.original_method = method
        self.init = kwargs.get('init')
        self.callback = kwargs.get('callback')

    def __call__(self, *args, **kwargs):
        return (self._Proxy__new_method)(*args, **kwargs)

    def __new_method(self, *args, **kwargs):
        if self.init:
            self.init()
        result = (self.original_method)(*args, **kwargs)
        if self.callback:
            if self.callback.__code__.co_argcount == 1:
                self.callback(result)
            else:
                self.callback()
        return result

    def delay(self, *args, **kwargs):
        t = threading.Thread(target=(self._Proxy__new_method), args=args, kwargs=kwargs)
        t.start()

    def execute(self, *args, **kwargs):
        (self._Proxy__new_method)(*args, **kwargs)


def task(*args, **kwargs):
    if len(args) == 1:
        if callable(args[0]):
            return Proxy(args[0])

    def wrapper(method):
        return Proxy(method, *args, **kwargs)

    return wrapper