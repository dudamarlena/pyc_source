# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/tailspin/plain.py
# Compiled at: 2009-03-03 00:34:10
import threading, sys
from time import time

class tailfish(object):

    def __init__(self, func, args, kw):
        self._func = func
        self._args = args
        self._kw = kw

    def __force__(self):
        return self.func(*self.args, **self.kw)


def tail(func):
    func._tail_state = threading.local()

    def helper(*args, **kw):
        if not hasattr(func._tail_state, 'recur'):
            func._tail_state.recur = True
        else:
            return tailfish(func, args, kw)
        f = func
        try:
            while True:
                ret = f(*args, **kw)
                if isinstance(ret, tailfish):
                    f = ret._func
                    args = ret._args
                    kw = ret._kw
                else:
                    return ret

        finally:
            del func._tail_state.recur

    return helper


__all__ = [
 'tail']