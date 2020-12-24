# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webdb/adapter/exceptions.py
# Compiled at: 2018-02-11 16:00:20
# Size of source mod 2**32: 284 bytes


class Error(BaseException):
    pass


class DatabaseError(Error):
    pass


class InterfaceError(Error):
    pass


class DataError(Error):
    pass


class OperationalError(Error):
    pass


class IntegretyError(Error):
    pass


class ProgrammingError(Error):
    pass


class NotSupportedError(Error):
    pass