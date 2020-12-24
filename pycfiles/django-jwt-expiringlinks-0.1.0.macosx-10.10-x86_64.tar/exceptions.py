# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/django-jwt/lib/python2.7/site-packages/django_jwt/exceptions.py
# Compiled at: 2015-12-28 11:05:50
"""django_jwt expections.

Local exceptions related to tokens inherit from the PyJWT base
InvalidTokenError.

"""
from jwt.exceptions import InvalidTokenError

class MaxUseError(InvalidTokenError):
    """Error raised when a token has exceeded its max_use cap."""
    pass


class TargetUrlError(InvalidTokenError):
    """Error raised when a token target_url does not match the request path."""
    pass