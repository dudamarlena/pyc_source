# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/AIS/exceptions.py
# Compiled at: 2018-10-22 10:39:31
# Size of source mod 2**32: 1005 bytes
"""
AIS.py - A Python interface for the Swisscom All-in Signing Service.

:copyright: (c) 2016 by Camptocamp
:license: AGPLv3, see README and LICENSE for more details

"""

class AISError(Exception):
    __doc__ = 'Generic AIS Error.'


class AuthenticationFailed(AISError):
    __doc__ = 'Authentication with AIS failed.\n\n    This means that AIS returned\n    http://ais.swisscom.ch/1.0/resultminor/AuthenticationFailed\n    '


class UnknownAISError(AISError):
    __doc__ = 'Unknown AIS Error.'


class MissingPreparedSignature(AISError):
    __doc__ = 'The PDF file needs to be prepared with an empty signature.'


minor_to_exception = {'http://ais.swisscom.ch/1.0/resultminor/AuthenticationFailed': AuthenticationFailed}

def error_for(response):
    """Return the correct error for a response."""
    result = response.json()['SignResponse']['Result']
    Exc = minor_to_exception.get(result['ResultMinor'], UnknownAISError)
    return Exc(result)