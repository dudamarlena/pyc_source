# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/SNMP-MPD-MIB.py
# Compiled at: 2019-08-18 17:24:05
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsUnion, ValueSizeConstraint, ValueRangeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueSizeConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection')
(NotificationGroup, ModuleCompliance, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance', 'ObjectGroup')
(iso, Counter32, Unsigned32, Gauge32, MibIdentifier, TimeTicks, NotificationType, ObjectIdentity, Bits, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, Integer32, Counter64, IpAddress, snmpModules) = mibBuilder.importSymbols('SNMPv2-SMI', 'iso', 'Counter32', 'Unsigned32', 'Gauge32', 'MibIdentifier', 'TimeTicks', 'NotificationType', 'ObjectIdentity', 'Bits', 'ModuleIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Integer32', 'Counter64', 'IpAddress', 'snmpModules')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
snmpMPDMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 11))
if mibBuilder.loadTexts:
    snmpMPDMIB.setRevisions(('1999-05-04 16:36', '1997-09-30 00:00'))
if mibBuilder.loadTexts:
    snmpMPDMIB.setLastUpdated('9905041636Z')
if mibBuilder.loadTexts:
    snmpMPDMIB.setOrganization('SNMPv3 Working Group')
if mibBuilder.loadTexts:
    snmpMPDMIB.setContactInfo('WG-EMail: snmpv3@lists.tislabs.com Subscribe: majordomo@lists.tislabs.com In message body: subscribe snmpv3 Chair: Russ Mundy TIS Labs at Network Associates postal: 3060 Washington Road Glenwood, MD 21738 USA EMail: mundy@tislabs.com phone: +1 301-854-6889 Co-editor: Jeffrey Case SNMP Research, Inc. postal: 3001 Kimberlin Heights Road Knoxville, TN 37920-9716 USA EMail: case@snmp.com phone: +1 423-573-1434 Co-editor Dave Harrington Cabletron Systems, Inc. postal: Post Office Box 5005 MailStop: Durham 35 Industrial Way Rochester, NH 03867-5005 USA EMail: dbh@ctron.com phone: +1 603-337-7357 Co-editor: Randy Presuhn BMC Software, Inc. postal: 965 Stewart Drive Sunnyvale, CA 94086 USA EMail: randy_presuhn@bmc.com phone: +1 408-616-3100 Co-editor: Bert Wijnen IBM T. J. Watson Research postal: Schagen 33 3461 GL Linschoten Netherlands EMail: wijnen@vnet.ibm.com phone: +31 348-432-794 ')
if mibBuilder.loadTexts:
    snmpMPDMIB.setDescription('The MIB for Message Processing and Dispatching')
snmpMPDAdmin = MibIdentifier((1, 3, 6, 1, 6, 3, 11, 1))
snmpMPDMIBObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 11, 2))
snmpMPDMIBConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 11, 3))
snmpMPDStats = MibIdentifier((1, 3, 6, 1, 6, 3, 11, 2, 1))
snmpUnknownSecurityModels = MibScalar((1, 3, 6, 1, 6, 3, 11, 2, 1, 1), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpUnknownSecurityModels.setStatus('current')
if mibBuilder.loadTexts:
    snmpUnknownSecurityModels.setDescription('The total number of packets received by the SNMP engine which were dropped because they referenced a securityModel that was not known to or supported by the SNMP engine. ')
snmpInvalidMsgs = MibScalar((1, 3, 6, 1, 6, 3, 11, 2, 1, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpInvalidMsgs.setStatus('current')
if mibBuilder.loadTexts:
    snmpInvalidMsgs.setDescription('The total number of packets received by the SNMP engine which were dropped because there were invalid or inconsistent components in the SNMP message. ')
snmpUnknownPDUHandlers = MibScalar((1, 3, 6, 1, 6, 3, 11, 2, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpUnknownPDUHandlers.setStatus('current')
if mibBuilder.loadTexts:
    snmpUnknownPDUHandlers.setDescription('The total number of packets received by the SNMP engine which were dropped because the PDU contained in the packet could not be passed to an application responsible for handling the pduType, e.g. no SNMP application had registered for the proper combination of the contextEngineID and the pduType. ')
snmpMPDMIBCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 11, 3, 1))
snmpMPDMIBGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 11, 3, 2))
snmpMPDCompliance = ModuleCompliance((1, 3, 6, 1, 6, 3, 11, 3, 1, 1)).setObjects(('SNMP-MPD-MIB',
                                                                                  'snmpMPDGroup'))
if mibBuilder.loadTexts:
    snmpMPDCompliance.setDescription('The compliance statement for SNMP entities which implement the SNMP-MPD-MIB. ')
snmpMPDGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 11, 3, 2, 1)).setObjects(('SNMP-MPD-MIB',
                                                                        'snmpUnknownSecurityModels'), ('SNMP-MPD-MIB',
                                                                                                       'snmpInvalidMsgs'), ('SNMP-MPD-MIB',
                                                                                                                            'snmpUnknownPDUHandlers'))
if mibBuilder.loadTexts:
    snmpMPDGroup.setDescription('A collection of objects providing for remote monitoring of the SNMP Message Processing and Dispatching process. ')
mibBuilder.exportSymbols('SNMP-MPD-MIB', snmpMPDMIBGroups=snmpMPDMIBGroups, PYSNMP_MODULE_ID=snmpMPDMIB, snmpMPDMIBConformance=snmpMPDMIBConformance, snmpMPDMIBCompliances=snmpMPDMIBCompliances, snmpUnknownPDUHandlers=snmpUnknownPDUHandlers, snmpMPDGroup=snmpMPDGroup, snmpMPDMIB=snmpMPDMIB, snmpInvalidMsgs=snmpInvalidMsgs, snmpMPDCompliance=snmpMPDCompliance, snmpMPDMIBObjects=snmpMPDMIBObjects, snmpMPDAdmin=snmpMPDAdmin, snmpMPDStats=snmpMPDStats, snmpUnknownSecurityModels=snmpUnknownSecurityModels)