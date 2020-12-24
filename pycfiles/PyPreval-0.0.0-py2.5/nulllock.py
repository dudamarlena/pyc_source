# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/nulllock.py
# Compiled at: 2008-02-20 17:53:52
"""
NullLock class that implements null operations, meaning
that the Store class will not serialize transactions.
Which means that serializing is the responsibility of the user.
"""

class NullLock(object):
    """ignore acquire/release"""

    def acquire(self):
        """acquire a lock to protect a critical region"""
        pass

    def release(self):
        """acquire a lock to protect a critical region"""
        pass