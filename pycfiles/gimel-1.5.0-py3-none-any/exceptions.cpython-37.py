# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/redis/exceptions.py
# Compiled at: 2019-07-06 06:05:05
# Size of source mod 2**32: 1224 bytes
"""Core exceptions raised by the Redis client"""
from redis._compat import unicode

class RedisError(Exception):
    pass


if not hasattr(RedisError, '__unicode__'):

    def __unicode__(self):
        if isinstance(self.args[0], unicode):
            return self.args[0]
        return unicode(self.args[0])


    RedisError.__unicode__ = __unicode__

class AuthenticationError(RedisError):
    pass


class ConnectionError(RedisError):
    pass


class TimeoutError(RedisError):
    pass


class BusyLoadingError(ConnectionError):
    pass


class InvalidResponse(RedisError):
    pass


class ResponseError(RedisError):
    pass


class DataError(RedisError):
    pass


class PubSubError(RedisError):
    pass


class WatchError(RedisError):
    pass


class NoScriptError(ResponseError):
    pass


class ExecAbortError(ResponseError):
    pass


class ReadOnlyError(ResponseError):
    pass


class LockError(RedisError, ValueError):
    __doc__ = 'Errors acquiring or releasing a lock'