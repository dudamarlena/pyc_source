# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/debian.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 594 bytes
"""
web2ldap plugin classes for attributes used on ldap://db.debian.org
"""
from web2ldap.app.schema.syntaxes import DynamicValueSelectList, syntax_registry

class DebianSupplementaryGid(DynamicValueSelectList):
    oid = 'DebianSupplementaryGid-oid'
    oid: str
    desc = 'Debian: sudoUser'
    desc: str
    ldap_url = 'ldap:///_?gid,gid?sub?(objectClass=debianGroup)'


syntax_registry.reg_at(DebianSupplementaryGid.oid, [
 '1.3.6.1.4.1.9586.100.4.2.11'])
syntax_registry.reg_syntaxes(__name__)