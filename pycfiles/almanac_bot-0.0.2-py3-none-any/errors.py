# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/apibits/errors.py
# Compiled at: 2015-08-31 22:18:13


class ApibitsError(Exception):

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


class ApiError(ApibitsError):

    def __init__(self, message=None, api_method=None):
        self.message = message
        self.api_method = api_method

    def code(self):
        if self.api_method:
            return self.api_method.status_code
        else:
            return

    def body(self):
        if self.api_method:
            return self.api_method.text
        else:
            return


class AuthenticationError(ApibitsError):
    pass


class ConnectionError(ApiError):
    pass