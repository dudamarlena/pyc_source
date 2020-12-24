# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/mocha/mocha/exceptions.py
# Compiled at: 2017-05-13 11:43:14
"""
exceptions.py

Raise Mocha specific exceptions
"""

class MochaError(Exception):
    """
    This exception is not reserved, but it used for all Mocha exception.
    It helps catch Core problems.
    """
    pass


class AppError(MochaError):
    """
    Use this exception in your application level.
    """
    pass


class ModelError(MochaError):
    """
    Use this exception in your model level.
    """
    pass