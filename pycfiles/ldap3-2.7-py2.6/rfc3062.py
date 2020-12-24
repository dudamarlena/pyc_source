# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ldap3\protocol\rfc3062.py
# Compiled at: 2020-02-23 02:01:39
"""
"""
from pyasn1.type.univ import OctetString, Sequence
from pyasn1.type.namedtype import NamedTypes, OptionalNamedType
from pyasn1.type.tag import Tag, tagClassContext, tagFormatSimple

class UserIdentity(OctetString):
    """
    userIdentity [0] OCTET STRING OPTIONAL
    """
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))
    encoding = 'utf-8'


class OldPasswd(OctetString):
    """
    oldPasswd [1] OCTET STRING OPTIONAL
    """
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 1))
    encoding = 'utf-8'


class NewPasswd(OctetString):
    """
    newPasswd [2] OCTET STRING OPTIONAL
    """
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 2))
    encoding = 'utf-8'


class GenPasswd(OctetString):
    """
    newPasswd [2] OCTET STRING OPTIONAL
    """
    tagSet = OctetString.tagSet.tagImplicitly(Tag(tagClassContext, tagFormatSimple, 0))
    encoding = 'utf-8'


class PasswdModifyRequestValue(Sequence):
    """
    PasswdModifyRequestValue ::= SEQUENCE {
        userIdentity [0] OCTET STRING OPTIONAL
        oldPasswd [1] OCTET STRING OPTIONAL
        newPasswd [2] OCTET STRING OPTIONAL }
    """
    componentType = NamedTypes(OptionalNamedType('userIdentity', UserIdentity()), OptionalNamedType('oldPasswd', OldPasswd()), OptionalNamedType('newPasswd', NewPasswd()))


class PasswdModifyResponseValue(Sequence):
    """
    PasswdModifyResponseValue ::= SEQUENCE {
       genPasswd [0] OCTET STRING OPTIONAL }
    """
    componentType = NamedTypes(OptionalNamedType('genPasswd', GenPasswd()))