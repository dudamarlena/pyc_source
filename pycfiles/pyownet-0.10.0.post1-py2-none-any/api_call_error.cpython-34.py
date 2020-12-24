# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/exceptions/api_call_error.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2121 bytes
__doc__ = '\nModule containing APICallError class\n'
import os
from pyowm.exceptions import OWMError

class APICallError(OWMError):
    """APICallError"""

    def __init__(self, message, triggering_error=None):
        self._message = message
        self._triggering_error = triggering_error

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Exception in calling OWM Weather API.', os.linesep,
         'Reason: ', self._message, os.linesep,
         'Caused by: ', str(self._triggering_error)])


class BadGatewayError(APICallError):
    """BadGatewayError"""
    pass


class APICallTimeoutError(APICallError):
    """APICallTimeoutError"""
    pass


class APIInvalidSSLCertificateError(APICallError):
    """APIInvalidSSLCertificateError"""
    pass