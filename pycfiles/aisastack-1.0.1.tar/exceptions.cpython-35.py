# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/AIS/exceptions.py
# Compiled at: 2018-10-22 10:39:31
# Size of source mod 2**32: 1005 bytes
__doc__ = '\nAIS.py - A Python interface for the Swisscom All-in Signing Service.\n\n:copyright: (c) 2016 by Camptocamp\n:license: AGPLv3, see README and LICENSE for more details\n\n'

class AISError(Exception):
    """AISError"""
    pass


class AuthenticationFailed(AISError):
    """AuthenticationFailed"""
    pass


class UnknownAISError(AISError):
    """UnknownAISError"""
    pass


class MissingPreparedSignature(AISError):
    """MissingPreparedSignature"""
    pass


minor_to_exception = {'http://ais.swisscom.ch/1.0/resultminor/AuthenticationFailed': AuthenticationFailed}

def error_for(response):
    """Return the correct error for a response."""
    result = response.json()['SignResponse']['Result']
    Exc = minor_to_exception.get(result['ResultMinor'], UnknownAISError)
    return Exc(result)