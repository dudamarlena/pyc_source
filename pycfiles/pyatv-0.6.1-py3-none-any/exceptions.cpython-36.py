# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/exceptions.py
# Compiled at: 2019-10-07 03:42:42
# Size of source mod 2**32: 1247 bytes
"""Local exceptions used by library."""

class NoUsableServiceError(Exception):
    __doc__ = 'Thrown when connecting to a device with no usable service.'


class AuthenticationError(Exception):
    __doc__ = 'Thrown when login fails.'


class NotSupportedError(NotImplementedError):
    __doc__ = 'Thrown when trying to perform an action that is not supported.'


class InvalidDmapDataError(Exception):
    __doc__ = 'Thrown when invalid DMAP data is parsed.'


class UnknownServerResponseError(Exception):
    __doc__ = 'Thrown when somethins unknown is send back from the Apple TV.'


class UnknownMediaKind(Exception):
    __doc__ = 'Thrown when an unknown media kind is found.'


class UnknownPlayState(Exception):
    __doc__ = 'Thrown when an unknown play state is found.'


class NoAsyncListenerError(Exception):
    __doc__ = 'Thrown when starting AsyncUpdater with no listener.'


class AsyncUpdaterRunningError(Exception):
    __doc__ = 'Thrown when performing an invalid action in AsyncUpdater..'


class NoCredentialsError(Exception):
    __doc__ = 'Thrown if performing an action before initialize is called.'


class DeviceAuthenticationError(Exception):
    __doc__ = 'Thrown when device authentication fails.'


class DeviceIdMissingError(Exception):
    __doc__ = 'Thrown when device id is missing.'