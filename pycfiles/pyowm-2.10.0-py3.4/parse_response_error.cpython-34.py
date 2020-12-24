# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/exceptions/parse_response_error.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 660 bytes
"""
Module containing ParseResponseError class
"""
import os
from pyowm.exceptions import OWMError

class ParseResponseError(OWMError):
    __doc__ = '\n    Error class that represents failures when parsing payload data in HTTP\n    responses sent by the OWM Weather API.\n\n    :param cause: the message of the error\n    :type cause: str\n    :returns: a *ParseResponseError* instance\n    '

    def __init__(self, cause):
        self._message = cause

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Exception in parsing OWM Weather API response',
         os.linesep, 'Reason: ', self._message])