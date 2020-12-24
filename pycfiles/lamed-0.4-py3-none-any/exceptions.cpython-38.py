# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/pb/598z8h910dvf2wrvwnbyl_2m0000gn/T/pip-install-03p63p8r/redis/redis/exceptions.py
# Compiled at: 2020-04-05 04:25:10
# Size of source mod 2**32: 1341 bytes
"""Core exceptions raised by the Redis client"""

class RedisError(Exception):
    pass


class ConnectionError(RedisError):
    pass


class TimeoutError(RedisError):
    pass


class AuthenticationError(ConnectionError):
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


class NoPermissionError(ResponseError):
    pass


class LockError(RedisError, ValueError):
    __doc__ = 'Errors acquiring or releasing a lock'


class LockNotOwnedError(LockError):
    __doc__ = 'Error trying to extend or release a lock that is (no longer) owned'


class ChildDeadlockedError(Exception):
    __doc__ = 'Error indicating that a child process is deadlocked after a fork()'


class AuthenticationWrongNumberOfArgsError(ResponseError):
    __doc__ = '\n    An error to indicate that the wrong number of args\n    were sent to the AUTH command\n    '