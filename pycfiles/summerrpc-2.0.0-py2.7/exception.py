# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/exception.py
# Compiled at: 2018-08-01 16:34:57


class BaseError(StandardError):
    pass


class RequestValidateError(BaseError):
    pass


class SerializerError(BaseError):

    def __init__(self, exc, *a, **kw):
        super(SerializerError, self).__init__(*a, **kw)
        self._exc = exc

    @property
    def exc(self):
        return self._exc


class SerializationError(SerializerError):
    pass


class DeserializationError(SerializerError):
    pass


class SocketAlreadyClosedError(BaseError):
    pass


class RemoteError(BaseError):
    pass


class NoRemoteServerError(RemoteError):
    pass


class ConcurrencyError(RemoteError):
    pass


class MaxConcurrencyReachedError(RemoteError):
    pass


class InvalidResponseError(RemoteError):
    pass


class FilteredError(BaseError):
    pass


class ConnectionError(BaseError):
    pass


class ConnectionAlreadyClosedError(ConnectionError):
    pass


class ConnectionWriteTimeout(ConnectionError):
    pass


class ConnectionReadTimeout(ConnectionError):
    pass


class MaxPendingWritesReachedError(ConnectionError):
    pass


class MaxPendingReadsReachedError(ConnectionError):
    pass