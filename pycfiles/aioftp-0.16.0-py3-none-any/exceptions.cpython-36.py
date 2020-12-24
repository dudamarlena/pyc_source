# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/exceptions.py
# Compiled at: 2019-01-02 15:52:59
# Size of source mod 2**32: 655 bytes


class InvalidTokenError(Exception):

    def __init__(self, *args, **kwargs):
        (Exception.__init__)(self, *args, **kwargs)


class NotOpenError(Exception):

    def __init__(self, *args, **kwargs):
        (Exception.__init__)(self, *args, **kwargs)


class AuthorizationError(Exception):

    def __init__(self, *args, **kwargs):
        (Exception.__init__)(self, *args, **kwargs)


class HttpRequestError(Exception):

    def __init__(self, *args, **kwargs):
        (Exception.__init__)(self, *args, **kwargs)


class InsufficientPermissionsError(HttpRequestError):

    def __init__(self, *args, **kwargs):
        (HttpRequestError.__init__)(self, *args, **kwargs)