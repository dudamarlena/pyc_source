# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/brukva/exceptions.py
# Compiled at: 2011-02-09 16:59:17


class RedisError(Exception):
    pass


class ConnectionError(RedisError):
    pass


class ResponseError(RedisError):

    def __init__(self, message, cmd_line):
        self.message = message
        self.cmd_line = cmd_line

    def __repr__(self):
        return 'ResponseError (on %s [%s, %s]): %s' % (self.cmd_line.cmd, self.cmd_line.args, self.cmd_line.kwargs, self.message)

    __str__ = __repr__


class InvalidResponse(RedisError):
    pass