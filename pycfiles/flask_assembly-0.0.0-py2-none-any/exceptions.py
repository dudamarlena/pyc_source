# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/exceptions.py
# Compiled at: 2019-08-23 12:47:12
"""
exceptions.py

Raise Flasik specific exceptions
"""

class FlasikError(Exception):
    """
    This exception is not reserved, but it used for all Flasik exception.
    It helps catch Core problems.
    """
    pass


class AppError(FlasikError):
    """
    Use this exception in your application level.
    """
    pass


class ModelError(FlasikError):
    """
    Use this exception in your model level.
    """
    pass