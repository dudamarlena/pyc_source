# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/T11-TC-MIB.py
# Compiled at: 2016-02-13 18:29:39
(ObjectIdentifier, OctetString, Integer) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'OctetString', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(IpAddress, Unsigned32, MibIdentifier, Integer32, TimeTicks, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, mib_2, NotificationType, Counter32, Counter64, ModuleIdentity, iso, Gauge32, Bits) = mibBuilder.importSymbols('SNMPv2-SMI', 'IpAddress', 'Unsigned32', 'MibIdentifier', 'Integer32', 'TimeTicks', 'ObjectIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'mib-2', 'NotificationType', 'Counter32', 'Counter64', 'ModuleIdentity', 'iso', 'Gauge32', 'Bits')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
t11TcMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 136)).setRevisions(('2006-03-02 00:00', ))
if mibBuilder.loadTexts:
    t11TcMIB.setLastUpdated('200603020000Z')
if mibBuilder.loadTexts:
    t11TcMIB.setOrganization('T11')
if mibBuilder.loadTexts:
    t11TcMIB.setContactInfo('     Claudio DeSanti\n                  Cisco Systems, Inc.\n                  170 West Tasman Drive\n                  San Jose, CA 95134 USA\n                  Phone: +1 408 853-9172\n                  EMail: cds@cisco.com\n\n                  Keith McCloghrie\n                  Cisco Systems, Inc.\n                  170 West Tasman Drive\n                  San Jose, CA USA 95134\n                  Phone: +1 408-526-5260\n                  EMail: kzm@cisco.com')
if mibBuilder.loadTexts:
    t11TcMIB.setDescription('This module defines textual conventions used in T11 MIBs.\n\n           Copyright (C) The Internet Society (2006).  This version\n           of this MIB module is part of RFC 4439;  see the RFC\n           itself for full legal notices.')

class T11FabricIndex(Unsigned32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(0, 4095)


mibBuilder.exportSymbols('T11-TC-MIB', T11FabricIndex=T11FabricIndex, PYSNMP_MODULE_ID=t11TcMIB, t11TcMIB=t11TcMIB)