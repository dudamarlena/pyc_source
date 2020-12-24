# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc1155.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ

class ObjectName(univ.ObjectIdentifier):
    __module__ = __name__


class SimpleSyntax(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('number', univ.Integer()), namedtype.NamedType('string', univ.OctetString()), namedtype.NamedType('object', univ.ObjectIdentifier()), namedtype.NamedType('empty', univ.Null()))


class IpAddress(univ.OctetString):
    __module__ = __name__
    tagSet = univ.OctetString.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0))
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueSizeConstraint(4, 4)


class NetworkAddress(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('internet', IpAddress()))


class Counter(univ.Integer):
    __module__ = __name__
    tagSet = univ.Integer.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 1))
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(0, 4294967295)


class Gauge(univ.Integer):
    __module__ = __name__
    tagSet = univ.Integer.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 2))
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(0, 4294967295)


class TimeTicks(univ.Integer):
    __module__ = __name__
    tagSet = univ.Integer.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 3))
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(0, 4294967295)


class Opaque(univ.OctetString):
    __module__ = __name__
    tagSet = univ.OctetString.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 4))


class ApplicationSyntax(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('address', NetworkAddress()), namedtype.NamedType('counter', Counter()), namedtype.NamedType('gauge', Gauge()), namedtype.NamedType('ticks', TimeTicks()), namedtype.NamedType('arbitrary', Opaque()))


class ObjectSyntax(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('simple', SimpleSyntax()), namedtype.NamedType('application-wide', ApplicationSyntax()))