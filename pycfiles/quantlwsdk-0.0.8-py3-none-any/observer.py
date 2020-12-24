# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\observer.py
# Compiled at: 2018-10-21 21:07:45
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, six
from pyalgotrade import dispatchprio

class Event(object):

    def __init__(self):
        self.__handlers = []
        self.__deferred = []
        self.__emitting = 0

    def __subscribeImpl(self, handler):
        assert not self.__emitting
        if handler not in self.__handlers:
            self.__handlers.append(handler)

    def __unsubscribeImpl(self, handler):
        assert not self.__emitting
        self.__handlers.remove(handler)

    def __applyChanges(self):
        assert not self.__emitting
        for action, param in self.__deferred:
            action(param)

        self.__deferred = []

    def subscribe(self, handler):
        if self.__emitting:
            self.__deferred.append((self.__subscribeImpl, handler))
        elif handler not in self.__handlers:
            self.__subscribeImpl(handler)

    def unsubscribe(self, handler):
        if self.__emitting:
            self.__deferred.append((self.__unsubscribeImpl, handler))
        else:
            self.__unsubscribeImpl(handler)

    def emit(self, *args, **kwargs):
        try:
            self.__emitting += 1
            for handler in self.__handlers:
                handler(*args, **kwargs)

        finally:
            self.__emitting -= 1
            if not self.__emitting:
                self.__applyChanges()


@six.add_metaclass(abc.ABCMeta)
class Subject(object):

    def __init__(self):
        self.__dispatchPrio = dispatchprio.LAST

    @abc.abstractmethod
    def start(self):
        pass

    @abc.abstractmethod
    def stop(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def join(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def eof(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def dispatch(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def peekDateTime(self):
        raise NotImplementedError()

    def getDispatchPriority(self):
        return self.__dispatchPrio

    def setDispatchPriority(self, dispatchPrio):
        self.__dispatchPrio = dispatchPrio

    def onDispatcherRegistered(self, dispatcher):
        pass