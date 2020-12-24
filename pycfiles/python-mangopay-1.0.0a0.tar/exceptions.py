# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thoas/Sites/Python/ulule/python-mangopay/mangopay/exceptions.py
# Compiled at: 2015-06-08 06:37:42


class APIError(Exception):

    def __init__(self, *args, **kwargs):
        self.code = kwargs.pop('code', None)
        self.url = kwargs.pop('url', None)
        self.content = kwargs.pop('content', None)
        super(APIError, self).__init__(*args, **kwargs)
        return


class DecodeError(APIError):

    def __init__(self, *args, **kwargs):
        self.body = kwargs.pop('body', None)
        self.headers = kwargs.pop('headers', None)
        self.url = kwargs.pop('url', None)
        self.content = kwargs.pop('content', None)
        super(DecodeError, self).__init__(*args, **kwargs)
        return


class AuthenticationError(APIError):
    pass


class CurrencyMismatch(Exception):
    pass