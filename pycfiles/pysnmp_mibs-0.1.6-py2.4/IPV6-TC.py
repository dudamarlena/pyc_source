# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/IPV6-TC.py
# Compiled at: 2016-02-13 18:18:33
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ValueSizeConstraint, ConstraintsIntersection, SingleValueConstraint, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection', 'SingleValueConstraint', 'ConstraintsUnion')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(TimeTicks, Counter32, iso, Bits, ObjectIdentity, NotificationType, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, ModuleIdentity, Integer32, Counter64, IpAddress, MibIdentifier) = mibBuilder.importSymbols('SNMPv2-SMI', 'TimeTicks', 'Counter32', 'iso', 'Bits', 'ObjectIdentity', 'NotificationType', 'Gauge32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Unsigned32', 'ModuleIdentity', 'Integer32', 'Counter64', 'IpAddress', 'MibIdentifier')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')

class Ipv6Address(OctetString, TextualConvention):
    __module__ = __name__
    displayHint = '2x:'
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(16, 16)
    fixedLength = 16


class Ipv6AddressPrefix(OctetString, TextualConvention):
    __module__ = __name__
    displayHint = '2x:'
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 16)


class Ipv6AddressIfIdentifier(OctetString, TextualConvention):
    __module__ = __name__
    displayHint = '2x:'
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 8)


class Ipv6IfIndex(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(1, 2147483647)


class Ipv6IfIndexOrZero(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 2147483647)


mibBuilder.exportSymbols('IPV6-TC', Ipv6Address=Ipv6Address, Ipv6IfIndex=Ipv6IfIndex, Ipv6AddressPrefix=Ipv6AddressPrefix, Ipv6AddressIfIdentifier=Ipv6AddressIfIdentifier, Ipv6IfIndexOrZero=Ipv6IfIndexOrZero)