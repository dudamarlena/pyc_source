# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/subentries.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1082 bytes
"""
web2ldap plugin classes for attributes defined for subentries (see RFC 3672)
"""
from web2ldap.app.schema.syntaxes import GSER, SelectList, syntax_registry

class SubtreeSpecification(GSER):
    oid = '1.3.6.1.4.1.1466.115.121.1.45'
    oid: str
    desc = 'SubtreeSpecification'
    desc: str


class AdministrativeRole(SelectList):
    oid = 'AdministrativeRole-oid'
    oid: str
    desc = 'RFC 3672: indicate that the associated administrative area is concerned with one or more administrative roles'
    attr_value_dict = {'2.5.23.1':'autonomousArea', 
     '2.5.23.2':'accessControlSpecificArea', 
     '2.5.23.3':'accessControlInnerArea', 
     '2.5.23.4':'subschemaAdminSpecificArea', 
     '2.5.23.5':'collectiveAttributeSpecificArea', 
     '2.5.23.6':'collectiveAttributeInnerArea'}


syntax_registry.reg_at(AdministrativeRole.oid, [
 '2.5.18.5'])
syntax_registry.reg_syntaxes(__name__)