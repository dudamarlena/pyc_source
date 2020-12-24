# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/exceptions/parse_response_error.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 660 bytes
__doc__ = '\nModule containing ParseResponseError class\n'
import os
from pyowm.exceptions import OWMError

class ParseResponseError(OWMError):
    """ParseResponseError"""

    def __init__(self, cause):
        self._message = cause

    def __str__(self):
        """Redefine __str__ hook for pretty-printing"""
        return ''.join(['Exception in parsing OWM Weather API response',
         os.linesep, 'Reason: ', self._message])