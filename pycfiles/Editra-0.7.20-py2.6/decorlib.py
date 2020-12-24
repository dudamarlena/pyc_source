# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/extern/decorlib.py
# Compiled at: 2008-10-31 22:25:32
"""
Collection of helpful decorator methods

"""
__all__ = [
 'anythread']
import wx, threading
_EVT_INVOKE_METHOD = wx.NewEventType()

class MethodInvocationEvent(wx.PyEvent):
    """Event fired to the GUI thread indicating a method invocation."""

    def __init__(self, func, args, kwds):
        wx.PyEvent.__init__(self)
        self.SetEventType(_EVT_INVOKE_METHOD)
        self.func = func
        self.args = args
        self.kwds = kwds
        self.blocker = threading.Semaphore(0)

    def invoke(self):
        wx.PostEvent(self.args[0], self)
        self.blocker.acquire()
        try:
            return self.result
        except AttributeError:
            raise self.exception

    def process(self):
        try:
            self.result = self.func(*self.args, **self.kwds)
        except Exception, e:
            self.exception = e

        self.blocker.release()


def handler(evt):
    evt.process()


def anythread(func):
    """Method decorator allowing call from any thread.
    The method is replaced by one that posts a MethodInvocationEvent to the
    object, then blocks waiting for it to be completed.  The target object
    if automatically connected to the _EVT_INVOKE_METHOD event if it wasn't
    alread connected.

    """

    def invoker(*args, **kwds):
        if wx.Thread_IsMain():
            return func(*args, **kwds)
        else:
            self = args[0]
            if not hasattr(self, '_AnyThread__connected'):
                self.Connect(-1, -1, _EVT_INVOKE_METHOD, handler)
                self._AnyThread__connected = True
            evt = MethodInvocationEvent(func, args, kwds)
            return evt.invoke()

    invoker.__name__ = func.__name__
    invoker.__doc__ = func.__doc__
    return invoker