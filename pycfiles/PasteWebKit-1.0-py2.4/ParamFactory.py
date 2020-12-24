# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/ParamFactory.py
# Compiled at: 2006-10-22 17:01:01
from threading import Lock

class ParamFactory:
    __module__ = __name__

    def __init__(self, klass, **extraMethods):
        self.lock = Lock()
        self.cache = {}
        self.klass = klass
        for (name, func) in extraMethods.items():
            setattr(self, name, func)

    def __call__(self, *args):
        self.lock.acquire()
        if not self.cache.has_key(args):
            value = self.klass(*args)
            self.cache[args] = value
            self.lock.release()
            return value
        else:
            self.lock.release()
            return self.cache[args]

    def allInstances(self):
        return self.cache.values()