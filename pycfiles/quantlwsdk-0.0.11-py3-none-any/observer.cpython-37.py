# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\observer.py
# Compiled at: 2019-06-05 03:26:08
# Size of source mod 2**32: 3531 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, six
from pyalgotrade import dispatchprio

class Event(object):

    def __init__(self):
        self._Event__handlers = []
        self._Event__deferred = []
        self._Event__emitting = 0

    def __subscribeImpl(self, handler):
        assert not self._Event__emitting
        if handler not in self._Event__handlers:
            self._Event__handlers.append(handler)

    def __unsubscribeImpl(self, handler):
        assert not self._Event__emitting
        self._Event__handlers.remove(handler)

    def __applyChanges(self):
        assert not self._Event__emitting
        for action, param in self._Event__deferred:
            action(param)

        self._Event__deferred = []

    def subscribe(self, handler):
        if self._Event__emitting:
            self._Event__deferred.append((self._Event__subscribeImpl, handler))
        else:
            if handler not in self._Event__handlers:
                self._Event__subscribeImpl(handler)

    def unsubscribe(self, handler):
        if self._Event__emitting:
            self._Event__deferred.append((self._Event__unsubscribeImpl, handler))
        else:
            self._Event__unsubscribeImpl(handler)

    def emit(self, *args, **kwargs):
        try:
            self._Event__emitting += 1
            for handler in self._Event__handlers:
                handler(*args, **kwargs)

        finally:
            self._Event__emitting -= 1
            if not self._Event__emitting:
                self._Event__applyChanges()


@six.add_metaclass(abc.ABCMeta)
class Subject(object):

    def __init__(self):
        self._Subject__dispatchPrio = dispatchprio.LAST

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
        return self._Subject__dispatchPrio

    def setDispatchPriority(self, dispatchPrio):
        self._Subject__dispatchPrio = dispatchPrio

    def onDispatcherRegistered(self, dispatcher):
        pass