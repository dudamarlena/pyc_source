# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/exceptions.py
# Compiled at: 2017-02-24 16:57:38
"""Fullauth's exceptions definition."""

class DeleteException(Exception):
    """Exception risen when the user can't be deleted."""
    pass


class ValidateError(ValueError):
    """Base of every validate error in pyramid_fullauth."""
    pass


class EmptyError(ValidateError):
    """Thrown whenever user is trying to set empty value."""
    pass


class ShortPasswordError(ValidateError):
    """Thrown when password doesn't meet the length requirement."""
    pass


class PasswordConfirmMismatchError(ValidateError):
    """Thrown when there's a mismatch with cpassword_confirm."""
    pass


class EmailValidationError(ValidateError):
    """Exception thrown, when there's incorrect email provided."""
    pass