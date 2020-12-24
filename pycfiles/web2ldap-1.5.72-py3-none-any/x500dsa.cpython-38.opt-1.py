# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/x500dsa.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 379 bytes
"""
web2ldap plugin classes for X.500 DSAs
"""
from web2ldap.app.schema.syntaxes import OctetString, syntax_registry

class AccessControlInformation(OctetString):
    oid = '1.3.6.1.4.1.1466.115.121.1.1'
    oid: str
    desc = 'X.500: Access Control Information (ACI)'
    desc: str


syntax_registry.reg_syntaxes(__name__)