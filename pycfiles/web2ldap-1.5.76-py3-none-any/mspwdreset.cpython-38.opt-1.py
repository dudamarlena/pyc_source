# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/mspwdreset.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 362 bytes
"""
web2ldap plugin classes for msPwdReset*
"""
from web2ldap.app.schema.syntaxes import HashAlgorithmOID, syntax_registry
syntax_registry.reg_at(HashAlgorithmOID.oid, [
 '1.3.6.1.4.1.5427.1.389.4.336'])
syntax_registry.reg_syntaxes(__name__)