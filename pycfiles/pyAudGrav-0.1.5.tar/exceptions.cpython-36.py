# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/exceptions.py
# Compiled at: 2019-10-07 03:42:42
# Size of source mod 2**32: 1247 bytes
__doc__ = 'Local exceptions used by library.'

class NoUsableServiceError(Exception):
    """NoUsableServiceError"""
    pass


class AuthenticationError(Exception):
    """AuthenticationError"""
    pass


class NotSupportedError(NotImplementedError):
    """NotSupportedError"""
    pass


class InvalidDmapDataError(Exception):
    """InvalidDmapDataError"""
    pass


class UnknownServerResponseError(Exception):
    """UnknownServerResponseError"""
    pass


class UnknownMediaKind(Exception):
    """UnknownMediaKind"""
    pass


class UnknownPlayState(Exception):
    """UnknownPlayState"""
    pass


class NoAsyncListenerError(Exception):
    """NoAsyncListenerError"""
    pass


class AsyncUpdaterRunningError(Exception):
    """AsyncUpdaterRunningError"""
    pass


class NoCredentialsError(Exception):
    """NoCredentialsError"""
    pass


class DeviceAuthenticationError(Exception):
    """DeviceAuthenticationError"""
    pass


class DeviceIdMissingError(Exception):
    """DeviceIdMissingError"""
    pass