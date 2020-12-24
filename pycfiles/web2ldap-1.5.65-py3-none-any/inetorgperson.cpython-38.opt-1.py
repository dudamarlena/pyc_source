# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/inetorgperson.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1214 bytes
"""
web2ldap plugin classes for selected attributes of inetOrgPerson
(see RFC 2798)

Basically some attribute values are composed from other attributes
but only if the structural object class of the entry is inetOrgPerson.
"""
from web2ldap.app.schema.syntaxes import ComposedAttribute, DirectoryString, syntax_registry

class CNInetOrgPerson(ComposedAttribute, DirectoryString):
    oid = 'CNInetOrgPerson-oid'
    oid: str
    desc = 'Attribute cn in object class inetOrgPerson'
    desc: str
    maxValues = 1
    compose_templates = ('{givenName} {sn}', )


class DisplayNameInetOrgPerson(ComposedAttribute, DirectoryString):
    oid = 'DisplayNameInetOrgPerson-oid'
    oid: str
    desc = 'Attribute displayName in object class inetOrgPerson'
    desc: str
    maxValues = 1
    compose_templates = ('{givenName} {sn} ({uid}/{employeeNumber})', '{givenName} {sn} ({uid}/{uniqueIdentifier})',
                         '{givenName} {sn} ({employeeNumber})', '{givenName} {sn} / {ou} ({departmentNumber})',
                         '{givenName} {sn} / {ou}', '{givenName} {sn} ({uid})', '{givenName} {sn}')


syntax_registry.reg_syntaxes(__name__)