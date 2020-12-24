# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/vchupwdpolicy.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 713 bytes
"""
web2ldap plugin classes for attributes defined in draft-vchu-ldap-pwd-policy
"""
from web2ldap.app.schema.syntaxes import OnOffFlag, syntax_registry
syntax_registry.reg_at(OnOffFlag.oid, [
 '2.16.840.1.113730.3.1.102',
 '2.16.840.1.113730.3.1.103',
 '2.16.840.1.113730.3.1.98',
 '2.16.840.1.113730.3.1.105',
 '2.16.840.1.113730.3.1.220',
 '2.16.840.1.113730.3.1.108'])
syntax_registry.reg_syntaxes(__name__)