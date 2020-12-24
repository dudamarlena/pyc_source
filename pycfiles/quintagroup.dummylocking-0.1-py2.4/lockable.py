# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/dummylocking/lockable.py
# Compiled at: 2009-03-17 09:06:20
from zope.interface import implements
from zope.component import adapts
from plone.locking.interfaces import ILockable
from plone.locking.interfaces import ITTWLockable
from plone.locking.interfaces import STEALABLE_LOCK

class DummyTTWLockable(object):
    """ This class provides all methods needed of ILockable adapter.
    """
    __module__ = __name__
    implements(ILockable)
    adapts(ITTWLockable)

    def __init__(self, context):
        self.context = context

    def lock(self, lock_type=STEALABLE_LOCK, children=False):
        pass

    def unlock(self, lock_type=STEALABLE_LOCK, stealable_only=True):
        pass

    def clear_locks(self):
        pass

    def locked(self):
        return False

    def can_safely_unlock(self, lock_type=STEALABLE_LOCK):
        return True

    def stealable(self, lock_type=STEALABLE_LOCK):
        return True

    def lock_info(self):
        return []