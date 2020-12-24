# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/factories/native.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 585 bytes
from threading import Lock
from .meta import LockFactoryMeta

class NativeLockFactory(LockFactoryMeta):
    __doc__ = 'Demonstrates use of alternative lock implementations'

    def __init__(self):
        self.all_locks = {}

    def new_lock(self, key, **params):
        return self.all_locks.setdefault(key, Lock())

    def get_lock_list(self):
        return list(self.all_locks.keys())

    def clear_all(self):
        self.all_locks.clear()