# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/exceptions.py
# Compiled at: 2015-05-09 16:52:10
# Size of source mod 2**32: 513 bytes
"""Module for warmama exceptions"""

class WarmamaException(Exception):
    __doc__ = 'Base class for Warmama exceptions\n\n    Attributes:\n        status (int): Response status a view should return if this exception\n            is encountered.\n    '
    status = 500


class BadRequest(WarmamaException):
    __doc__ = 'Exception raised for invalid form data or otherwise 400 responses'
    status = 400


class Forbidden(WarmamaException):
    __doc__ = 'Exception raised on authentication or permission failure'
    status = 403