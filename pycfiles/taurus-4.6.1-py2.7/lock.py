# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/lock.py
# Compiled at: 2019-08-19 15:09:29
"""This module defines a *slow* lock class that provides additional debugging
information"""
from builtins import object
import threading, logging
__all__ = [
 'TaurusLock']
__docformat__ = 'restructuredtext'
_VERBOSE = False

def TaurusLock(verbose=None, name=None, lock=None):
    if verbose is None:
        verbose = _VERBOSE
    if verbose:
        return _TaurusLock(name=name, lock=lock)
    else:
        if lock is None:
            return threading.Lock()
        return lock


class _TaurusLock(object):
    """A sardana lock"""

    def __init__(self, name=None, lock=None, level=logging.DEBUG):
        name = name or self.__class__.__name__
        self.__name = name
        self.__logger = logging.getLogger(name=name)
        self.__level = level
        if lock is None:
            lock = threading.Lock()
        self.__block = lock
        self.__owner = None
        return

    def __repr__(self):
        owner = self.__owner
        if owner is not None:
            owner = owner.name
        return '<%s owner=%r>' % (self.__name, owner)

    def owner_name(self):
        owner = self.__owner
        if owner is not None:
            return owner.name
        else:
            return

    def _note(self, msg, *args):
        self.__logger.log(self.__level, msg, *args)

    def acquire(self, blocking=1):
        self._note('[START] acquire(%s) [owner=%s]', blocking, self.owner_name())
        rc = self.__block.acquire(blocking)
        me = threading.current_thread()
        if rc:
            self.__owner = me
            state = 'success'
        else:
            state = 'failure'
        self._note('[ END ] acquire(%s) %s [owner=%s]', blocking, state, self.owner_name())
        return rc

    __enter__ = acquire

    def release(self):
        self._note('[START] release() [owner=%s]', self.owner_name())
        self.__block.release()
        self.__owner = None
        self._note('[ END ] release() [owner=%s]', self.owner_name())
        return

    def __exit__(self, t, v, tb):
        self.release()