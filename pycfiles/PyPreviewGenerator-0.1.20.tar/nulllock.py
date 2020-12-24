# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pypreval/nulllock.py
# Compiled at: 2008-02-20 17:53:52
__doc__ = '\nNullLock class that implements null operations, meaning\nthat the Store class will not serialize transactions.\nWhich means that serializing is the responsibility of the user.\n'

class NullLock(object):
    """ignore acquire/release"""

    def acquire(self):
        """acquire a lock to protect a critical region"""
        pass

    def release(self):
        """acquire a lock to protect a critical region"""
        pass