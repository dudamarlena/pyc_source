# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/synchronized.py
# Compiled at: 2007-12-02 16:26:56
from threading import *

class synchronized(object):
    """

    >>> class Test(object):
    ...   def __init__(self, val):
    ...     self.val = val
    ...   @autosynchronized
    ...   def test(self, arg):
    ...     self.val = self.val + arg
    ...     return self.val

    >>> t = Test(4)
    >>> t.test(10)
    14
    >>> t.test(4)
    18

    """
    __module__ = __name__

    def __init__(self, lock):
        self.lock = lock

    def __call__(self, func):

        def _inner_synchronized(*args, **kwargs):
            self.lock.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                self.lock.release()

        return _inner_synchronized


def autosynchronized(func):
    return synchronized(Lock())(func)


from salamoia.tests import *
runDocTests()