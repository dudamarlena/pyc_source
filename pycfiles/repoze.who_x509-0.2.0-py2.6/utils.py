# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/repoze/who/plugins/x509/utils.py
# Compiled at: 2012-03-22 17:15:19
"""
This module contains utilities related to repoze who x509 plugin.
"""
from dateutil.parser import parse as date_parse
from dateutil.tz import tzutc
from datetime import datetime
import re
VERIFY_KEY = 'SSL_CLIENT_VERIFY'
VALIDITY_START_KEY = 'SSL_CLIENT_V_START'
VALIDITY_END_KEY = 'SSL_CLIENT_V_END'
_DN_SSL_REGEX = re.compile('(/\\s*\\w+=)')
_TZ_UTC = tzutc()
__all__ = [
 'parse_dn', 'verify_certificate', 'VERIFY_KEY',
 'VALIDITY_START_KEY', 'VALIDITY_END_KEY']

def parse_dn(dn):
    """
    Parses a OpenSSL-like distinguished name into a dictionary. The keys are
    the attribute types and the values are lists (multiple values for that
    type).

    "Multi-values" are not supported (e.g., O=company+CN=name).
    
    :param dn: The distinguished name.
    
    :raise ValueError: When you input an invalid or empty distinguished name.
    """
    parsed = {}
    split_string = _DN_SSL_REGEX.split(dn)
    if split_string[0] == '':
        split_string.pop(0)
    for i in range(0, len(split_string), 2):
        try:
            type_, value = split_string[i][1:-1], split_string[(i + 1)]
        except IndexError:
            raise ValueError('Invalid DN')

        if len(value) == 0:
            raise ValueError('Invalid DN: Invalid value')
        if type_ not in parsed:
            parsed[type_] = []
        parsed[type_].append(value)

    if len(parsed) == 0:
        raise ValueError('Invalid DN: Empty DN')
    return parsed


def verify_certificate(environ, verify_key, validity_start_key, validity_end_key):
    """
    Checks if the client certificate is valid. Start and end data is optional,
    as not all SSL mods give that information.

    :param environ: The WSGI environment.
    :param verify_key: The key for the value in the environment where it was
        stored if the certificate is valid or not.
    :param validity_start_key: The key for the value in the environment with
        the encoded datetime that indicates the start of the validity range.
    :param validity_end_key: The key for the value in the environment with the
        encoded datetime that indicates the end of the validity range.
    """
    verified = environ.get(verify_key)
    validity_start = environ.get(validity_start_key)
    validity_end = environ.get(validity_end_key)
    if verified != 'SUCCESS':
        return False
    else:
        if validity_start is None or validity_end is None:
            return True
        validity_start = date_parse(validity_start)
        validity_end = date_parse(validity_end)
        if validity_start.tzinfo != _TZ_UTC or validity_end.tzinfo != _TZ_UTC:
            return False
        now = datetime.utcnow().replace(tzinfo=_TZ_UTC)
        return validity_start <= now <= validity_end