# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3779.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5280
id_pe_ipAddrBlocks = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.7')

class IPAddress(univ.BitString):
    __module__ = __name__


class IPAddressRange(univ.Sequence):
    __module__ = __name__


IPAddressRange.componentType = namedtype.NamedTypes(namedtype.NamedType('min', IPAddress()), namedtype.NamedType('max', IPAddress()))

class IPAddressOrRange(univ.Choice):
    __module__ = __name__


IPAddressOrRange.componentType = namedtype.NamedTypes(namedtype.NamedType('addressPrefix', IPAddress()), namedtype.NamedType('addressRange', IPAddressRange()))

class IPAddressChoice(univ.Choice):
    __module__ = __name__


IPAddressChoice.componentType = namedtype.NamedTypes(namedtype.NamedType('inherit', univ.Null()), namedtype.NamedType('addressesOrRanges', univ.SequenceOf(componentType=IPAddressOrRange())))

class IPAddressFamily(univ.Sequence):
    __module__ = __name__


IPAddressFamily.componentType = namedtype.NamedTypes(namedtype.NamedType('addressFamily', univ.OctetString().subtype(subtypeSpec=constraint.ValueSizeConstraint(2, 3))), namedtype.NamedType('ipAddressChoice', IPAddressChoice()))

class IPAddrBlocks(univ.SequenceOf):
    __module__ = __name__


IPAddrBlocks.componentType = IPAddressFamily()
id_pe_autonomousSysIds = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.8')

class ASId(univ.Integer):
    __module__ = __name__


class ASRange(univ.Sequence):
    __module__ = __name__


ASRange.componentType = namedtype.NamedTypes(namedtype.NamedType('min', ASId()), namedtype.NamedType('max', ASId()))

class ASIdOrRange(univ.Choice):
    __module__ = __name__


ASIdOrRange.componentType = namedtype.NamedTypes(namedtype.NamedType('id', ASId()), namedtype.NamedType('range', ASRange()))

class ASIdentifierChoice(univ.Choice):
    __module__ = __name__


ASIdentifierChoice.componentType = namedtype.NamedTypes(namedtype.NamedType('inherit', univ.Null()), namedtype.NamedType('asIdsOrRanges', univ.SequenceOf(componentType=ASIdOrRange())))

class ASIdentifiers(univ.Sequence):
    __module__ = __name__


ASIdentifiers.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('asnum', ASIdentifierChoice().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.OptionalNamedType('rdi', ASIdentifierChoice().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))
_certificateExtensionsMapUpdate = {id_pe_ipAddrBlocks: IPAddrBlocks(), id_pe_autonomousSysIds: ASIdentifiers()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)