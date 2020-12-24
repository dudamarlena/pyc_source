# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/exception.py
# Compiled at: 2019-08-29 07:14:47


class CBaseException(Exception):
    pass


class ConnectionException(Exception):
    pass


class DataException(CBaseException):
    pass


class SyntaxException(CBaseException):
    pass


class GenericException(CBaseException):
    pass


class UserQuitException(CBaseException):
    pass


class CodeDirIsNoneException(CBaseException):
    pass