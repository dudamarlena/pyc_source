# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/PYSNMP-USM-MIB.py
# Compiled at: 2019-08-18 17:24:05
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ConstraintsUnion')
(pysnmpModuleIDs,) = mibBuilder.importSymbols('PYSNMP-MIB', 'pysnmpModuleIDs')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(usmUserEntry,) = mibBuilder.importSymbols('SNMP-USER-BASED-SM-MIB', 'usmUserEntry')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(ModuleIdentity, iso, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, NotificationType, IpAddress, MibIdentifier, Unsigned32, Counter32, ObjectIdentity, Counter64, Bits, Integer32, TimeTicks) = mibBuilder.importSymbols('SNMPv2-SMI', 'ModuleIdentity', 'iso', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'NotificationType', 'IpAddress', 'MibIdentifier', 'Unsigned32', 'Counter32', 'ObjectIdentity', 'Counter64', 'Bits', 'Integer32', 'TimeTicks')
(RowStatus, DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'RowStatus', 'DisplayString', 'TextualConvention')
pysnmpUsmMIB = ModuleIdentity((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1))
if mibBuilder.loadTexts:
    pysnmpUsmMIB.setRevisions(('2017-04-14 00:00', '2005-05-14 00:00'))
if mibBuilder.loadTexts:
    pysnmpUsmMIB.setLastUpdated('201704140000Z')
if mibBuilder.loadTexts:
    pysnmpUsmMIB.setOrganization('The PySNMP Project')
if mibBuilder.loadTexts:
    pysnmpUsmMIB.setContactInfo('E-mail: Ilya Etingof <etingof@gmail.com> GitHub: https://github.com/etingof/pysnmp')
if mibBuilder.loadTexts:
    pysnmpUsmMIB.setDescription('This MIB module defines objects specific to User Security Model (USM) implementation at PySNMP.')
pysnmpUsmMIBObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1))
pysnmpUsmMIBConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 2))
pysnmpUsmCfg = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 1))
pysnmpUsmDiscoverable = MibScalar((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1))).clone(namedValues=NamedValues(('notDiscoverable',
                                                                                                                                                                                             0), ('discoverable',
                                                                                                                                                                                                  1))).clone('discoverable')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pysnmpUsmDiscoverable.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmDiscoverable.setDescription('Whether SNMP engine would support its discovery by responding to unknown clients.')
pysnmpUsmDiscovery = MibScalar((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1))).clone(namedValues=NamedValues(('doNotDiscover',
                                                                                                                                                                                          0), ('doDiscover',
                                                                                                                                                                                               1))).clone('doDiscover')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pysnmpUsmDiscovery.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmDiscovery.setDescription('Whether SNMP engine would try to figure out the EngineIDs of its peers by sending discover requests.')
pysnmpUsmKeyType = MibScalar((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2))).clone(namedValues=NamedValues(('passphrase',
                                                                                                                                                                                           0), ('master',
                                                                                                                                                                                                1), ('localized',
                                                                                                                                                                                                     2))).clone('passphrase')).setMaxAccess('not-accessible')
if mibBuilder.loadTexts:
    pysnmpUsmKeyType.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmKeyType.setDescription('When configuring USM user, the value of this enumeration determines how the keys should be treated. The default value "passphrase" means that given keys are plain-text pass-phrases, "master" indicates that the keys are pre-hashed pass-phrases, while "localized" stands for pre-hashed pass-phrases mixed with SNMP Security Engine ID value.')
pysnmpUsmUser = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 3))
pysnmpUsmSecretTable = MibTable((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 2))
if mibBuilder.loadTexts:
    pysnmpUsmSecretTable.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmSecretTable.setDescription("The table of USM users passphrases configured in the SNMP engine's Local Configuration Datastore (LCD).")
pysnmpUsmSecretEntry = MibTableRow((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 2, 1)).setIndexNames((1,
                                                                                               'PYSNMP-USM-MIB',
                                                                                               'pysnmpUsmSecretUserName'))
if mibBuilder.loadTexts:
    pysnmpUsmSecretEntry.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmSecretEntry.setDescription('Information about a particular USM user credentials.')
pysnmpUsmSecretUserName = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 2, 1,
                                          1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    pysnmpUsmSecretUserName.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmSecretUserName.setDescription('The username string for which a row in this table represents a configuration.')
pysnmpUsmSecretAuthKey = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 2, 1,
                                         2), OctetString('\x00\x00\x00\x00\x00\x00\x00\x00').subtype(subtypeSpec=ValueSizeConstraint(8, 65535)))
if mibBuilder.loadTexts:
    pysnmpUsmSecretAuthKey.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmSecretAuthKey.setDescription("User's authentication passphrase used for localized key generation.")
