# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\sasl\external.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from ...protocol.sasl.sasl import send_sasl_negotiation

def sasl_external(connection, controls):
    result = send_sasl_negotiation(connection, controls, connection.sasl_credentials)
    return result