# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/ibmds.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 712 bytes
"""
web2ldap plugin classes for IBM Tivoliy Directory Server
"""
from web2ldap.app.schema.syntaxes import syntax_registry, OID, DistinguishedName, OctetString
syntax_registry.reg_at(OID.oid, [
 '1.3.18.0.2.4.2482',
 '1.3.18.0.2.4.2481',
 'ibm-supportedacimechanisms'])
syntax_registry.reg_at(DistinguishedName.oid, [
 'ibm-adminid'])
syntax_registry.reg_at(OctetString.oid, [
 '1.3.18.0.2.4.3127',
 '1.3.18.0.2.4.3116'])
syntax_registry.reg_syntaxes(__name__)