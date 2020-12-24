# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/observer.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import abc
from pyalgotrade import dispatchprio

class Event(object):

    def __init__(self):
        self.__handlers = []
        self.__toSubscribe = []
        self.__toUnsubscribe = []
        self.__emitting = False

    def __applyChanges(self):
        if len(self.__toSubscribe):
            for handler in self.__toSubscribe:
                if handler not in self.__handlers:
                    self.__handlers.append(handler)

            self.__toSubscribe = []
        if len(self.__toUnsubscribe):
            for handler in self.__toUnsubscribe:
                self.__handlers.remove(handler)

            self.__toUnsubscribe = []

    def subscribe(self, handler):
        if self.__emitting:
            self.__toSubscribe.append(handler)
        elif handler not in self.__handlers:
            self.__handlers.append(handler)

    def unsubscribe(self, handler):
        if self.__emitting:
            self.__toUnsubscribe.append(handler)
        else:
            self.__handlers.remove(handler)

    def emit(self, *args, **kwargs):
        try:
            self.__emitting = True
            for handler in self.__handlers:
                handler(*args, **kwargs)

        finally:
            self.__emitting = False
            self.__applyChanges()


class Subject(object):
    __metaclass__ = abc.ABCMeta

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