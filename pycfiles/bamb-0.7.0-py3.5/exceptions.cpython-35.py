# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/domain/exceptions.py
# Compiled at: 2017-09-08 11:08:24
# Size of source mod 2**32: 2136 bytes


class AppException(RuntimeError):

    def __init__(self, *args, **kwargs):
        self.err_code = 1000
        RuntimeError.__init__(self, *args, **kwargs)

    def __str__(self):
        return self.__class__.__name__ + '[' + str(self.err_code) + '] ' + RuntimeError.__str__(self)


class NotFoundException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1001


class IllegalArgumentException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1002


class DuplicatedException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1003


class IllegalOperationException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1004


class FailedToLoadException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1005


class CannotConnectException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1006


class StateErrorException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1007


class InternalErrorException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1008


class OperationFailedException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1009


class DatabaseErrorException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1010


class InvalidTypeException(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1011