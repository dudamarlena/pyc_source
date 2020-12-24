# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/IPV6-FLOW-LABEL-MIB.py
# Compiled at: 2016-02-13 18:18:29
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, SingleValueConstraint, ValueSizeConstraint, ConstraintsIntersection, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection', 'ConstraintsUnion')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(mib_2, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, ModuleIdentity, Counter64, Unsigned32, MibIdentifier, NotificationType, IpAddress, Bits, Integer32, TimeTicks, iso, ObjectIdentity, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'mib-2', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'ModuleIdentity', 'Counter64', 'Unsigned32', 'MibIdentifier', 'NotificationType', 'IpAddress', 'Bits', 'Integer32', 'TimeTicks', 'iso', 'ObjectIdentity', 'Counter32')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
ipv6FlowLabelMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 103)).setRevisions(('2003-08-28 00:00', ))
if mibBuilder.loadTexts:
    ipv6FlowLabelMIB.setLastUpdated('200308280000Z')
if mibBuilder.loadTexts:
    ipv6FlowLabelMIB.setOrganization('IETF Operations and Management Area')
if mibBuilder.loadTexts:
    ipv6FlowLabelMIB.setContactInfo('Bert Wijnen (Editor)\n                      Lucent Technologies\n                      Schagen 33\n                      3461 GL Linschoten\n                      Netherlands\n                      Phone: +31 348-407-775\n                      EMail: bwijnen@lucent.com\n\n                      Send comments to <mibs@ops.ietf.org>.\n                     ')
if mibBuilder.loadTexts:
    ipv6FlowLabelMIB.setDescription('This MIB module provides commonly used textual\n                      conventions for IPv6 Flow Labels.\n\n                      Copyright (C) The Internet Society (2003).  This\n                      version of this MIB module is part of RFC 3595,\n                      see the RFC itself for full legal notices.\n                     ')

class IPv6FlowLabel(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 1048575)


class IPv6FlowLabelOrAny(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(ValueRangeConstraint(-1, -1), ValueRangeConstraint(0, 1048575))


mibBuilder.exportSymbols('IPV6-FLOW-LABEL-MIB', ipv6FlowLabelMIB=ipv6FlowLabelMIB, IPv6FlowLabel=IPv6FlowLabel, IPv6FlowLabelOrAny=IPv6FlowLabelOrAny, PYSNMP_MODULE_ID=ipv6FlowLabelMIB)