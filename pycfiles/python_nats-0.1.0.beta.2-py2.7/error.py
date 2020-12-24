# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nats/error.py
# Compiled at: 2014-08-31 00:36:00


class UriInvalidException(Exception):

    def __init__(self, uri):
        self.invalidUri = uri
        self.message = ('[{}] {} is invalid!').format(str(self.__class__).split('.')[1], uri)


class NotImplementException(Exception):

    def __init__(self):
        self.message = 'Not supported usage.'


class NatsException(Exception):

    def __init__(self, desc):
        self.message = ('[{}] {}').format(str(self.__class__).split('.')[1], desc)


class NatsParseDataException(NatsException):
    pass


class NatsServerException(NatsException):
    pass


class NatsClientException(NatsException):
    pass


class NatsConnectException(NatsException):
    pass


class NatsAuthException(NatsException):
    pass