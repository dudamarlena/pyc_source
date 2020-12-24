# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/h350.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 641 bytes
"""
web2ldap plugin classes for H.350 Directory Services (see RFC 3944)
"""
from web2ldap.app.schema.syntaxes import Uri, LDAPUrl, syntax_registry

class CommURI(LDAPUrl):
    oid = 'CommURI-oid'
    oid: str
    desc = 'Labeled URI format to point to the distinguished name of the commUniqueId'
    desc: str


syntax_registry.reg_at(CommURI.oid, [
 '0.0.8.350.1.1.1.1.1',
 '0.0.8.350.1.1.2.1.2'])
syntax_registry.reg_at(Uri.oid, [
 '0.0.8.350.1.1.6.1.1'])
syntax_registry.reg_syntaxes(__name__)