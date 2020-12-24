# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/btrdb/exceptions.py
# Compiled at: 2019-06-20 09:27:12
# Size of source mod 2**32: 1953 bytes
"""
Module for custom exceptions
"""

class BTrDBError(Exception):
    __doc__ = '\n    The primary exception for grpc related errors.\n    '

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
    __doc__ = '\n    An error has occurred while interacting with the BTrDB server or when trying to establish a connection.\n    '


class InvalidOperation(Exception):
    __doc__ = '\n    An invalid BTrDB operation has been requested.\n    '


class NotFound(Exception):
    __doc__ = '\n    A problem interacting with the BTrDB server.\n    '


class BTRDBValueError(ValueError):
    __doc__ = '\n    A problem interacting with the BTrDB server.\n    '


class BTRDBTypeError(TypeError):
    __doc__ = '\n    A problem interacting with the BTrDB server.\n    '


class CredentialsFileNotFound(FileNotFoundError):
    __doc__ = '\n    The credentials file could not be found.\n    '


class ProfileNotFound(Exception):
    __doc__ = '\n    A requested profile could not be found in the credentials file.\n    '