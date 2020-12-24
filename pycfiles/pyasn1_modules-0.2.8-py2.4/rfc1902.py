# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc1902.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ

class Integer(univ.Integer):
    __module__ = __name__
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(-2147483648, 2147483647)


class Integer32(univ.Integer):
    __module__ = __name__
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(-2147483648, 2147483647)


class OctetString(univ.OctetString):
    __module__ = __name__
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueSizeConstraint(0, 65535)


class IpAddress(univ.OctetString):
    __module__ = __name__
    tagSet = univ.OctetString.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 0))
    subtypeSpec = univ.OctetString.subtypeSpec + constraint.ValueSizeConstraint(4, 4)


class Counter32(univ.Integer):
    __module__ = __name__
    tagSet = univ.Integer.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 1))
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(0, 4294967295)


class Gauge32(univ.Integer):
    __module__ = __name__
    tagSet = univ.Integer.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 2))
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(0, 4294967295)


class Unsigned32(univ.Integer):
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


class Counter64(univ.Integer):
    __module__ = __name__
    tagSet = univ.Integer.tagSet.tagImplicitly(tag.Tag(tag.tagClassApplication, tag.tagFormatSimple, 6))
    subtypeSpec = univ.Integer.subtypeSpec + constraint.ValueRangeConstraint(0, 18446744073709551615)


class Bits(univ.OctetString):
    __module__ = __name__


class ObjectName(univ.ObjectIdentifier):
    __module__ = __name__


class SimpleSyntax(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('integer-value', Integer()), namedtype.NamedType('string-value', OctetString()), namedtype.NamedType('objectID-value', univ.ObjectIdentifier()))


class ApplicationSyntax(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('ipAddress-value', IpAddress()), namedtype.NamedType('counter-value', Counter32()), namedtype.NamedType('timeticks-value', TimeTicks()), namedtype.NamedType('arbitrary-value', Opaque()), namedtype.NamedType('big-counter-value', Counter64()), namedtype.NamedType('gauge32-value', Gauge32()))


class ObjectSyntax(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('simple', SimpleSyntax()), namedtype.NamedType('application-wide', ApplicationSyntax()))