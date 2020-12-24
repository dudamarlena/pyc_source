# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/exceptions.py
# Compiled at: 2017-02-24 16:57:38
__doc__ = "Fullauth's exceptions definition."

class DeleteException(Exception):
    """Exception risen when the user can't be deleted."""


class ValidateError(ValueError):
    """Base of every validate error in pyramid_fullauth."""


class EmptyError(ValidateError):
    """Thrown whenever user is trying to set empty value."""


class ShortPasswordError(ValidateError):
    """Thrown when password doesn't meet the length requirement."""


class PasswordConfirmMismatchError(ValidateError):
    """Thrown when there's a mismatch with cpassword_confirm."""


class EmailValidationError(ValidateError):
    """Exception thrown, when there's incorrect email provided."""