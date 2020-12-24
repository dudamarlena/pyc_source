# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\errors.py
# Compiled at: 2017-08-03 07:38:56
# Size of source mod 2**32: 2047 bytes


class MoeError(Exception):
    __doc__ = '\n    Just making it more clear where the error comes from\n    '


class NoSSL(MoeError):
    __doc__ = "\n    Raised when we can't import SSL. Necessary for TLS and SSL Socket Wraps.\n    "

    def __repr__(self):
        return 'No SSL Library available. Please install OpenSSL or some alternative.'


class UserLoginFailed(MoeError):
    __doc__ = "\n    Raised when user details were not authenticated by the endpoint for the API.\n    If available, a message that was provided from the API is given.\n    Otherwise, it's just a login failed message.\n    "

    def __init__(self, msg):
        self.message = msg

    def __repr__(self):
        return 'We attempted to login using those details but got an error.\nError: {}'.format(self.message)


class GeneralLoginError(MoeError):
    __doc__ = '\n    Raised when an API refuses to allow us to login for some reason other than user credentials. Mostly for VNDB.\n    '

    def __init__(self, msg):
        self.message = msg

    def __repr__(self):
        return 'We attempted to login but the server responded with: {}'.format(self.message)


class ServerError(MoeError):
    __doc__ = '\n    Raised when we encounter an error retrieving information from the server.\n    '

    def __init__(self, message=None, code=500):
        self.msg = message
        self.code = code

    def __repr__(self):
        if self.msg:
            return 'Server Error encounted.\nCode: {}\nMessage: {}'.format(self.code, self.msg)
        else:
            return 'Encountered a server error attempting to access information.'


class NotSaving(MoeError):
    __doc__ = "\n    Raised when someone asks KitsuAuth to pull a token but they haven't asked KitsuAuth to save their tokens.\n    "

    def __repr__(self):
        return 'KitsuAuth is not currently saving your tokens. It cannot retrieve them.'


class UserNotFound(MoeError):
    __doc__ = "\n    Raised when the user isn't found in the token cache.\n    "

    def __repr__(self):
        return 'KitsuAuth could not find that user in the token cache.'