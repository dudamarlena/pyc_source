# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6482.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5652
MAX = float('inf')
id_ct_routeOriginAuthz = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.24')

class ASID(univ.Integer):
    __module__ = __name__


class IPAddress(univ.BitString):
    __module__ = __name__


class ROAIPAddress(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('address', IPAddress()), namedtype.OptionalNamedType('maxLength', univ.Integer()))


class ROAIPAddressFamily(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('addressFamily', univ.OctetString().subtype(subtypeSpec=constraint.ValueSizeConstraint(2, 3))), namedtype.NamedType('addresses', univ.SequenceOf(componentType=ROAIPAddress()).subtype(subtypeSpec=constraint.ValueSizeConstraint(1, MAX))))


class RouteOriginAttestation(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', univ.Integer().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=0)), namedtype.NamedType('asID', ASID()), namedtype.NamedType('ipAddrBlocks', univ.SequenceOf(componentType=ROAIPAddressFamily()).subtype(subtypeSpec=constraint.ValueSizeConstraint(1, MAX))))


_cmsContentTypesMapUpdate = {id_ct_routeOriginAuthz: RouteOriginAttestation()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)