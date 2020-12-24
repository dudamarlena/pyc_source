# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/yedis/exceptions.py
# Compiled at: 2018-10-31 18:35:23
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
    """Errors acquiring or releasing a lock"""
    pass