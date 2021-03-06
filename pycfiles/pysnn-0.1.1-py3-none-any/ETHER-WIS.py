# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/ETHER-WIS.py
# Compiled at: 2016-02-13 18:12:12
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsUnion, ValueSizeConstraint, ConstraintsIntersection, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueSizeConstraint', 'ConstraintsIntersection', 'ValueRangeConstraint')
(ifIndex,) = mibBuilder.importSymbols('IF-MIB', 'ifIndex')
(ObjectGroup, ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'ModuleCompliance', 'NotificationGroup')
(Integer32, ModuleIdentity, Gauge32, Unsigned32, Bits, NotificationType, iso, transmission, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, MibIdentifier, IpAddress, Counter32, ObjectIdentity, TimeTicks) = mibBuilder.importSymbols('SNMPv2-SMI', 'Integer32', 'ModuleIdentity', 'Gauge32', 'Unsigned32', 'Bits', 'NotificationType', 'iso', 'transmission', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64', 'MibIdentifier', 'IpAddress', 'Counter32', 'ObjectIdentity', 'TimeTicks')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
(sonetPathStuff2, sonetMediumLineType, sonetMediumType, sonetFarEndPathStuff2, sonetMediumLoopbackConfig, sonetSectionStuff2, sonetMediumLineCoding, sonetMediumCircuitIdentifier, sonetSESthresholdSet, sonetFarEndLineStuff2, sonetPathCurrentWidth, sonetLineStuff2, sonetMediumStuff2) = mibBuilder.importSymbols('SONET-MIB', 'sonetPathStuff2', 'sonetMediumLineType', 'sonetMediumType', 'sonetFarEndPathStuff2', 'sonetMediumLoopbackConfig', 'sonetSectionStuff2', 'sonetMediumLineCoding', 'sonetMediumCircuitIdentifier', 'sonetSESthresholdSet', 'sonetFarEndLineStuff2', 'sonetPathCurrentWidth', 'sonetLineStuff2', 'sonetMediumStuff2')
etherWisMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 134)).setRevisions(('2003-09-19 00:00', ))
if mibBuilder.loadTexts:
    etherWisMIB.setLastUpdated('200309190000Z')
if mibBuilder.loadTexts:
    etherWisMIB.setOrganization('IETF Ethernet Interfaces and Hub MIB\n                        Working Group')
if mibBuilder.loadTexts:
    etherWisMIB.setContactInfo('WG charter:\n                 http://www.ietf.org/html.charters/hubmib-charter.html\n\n               Mailing Lists:\n                 General Discussion: hubmib@ietf.org\n                 To Subscribe: hubmib-request@ietf.org\n                 In Body: subscribe your_email_address\n\n                Chair: Dan Romascanu\n               Postal: Avaya Inc.\n                       Atidim Technology Park, Bldg. 3\n                       Tel Aviv 61131\n                       Israel\n                  Tel: +972 3 645 8414\n               E-mail: dromasca@avaya.com\n\n               Editor: C. M. Heard\n               Postal: 600 Rainbow Dr. #141\n                       Mountain View, CA 94041-2542\n                       USA\n                  Tel: +1 650-964-8391\n               E-mail: heard@pobox.com')
if mibBuilder.loadTexts:
    etherWisMIB.setDescription("The objects in this MIB module are used in conjunction\n         with objects in the SONET-MIB and the MAU-MIB to manage\n         the Ethernet WAN Interface Sublayer (WIS).\n\n         The following reference is used throughout this MIB module:\n\n         [IEEE 802.3 Std] refers to:\n            IEEE Std 802.3, 2000 Edition: 'IEEE Standard for\n            Information technology - Telecommunications and\n            information exchange between systems - Local and\n            metropolitan area networks - Specific requirements -\n            Part 3: Carrier sense multiple access with collision\n            detection (CSMA/CD) access method and physical layer\n            specifications', as amended by IEEE Std 802.3ae-2002,\n            'IEEE Standard for Carrier Sense Multiple Access with\n            Collision Detection (CSMA/CD) Access Method and\n            Physical Layer Specifications - Media Access Control\n            (MAC) Parameters, Physical Layer and Management\n            Parameters for 10 Gb/s Operation', 30 August 2002.\n\n         Of particular interest are Clause 50, 'WAN Interface\n         Sublayer (WIS), type 10GBASE-W', Clause 30, '10Mb/s,\n         100Mb/s, 1000Mb/s, and 10Gb/s MAC Control, and Link\n         Aggregation Management', and Clause 45, 'Management\n         Data Input/Output (MDIO) Interface'.\n\n         Copyright (C) The Internet Society (2003).  This version\n         of this MIB module is part of RFC 3637;  see the RFC\n         itself for full legal notices.")
etherWisObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 1))
etherWisObjectsPath = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 2))
etherWisConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 3))
etherWisDevice = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 1, 1))
etherWisSection = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 1, 2))
etherWisPath = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 2, 1))
etherWisFarEndPath = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 2, 2))
etherWisDeviceTable = MibTable((1, 3, 6, 1, 2, 1, 10, 134, 1, 1, 1))
if mibBuilder.loadTexts:
    etherWisDeviceTable.setDescription('The table for Ethernet WIS devices')
etherWisDeviceEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 134, 1, 1, 1, 1)).setIndexNames((0,
                                                                                          'IF-MIB',
                                                                                          'ifIndex'))
if mibBuilder.loadTexts:
    etherWisDeviceEntry.setDescription('An entry in the Ethernet WIS device table.  For each\n          instance of this object there MUST be a corresponding\n          instance of sonetMediumEntry.')
etherWisDeviceTxTestPatternMode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 1, 1,
                                                  1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                                1), ('squareWave',
                                                                                                                                                                                     2), ('prbs31',
                                                                                                                                                                                          3), ('mixedFrequency',
                                                                                                                                                                                               4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    etherWisDeviceTxTestPatternMode.setDescription('This variable controls the transmit test pattern mode.\n          The value none(1) puts the the WIS transmit path into\n          the normal operating mode.  The value squareWave(2) puts\n          the WIS transmit path into the square wave test pattern\n          mode described in [IEEE 802.3 Std.] subclause 50.3.8.1.\n          The value prbs31(3) puts the WIS transmit path into the\n          PRBS31 test pattern mode described in [IEEE 802.3 Std.]\n          subclause 50.3.8.2.  The value mixedFrequency(4) puts the\n          WIS transmit path into the mixed frequency test pattern\n          mode described in [IEEE 802.3 Std.] subclause 50.3.8.3.\n          Any attempt to set this object to a value other than\n          none(1) when the corresponding instance of ifAdminStatus\n          has the value up(1) MUST be rejected with the error\n          inconsistentValue, and any attempt to set the corresponding\n          instance of ifAdminStatus to the value up(1) when an\n          instance of this object has a value other than none(1)\n          MUST be rejected with the error inconsistentValue.')
etherWisDeviceRxTestPatternMode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 1, 1,
                                                  1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 3, 4))).clone(namedValues=NamedValues(('none',
                                                                                                                                                                             1), ('prbs31',
                                                                                                                                                                                  3), ('mixedFrequency',
                                                                                                                                                                                       4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    etherWisDeviceRxTestPatternMode.setDescription('This variable controls the receive test pattern mode.\n          The value none(1) puts the the WIS receive path into the\n          normal operating mode.  The value prbs31(3) puts the WIS\n          receive path into the PRBS31 test pattern mode described\n          in [IEEE 802.3 Std.] subclause 50.3.8.2.  The value\n          mixedFrequency(4) puts the WIS receive path into the mixed\n          frequency test pattern mode described in [IEEE 802.3 Std.]\n          subclause 50.3.8.3.  Any attempt to set this object to a\n          value other than none(1) when the corresponding instance\n          of ifAdminStatus has the value up(1) MUST be rejected with\n          the error inconsistentValue, and any attempt to set the\n          corresponding instance of ifAdminStatus to the value up(1)\n          when an instance of this object has a value other than\n          none(1) MUST be rejected with the error inconsistentValue.')
etherWisDeviceRxTestPatternErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 1, 1,
                                                    1, 1, 3), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    etherWisDeviceRxTestPatternErrors.setDescription('This object counts the number of errors detected when the\n          WIS receive path is operating in the PRBS31 test pattern\n          mode.  It is reset to zero when the WIS receive path\n          initially enters that mode, and it increments each time\n          the PRBS pattern checker detects an error as described in\n          [IEEE 802.3 Std.] subclause 50.3.8.2 unless its value is\n          65535, in which case it remains unchanged.  This object is\n          writeable so that it may be reset upon explicit request\n          of a command generator application while the WIS receive\n          path continues to operate in PRBS31 test pattern mode.')
etherWisSectionCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 134, 1, 2, 1))
if mibBuilder.loadTexts:
    etherWisSectionCurrentTable.setDescription('The table for the current state of Ethernet WIS sections.')
etherWisSectionCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 134, 1, 2, 1, 1)).setIndexNames((0,
                                                                                                  'IF-MIB',
                                                                                                  'ifIndex'))
if mibBuilder.loadTexts:
    etherWisSectionCurrentEntry.setDescription('An entry in the etherWisSectionCurrentTable.  For each\n          instance of this object there MUST be a corresponding\n          instance of sonetSectionCurrentEntry.')
etherWisSectionCurrentJ0Transmitted = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 1,
                                                      2, 1, 1, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(16, 16)).setFixedLength(16)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    etherWisSectionCurrentJ0Transmitted.setDescription("This is the 16-octet section trace message that\n          is transmitted in the J0 byte.  The value SHOULD\n          be '89'h followed by fifteen octets of '00'h\n          (or some cyclic shift thereof) when the section\n          trace function is not used, and the implementation\n          SHOULD use that value (or a cyclic shift thereof)\n          as a default if no other value has been set.")
etherWisSectionCurrentJ0Received = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 1, 2,
                                                   1, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(16, 16)).setFixedLength(16)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherWisSectionCurrentJ0Received.setDescription('This is the 16-octet section trace message that\n          was most recently received in the J0 byte.')
etherWisPathCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 134, 2, 1, 1))
if mibBuilder.loadTexts:
    etherWisPathCurrentTable.setDescription('The table for the current state of Ethernet WIS paths.')
etherWisPathCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 134, 2, 1, 1, 1)).setIndexNames((0,
                                                                                               'IF-MIB',
                                                                                               'ifIndex'))
if mibBuilder.loadTexts:
    etherWisPathCurrentEntry.setDescription('An entry in the etherWisPathCurrentTable.  For each\n          instance of this object there MUST be a corresponding\n          instance of sonetPathCurrentEntry.')
etherWisPathCurrentStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 2, 1, 1, 1,
                                            1), Bits().clone(namedValues=NamedValues(('etherWisPathLOP',
                                                                                      0), ('etherWisPathAIS',
                                                                                           1), ('etherWisPathPLM',
                                                                                                2), ('etherWisPathLCD',
                                                                                                     3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherWisPathCurrentStatus.setDescription('This variable indicates the current status of the\n          path payload with a bit map that can indicate multiple\n          defects at once.  The bit positions are assigned as\n          follows:\n\n          etherWisPathLOP(0)\n             This bit is set to indicate that an\n             LOP-P (Loss of Pointer - Path) defect\n             is being experienced.  Note:  when this\n             bit is set, sonetPathSTSLOP MUST be set\n             in the corresponding instance of\n             sonetPathCurrentStatus.\n\n          etherWisPathAIS(1)\n             This bit is set to indicate that an\n             AIS-P (Alarm Indication Signal - Path)\n             defect is being experienced.  Note:  when\n             this bit is set, sonetPathSTSAIS MUST be\n             set in the corresponding instance of\n             sonetPathCurrentStatus.\n\n          etherWisPathPLM(1)\n             This bit is set to indicate that a\n             PLM-P (Payload Label Mismatch - Path)\n             defect is being experienced.  Note:  when\n             this bit is set, sonetPathSignalLabelMismatch\n             MUST be set in the corresponding instance of\n             sonetPathCurrentStatus.\n\n          etherWisPathLCD(3)\n             This bit is set to indicate that an\n             LCD-P (Loss of Codegroup Delination - Path)\n             defect is being experienced.  Since this\n             defect is detected by the PCS and not by\n             the path layer itself, there is no\n             corresponding bit in sonetPathCurrentStatus.')
etherWisPathCurrentJ1Transmitted = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 2, 1,
                                                   1, 1, 2), OctetString().subtype(subtypeSpec=ValueSizeConstraint(16, 16)).setFixedLength(16)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    etherWisPathCurrentJ1Transmitted.setDescription("This is the 16-octet path trace message that\n          is transmitted in the J1 byte.  The value SHOULD\n          be '89'h followed by fifteen octets of '00'h\n          (or some cyclic shift thereof) when the path\n          trace function is not used, and the implementation\n          SHOULD use that value (or a cyclic shift thereof)\n          as a default if no other value has been set.")
etherWisPathCurrentJ1Received = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 2, 1, 1,
                                                1, 3), OctetString().subtype(subtypeSpec=ValueSizeConstraint(16, 16)).setFixedLength(16)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherWisPathCurrentJ1Received.setDescription('This is the 16-octet path trace message that\n          was most recently received in the J1 byte.')
etherWisFarEndPathCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 134, 2, 2, 1))
if mibBuilder.loadTexts:
    etherWisFarEndPathCurrentTable.setDescription('The table for the current far-end state of Ethernet WIS\n          paths.')
etherWisFarEndPathCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 134, 2, 2, 1, 1)).setIndexNames((0,
                                                                                                     'IF-MIB',
                                                                                                     'ifIndex'))
if mibBuilder.loadTexts:
    etherWisFarEndPathCurrentEntry.setDescription('An entry in the etherWisFarEndPathCurrentTable.  For each\n          instance of this object there MUST be a corresponding\n          instance of sonetFarEndPathCurrentEntry.')
etherWisFarEndPathCurrentStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 134, 2, 2,
                                                  1, 1, 1), Bits().clone(namedValues=NamedValues(('etherWisFarEndPayloadDefect',
                                                                                                  0), ('etherWisFarEndServerDefect',
                                                                                                       1)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    etherWisFarEndPathCurrentStatus.setDescription('This variable indicates the current status at the\n          far end of the path using a bit map that can indicate\n          multiple defects at once.  The bit positions are\n          assigned as follows:\n\n          etherWisFarEndPayloadDefect(0)\n             A far end payload defect (i.e., far end\n             PLM-P or LCD-P) is currently being signaled\n             in G1 bits 5-7.\n\n          etherWisFarEndServerDefect(1)\n             A far end server defect (i.e., far end\n             LOP-P or AIS-P) is currently being signaled\n             in G1 bits 5-7.  Note:  when this bit is set,\n             sonetPathSTSRDI MUST be set in the corresponding\n             instance of sonetPathCurrentStatus.')
etherWisGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 3, 1))
etherWisCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 134, 3, 2))
etherWisDeviceGroupBasic = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 134, 3, 1, 1)).setObjects(*(('ETHER-WIS', 'etherWisDeviceTxTestPatternMode'), ('ETHER-WIS', 'etherWisDeviceRxTestPatternMode')))
if mibBuilder.loadTexts:
    etherWisDeviceGroupBasic.setDescription('A collection of objects that support test\n          features required of all WIS devices.')
etherWisDeviceGroupExtra = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 134, 3, 1, 2)).setObjects(*(('ETHER-WIS', 'etherWisDeviceRxTestPatternErrors'), ))
if mibBuilder.loadTexts:
    etherWisDeviceGroupExtra.setDescription('A collection of objects that support\n          optional WIS device test features.')
etherWisSectionGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 134, 3, 1, 3)).setObjects(*(('ETHER-WIS', 'etherWisSectionCurrentJ0Transmitted'), ('ETHER-WIS', 'etherWisSectionCurrentJ0Received')))
if mibBuilder.loadTexts:
    etherWisSectionGroup.setDescription('A collection of objects that provide\n          required information about a WIS section.')
etherWisPathGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 134, 3, 1, 4)).setObjects(*(('ETHER-WIS', 'etherWisPathCurrentStatus'), ('ETHER-WIS', 'etherWisPathCurrentJ1Transmitted'), ('ETHER-WIS', 'etherWisPathCurrentJ1Received')))
if mibBuilder.loadTexts:
    etherWisPathGroup.setDescription('A collection of objects that provide\n          required information about a WIS path.')
etherWisFarEndPathGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 134, 3, 1, 5)).setObjects(*(('ETHER-WIS', 'etherWisFarEndPathCurrentStatus'), ))
if mibBuilder.loadTexts:
    etherWisFarEndPathGroup.setDescription('A collection of objects that provide required\n          information about the far end of a WIS path.')
etherWisCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 134, 3, 2, 1)).setObjects(*(('ETHER-WIS', 'etherWisDeviceGroupBasic'), ('ETHER-WIS', 'etherWisSectionGroup'), ('ETHER-WIS', 'etherWisPathGroup'), ('ETHER-WIS', 'etherWisFarEndPathGroup'), ('SONET-MIB', 'sonetMediumStuff2'), ('SONET-MIB', 'sonetSectionStuff2'), ('SONET-MIB', 'sonetLineStuff2'), ('SONET-MIB', 'sonetFarEndLineStuff2'), ('SONET-MIB', 'sonetPathStuff2'), ('SONET-MIB', 'sonetFarEndPathStuff2')))
if mibBuilder.loadTexts:
    etherWisCompliance.setDescription('The compliance statement for interfaces that include\n          the Ethernet WIS.  Compliance with the following\n          external compliance statements is prerequisite:\n\n          MIB Module             Compliance Statement\n          ----------             --------------------\n          IF-MIB                 ifCompliance3\n          IF-INVERTED-STACK-MIB  ifInvCompliance\n          EtherLike-MIB          dot3Compliance2\n          MAU-MIB                mauModIfCompl3')
mibBuilder.exportSymbols('ETHER-WIS', etherWisDeviceGroupExtra=etherWisDeviceGroupExtra, etherWisPath=etherWisPath, etherWisDeviceTxTestPatternMode=etherWisDeviceTxTestPatternMode, etherWisPathCurrentJ1Received=etherWisPathCurrentJ1Received, etherWisGroups=etherWisGroups, etherWisFarEndPath=etherWisFarEndPath, etherWisConformance=etherWisConformance, etherWisFarEndPathCurrentStatus=etherWisFarEndPathCurrentStatus, etherWisDeviceEntry=etherWisDeviceEntry, PYSNMP_MODULE_ID=etherWisMIB, etherWisFarEndPathCurrentTable=etherWisFarEndPathCurrentTable, etherWisMIB=etherWisMIB, etherWisPathCurrentJ1Transmitted=etherWisPathCurrentJ1Transmitted, etherWisObjects=etherWisObjects, etherWisSectionCurrentJ0Received=etherWisSectionCurrentJ0Received, etherWisPathGroup=etherWisPathGroup, etherWisSection=etherWisSection, etherWisSectionCurrentEntry=etherWisSectionCurrentEntry, etherWisFarEndPathCurrentEntry=etherWisFarEndPathCurrentEntry, etherWisDevice=etherWisDevice, etherWisSectionCurrentTable=etherWisSectionCurrentTable, etherWisDeviceRxTestPatternMode=etherWisDeviceRxTestPatternMode, etherWisDeviceRxTestPatternErrors=etherWisDeviceRxTestPatternErrors, etherWisCompliance=etherWisCompliance, etherWisDeviceGroupBasic=etherWisDeviceGroupBasic, etherWisSectionGroup=etherWisSectionGroup, etherWisFarEndPathGroup=etherWisFarEndPathGroup, etherWisPathCurrentStatus=etherWisPathCurrentStatus, etherWisPathCurrentTable=etherWisPathCurrentTable, etherWisDeviceTable=etherWisDeviceTable, etherWisObjectsPath=etherWisObjectsPath, etherWisSectionCurrentJ0Transmitted=etherWisSectionCurrentJ0Transmitted, etherWisPathCurrentEntry=etherWisPathCurrentEntry, etherWisCompliances=etherWisCompliances)