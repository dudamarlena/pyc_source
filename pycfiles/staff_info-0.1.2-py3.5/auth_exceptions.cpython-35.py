# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auth/auth_exceptions.py
# Compiled at: 2018-03-02 08:34:56
# Size of source mod 2**32: 553 bytes


class AuthException(Exception):

    def __init__(self, username, user=None):
        super().__init__(username, user)
        self.username = username
        self.user = user


class UserAlreadyExistException(AuthException):
    pass


class UserNotExistException(AuthException):
    pass


class NotLoggedInError(AuthException):
    pass


class PasswordMissmatchException(AuthException):
    pass


class PasswordTooShortException(AuthException):
    pass


class PermissionError(Exception):
    pass


class NotPermittedError(Exception):
    pass