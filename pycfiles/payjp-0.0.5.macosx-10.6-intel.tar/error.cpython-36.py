# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages/payjp/error.py
# Compiled at: 2018-06-22 02:45:13
# Size of source mod 2**32: 1361 bytes


class PayjpException(Exception):

    def __init__(self, message=None, http_body=None, http_status=None, json_body=None):
        super(PayjpException, self).__init__(message)
        if http_body:
            if hasattr(http_body, 'decode'):
                try:
                    http_body = http_body.decode('utf-8')
                except:
                    http_body = '<Could not decode body as utf-8. Please report to support@pay.jp>'

        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body


class APIError(PayjpException):
    pass


class APIConnectionError(PayjpException):
    pass


class CardError(PayjpException):

    def __init__(self, message, param, code, http_body=None, http_status=None, json_body=None):
        super(CardError, self).__init__(message, http_body, http_status, json_body)
        self.param = param
        self.code = code


class AuthenticationError(PayjpException):
    pass


class InvalidRequestError(PayjpException):

    def __init__(self, message, param, http_body=None, http_status=None, json_body=None):
        super(InvalidRequestError, self).__init__(message, http_body, http_status, json_body)
        self.param = param