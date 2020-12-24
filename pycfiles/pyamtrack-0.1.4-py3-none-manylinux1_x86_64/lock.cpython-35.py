# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/lock.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 2912 bytes
__doc__ = "PyAMS_utils.lock module\n\nThis module is use to manage shared locks; these locks can be used accross several\nprocesses; the lock relies on a shared value stored info Beaker's cache.\n"
import time
from threading import local
from beaker import cache
__docformat__ = 'restructuredtext'
_LOCAL = local()

def get_locks_cache():
    """Get locks shared cache"""
    try:
        locks_cache = _LOCAL.locks_cache
    except AttributeError:
        manager = cache.CacheManager(**cache.cache_regions['persistent'])
        locks_cache = _LOCAL.locks_cache = manager.get_cache('PyAMS::locks')

    return locks_cache


class LockException(Exception):
    """LockException"""
    pass


class CacheLock:
    """CacheLock"""

    def __init__(self, name, wait=True):
        self.key = 'PyAMS::lock::{0}'.format(name)
        self.wait = wait
        self.has_lock = False

    def __enter__(self):
        locks_cache = get_locks_cache()
        while True:
            test = locks_cache.has_key(self.key)
            if test:
                if not self.wait:
                    raise LockException()
                time.sleep(0.1)
            else:
                locks_cache.set_value(self.key, 1)
                self.has_lock = True
                return

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.has_lock:
            get_locks_cache().remove_value(self.key)
        return False


def locked(name, wait=True):
    """Locked function decorator

    Can be used with any function or method which requires a global shared lock.

    :param str name: name of the lock to use as shared key
    :param boolean wait: if *False*, a *LockException* is raised if lock can't be taken; otherwise,
        application waits until lock is released
    """

    def lock_decorator(func):

        def wrapper(*args, **kwargs):
            with CacheLock(name, wait):
                return func(*args, **kwargs)

        return wrapper

    return lock_decorator