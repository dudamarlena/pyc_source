# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/errors.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 1180 bytes
import sys

class PasswordSetError(Exception):
    __doc__ = "Raised when the password can't be set.\n    "


class PasswordDeleteError(Exception):
    __doc__ = "Raised when the password can't be deleted.\n    "


class InitError(Exception):
    __doc__ = 'Raised when the keyring could not be initialised\n    '


class ExceptionRaisedContext(object):
    __doc__ = '\n    An exception-trapping context that indicates whether an exception was\n    raised.\n    '

    def __init__(self, ExpectedException=Exception):
        self.ExpectedException = ExpectedException
        self.exc_info = None

    def __enter__(self):
        self.exc_info = object.__new__(ExceptionInfo)
        return self.exc_info

    def __exit__(self, *exc_info):
        self.exc_info.__init__(*exc_info)
        return self.exc_info.type and issubclass(self.exc_info.type, self.ExpectedException)


class ExceptionInfo(object):

    def __init__(self, *info):
        if not info:
            info = sys.exc_info()
        self.type, self.value, self.traceback = info

    def __bool__(self):
        """
        Return True if an exception occurred
        """
        return bool(self.type)

    __nonzero__ = __bool__