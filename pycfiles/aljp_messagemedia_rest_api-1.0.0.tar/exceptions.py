# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/opensearchsdk/apiclient/exceptions.py
# Compiled at: 2015-11-27 08:29:32


class HttpException(Exception):
    """base exception for http request"""

    def __init__(self, message=None, details=None, status_code=None):
        self.message = self.__class__.__name__ if message is None else message
        super(Exception, self).__init__(self.message)
        self.details = details
        self.status_code = status_code
        return

    def __unicode__(self):
        msg = self.__class__.__name__ + ': ' + self.message
        if self.details:
            msg += ', ' + self.details
        return msg

    def __str__(self):
        return self.__unicode__()


class NotFoundException(HttpException):
    """404"""

    def __init__(self, message=None, details=None, status_code=None):
        super(NotFoundException, self).__init__(message, details, status_code)


class InvalidResponse(HttpException):
    """response from server is not valid for this request."""

    def __init__(self, response):
        super(InvalidResponse, self).__init__()
        self.response = response