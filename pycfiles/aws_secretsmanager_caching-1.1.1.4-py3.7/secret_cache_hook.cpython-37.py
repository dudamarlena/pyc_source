# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/aws_secretsmanager_caching/cache/secret_cache_hook.py
# Compiled at: 2019-05-13 16:05:47
# Size of source mod 2**32: 1267 bytes
"""Secret cache hook"""
from abc import ABCMeta, abstractmethod

class SecretCacheHook:
    __doc__ = 'Interface to hook the local in-memory cache.  This interface will allow\n    for clients to perform actions on the items being stored in the in-memory\n    cache.  One example would be encrypting/decrypting items stored in the\n    in-memory cache.'
    __metaclass__ = ABCMeta

    def __init__(self):
        """Construct the secret cache hook."""
        pass

    @abstractmethod
    def put(self, obj):
        """Prepare the object for storing in the cache"""
        pass

    @abstractmethod
    def get(self, cached_obj):
        """Derive the object from the cached object."""
        pass