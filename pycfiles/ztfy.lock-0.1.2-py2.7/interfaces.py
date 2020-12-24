# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/lock/interfaces.py
# Compiled at: 2012-06-11 15:35:37
from zope.interface import Interface, Attribute
from zope.schema import Choice, TextLine
from ztfy.utils.schema import StringLine
from ztfy.lock import _

class ILockingUtility(Interface):
    """Locking utility interface"""
    policy = Choice(title=_('Locking policy'), description=_('Locking policy can be used to create locks in multi-processes and/or multi-hosts environments'), vocabulary='ZTFY locking helpers', required=False)

    def getLock(self, target, wait=False):
        """Try to get lock for given object"""
        pass

    def releaseLock(self, lock):
        """Release given lock
        
        Input value is the one returned by getLock()
        """
        pass


class ILockingHelper(Interface):
    """Base interface for locker informations"""
    marker_interface = Attribute(_('Class name of lock helper target marker interface'))

    def getLock(self, utility, target):
        """Try to get lock for given object"""
        pass

    def releaseLock(self, lock):
        """Release given lock
        
        Input value is the one returned by getLock()
        """
        pass


class IFileLockingInfo(Interface):
    """File locking info"""
    locks_path = TextLine(title=_('Locks base path'), description=_("Full path of server's directory storing locks"), required=True, default='/var/lock')


class IFileLockingHelper(ILockingHelper):
    """File locking utility"""
    pass


class IFileLockingTarget(Interface):
    """Marker interface for lockers using file locking"""
    pass


class IMemcachedLockingInfo(Interface):
    """Memcached locker info"""
    memcached_client = TextLine(title=_('Memcached client'), description=_('Name of memcached client connection'), required=True)
    locks_namespace = StringLine(title=_('Locks namespace'), description=_('Memcached namespace used to define locks'), required=True, default='ztfy.lock')


class IMemcachedLockingHelper(ILockingHelper):
    """Memcached locking helper utility"""
    pass


class IMemcachedLockingTarget(Interface):
    """Marker interface for lockers using memcached locking"""
    pass