# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/exceptions/api_response_error.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2224 bytes
__doc__ = '\nModule containing APIResponseError class\n'
import os
from pyowm.exceptions import OWMError

class APIResponseError(OWMError):
    """APIResponseError"""

    def __init__(self, cause, status_code):
        self._message = cause
        self.status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['HTTP status code %s was returned by the OWM API' % str(self.status_code), os.linesep, 'Reason: ',
         self._message])


class NotFoundError(APIResponseError):
    """NotFoundError"""

    def __init__(self, cause, status_code=404):
        self._message = cause
        self.status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['The searched item was not found.', os.linesep,
         'Reason: ', self._message])


class UnauthorizedError(APIResponseError):
    """UnauthorizedError"""

    def __init__(self, cause, status_code=403):
        self._message = cause
        self._status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Your API subscription level does not allow to perform this operation',
         os.linesep,
         'Reason: ', self._message])