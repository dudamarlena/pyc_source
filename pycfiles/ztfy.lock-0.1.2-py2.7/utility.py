# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/lock/utility.py
# Compiled at: 2012-06-11 15:35:37
from persistent import Persistent
from ztfy.lock.interfaces import ILockingUtility, ILockingHelper
from zope.component import queryUtility, getUtility
from zope.container.contained import Contained
from zope.interface import implements, alsoProvides, noLongerProvides
from zope.schema.fieldproperty import FieldProperty
from ztfy.lock.helper import ThreadLockingHelper

class LockingUtility(Persistent, Contained):
    """Locker utility class"""
    implements(ILockingUtility)
    _policy = FieldProperty(ILockingUtility['policy'])

    @property
    def policy(self):
        return self._policy

    @policy.setter
    def policy(self, value):
        if value != self._policy:
            if self._policy is not None:
                locker = queryUtility(ILockingHelper, self._policy)
                if locker is not None and locker.marker_interface is not None and locker.marker_interface.providedBy(self):
                    noLongerProvides(self, locker.marker_interface)
            self._policy = value
            if value:
                locker = getUtility(ILockingHelper, value)
                if locker.marker_interface is not None:
                    alsoProvides(self, locker.marker_interface)
        return

    def _getLocker(self):
        if not self._policy:
            return ThreadLockingHelper
        else:
            return getUtility(ILockingHelper, self._policy)

    def getLock(self, target, wait=False):
        helper = self._getLocker()
        if helper is not None:
            lock = helper.getLock(target)
            while lock is None and wait:
                lock = helper.getLock(self, target)

            if lock is not None:
                return (helper, lock)
        return

    def releaseLock(self, lock):
        if lock is None:
            return
        else:
            helper, lock = lock
            helper.releaseLock(lock)
            return