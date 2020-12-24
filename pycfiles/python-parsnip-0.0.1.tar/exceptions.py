# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pastylegs/Dropbox/GitHub/python-parsnip/parsnip/exceptions.py
# Compiled at: 2012-05-02 05:37:21


class ParsnipException(Exception):

    def __init__(self, msg, webtexter=None):
        self.args = (msg, webtexter)
        self.msg = msg
        self.webtexter = webtexter

    def __str__(self):
        return repr('[%s] %s - %s' % (self.webtexter.NETWORK_NAME, self.webtexter.phone_number, self.msg))


class LoginError(ParsnipException):
    pass


class MessageSendingError(ParsnipException):
    pass


class ConnectionError(ParsnipException):
    pass


class ResourceError(ParsnipException):
    pass