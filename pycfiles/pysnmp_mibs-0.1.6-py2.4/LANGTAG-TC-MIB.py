# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/LANGTAG-TC-MIB.py
# Compiled at: 2016-02-13 18:17:53
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, SingleValueConstraint, ValueSizeConstraint, ConstraintsIntersection, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection', 'ConstraintsUnion')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Counter32, Counter64, iso, mib_2, NotificationType, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, Gauge32, ObjectIdentity, Unsigned32, MibIdentifier, Integer32, ModuleIdentity, Bits, TimeTicks) = mibBuilder.importSymbols('SNMPv2-SMI', 'Counter32', 'Counter64', 'iso', 'mib-2', 'NotificationType', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'IpAddress', 'Gauge32', 'ObjectIdentity', 'Unsigned32', 'MibIdentifier', 'Integer32', 'ModuleIdentity', 'Bits', 'TimeTicks')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
langTagTcMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 165)).setRevisions(('2007-11-09 00:00', ))
if mibBuilder.loadTexts:
    langTagTcMIB.setLastUpdated('200711090000Z')
if mibBuilder.loadTexts:
    langTagTcMIB.setOrganization('IETF Operations and Management (OPS) Area')
if mibBuilder.loadTexts:
    langTagTcMIB.setContactInfo('EMail: ops-area@ietf.org\n                  Home page: http://www.ops.ietf.org/')
if mibBuilder.loadTexts:
    langTagTcMIB.setDescription('This MIB module defines a textual convention for\n            representing BCP 47 language tags.')

class LangTag(OctetString, TextualConvention):
    __module__ = __name__
    displayHint = '1a'
    subtypeSpec = OctetString.subtypeSpec + ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(2, 63))


mibBuilder.exportSymbols('LANGTAG-TC-MIB', PYSNMP_MODULE_ID=langTagTcMIB, langTagTcMIB=langTagTcMIB, LangTag=LangTag)