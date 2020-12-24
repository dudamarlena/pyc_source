# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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