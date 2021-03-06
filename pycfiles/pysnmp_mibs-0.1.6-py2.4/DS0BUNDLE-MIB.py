# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DS0BUNDLE-MIB.py
# Compiled at: 2016-02-13 18:10:44
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, SingleValueConstraint, ConstraintsIntersection, ValueRangeConstraint, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'SingleValueConstraint', 'ConstraintsIntersection', 'ValueRangeConstraint', 'ConstraintsUnion')
(ifIndex, InterfaceIndex) = mibBuilder.importSymbols('IF-MIB', 'ifIndex', 'InterfaceIndex')
(ModuleCompliance, ObjectGroup, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'ObjectGroup', 'NotificationGroup')
(ModuleIdentity, Counter64, NotificationType, TimeTicks, Bits, Counter32, IpAddress, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, Integer32, MibIdentifier, Unsigned32, transmission, ObjectIdentity, iso) = mibBuilder.importSymbols('SNMPv2-SMI', 'ModuleIdentity', 'Counter64', 'NotificationType', 'TimeTicks', 'Bits', 'Counter32', 'IpAddress', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'Integer32', 'MibIdentifier', 'Unsigned32', 'transmission', 'ObjectIdentity', 'iso')
(TextualConvention, TestAndIncr, RowStatus, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'TestAndIncr', 'RowStatus', 'DisplayString')
ds0Bundle = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 82)).setRevisions(('1998-05-24 20:10', ))
if mibBuilder.loadTexts:
    ds0Bundle.setLastUpdated('9807161630Z')
if mibBuilder.loadTexts:
    ds0Bundle.setOrganization('IETF Trunk MIB Working Group')
if mibBuilder.loadTexts:
    ds0Bundle.setContactInfo('        David Fowler\n\n          Postal: Newbridge Networks Corporation\n                  600 March Road\n                  Kanata, Ontario, Canada K2K 2E6\n\n                  Tel: +1 613 591 3600\n                  Fax: +1 613 599 3619\n\n          E-mail: davef@newbridge.com')
if mibBuilder.loadTexts:
    ds0Bundle.setDescription('The MIB module to describe\n             DS0 Bundle interfaces objects.')
dsx0BundleNextIndex = MibScalar((1, 3, 6, 1, 2, 1, 10, 82, 2), TestAndIncr()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    dsx0BundleNextIndex.setDescription('This object is used to assist the manager in\n               selecting a value for dsx0BundleIndex.  Because\n               this object is of syntax TestAndIncr (see the\n               SNMPv2-TC document, RFC 1903) it can also be used\n               to avoid race conditions with multiple managers\n               trying to create rows in the table.\n\n               If the result of the SET for dsx0BundleNextIndex\n               is not success, this means the value has been\n               changed from index (i.e. another manager used the\n               value), so a new value is required.\n\n               The algorithm is:\n               done = false\n               while done == false\n                   index = GET (dsx0BundleNextIndex.0)\n                   SET (dsx0BundleNextIndex.0=index)\n                   if (set failed)\n                     done = false\n                   else\n                     SET(dsx0BundleRowStatus.index=createAndGo)\n                     if (set failed)\n                       done = false\n                     else\n                       done = true\n                       other error handling')
dsx0BundleTable = MibTable((1, 3, 6, 1, 2, 1, 10, 82, 3))
if mibBuilder.loadTexts:
    dsx0BundleTable.setDescription("There is an row in this table for each ds0Bundle\n               in the system.  This table can be used to\n               (indirectly) create rows in the ifTable with\n               ifType = 'ds0Bundle(82)'.")
dsx0BundleEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 82, 3, 1)).setIndexNames((0, 'DS0BUNDLE-MIB',
                                                                               'dsx0BundleIndex'))
if mibBuilder.loadTexts:
    dsx0BundleEntry.setDescription('There is a row in entry in this table for each\n               ds0Bundle interface.')
dsx0BundleIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 82, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647)))
if mibBuilder.loadTexts:
    dsx0BundleIndex.setDescription('A unique identifier for a ds0Bundle.  This is not\n               the same value as ifIndex.  This table is not\n               indexed by ifIndex because the manager has to\n               choose the index in a createable row and the agent\n               must be allowed to select ifIndex values.')
dsx0BundleIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 82, 3, 1, 2), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx0BundleIfIndex.setDescription('The ifIndex value the agent selected for the\n               (new) ds0Bundle interface.')
dsx0BundleCircuitIdentifier = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 82, 3, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dsx0BundleCircuitIdentifier.setDescription("This variable contains the transmission vendor's\n               circuit identifier, for the purpose of\n               facilitating troubleshooting.")
dsx0BundleRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 82, 3, 1, 4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dsx0BundleRowStatus.setDescription('This object is used to create and delete rows in\n               this table.')
dsx0BondingTable = MibTable((1, 3, 6, 1, 2, 1, 10, 82, 1))
if mibBuilder.loadTexts:
    dsx0BondingTable.setDescription('The DS0 Bonding table.')
