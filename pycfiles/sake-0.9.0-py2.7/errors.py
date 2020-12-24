# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\errors.py
# Compiled at: 2011-03-09 01:25:51
"""
Standard sake exceptions.
"""

class CoreError(RuntimeError):
    """ The base sake exception. """
    pass


class LoginError(CoreError):
    """ Raised when a failure happens in the login process. """
    pass


class NetworkError(CoreError):
    """ The base network-related exception. """
    pass


class RpcError(NetworkError):
    """ Raised when a failure in networking RPC occurs. """
    pass


class RpcTimeoutError(NetworkError):
    """ Raised when a networking RPC operation times out. """
    pass


class RpcRemoteError(NetworkError):
    """ Raised when a networking RPC operation fails on the remote endpoint. """
    pass


class ServiceNotFoundError(CoreError):
    """ Raised when a access to a non-existent service is attempted. """
    pass


class TimeoutError(CoreError):
    """ Raised when a general operation times out. """
    pass


class AccessError(CoreError):
    """ Raised when a caller does not have access to perform the call they are making. """
    pass


import __builtin__
__builtin__.RpcError = RpcError
__builtin__.TimeoutError = TimeoutError