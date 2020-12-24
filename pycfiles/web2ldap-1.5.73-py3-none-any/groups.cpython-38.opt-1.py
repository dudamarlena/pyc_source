# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/plugins/groups.py
# Compiled at: 2019-10-22 11:17:54
# Size of source mod 2**32: 1236 bytes
"""
web2ldap plugin classes for group related attributes
"""
from web2ldap.app.schema.syntaxes import DistinguishedName, syntax_registry

class Member(DistinguishedName):
    oid = 'Member-oid'
    oid: str
    desc = 'member attribute in a group entry'
    desc: str


syntax_registry.reg_at(Member.oid, [
 '2.5.4.31'])

class MemberOf(DistinguishedName):
    oid = 'MemberOf-oid'
    oid: str
    desc = 'memberOf attribute in a group member entry'
    desc: str
    ref_attrs = ((None, 'Group members', None, 'Search all members of this group'), )


syntax_registry.reg_at(MemberOf.oid, [
 '1.2.840.113556.1.2.102'])

class GroupEntryDN(DistinguishedName):
    oid = 'GroupEntryDN-oid'
    oid: str
    desc = 'entryDN attribute in a group entry'
    desc: str
    ref_attrs = (('memberOf', 'Group members', None, 'Search all members of this group'), )


syntax_registry.reg_at((GroupEntryDN.oid),
  [
 '1.3.6.1.1.20'],
  structural_oc_oids=[
 '2.5.6.9',
 '2.5.6.17',
 '1.2.826.0.1.3458854.2.1.1.1'])
syntax_registry.reg_syntaxes(__name__)