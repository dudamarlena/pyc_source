# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\errors.py
# Compiled at: 2017-08-03 07:38:56
# Size of source mod 2**32: 2047 bytes


class MoeError(Exception):
    """MoeError"""
    pass


class NoSSL(MoeError):
    """NoSSL"""

    def __repr__(self):
        return 'No SSL Library available. Please install OpenSSL or some alternative.'


class UserLoginFailed(MoeError):
    """UserLoginFailed"""

    def __init__(self, msg):
        self.message = msg

    def __repr__(self):
        return 'We attempted to login using those details but got an error.\nError: {}'.format(self.message)


class GeneralLoginError(MoeError):
    """GeneralLoginError"""

    def __init__(self, msg):
        self.message = msg

    def __repr__(self):
        return 'We attempted to login but the server responded with: {}'.format(self.message)


class ServerError(MoeError):
    """ServerError"""

    def __init__(self, message=None, code=500):
        self.msg = message
        self.code = code

    def __repr__(self):
        if self.msg:
            return 'Server Error encounted.\nCode: {}\nMessage: {}'.format(self.code, self.msg)
        else:
            return 'Encountered a server error attempting to access information.'


class NotSaving(MoeError):
    """NotSaving"""

    def __repr__(self):
        return 'KitsuAuth is not currently saving your tokens. It cannot retrieve them.'


class UserNotFound(MoeError):
    """UserNotFound"""

    def __repr__(self):
        return 'KitsuAuth could not find that user in the token cache.'