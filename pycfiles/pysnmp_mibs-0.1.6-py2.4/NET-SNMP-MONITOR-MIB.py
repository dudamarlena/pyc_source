# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/NET-SNMP-MONITOR-MIB.py
# Compiled at: 2016-02-13 18:22:39
(ObjectIdentifier, OctetString, Integer) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'OctetString', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ConstraintsUnion', 'SingleValueConstraint')
(netSnmpModuleIDs, netSnmpObjects) = mibBuilder.importSymbols('NET-SNMP-MIB', 'netSnmpModuleIDs', 'netSnmpObjects')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, NotificationType, Unsigned32, Counter32, ObjectIdentity, Integer32, Bits, TimeTicks, Gauge32, IpAddress, ModuleIdentity, iso, MibIdentifier) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64', 'NotificationType', 'Unsigned32', 'Counter32', 'ObjectIdentity', 'Integer32', 'Bits', 'TimeTicks', 'Gauge32', 'IpAddress', 'ModuleIdentity', 'iso', 'MibIdentifier')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
netSnmpMonitorMIB = ModuleIdentity((1, 3, 6, 1, 4, 1, 8072, 3, 1, 3)).setRevisions(('2002-02-09 00:00', ))
if mibBuilder.loadTexts:
    netSnmpMonitorMIB.setLastUpdated('200202090000Z')
if mibBuilder.loadTexts:
    netSnmpMonitorMIB.setOrganization('www.net-snmp.org')
if mibBuilder.loadTexts:
    netSnmpMonitorMIB.setContactInfo('postal:   Wes Hardaker\n                    P.O. Box 382\n                    Davis CA  95617\n\n          email:    net-snmp-coders@lists.sourceforge.net')
if mibBuilder.loadTexts:
    netSnmpMonitorMIB.setDescription('Configured elements of the system to monitor\n\t (XXX - ugh! - need a better description!)')
nsProcess = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 1, 21))
nsDisk = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 1, 22))
nsFile = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 1, 23))
nsLog = MibIdentifier((1, 3, 6, 1, 4, 1, 8072, 1, 24))
mibBuilder.exportSymbols('NET-SNMP-MONITOR-MIB', nsProcess=nsProcess, nsFile=nsFile, PYSNMP_MODULE_ID=netSnmpMonitorMIB, nsDisk=nsDisk, netSnmpMonitorMIB=netSnmpMonitorMIB, nsLog=nsLog)