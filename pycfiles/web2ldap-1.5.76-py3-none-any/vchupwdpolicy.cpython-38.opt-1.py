# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/vchupwdpolicy.py
# Compiled at: 2020-04-23 17:52:33
# Size of source mod 2**32: 980 bytes
"""
web2ldap plugin classes for attributes defined in draft-vchu-ldap-pwd-policy
"""
from web2ldap.app.schema.syntaxes import SelectList, syntax_registry

class OnOffFlag(SelectList):
    __doc__ = '\n    Plugin class for flag attribute with value "on" or "off"\n    '
    oid = 'OnOffFlag-oid'
    oid: str
    desc = 'Only values "on" or "off" are allowed'
    desc: str
    attr_value_dict = {'on':'on',  'off':'off'}


syntax_registry.reg_at(OnOffFlag.oid, [
 '2.16.840.1.113730.3.1.102',
 '2.16.840.1.113730.3.1.103',
 '2.16.840.1.113730.3.1.98',
 '2.16.840.1.113730.3.1.105',
 '2.16.840.1.113730.3.1.220',
 '2.16.840.1.113730.3.1.108'])
syntax_registry.reg_syntaxes(__name__)