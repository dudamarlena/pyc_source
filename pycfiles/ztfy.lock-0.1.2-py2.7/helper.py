# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/lock/helper.py
# Compiled at: 2012-06-11 15:35:37
import os
from persistent import Persistent
from threading import Lock
from lovely.memcached.interfaces import IMemcachedClient
from zope.annotation.interfaces import IAnnotations
from zope.schema.interfaces import IVocabularyFactory
from ztfy.lock.interfaces import ILockingHelper, IFileLockingInfo, IFileLockingHelper, IFileLockingTarget, IMemcachedLockingInfo, IMemcachedLockingHelper, IMemcachedLockingTarget
from zc.lockfile import LockFile, LockError
from zope.component import adapter, queryUtility
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.interface import implementer, implements, classProvides
from zope.schema.fieldproperty import FieldProperty
from ztfy.utils.catalog import getIntIdUtility
from ztfy.lock import _
_ThreadLocks = {}

class ThreadLockingHelper(object):
    """Thread locking helper"""
    implements(ILockingHelper)
    marker_interface = None

    def getLock(self, utility, target):
        intids = getIntIdUtility()
        oid = intids.register(target)
        if oid in _ThreadLocks:
            return None
        else:
            lock = _ThreadLocks[oid] = Lock()
            lock.acquire(blocking=False)
            return (oid, lock)

    def releaseLock(self, lock):
        assert isinstance(lock, tuple)
        oid, lock = lock
        assert isinstance(lock, Lock)
        if oid in _ThreadLocks:
            lock.release()
            del _ThreadLocks[oid]


ThreadLockingHelper = ThreadLockingHelper()
FILE_LOCKING_INFO_KEY = 'ztfy.lock.lockfile'

class FileLockingInfo(Persistent):
    """File locking infos"""
    implements(IFileLockingInfo)
    locks_path = FieldProperty(IFileLockingInfo['locks_path'])


@adapter(IFileLockingTarget)
@implementer(IFileLockingInfo)
def FileLockingInfoFactory(context):
    """File locker info factory"""
    annotations = IAnnotations(context)
    helper = annotations.get(FILE_LOCKING_INFO_KEY)
    if helper is None:
        helper = annotations[FILE_LOCKING_INFO_KEY] = FileLockingInfo()
    return helper


class FileLockingHelper(object):
    """File locking helper"""
    implements(IFileLockingHelper)
    marker_interface = IFileLockingTarget

    def getLock(self, utility, target):
        info = IFileLockingInfo(utility, None)
        if info is None or not info.locks_path:
            raise Exception(_('Locking utility is not configured to use file locking !'))
        intids = getIntIdUtility()
        lock_path = os.path.join(info.locks_path, 'uid-%d.lock' % intids.register(target))
        try:
            return LockFile(lock_path)
        except LockError:
            return

        return

    def releaseLock(self, lock):
        assert isinstance(lock, LockFile)
        lock.close()
        if os.path.exists(lock._path):
            os.unlink(lock._path)


FileLockingHelper = FileLockingHelper()
MEMCACHED_LOCKING_INFO_KEY = 'ztfy.lock.memcached'

class MemcachedLockingInfo(Persistent):
    """Memcached locking infos"""
    implements(IMemcachedLockingInfo)
    memcached_client = FieldProperty(IMemcachedLockingInfo['memcached_client'])
    locks_namespace = FieldProperty(IMemcachedLockingInfo['locks_namespace'])


@adapter(IMemcachedLockingTarget)
@implementer(IMemcachedLockingInfo)
def MemcachedLockingInfoFactory(context):
    """Memcached locking info factory"""
    annotations = IAnnotations(context)
    helper = annotations.get(MEMCACHED_LOCKING_INFO_KEY)
    if helper is None:
        helper = annotations[MEMCACHED_LOCKING_INFO_KEY] = MemcachedLockingInfo()
    return helper


class MemcachedLockingHelper(object):
    """Memcached locking helper"""
    implements(IMemcachedLockingHelper)
    marker_interface = IMemcachedLockingTarget

    def getLock(self, utility, target):
        info = IMemcachedLockingInfo(utility, None)
        if info is None or not info.memcached_client:
            raise Exception(_('Locking utility is not configured to use memcached locking !'))
        memcached = queryUtility(IMemcachedClient, info.memcached_client)
        if memcached is None:
            raise Exception(_("Memcached client '%s' can't be found !") % info.memcached_client)
        intids = getIntIdUtility()
        key = 'uid-%d.lock' % intids.register(target)
        result = memcached.client.add(key, 'LOCKED')
        if not result:
            return
        else:
            return (
             memcached, key)
            return

    def releaseLock(self, lock):
        assert isinstance(lock, tuple)
        memcached, key = lock
        memcached.client.delete(key)


MemcachedLockingHelper = MemcachedLockingHelper()

class LockingHelpersVocabulary(UtilityVocabulary):
    """Locking helpers vocabulary"""
    classProvides(IVocabularyFactory)
    interface = ILockingHelper
    nameOnly = True