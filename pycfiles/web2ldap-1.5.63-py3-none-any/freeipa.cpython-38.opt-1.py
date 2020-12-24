# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/freeipa.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 737 bytes
"""
web2ldap plugin classes for FreeIPA
"""
from web2ldap.app.schema.syntaxes import UUID, DNSDomain, syntax_registry
from web2ldap.app.plugins.samba import SambaSID
from web2ldap.app.plugins.opensshlpk import SshPublicKey
syntax_registry.reg_at(UUID.oid, [
 '2.16.840.1.113730.3.8.3.1'])
syntax_registry.reg_at(DNSDomain.oid, [
 '2.16.840.1.113730.3.8.3.4'])
syntax_registry.reg_at(SshPublicKey.oid, [
 '2.16.840.1.113730.3.8.11.31'])
syntax_registry.reg_at(SambaSID.oid, [
 '2.16.840.1.113730.3.8.11.2'])
syntax_registry.reg_syntaxes(__name__)