# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/src/utils/custom_exceptions.py
# Compiled at: 2018-08-06 09:29:00


class ValidationError(Exception):

    def __init__(self, message, errors):
        super(ValidationError, self).__init__(message)
        self.errors = errors


class ZASCursorError(Exception):
    """
    test
    """
    pass


class ZASConnectionError(Exception):
    """
    test
    """
    pass


class DBHandlerError(Exception):
    """
    test
    """
    pass


class ProcessError(Exception):
    """
    test
    """
    pass


class StackTraceBack(Exception):
    """
    test
    """
    pass


class ErrorInsertion(Exception):
    """
    test
    """
    pass


class ThreadsCrash(Exception):
    """
    test
    """
    pass