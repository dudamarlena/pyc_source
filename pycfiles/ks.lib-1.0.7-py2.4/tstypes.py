# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/lib/tstypes/tstypes.py
# Compiled at: 2008-10-21 04:34:39
"""TSTypes

$Id: tstypes.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from threading import RLock, Lock

class TSDict(dict):
    __module__ = __name__

    def __init__(self):
        self.lock_obj = RLock()

    def lock(self):
        return self.lock_obj.acquire()

    def unlock(self):
        return self.lock_obj.release()


class TSList(list):
    __module__ = __name__

    def __init__(self):
        self.lock_obj = RLock()

    def lock(self):
        return self.lock_obj.acquire()

    def unlock(self):
        return self.lock_obj.release()


class TSObject(object):
    __module__ = __name__

    def __init__(self, value=None):
        self.lock_obj = RLock()
        self._value = value

    def lock(self):
        return self.lock_obj.acquire()

    def unlock(self):
        return self.lock_obj.release()

    def _getValue(self):
        return self._value

    def _setValue(self, value):
        self._value = value

    value = property(_getValue, _setValue)