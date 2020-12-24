# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/greins/synchronization.py
# Compiled at: 2011-09-19 19:30:16


def synchronized(lock_attr):
    """Decorator for conveniently locking a member function
       with exception handling.  This could be replaced by 'with'
       in Python 2.5."""

    def decorator(function):

        def wrapped(self, *args, **kwargs):
            lock = getattr(self, lock_attr, None)
            lock.acquire()
            try:
                return function(self, *args, **kwargs)
            finally:
                lock.release()

            return

        return wrapped

    return decorator