# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/exceptions.py
# Compiled at: 2019-06-20 09:27:12
# Size of source mod 2**32: 1953 bytes
__doc__ = '\nModule for custom exceptions\n'

class BTrDBError(Exception):
    """BTrDBError"""

    def __init__(self, code, msg, mash):
        self.code = code
        self.msg = msg
        self.mash = mash

    @staticmethod
    def fromProtoStat(protoStatus):
        return BTrDBError(protoStatus.code, protoStatus.msg, protoStatus.mash)

    @staticmethod
    def checkProtoStat(protoStatus):
        stat = BTrDBError.fromProtoStat(protoStatus)
        if stat.isError():
            raise stat

    def isError(self):
        return self.code != 0

    def __repr__(self):
        return '{3}({0}, {1}, {2})'.format(repr(self.code), repr(self.msg), repr(self.mash), self.__class__.__name__)

    def __str__(self):
        if self.isError():
            return '[{0}] {1}'.format(self.code, self.msg)
        return '<success>'


class ConnectionError(Exception):
    """ConnectionError"""
    pass


class InvalidOperation(Exception):
    """InvalidOperation"""
    pass


class NotFound(Exception):
    """NotFound"""
    pass


class BTRDBValueError(ValueError):
    """BTRDBValueError"""
    pass


class BTRDBTypeError(TypeError):
    """BTRDBTypeError"""
    pass


class CredentialsFileNotFound(FileNotFoundError):
    """CredentialsFileNotFound"""
    pass


class ProfileNotFound(Exception):
    """ProfileNotFound"""
    pass