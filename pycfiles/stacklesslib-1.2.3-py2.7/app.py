# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\stacklesslib\app.py
# Compiled at: 2017-12-11 20:12:50
"""
This module contains a collection of classes and functions that are generally
swapped out to a different implementation if an application is running under
the stackless-framework.  It is intended for things such as sleep(), whose
Stackless-implementation won't work unless the framework is being ticket.
Contrast this with stacklesslib.locks.Lock() which also works as a normal
thread locking primitive.
The replacement is indirected, so that client code can bind directly
to the functions here, e.g. use "from stacklesslib.app import sleep"
"""
import time, threading
from . import events
from .base import atomic, SignalChannel

class _SleepHandler(object):
    """
    A class to support sleep functionality
    """

    def __init__(self):
        self.chan = SignalChannel()

    def sleep(self, delay):
        if delay <= 0:
            c = self.chan
        else:
            c = SignalChannel()
        if delay <= 0:
            _event_queue.call_soon(c.signal)
        else:
            _event_queue.call_later(delay, c.signal)
        c.receive()


class _ObjProxy(object):

    def __init__(self, name):
        self._name = name

    def __getattr__(self, attr):
        return getattr(globals()[self._name], attr)


def sleep(delay):
    _sleep(delay)


def Event():
    return _Event()


def Lock():
    return _Lock()


def RLock():
    return _Rlock()


def Condition():
    return _Condition()


def Semaphore():
    return _Semaphore()


event_queue = _ObjProxy('_event_queue')

def install_vanilla():
    """
    Set up the globals to use default thread-blocking features
    """
    g = globals()
    g['_sleep'] = time.sleep
    g['_Event'] = threading.Event
    g['_Lock'] = threading.Lock
    g['_Rlock'] = threading.RLock
    g['_Condition'] = threading.Condition
    g['_Semaphore'] = threading.Semaphore
    g['_event_queue'] = events.DummyEventQueue()


def install_stackless():
    """
    Set up the globals for a functioning event event loop
    """
    from . import locks
    from . import main
    g = globals()
    g['_sleep'] = _SleepHandler().sleep
    g['_Event'] = locks.Event
    g['_Lock'] = locks.Lock
    g['_Rlock'] = locks.RLock
    g['_Condition'] = locks.Condition
    g['_Semaphore'] = locks.Semaphore
    g['_event_queue'] = main.event_queue


install_vanilla()