# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/exception.py
# Compiled at: 2017-06-06 22:44:39
# Size of source mod 2**32: 315 bytes


class ProtocolError(Exception):
    pass


class ProxyAuthError(Exception):
    pass


class ConnectToRemoteError(Exception):
    pass


class ConnectionError(Exception):
    pass


class RequestNotSucceed(Exception):
    pass


class InvalidRequest(Exception):
    pass


class WrongProtocol(InvalidRequest):
    pass