pysnmpUsmSecretPrivKey = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 2, 1,
                                         3), OctetString('\x00\x00\x00\x00\x00\x00\x00\x00').subtype(subtypeSpec=ValueSizeConstraint(8, 65535)))
if mibBuilder.loadTexts:
    pysnmpUsmSecretPrivKey.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmSecretPrivKey.setDescription("User's encryption passphrase used for localized key generation.")
pysnmpUsmSecretStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 2, 1,
                                        4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pysnmpUsmSecretStatus.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmSecretStatus.setDescription('Table status')
pysnmpUsmKeyTable = MibTable((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 3))
if mibBuilder.loadTexts:
    pysnmpUsmKeyTable.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmKeyTable.setDescription("The table of USM users localized keys configured in the SNMP engine's Local Configuration Datastore (LCD).")
pysnmpUsmKeyEntry = MibTableRow((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 3, 1))
usmUserEntry.registerAugmentions(('PYSNMP-USM-MIB', 'pysnmpUsmKeyEntry'))
pysnmpUsmKeyEntry.setIndexNames(*usmUserEntry.getIndexNames())
if mibBuilder.loadTexts:
    pysnmpUsmKeyEntry.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmKeyEntry.setDescription('Information about a particular USM user credentials.')
pysnmpUsmKeyAuthLocalized = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 3,
                                            1, 1), OctetString('\x00\x00\x00\x00\x00\x00\x00\x00').subtype(subtypeSpec=ValueSizeConstraint(8, 64)))
if mibBuilder.loadTexts:
    pysnmpUsmKeyAuthLocalized.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmKeyAuthLocalized.setDescription("User's localized key used for authentication.")
pysnmpUsmKeyPrivLocalized = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 3,
                                            1, 2), OctetString('\x00\x00\x00\x00\x00\x00\x00\x00').subtype(subtypeSpec=ValueSizeConstraint(8, 64)))
if mibBuilder.loadTexts:
    pysnmpUsmKeyPrivLocalized.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmKeyPrivLocalized.setDescription("User's localized key used for encryption.")
pysnmpUsmKeyAuth = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 3, 1, 3), OctetString('\x00\x00\x00\x00\x00\x00\x00\x00').subtype(subtypeSpec=ValueSizeConstraint(8, 64)))
if mibBuilder.loadTexts:
    pysnmpUsmKeyAuth.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmKeyAuth.setDescription("User's non-localized key used for authentication.")
pysnmpUsmKeyPriv = MibTableColumn((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 1, 3, 1, 4), OctetString('\x00\x00\x00\x00\x00\x00\x00\x00').subtype(subtypeSpec=ValueSizeConstraint(8, 64)))
if mibBuilder.loadTexts:
    pysnmpUsmKeyPriv.setStatus('current')
if mibBuilder.loadTexts:
    pysnmpUsmKeyPriv.setDescription("User's non-localized key used for encryption.")
pysnmpUsmMIBCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 2, 1))
pysnmpUsmMIBGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 20408, 3, 1, 1, 2, 2))
mibBuilder.exportSymbols('PYSNMP-USM-MIB', pysnmpUsmCfg=pysnmpUsmCfg, pysnmpUsmDiscoverable=pysnmpUsmDiscoverable, pysnmpUsmKeyType=pysnmpUsmKeyType, pysnmpUsmKeyEntry=pysnmpUsmKeyEntry, pysnmpUsmKeyTable=pysnmpUsmKeyTable, pysnmpUsmKeyPrivLocalized=pysnmpUsmKeyPrivLocalized, pysnmpUsmMIBCompliances=pysnmpUsmMIBCompliances, pysnmpUsmMIBObjects=pysnmpUsmMIBObjects, pysnmpUsmSecretTable=pysnmpUsmSecretTable, PYSNMP_MODULE_ID=pysnmpUsmMIB, pysnmpUsmSecretEntry=pysnmpUsmSecretEntry, pysnmpUsmMIBConformance=pysnmpUsmMIBConformance, pysnmpUsmUser=pysnmpUsmUser, pysnmpUsmKeyAuth=pysnmpUsmKeyAuth, pysnmpUsmSecretPrivKey=pysnmpUsmSecretPrivKey, pysnmpUsmKeyAuthLocalized=pysnmpUsmKeyAuthLocalized, pysnmpUsmMIB=pysnmpUsmMIB, pysnmpUsmDiscovery=pysnmpUsmDiscovery, pysnmpUsmSecretUserName=pysnmpUsmSecretUserName, pysnmpUsmKeyPriv=pysnmpUsmKeyPriv, pysnmpUsmSecretAuthKey=pysnmpUsmSecretAuthKey, pysnmpUsmSecretStatus=pysnmpUsmSecretStatus, pysnmpUsmMIBGroups=pysnmpUsmMIBGroups)