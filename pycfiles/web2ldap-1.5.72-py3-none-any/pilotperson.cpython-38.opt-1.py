# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/pilotperson.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 703 bytes
"""
web2ldap plugin classes for attributes defined for pilotPerson

see also RFC1274
"""
from web2ldap.app.schema.syntaxes import SelectList, syntax_registry

class MailPreferenceOption(SelectList):
    oid = 'MailPreferenceOption-oid'
    oid: str
    desc = 'RFC1274: mail preference option syntax'
    desc: str
    attr_value_dict = {'':'', 
     '0':'no-list-inclusion', 
     '1':'any-list-inclusion', 
     '2':'professional-list-inclusion'}


syntax_registry.reg_at(MailPreferenceOption.oid, [
 '0.9.2342.19200300.100.1.47'])
syntax_registry.reg_syntaxes(__name__)