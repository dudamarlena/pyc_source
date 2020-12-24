# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/PYSNMP-SOURCE-MIB.py
# Compiled at: 2019-08-18 17:24:05
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ConstraintsUnion')
(pysnmpModuleIDs,) = mibBuilder.importSymbols('PYSNMP-MIB', 'pysnmpModuleIDs')
(snmpTargetAddrEntry,) = mibBuilder.importSymbols('SNMP-TARGET-MIB', 'snmpTargetAddrEntry')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(ModuleIdentity, iso, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, NotificationType, IpAddress, MibIdentifier, Unsigned32, Counter32, ObjectIdentity, Counter64, Bits, Integer32, TimeTicks) = mibBuilder.importSymbols('SNMPv2-SMI', 'ModuleIdentity', 'iso', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'NotificationType', 'IpAddress', 'MibIdentifier', 'Unsigned32', 'Counter32', 'ObjectIdentity', 'Counter64', 'Bits', 'Integer32', 'TimeTicks')
(TextualConvention, DisplayString, TAddress) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString', 'TAddress')
pysnmpSourceMIB = ModuleIdentity((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8))
if mibBuilder.loadTexts:
    pysnmpSourceMIB.setRevisions(('2017-04-14 00:00', '2015-01-16 00:00'))
if mibBuilder.loadTexts:
    pysnmpSourceMIB.setLastUpdated('201704140000Z')
if mibBuilder.loadTexts:
    pysnmpSourceMIB.setOrganization('The PySNMP Project')
if mibBuilder.loadTexts:
    pysnmpSourceMIB.setContactInfo('E-mail: Ilya Etingof <etingof@gmail.com> GitHub: https://github.com/etingof/pysnmp')
if mibBuilder.loadTexts:
    pysnmpSourceMIB.setDescription('This MIB module defines implementation specific objects that provide variable source transport endpoints feature to SNMP Engine and Standard SNMP Applications.')
pysnmpSourceMIBObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8, 1))
pysnmpSourceMIBConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8, 2))
snmpSourceAddrTable = MibTable((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8, 1, 1))
if mibBuilder.loadTexts:
    snmpSourceAddrTable.setStatus('current')
if mibBuilder.loadTexts:
    snmpSourceAddrTable.setDescription('A table of transport addresses to be used as a source in the generation of SNMP messages. This table contains additional objects for the SNMP-TRANSPORT-ADDRESS::snmpSourceAddressTable.')
snmpSourceAddrEntry = MibTableRow((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8, 1, 1, 1))
snmpTargetAddrEntry.registerAugmentions(('PYSNMP-SOURCE-MIB', 'snmpSourceAddrEntry'))
snmpSourceAddrEntry.setIndexNames(*snmpTargetAddrEntry.getIndexNames())
if mibBuilder.loadTexts:
    snmpSourceAddrEntry.setStatus('current')
if mibBuilder.loadTexts:
    snmpSourceAddrEntry.setDescription('A transport address to be used as a source in the generation of SNMP operations. An entry containing additional management information applicable to a particular target.')
snmpSourceAddrTAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8, 1, 1, 1,
                                         1), TAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    snmpSourceAddrTAddress.setStatus('current')
if mibBuilder.loadTexts:
    snmpSourceAddrTAddress.setDescription('This object contains a transport address. The format of this address depends on the value of the snmpSourceAddrTDomain object.')
pysnmpSourceMIBCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8, 2, 1))
pysnmpSourceMIBGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 8, 2, 2))
mibBuilder.exportSymbols('PYSNMP-SOURCE-MIB', pysnmpSourceMIBConformance=pysnmpSourceMIBConformance, pysnmpSourceMIB=pysnmpSourceMIB, snmpSourceAddrTable=snmpSourceAddrTable, snmpSourceAddrEntry=snmpSourceAddrEntry, pysnmpSourceMIBGroups=pysnmpSourceMIBGroups, PYSNMP_MODULE_ID=pysnmpSourceMIB, snmpSourceAddrTAddress=snmpSourceAddrTAddress, pysnmpSourceMIBObjects=pysnmpSourceMIBObjects, pysnmpSourceMIBCompliances=pysnmpSourceMIBCompliances)