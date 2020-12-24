# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/singleton.py
# Compiled at: 2019-03-10 21:30:22
# Size of source mod 2**32: 2714 bytes
__author__ = [
 'reyoung', 'danceiny']
from threading import Lock

class Singleton(object):
    __doc__ = '\n    The Singleton class decorator.\n    Like:\n        from singleton.singleton import Singleton\n\n        @Singleton\n        class IntSingleton(object):\n            def __init__(self):\n                pass\n    Use IntSingleton() get the instance\n    '

    def __init__(self, cls):
        """
        :param cls: decorator class type
        """
        self._Singleton__cls = cls
        self._Singleton__instance = None

    def instance(self):
        """
        Get singleton instance
        :return: instance object
        """
        if not self.is_initialized():
            self.initialize()
        return self._Singleton__instance

    def initialize(self, *args, **kwargs):
        """
        Initialize singleton object if it has not been initialized
        :param args: class init parameters
        :param kwargs: class init parameters
        """
        if not self.is_initialized():
            self._Singleton__instance = (self._Singleton__cls)(*args, **kwargs)

    def is_initialized(self):
        """
        :return: true if instance is initialized
        """
        return self._Singleton__instance is not None

    def __call__(self, *args, **kwargs):
        if not self.is_initialized():
            (self.initialize)(*args, **kwargs)
        return self._Singleton__instance

    def __instancecheck__(self, inst):
        """
        Helper for isinstance check
        """
        return isinstance(inst, self._Singleton__cls)

    def __getattr__(self, item):
        return getattr(self._Singleton__instance, item)


class ThreadSafeSingleton(object):

    def __init__(self, cls):
        self._ThreadSafeSingleton__cls = cls
        self._ThreadSafeSingleton__instance = None
        self._ThreadSafeSingleton__mutex = Lock()

    def is_initialized(self):
        self._ThreadSafeSingleton__mutex.acquire()
        try:
            return self._ThreadSafeSingleton__instance is not None
        finally:
            self._ThreadSafeSingleton__mutex.release()

    def instance(self):
        self._ThreadSafeSingleton__mutex.acquire()
        try:
            if self._ThreadSafeSingleton__instance is None:
                self._ThreadSafeSingleton__instance = self._ThreadSafeSingleton__cls()
            return self._ThreadSafeSingleton__instance
        finally:
            self._ThreadSafeSingleton__mutex.release()

    def __call__(self, *args, **kwargs):
        self._ThreadSafeSingleton__mutex.acquire()
        try:
            if self._ThreadSafeSingleton__instance is None:
                self._ThreadSafeSingleton__instance = (self._ThreadSafeSingleton__cls)(*args, **kwargs)
        finally:
            return

        self._ThreadSafeSingleton__mutex.release()
        return self._ThreadSafeSingleton__instance

    def __instancecheck__(self, inst):
        """
        Helper for isinstance check
        """
        return isinstance(inst, self._ThreadSafeSingleton__cls)

    def __getattr__(self, item):
        return getattr(self._ThreadSafeSingleton__instance, item)