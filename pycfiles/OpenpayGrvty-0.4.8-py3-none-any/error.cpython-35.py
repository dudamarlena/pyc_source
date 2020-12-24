# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/daniel/Documents/VentasMedicas/openpay_python/build/lib/openpay/error.py
# Compiled at: 2018-02-18 18:44:07
# Size of source mod 2**32: 1347 bytes


class OpenpayError(Exception):

    def __init__(self, message=None, http_body=None, http_status=None, json_body=None):
        super(OpenpayError, self).__init__(message)
        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf=8')
            except:
                http_body = '<Could not decode body as utf-8. Please report to support@openpay.mx>'

        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body


class APIError(OpenpayError):
    pass


class APIConnectionError(OpenpayError):
    pass


class CardError(OpenpayError):

    def __init__(self, message, param, code, http_body=None, http_status=None, json_body=None):
        super(CardError, self).__init__(message, http_body, http_status, json_body)
        self.param = param
        self.code = code


class InvalidRequestError(OpenpayError):

    def __init__(self, message, param, http_body=None, http_status=None, json_body=None):
        super(InvalidRequestError, self).__init__(message, http_body, http_status, json_body)
        self.param = param


class AuthenticationError(OpenpayError):
    pass