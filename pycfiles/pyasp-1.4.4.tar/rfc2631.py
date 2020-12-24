# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc2631.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ

class KeySpecificInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('algorithm', univ.ObjectIdentifier()), namedtype.NamedType('counter', univ.OctetString().subtype(subtypeSpec=constraint.ValueSizeConstraint(4, 4))))


class OtherInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('keyInfo', KeySpecificInfo()), namedtype.OptionalNamedType('partyAInfo', univ.OctetString().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('suppPubInfo', univ.OctetString().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))