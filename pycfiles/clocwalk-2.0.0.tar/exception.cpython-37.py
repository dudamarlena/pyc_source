# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/exception.py
# Compiled at: 2020-02-24 23:38:00
# Size of source mod 2**32: 503 bytes


class CodeBaseException(Exception):
    pass


class ConnectionException(Exception):
    pass


class DataException(CodeBaseException):
    pass


class SyntaxException(CodeBaseException):
    pass


class GenericException(CodeBaseException):
    pass


class UserQuitException(CodeBaseException):
    pass


class CodeDirIsNoneException(CodeBaseException):
    pass


class HTTPStatusCodeError(CodeBaseException):
    pass


class NoUpgradeRequiredError(CodeBaseException):
    pass