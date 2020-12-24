# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/SNMPv2-TC-v1.py
# Compiled at: 2016-02-13 18:08:56
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(NotificationType, Integer32, MibIdentifier, Counter64, iso, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, ModuleIdentity, IpAddress, Bits, Unsigned32, ObjectIdentity, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'NotificationType', 'Integer32', 'MibIdentifier', 'Counter64', 'iso', 'TimeTicks', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'ModuleIdentity', 'IpAddress', 'Bits', 'Unsigned32', 'ObjectIdentity', 'Counter32')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')

class DisplayString(OctetString):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 255)


class PhysAddress(OctetString):
    __module__ = __name__


class MacAddress(OctetString):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(6, 6)
    fixedLength = 6


class TruthValue(Integer32):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('true', 1), ('false', 2))


class TestAndIncr(Integer32):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 2147483647)


class AutonomousType(ObjectIdentifier):
    __module__ = __name__


class InstancePointer(ObjectIdentifier):
    __module__ = __name__


class VariablePointer(ObjectIdentifier):
    __module__ = __name__


class RowPointer(ObjectIdentifier):
    __module__ = __name__


class RowStatus(Integer32):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))
    namedValues = NamedValues(('active', 1), ('notInService', 2), ('notReady', 3), ('createAndGo',
                                                                                    4), ('createAndWait',
                                                                                         5), ('destroy',
                                                                                              6))


class TimeStamp(TimeTicks):
    __module__ = __name__


class TimeInterval(Integer32):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 2147483647)


class DateAndTime(OctetString):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(11, 11)
    fixedLength = 11


class StorageType(Integer32):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))
    namedValues = NamedValues(('other', 1), ('volatile', 2), ('nonVolatile', 3), ('permanent',
                                                                                  4), ('readOnly',
                                                                                       5))


class TDomain(ObjectIdentifier):
    __module__ = __name__


class TAddress(OctetString):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(1, 255)


mibBuilder.exportSymbols('SNMPv2-TC-v1', TDomain=TDomain, VariablePointer=VariablePointer, InstancePointer=InstancePointer, StorageType=StorageType, PhysAddress=PhysAddress, TestAndIncr=TestAndIncr, AutonomousType=AutonomousType, TimeStamp=TimeStamp, RowPointer=RowPointer, TAddress=TAddress, DateAndTime=DateAndTime, RowStatus=RowStatus, MacAddress=MacAddress, DisplayString=DisplayString, TimeInterval=TimeInterval, TruthValue=TruthValue)