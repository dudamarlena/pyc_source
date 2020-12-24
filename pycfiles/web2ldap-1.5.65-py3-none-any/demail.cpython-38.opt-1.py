# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/demail.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 714 bytes
"""
web2ldap plugin classes for attributes defined for DE-Mail
"""
import os.path, web2ldapcnf
from web2ldap.app.schema.syntaxes import PropertiesSelectList, syntax_registry

class DemailMaxAuthLevel(PropertiesSelectList):
    oid = 'DemailMaxAuthLevel-oid'
    oid: str
    desc = 'Maximum authentication level of person/user in DE-Mail'
    desc: str
    properties_pathname = os.path.join(web2ldapcnf.etc_dir, 'properties', 'attribute_select_demailMaxAuthLevel.properties')


syntax_registry.reg_at(DemailMaxAuthLevel.oid, [
 '1.3.6.1.4.1.7924.2.1.1.1'])
syntax_registry.reg_syntaxes(__name__)