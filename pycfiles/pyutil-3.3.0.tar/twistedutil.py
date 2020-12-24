# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/twistedutil.py
# Compiled at: 2018-01-06 14:43:43
import warnings
from twisted.internet import reactor
from weakutil import WeakMethod

def callLater_weakly(delay, func, *args, **kwargs):
    """
    Call func later, but if func is a bound method then make the reference it holds to object be a weak reference.

    Therefore, if this scheduled event is a bound method and it is the only thing keeping the object from being garbage collected, the object will be garbage collected and the event will be cancelled.
    """
    warnings.warn('deprecated', DeprecationWarning)

    def cleanup(weakmeth, thedeadweakref):
        if weakmeth.callId.active():
            weakmeth.callId.cancel()

    weakmeth = WeakMethod(func, callback=cleanup)
    weakmeth.callId = reactor.callLater(delay, weakmeth, *args, **kwargs)
    return weakmeth