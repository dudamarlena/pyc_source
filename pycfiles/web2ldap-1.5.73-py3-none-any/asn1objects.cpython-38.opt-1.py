# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/asn1objects.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 453 bytes
"""
web2ldap plugin classes for ASN.1 objects
"""
from web2ldap.app.schema.syntaxes import ASN1Object, syntax_registry
syntax_registry.reg_at(ASN1Object.oid, [
 '1.3.6.1.4.1.8301.3.6.1.1',
 '1.3.6.1.4.1.8301.3.6.1.2',
 '0.2.262.1.10.7.124'])
syntax_registry.reg_syntaxes(__name__)