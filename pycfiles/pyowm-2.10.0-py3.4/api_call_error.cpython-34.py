# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/exceptions/api_call_error.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2121 bytes
"""
Module containing APICallError class
"""
import os
from pyowm.exceptions import OWMError

class APICallError(OWMError):
    __doc__ = '\n    Error class that represents network/infrastructural failures when invoking OWM Weather API, in\n    example due to network errors.\n\n    :param message: the message of the error\n    :type message: str\n    :param triggering_error: optional *Exception* object that triggered this\n        error (defaults to ``None``)\n    :type triggering_error: an *Exception* subtype\n    '

    def __init__(self, message, triggering_error=None):
        self._message = message
        self._triggering_error = triggering_error

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Exception in calling OWM Weather API.', os.linesep,
         'Reason: ', self._message, os.linesep,
         'Caused by: ', str(self._triggering_error)])


class BadGatewayError(APICallError):
    __doc__ = '\n    Error class that represents 502 errors - i.e when upstream backend\n    cannot communicate with API gateways.\n\n    :param message: the message of the error\n    :type message: str\n    :param triggering_error: optional *Exception* object that triggered this\n        error (defaults to ``None``)\n    :type triggering_error: an *Exception* subtype\n    '


class APICallTimeoutError(APICallError):
    __doc__ = '\n    Error class that represents response timeout conditions\n\n    :param message: the message of the error\n    :type message: str\n    :param triggering_error: optional *Exception* object that triggered this\n        error (defaults to ``None``)\n    :type triggering_error: an *Exception* subtype\n    '


class APIInvalidSSLCertificateError(APICallError):
    __doc__ = '\n    Error class that represents failure in verifying the SSL certificate provided\n    by the OWM API\n\n    :param message: the message of the error\n    :type message: str\n    :param triggering_error: optional *Exception* object that triggered this\n        error (defaults to ``None``)\n    :type triggering_error: an *Exception* subtype\n    '