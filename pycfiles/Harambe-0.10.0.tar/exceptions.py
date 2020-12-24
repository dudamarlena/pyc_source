# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/harambe/harambe/exceptions.py
# Compiled at: 2017-02-26 06:58:35
"""
Harambe

Error

"""

class Harambe(Exception):
    """
    This exception is not reserved, but it used for all Harambe exception.
    It helps catch Core problems.
    """
    pass


class AppError(Harambe):
    """
    Use this exception in your application level.
    """
    pass


class ModelError(AppError):
    """
    Use this exception in your model level.
    """
    pass


class ExtensionError(Harambe):
    """
    This Exception wraps the exception that was raised.
    Having multiple extension, we need a way to catch them all :)
    """

    def __init__(self, exc):
        """
        :param exc: Exception
        """
        self.exception = exc
        message = '%s : %s' % (exc.__class__.__name__, exc.message)
        super(self.__class__, self).__init__(message)