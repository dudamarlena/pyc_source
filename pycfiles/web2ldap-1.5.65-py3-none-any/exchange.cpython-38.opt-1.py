# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/exchange.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 862 bytes
"""
web2ldap plugin classes for MS Exchange 5.5
"""
from web2ldap.app.schema.syntaxes import syntax_registry, RFC822Address, Binary
from web2ldap.app.plugins.activedirectory import MsAdGUID
syntax_registry.reg_at(RFC822Address.oid, [
 '1.2.840.113556.1.2.728',
 '1.2.840.113556.1.2.729'])
syntax_registry.reg_at(Binary.oid, [
 '1.2.840.113556.1.4.7000.102.80',
 '1.2.840.113556.1.4.7000.102.50765'])
syntax_registry.reg_at(MsAdGUID.oid, [
 '1.2.840.113556.1.4.7000.102.11058'])
syntax_registry.reg_syntaxes(__name__)