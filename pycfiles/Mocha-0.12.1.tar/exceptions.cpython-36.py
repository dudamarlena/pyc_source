# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/shaft/shaft/exceptions.py
# Compiled at: 2016-12-17 21:25:36
# Size of source mod 2**32: 805 bytes
"""
Shaft

Error

"""

class ShaftError(Exception):
    __doc__ = '\n    This exception is not reserved, but it used for all Shaft exception.\n    It helps catch Core problems.\n    '


class AppError(ShaftError):
    __doc__ = '\n    Use this exception in your application level.\n    '


class ModelError(AppError):
    __doc__ = '\n    Use this exception in your model level.\n    '


class ExtensionError(ShaftError):
    __doc__ = '\n    This Exception wraps the exception that was raised.\n    Having multiple extension, we need a way to catch them all :)\n    '

    def __init__(self, exc):
        self.exception = exc
        message = '%s : %s' % (exc.__class__.__name__, exc.message)
        super(self.__class__, self).__init__(message)