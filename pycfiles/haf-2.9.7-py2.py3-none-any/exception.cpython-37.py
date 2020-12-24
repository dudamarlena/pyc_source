# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: J:\workspace\python\haf\haf\common\exception.py
# Compiled at: 2020-03-21 04:56:32
# Size of source mod 2**32: 1003 bytes
import sys

class BaseException(Exception):

    def __init__(self):
        self.exception = sys.exec_info()


class FailFrameworkException(BaseException):

    def __init__(self):
        pass


class FailAssertException(AssertionError):

    def __init__(self):
        pass


class FailLoaderException(BaseException):

    def __init__(self):
        pass


class FailRunnerException(BaseException):

    def __init__(self):
        pass


class FailRecorderException(BaseException):

    def __init__(self):
        pass


class FailCaseException(BaseException):

    def __init__(self):
        pass


class FailResultException(BaseException):

    def __init__(self):
        pass


class SkipCaseException(BaseException):

    def __init__(self):
        pass


class FailBusException(BaseException):

    def __init__(self):
        pass


class FailLoadCaseFromPyException(BaseException):

    def __init__(self):
        pass