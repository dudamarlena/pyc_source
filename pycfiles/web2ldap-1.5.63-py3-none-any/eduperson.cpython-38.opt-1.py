# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/eduperson.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 2106 bytes
"""
web2ldap plugin classes for attributes defined eduPerson

See http://middleware.internet2.edu/eduperson/
"""
import re
from web2ldap.app.schema.syntaxes import IA5String, SelectList, DynamicDNSelectList, syntax_registry

class EduPersonAffiliation(SelectList):
    oid = 'EduPersonAffiliation-oid'
    oid: str
    desc = 'Affiliation (see eduPerson)'
    desc: str
    attr_value_dict = {'':'', 
     'faculty':'faculty', 
     'student':'student', 
     'staff':'staff', 
     'alum':'alum', 
     'member':'member', 
     'affiliate':'affiliate', 
     'employee':'employee', 
     'library-walk-in':'library-walk-in'}


syntax_registry.reg_at(EduPersonAffiliation.oid, [
 '1.3.6.1.4.1.5923.1.1.1.1',
 '1.3.6.1.4.1.5923.1.1.1.5'])

class EduPersonScopedAffiliation(IA5String):
    oid = 'EduPersonScopedAffiliation-oid'
    oid: str
    desc = 'Scoped affiliation (see eduPerson)'
    desc: str
    reObj = re.compile('^(faculty|student|staff|alum|member|affiliate|employee|library-walk-in)@[a-zA-Z0-9.-]+$')


syntax_registry.reg_at(EduPersonScopedAffiliation.oid, [
 '1.3.6.1.4.1.5923.1.1.1.9'])

class EduPersonOrgUnitDN(DynamicDNSelectList):
    oid = 'EduPersonOrgUnitDN-oid'
    oid: str
    desc = 'DN of associated organizational unit entry (see eduPerson)'
    desc: str
    ldap_url = 'ldap:///_??sub?(objectClass=organizationalUnit)'


syntax_registry.reg_at(EduPersonOrgUnitDN.oid, [
 '1.3.6.1.4.1.5923.1.1.1.4',
 '1.3.6.1.4.1.5923.1.1.1.8'])

class EduPersonOrgDN(DynamicDNSelectList):
    oid = 'EduPersonOrgDN-oid'
    oid: str
    desc = 'DN of associated organization entry (see eduPerson)'
    desc: str
    ldap_url = 'ldap:///_??sub?(objectClass=organization)'


syntax_registry.reg_at(EduPersonOrgDN.oid, [
 '1.3.6.1.4.1.5923.1.1.1.3'])
syntax_registry.reg_syntaxes(__name__)