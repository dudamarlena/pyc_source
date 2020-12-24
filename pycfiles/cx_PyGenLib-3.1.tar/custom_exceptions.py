# uncompyle6 version 3.6.7
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/lameiro/projects/cx_oracle_on_ctypes/cx_Oracle/custom_exceptions.py
# Compiled at: 2015-05-19 16:59:20
from utils import python3_or_better
if python3_or_better():
    CXORA_BASE_EXCEPTION = Exception
    CXORA_TYPE_ERROR = 'expecting string or bytes object'
else:
    CXORA_BASE_EXCEPTION = StandardError
    CXORA_TYPE_ERROR = 'expecting string, unicode or buffer object'

class Warning(CXORA_BASE_EXCEPTION):
    pass


class Error(CXORA_BASE_EXCEPTION):
    pass


class InterfaceError(Error):
    pass


class DatabaseError(Error):
    pass


class DataError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class IntegrityError(DatabaseError):
    pass


class InternalError(DatabaseError):
    pass


class ProgrammingError(DatabaseError):
    pass


class NotSupportedError(DatabaseError):
    pass