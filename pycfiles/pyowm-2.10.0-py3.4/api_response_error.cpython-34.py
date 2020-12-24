# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/exceptions/api_response_error.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2224 bytes
"""
Module containing APIResponseError class
"""
import os
from pyowm.exceptions import OWMError

class APIResponseError(OWMError):
    __doc__ = '\n    Error class that represents HTTP error status codes in OWM Weather API\n    responses.\n\n    :param cause: the message of the error\n    :type cause: str\n    :param status_code: the HTTP error status code\n    :type status_code: int\n    :returns: a *APIResponseError* instance\n    '

    def __init__(self, cause, status_code):
        self._message = cause
        self.status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['HTTP status code %s was returned by the OWM API' % str(self.status_code), os.linesep, 'Reason: ',
         self._message])


class NotFoundError(APIResponseError):
    __doc__ = '\n    Error class that represents the situation when an entity is not found into\n    a collection of entities.\n\n    :param cause: the message of the error\n    :type cause: str\n    :param status_code: the HTTP error status code\n    :type status_code: int\n    :returns: a *NotFoundError* instance\n    '

    def __init__(self, cause, status_code=404):
        self._message = cause
        self.status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['The searched item was not found.', os.linesep,
         'Reason: ', self._message])


class UnauthorizedError(APIResponseError):
    __doc__ = '\n    Error class that represents the situation when an entity cannot be retrieved\n    due to user subscription unsufficient capabilities.\n\n    :param cause: the message of the error\n    :type cause: str\n    :param status_code: the HTTP error status code\n    :type status_code: int\n    :returns: a *UnauthorizedError* instance\n    '

    def __init__(self, cause, status_code=403):
        self._message = cause
        self._status_code = status_code

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Your API subscription level does not allow to perform this operation',
         os.linesep,
         'Reason: ', self._message])