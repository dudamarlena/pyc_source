# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/entrust.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1000 bytes
"""
web2ldap plugin classes for Entrust PKI
"""
from web2ldap.app.schema.syntaxes import Binary, syntax_registry
syntax_registry.reg_at(Binary.oid, [
 '1.2.840.113533.7.68.22',
 '1.2.840.113533.7.79.0',
 '1.2.840.113533.7.68.28',
 '1.2.840.113533.7.68.24',
 '1.2.840.113533.7.68.27',
 '1.2.840.113533.7.68.23',
 '1.2.840.113533.7.68.25',
 '1.2.840.113533.7.68.26',
 '1.2.840.113533.7.68.30',
 '2.16.840.1.114027.22.4'])
syntax_registry.reg_syntaxes(__name__)