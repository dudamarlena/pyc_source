# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redis/exceptions.py
# Compiled at: 2012-02-14 23:34:00
"""Core exceptions raised by the Redis client"""

class RedisError(Exception):
    pass


class AuthenticationError(RedisError):
    pass


class ConnectionError(RedisError):
    pass


class ResponseError(RedisError):
    pass


class InvalidResponse(RedisError):
    pass


class InvalidData(RedisError):
    pass