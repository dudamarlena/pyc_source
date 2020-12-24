# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/singleton/singleton.py
# Compiled at: 2013-12-18 23:38:22
__author__ = 'reyoung'

class Singleton(object):
    """
    The Singleton class decorator.
    Like:
        from singleton.singleton import Singleton

        @Singleton
        class IntSingleton(object):
            def __init__(self):
                pass
    Use IntSingleton.instance() get the instance
    """

    def __init__(self, cls):
        """
        :param cls: decorator class type
        """
        self.__cls = cls
        self.__instance = None
        return

    def initialize(self, *args, **kwargs):
        """
        Initialize singleton object if it has not been initialized
        :param args: class init parameters
        :param kwargs: class init parameters
        """
        if not self.is_initialized():
            self.__instance = self.__cls(*args, **kwargs)

    def is_initialized(self):
        """
        :return: true if instance is initialized
        """
        return self.__instance is not None

    def instance(self):
        """
        Get singleton instance
        :return: instance object
        """
        if not self.is_initialized():
            self.initialize()
        return self.__instance

    def __call__(self, *args, **kwargs):
        """
        Disable new instance of original class
        :raise TypeError:
        """
        raise TypeError('Singletons must be access by instance')

    def __instancecheck__(self, inst):
        """
        Helper for isinstance check
        """
        return isinstance(inst, self.__cls)


from threading import Lock

class ThreadSafeSingleton(object):

    def __init__(self, cls):
        self.__cls = cls
        self.__instance = None
        self.__mutex = Lock()
        return

    def is_initialized(self):
        self.__mutex.acquire()
        try:
            return self.__instance is not None
        finally:
            self.__mutex.release()

        return

    def initialize(self, *args, **kwargs):
        self.__mutex.acquire()
        try:
            if self.__instance is None:
                self.__instance = self.__cls(*args, **kwargs)
        finally:
            self.__mutex.release()

        return

    def instance(self):
        self.__mutex.acquire()
        try:
            if self.__instance is None:
                self.__instance = self.__cls()
            return self.__instance
        finally:
            self.__mutex.release()

        return

    def __call__(self, *args, **kwargs):
        """
        Disable new instance of original class
        :raise TypeError:
        """
        raise TypeError('Singletons must be access by instance')

    def __instancecheck__(self, inst):
        """
        Helper for isinstance check
        """
        return isinstance(inst, self.__cls)