# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\sasl\plain.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ...protocol.sasl.sasl import send_sasl_negotiation
from .sasl import sasl_prep
from ...utils.conv import to_raw, to_unicode

def sasl_plain(connection, controls):
    authzid = connection.sasl_credentials[0]
    authcid = connection.sasl_credentials[1]
    passwd = connection.sasl_credentials[2]
    payload = ''
    if authzid:
        payload += to_raw(sasl_prep(to_unicode(authzid)))
    payload += '\x00'
    if authcid:
        payload += to_raw(sasl_prep(to_unicode(authcid)))
    payload += '\x00'
    if passwd:
        payload += to_raw(sasl_prep(to_unicode(passwd)))
    result = send_sasl_negotiation(connection, controls, payload)
    return result