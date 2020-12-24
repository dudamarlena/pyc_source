# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\novell.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from pyasn1.type.univ import OctetString, Integer, Sequence, SequenceOf
from pyasn1.type.namedtype import NamedType, NamedTypes, OptionalNamedType
from pyasn1.type.tag import Tag, tagFormatSimple, tagClassUniversal, TagSet
NMAS_LDAP_EXT_VERSION = 1

class Identity(OctetString):
    encoding = 'utf-8'


class LDAPDN(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassUniversal, tagFormatSimple, 4))
    encoding = 'utf-8'


class Password(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassUniversal, tagFormatSimple, 4))
    encoding = 'utf-8'


class LDAPOID(OctetString):
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassUniversal, tagFormatSimple, 4))
    encoding = 'utf-8'


class GroupCookie(Integer):
    tagSet = Integer.tagSet.tagImplicitly(Tag(tagClassUniversal, tagFormatSimple, 2))


class NmasVer(Integer):
    tagSet = Integer.tagSet.tagImplicitly(Tag(tagClassUniversal, tagFormatSimple, 2))


class Error(Integer):
    tagSet = Integer.tagSet.tagImplicitly(Tag(tagClassUniversal, tagFormatSimple, 2))


class NmasGetUniversalPasswordRequestValue(Sequence):
    componentType = NamedTypes(NamedType('nmasver', NmasVer()), NamedType('reqdn', Identity()))


class NmasGetUniversalPasswordResponseValue(Sequence):
    componentType = NamedTypes(NamedType('nmasver', NmasVer()), NamedType('err', Error()), OptionalNamedType('passwd', Password()))


class NmasSetUniversalPasswordRequestValue(Sequence):
    componentType = NamedTypes(NamedType('nmasver', NmasVer()), NamedType('reqdn', Identity()), NamedType('new_passwd', Password()))


class NmasSetUniversalPasswordResponseValue(Sequence):
    componentType = NamedTypes(NamedType('nmasver', NmasVer()), NamedType('err', Error()))


class ReplicaList(SequenceOf):
    componentType = OctetString()


class ReplicaInfoRequestValue(Sequence):
    tagSet = TagSet()
    componentType = NamedTypes(NamedType('server_dn', LDAPDN()), NamedType('partition_dn', LDAPDN()))


class ReplicaInfoResponseValue(Sequence):
    tagSet = TagSet()
    componentType = NamedTypes(NamedType('partition_id', Integer()), NamedType('replica_state', Integer()), NamedType('modification_time', Integer()), NamedType('purge_time', Integer()), NamedType('local_partition_id', Integer()), NamedType('partition_dn', LDAPDN()), NamedType('replica_type', Integer()), NamedType('flags', Integer()))


class CreateGroupTypeRequestValue(Sequence):
    componentType = NamedTypes(NamedType('createGroupType', LDAPOID()), OptionalNamedType('createGroupValue', OctetString()))


class CreateGroupTypeResponseValue(Sequence):
    componentType = NamedTypes(NamedType('createGroupCookie', GroupCookie()), OptionalNamedType('createGroupValue', OctetString()))


class EndGroupTypeRequestValue(Sequence):
    componentType = NamedTypes(NamedType('endGroupCookie', GroupCookie()), OptionalNamedType('endGroupValue', OctetString()))


class EndGroupTypeResponseValue(Sequence):
    componentType = NamedTypes(OptionalNamedType('endGroupValue', OctetString()))


class GroupingControlValue(Sequence):
    componentType = NamedTypes(NamedType('groupingCookie', GroupCookie()), OptionalNamedType('groupValue', OctetString()))