# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/factories/meta.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 425 bytes
from abc import ABC, abstractmethod

class LockFactoryMeta(ABC):

    @abstractmethod
    def new_lock(self, key, **params):
        """Must return an object with a Lock-like interface"""
        pass

    @abstractmethod
    def get_lock_list(self):
        """Must return a list of string keys of existing locks"""
        pass

    @abstractmethod
    def clear_all(self):
        """Must clear all locks from the system (primarily for testing)"""
        pass