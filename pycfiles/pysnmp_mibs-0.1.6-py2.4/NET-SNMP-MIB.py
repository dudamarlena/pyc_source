# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/NET-SNMP-MIB.py
# Compiled at: 2016-02-13 18:22:30
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'SingleValueConstraint')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(ObjectIdentity, iso, Counter64, NotificationType, IpAddress, Integer32, enterprises, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, TimeTicks, Gauge32, Counter32, ModuleIdentity, Unsigned32, Bits) = mibBuilder.importSymbols('SNMPv2-SMI', 'ObjectIdentity', 'iso', 'Counter64', 'NotificationType', 'IpAddress', 'Integer32', 'enterprises', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'MibIdentifier', 'TimeTicks', 'Gauge32', 'Counter32', 'ModuleIdentity', 'Unsigned32', 'Bits')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
netSnmp = ModuleIdentity((1, 3, 6, 1, 4, 1, 8072)).setRevisions(('2002-01-30 00:00', ))
if mibBuilder.loadTexts:
    netSnmp.setLastUpdated('200201300000Z')
if mibBuilder.loadTexts:
    netSnmp.setOrganization('www.net-snmp.org')
if mibBuilder.loadTexts:
    netSnmp.setContactInfo('postal:   Wes Hardaker\n                    P.O. Box 382\n                    Davis CA  95617\n\n          email:    net-snmp-coders@lists.sourceforge.net')
if mibBuilder.loadTexts:
    netSnmp.setDescription('Top-level infrastructure of the Net-SNMP project enterprise MIB tree')
netSnmpObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 1))
netSnmpEnumerations = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 3))
netSnmpModuleIDs = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 3, 1))
netSnmpAgentOIDs = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 3, 2))
netSnmpDomains = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 3, 3))
netSnmpExperimental = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 9999))
netSnmpPlaypen = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 9999, 9999))
netSnmpNotificationPrefix = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 4))
netSnmpNotifications = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 4, 0))
netSnmpNotificationObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 4, 1))
netSnmpConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 5))
netSnmpCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 5, 1))
netSnmpGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 5, 2))
mibBuilder.exportSymbols('NET-SNMP-MIB', netSnmpObjects=netSnmpObjects, PYSNMP_MODULE_ID=netSnmp, netSnmpExperimental=netSnmpExperimental, netSnmpEnumerations=netSnmpEnumerations, netSnmp=netSnmp, netSnmpCompliances=netSnmpCompliances, netSnmpAgentOIDs=netSnmpAgentOIDs, netSnmpDomains=netSnmpDomains, netSnmpConformance=netSnmpConformance, netSnmpModuleIDs=netSnmpModuleIDs, netSnmpPlaypen=netSnmpPlaypen, netSnmpNotificationPrefix=netSnmpNotificationPrefix, netSnmpNotifications=netSnmpNotifications, netSnmpNotificationObjects=netSnmpNotificationObjects, netSnmpGroups=netSnmpGroups)