dsx0BondingEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 82, 1, 1)).setIndexNames((0,
                                                                                'IF-MIB',
                                                                                'ifIndex'))
if mibBuilder.loadTexts:
    dsx0BondingEntry.setDescription('An entry in the DS0 Bonding table.  There is a\n               row in this table for each DS0Bundle interface.')
dsx0BondMode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 82, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                             1), ('other',
                                                                                                                                                                                                  2), ('mode0',
                                                                                                                                                                                                       3), ('mode1',
                                                                                                                                                                                                            4), ('mode2',
                                                                                                                                                                                                                 5), ('mode3',
                                                                                                                                                                                                                      6)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dsx0BondMode.setDescription('This object indicates which BONDing mode is used,\n               if any, for a ds0Bundle.  Mode0 provides parameter\n               and number exchange with no synchronization.  Mode\n               1 provides parameter and number exchange.  Mode 1\n               also provides synchronization during\n               initialization but does not include inband\n               monitoring.  Mode 2 provides all of the above plus\n               inband monitoring.  Mode 2 also steals 1/64th of\n               the bandwidth of each channel (thus not supporting\n               n x 56/64 kbit/s data channels for most values of\n               n). Mode 3 provides all of the above, but also\n               provides n x 56/64 kbit/s data channels.  Most\n               common implementations of Mode 3 add an extra\n               channel to support the inband monitoring overhead.\n               ModeNone should be used when the interface is not\n               performing bandwidth-on-demand.')
dsx0BondStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 82, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('idle',
                                                                                                                                                                                      1), ('callSetup',
                                                                                                                                                                                           2), ('dataTransfer',
                                                                                                                                                                                                3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dsx0BondStatus.setDescription('This object indicates the current status of the\n               bonding call using this ds0Bundle. idle(1) should\n               be used when the bonding mode is set to none(1).')
dsx0BondRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 82, 1, 1, 3), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    dsx0BondRowStatus.setDescription('This object is used to create new rows in this\n               table, modify existing rows, and to delete\n               existing rows.')
ds0BundleConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 82, 4))
ds0BundleGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 82, 4, 1))
ds0BundleCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 82, 4, 2))
ds0BundleCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 82, 4, 2, 1)).setObjects(*(('DS0BUNDLE-MIB', 'ds0BundleConfigGroup'), ('DS0BUNDLE-MIB', 'ds0BondingGroup')))
if mibBuilder.loadTexts:
    ds0BundleCompliance.setDescription('The compliance statement for DS0Bundle\n               interfaces.')
ds0BondingGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 82, 4, 1, 1)).setObjects(*(('DS0BUNDLE-MIB', 'dsx0BondMode'), ('DS0BUNDLE-MIB', 'dsx0BondStatus'), ('DS0BUNDLE-MIB', 'dsx0BondRowStatus')))
if mibBuilder.loadTexts:
    ds0BondingGroup.setDescription('A collection of objects providing\n                           configuration information applicable\n                           to all DS0 interfaces.')
ds0BundleConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 82, 4, 1, 2)).setObjects(*(('DS0BUNDLE-MIB', 'dsx0BundleNextIndex'), ('DS0BUNDLE-MIB', 'dsx0BundleIfIndex'), ('DS0BUNDLE-MIB', 'dsx0BundleCircuitIdentifier'), ('DS0BUNDLE-MIB', 'dsx0BundleRowStatus')))
if mibBuilder.loadTexts:
    ds0BundleConfigGroup.setDescription('A collection of objects providing the ability to\n               create a new ds0Bundle in the ifTable as well as\n               configuration information about the ds0Bundle.')
mibBuilder.exportSymbols('DS0BUNDLE-MIB', dsx0BundleRowStatus=dsx0BundleRowStatus, dsx0BondingEntry=dsx0BondingEntry, ds0BundleCompliance=ds0BundleCompliance, dsx0BondRowStatus=dsx0BondRowStatus, PYSNMP_MODULE_ID=ds0Bundle, dsx0BundleNextIndex=dsx0BundleNextIndex, dsx0BondingTable=dsx0BondingTable, ds0BundleConformance=ds0BundleConformance, ds0BundleCompliances=ds0BundleCompliances, ds0BondingGroup=ds0BondingGroup, dsx0BundleIfIndex=dsx0BundleIfIndex, dsx0BundleEntry=dsx0BundleEntry, dsx0BundleCircuitIdentifier=dsx0BundleCircuitIdentifier, dsx0BondStatus=dsx0BondStatus, ds0BundleConfigGroup=ds0BundleConfigGroup, ds0Bundle=ds0Bundle, dsx0BondMode=dsx0BondMode, dsx0BundleIndex=dsx0BundleIndex, ds0BundleGroups=ds0BundleGroups, dsx0BundleTable=dsx0BundleTable)