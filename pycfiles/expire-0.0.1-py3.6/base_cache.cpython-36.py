# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/expire/base_cache.py
# Compiled at: 2017-12-26 08:35:17
# Size of source mod 2**32: 1452 bytes
import abc

class BaseCache(metaclass=abc.ABCMeta):
    __doc__ = '\n    The class defines some functions that is necessary provided by RedisCache MemoryCache MemcachedCache\n    '

    def __init__(self, serializer, namespace=None, **kwargs):
        self.namespace = namespace
        self.serializer = serializer()

    @abc.abstractmethod
    def set(self, key, value, ttl=None, **kwargs):
        """
        Set the value at key ``key`` to ``value``
        """
        pass

    @abc.abstractmethod
    def get(self, key, default=None, **kwargs):
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        pass

    @abc.abstractmethod
    def delete(self, *keys, **kwargs):
        """
        Delete one or more keys specified by ``keys``
        """
        pass

    @abc.abstractmethod
    def exists(self, key, **kwargs):
        """
        Returns a boolean indicating whether key ``name`` exists
        """
        pass

    @abc.abstractmethod
    def incr(self, key, **kwargs):
        """
        Increments the value of ``key``.
        """
        pass


class BaseSerializer(metaclass=abc.ABCMeta):
    __doc__ = '\n    The class defines some functions that is necessary provided by JsonSerializer PickleSerializer\n    '

    @abc.abstractmethod
    def dumps(self, value, **kwargs):
        pass

    @abc.abstractmethod
    def loads(self, value, **kwargs):
        pass