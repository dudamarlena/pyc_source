# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/redis/exceptions.py
# Compiled at: 2012-02-14 23:34:00
__doc__ = 'Core exceptions raised by the Redis client'

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