# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/ETHER-CHIPSET-MIB.py
# Compiled at: 2016-02-13 18:11:58
(ObjectIdentifier, OctetString, Integer) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'OctetString', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection')
(dot3,) = mibBuilder.importSymbols('EtherLike-MIB', 'dot3')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(iso, Counter64, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, IpAddress, mib_2, TimeTicks, ObjectIdentity, Gauge32, Counter32, NotificationType, MibIdentifier, Integer32, Bits) = mibBuilder.importSymbols('SNMPv2-SMI', 'iso', 'Counter64', 'ModuleIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Unsigned32', 'IpAddress', 'mib-2', 'TimeTicks', 'ObjectIdentity', 'Gauge32', 'Counter32', 'NotificationType', 'MibIdentifier', 'Integer32', 'Bits')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
etherChipsetMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 70)).setRevisions(('1999-08-24 04:00', ))
if mibBuilder.loadTexts:
    etherChipsetMIB.setLastUpdated('9908240400Z')
if mibBuilder.loadTexts:
    etherChipsetMIB.setOrganization('IETF 802.3 Hub MIB Working Group')
if mibBuilder.loadTexts:
    etherChipsetMIB.setContactInfo('WG E-mail: hubmib@hprnd.rose.hp.com\n             To subscribe: hubmib-request@hprnd.rose.hp.com\n\n                    Chair: Dan Romascanu\n                   Postal: Lucent Technologies\n                           Atidum Technology Park, Bldg. 3\n                           Tel Aviv 61131\n                           Israel\n                      Tel: +972 3 645 8414\n                   E-mail: dromasca@lucent.com\n\n                  Editor: John Flick\n                  Postal: Hewlett-Packard Company\n                          8000 Foothills Blvd. M/S 5556\n                          Roseville, CA 95747-5556\n                          USA\n\n                     Tel: +1 916 785 4018\n                     Fax: +1 916 785 3583\n                  E-mail: johnf@rose.hp.com')
if mibBuilder.loadTexts:
    etherChipsetMIB.setDescription('This MIB module contains registered values for\n                       use by the dot3StatsEtherChipSet object in\n                       the EtherLike-MIB.  This object is used to\n                       identify the MAC hardware used to communicate\n                       on an interface.\n\n                       Note that the dot3StatsEtherChipSet object\n                       has been deprecated.  The primary purpose of\n                       this module is to capture historic assignments\n                       made by the various IETF working groups that\n                       have been responsible for maintaining the\n                       EtherLike-MIB.  Implementations which support\n                       the dot3StatsEtherChipSet object for backwards\n                       compatability may continue to use these values.\n                       For those chipsets not represented in this\n                       module, registration is required in other\n                       documentation, e.g., assignment within that\n                       part of the registration tree delegated to\n                       individual enterprises (see RFC 1155 and RFC\n                       1902).')
dot3ChipSets = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8))
dot3ChipSetAMD = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 1))
dot3ChipSetAMD7990 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 1))
if mibBuilder.loadTexts:
    dot3ChipSetAMD7990.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am7990 Local Area Network\n                       Controller for Ethernet (LANCE).')
dot3ChipSetAMD79900 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 2))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79900.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79900 chip.')
dot3ChipSetAMD79C940 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 3))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C940.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C940 Media Access Controller\n                       for Ethernet (MACE).')
dot3ChipSetAMD79C90 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 4))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C90.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C90 CMOS Local Area Network\n                       Controller for Ethernet (C-LANCE).')
dot3ChipSetAMD79C960 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 5))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C960.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C960 PCnet-ISA Single Chip\n                       Ethernet Controller for ISA.')
dot3ChipSetAMD79C961 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 6))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C961.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C961 PCnet-ISA+ Single Chip\n                       Plug & Play Full-Duplex Ethernet Controller\n                       for ISA.')
dot3ChipSetAMD79C961A = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 7))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C961A.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C961A PCnet-ISA II Single Chip\n                       Plug & Play Full-Duplex Ethernet Controller\n                       for ISA.')
dot3ChipSetAMD79C965 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 8))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C965.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C965 PCnet-32 Single Chip\n                       Ethernet Controller for PCI.')
dot3ChipSetAMD79C970 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 9))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C970.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C970 PCnet PCI Single Chip\n                       Ethernet Controller for PCI Local Bus.')
dot3ChipSetAMD79C970A = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 10))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C970A.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices AM79C970A PCnet PCI II Single Chip\n                       Full-Duplex Ethernet Controller for PCI Local\n                       Bus.')
dot3ChipSetAMD79C971 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 11))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C971.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C971 PCnet-FAST Single Chip\n                       Full-Duplex 10/100 Mbps Ethernet Controller for\n                       PCI Local Bus.')
dot3ChipSetAMD79C972 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 1, 12))
if mibBuilder.loadTexts:
    dot3ChipSetAMD79C972.setDescription('The authoritative identifier for the Advanced\n                       Micro Devices Am79C972 PCnet-FAST+ Enhanced\n                       10/100 Mbps PCI Ethernet Controller with OnNow\n                       Support.')
dot3ChipSetIntel = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 2))
dot3ChipSetIntel82586 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 2, 1))
if mibBuilder.loadTexts:
    dot3ChipSetIntel82586.setDescription('The authoritative identifier for the Intel\n                       82586 IEEE 802.3 Ethernet LAN Coprocessor.')
dot3ChipSetIntel82596 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 2, 2))
if mibBuilder.loadTexts:
    dot3ChipSetIntel82596.setDescription('The authoritative identifier for the Intel\n                       82596 High-Performance 32-Bit Local Area Network\n                       Coprocessor.')
dot3ChipSetIntel82595 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 2, 3))
if mibBuilder.loadTexts:
    dot3ChipSetIntel82595.setDescription('The authoritative identifier for the Intel\n                       82595 High Integration Ethernet Controller.')
dot3ChipSetIntel82557 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 2, 4))
if mibBuilder.loadTexts:
    dot3ChipSetIntel82557.setDescription('The authoritative identifier for the Intel\n                       82557 Fast Ethernet PCI Bus Lan Controller.')
dot3ChipSetIntel82558 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 2, 5))
if mibBuilder.loadTexts:
    dot3ChipSetIntel82558.setDescription('The authoritative identifier for the Intel\n                       82558 Fast Ethernet PCI Bus LAN Controller with\n                       Integrated PHY.')
dot3ChipSetSeeq = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 3))
dot3ChipSetSeeq8003 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 1))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq8003.setDescription('The authoritative identifier for the SEEQ\n                       8003 chip set.')
dot3ChipSetSeeq80C03 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 2))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq80C03.setDescription('The authoritative identifier for the SEEQ\n                       80C03 Full-Duplex CMOS Ethernet Data Link\n                       Controller (MAC).')
dot3ChipSetSeeq84C30 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 3))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq84C30.setDescription('The authoritative identifier for the SEEQ\n                       4-Port 84C30 Full-Duplex CMOS Ethernet 10\n                       MBit/Sec Data Link Controller (MAC).')
dot3ChipSetSeeq8431 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 4))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq8431.setDescription('The authoritative identifier for the SEEQ\n                       4-Port 8431 Full-Duplex CMOS Ethernet 10\n                       MBit/Sec Data Link Controller (MAC).')
dot3ChipSetSeeq80C300 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 5))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq80C300.setDescription('The authoritative identifier for the SEEQ\n                       80C300 Full-Duplex CMOS Ethernet 10/100\n                       Mbit/Sec Data Link Controller (MAC).')
dot3ChipSetSeeq84C300 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 6))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq84C300.setDescription('The authoritative identifier for the SEEQ\n                       4-Port 84C300 Fast Ethernet Controller (MAC).')
dot3ChipSetSeeq84301 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 7))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq84301.setDescription('The authoritative identifier for the SEEQ\n                       4-Port 84301 Fast Ethernet Controller (MAC).')
dot3ChipSetSeeq84302 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 8))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq84302.setDescription('The authoritative identifier for the SEEQ\n                       4-Port 84302 Fast Ethernet Controller (MAC).')
dot3ChipSetSeeq8100 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 3, 9))
if mibBuilder.loadTexts:
    dot3ChipSetSeeq8100.setDescription('The authoritative identifier for the SEEQ\n                       8100 Gigabit Ethernet Controller (MAC & PCS).')
dot3ChipSetNational = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 4))
dot3ChipSetNational8390 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 1))
if mibBuilder.loadTexts:
    dot3ChipSetNational8390.setDescription('The authoritative identifier for the National\n                       Semiconductor DP8390 Network Interface\n                       Controller.')
dot3ChipSetNationalSonic = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 2))
if mibBuilder.loadTexts:
    dot3ChipSetNationalSonic.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83932 Systems-Oriented Network\n                       Interface Controller (SONIC).')
dot3ChipSetNational83901 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 3))
if mibBuilder.loadTexts:
    dot3ChipSetNational83901.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83901 Serial Network Interface\n                       Controller (SNIC).')
dot3ChipSetNational83902 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 4))
if mibBuilder.loadTexts:
    dot3ChipSetNational83902.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83902 Serial Network Interface\n                       Controller for Twisted Pair (ST-NIC).')
dot3ChipSetNational83905 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 5))
if mibBuilder.loadTexts:
    dot3ChipSetNational83905.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83905 AT Local Area Network\n                       Twisted-Pair Interface (AT/LANTIC).')
dot3ChipSetNational83907 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 6))
if mibBuilder.loadTexts:
    dot3ChipSetNational83907.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83907 AT Twisted-Pair Enhanced\n                       Coaxial Network Interface Controller\n                       (AT/LANTIC II).')
dot3ChipSetNational83916 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 7))
if mibBuilder.loadTexts:
    dot3ChipSetNational83916.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83916 Systems-Oriented Network\n                       Interface Controller (SONIC-16).')
dot3ChipSetNational83934 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 8))
if mibBuilder.loadTexts:
    dot3ChipSetNational83934.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83934 Systems-Oriented Network\n                       Interface Controller with Twisted Pair Interface\n                       (SONIC-T).')
dot3ChipSetNational83936 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 4, 9))
if mibBuilder.loadTexts:
    dot3ChipSetNational83936.setDescription('The authoritative identifier for the National\n                       Semiconductor DP83936AVUL Full-Duplex Systems-\n                       Oriented Network Interface Controller with\n                       Twisted Pair Interface (SONIC-T).')
dot3ChipSetFujitsu = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 5))
dot3ChipSetFujitsu86950 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 5, 1))
if mibBuilder.loadTexts:
    dot3ChipSetFujitsu86950.setDescription('The authoritative identifier for the Fujitsu\n                       86950 chip.')
dot3ChipSetFujitsu86960 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 5, 2))
if mibBuilder.loadTexts:
    dot3ChipSetFujitsu86960.setDescription('The authoritative identifier for the Fujitsu\n                       MB86960 Network Interface Controller with\n                       Encoder/Decoder (NICE).')
dot3ChipSetFujitsu86964 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 5, 3))
if mibBuilder.loadTexts:
    dot3ChipSetFujitsu86964.setDescription('The authoritative identifier for the Fujitsu\n                       MB86964 Ethernet Controller with 10BASE-T\n                       Tranceiver.')
dot3ChipSetFujitsu86965A = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 5, 4))
if mibBuilder.loadTexts:
    dot3ChipSetFujitsu86965A.setDescription('The authoritative identifier for the Fujitsu\n                       MB86965A EtherCoupler Single-Chip Ethernet\n                       Controller.')
dot3ChipSetFujitsu86965B = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 5, 5))
if mibBuilder.loadTexts:
    dot3ChipSetFujitsu86965B.setDescription('The authoritative identifier for the Fujitsu\n                       MB86965B EtherCoupler Single-Chip Ethernet\n                       Controller (supports full-duplex).')
dot3ChipSetDigital = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 6))
dot3ChipSetDigitalDC21040 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 6, 1))
if mibBuilder.loadTexts:
    dot3ChipSetDigitalDC21040.setDescription('The authoritative identifier for the Digital\n                       Semiconductor DC21040 chip.')
dot3ChipSetDigital21041 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 6, 2))
if mibBuilder.loadTexts:
    dot3ChipSetDigital21041.setDescription('The authoritative identifier for the Digital\n                       Semiconductor 21041 PCI Ethernet LAN\n                       Controller.')
dot3ChipSetDigital21140 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 6, 3))
if mibBuilder.loadTexts:
    dot3ChipSetDigital21140.setDescription('The authoritative identifier for the Digital\n                       Semiconductor 21140 PCI Fast Ethernet LAN\n                       Controller.')
dot3ChipSetDigital21143 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 6, 4))
if mibBuilder.loadTexts:
    dot3ChipSetDigital21143.setDescription('The authoritative identifier for the Digital\n                       Semiconductor 21143 PCI/CardBus 10/100-Mb/s\n                       Ethernet LAN Controller.')
dot3ChipSetDigital21340 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 6, 5))
if mibBuilder.loadTexts:
    dot3ChipSetDigital21340.setDescription('The authoritative identifier for the Digital\n                       Semiconductor 21340 10/100-MB/s managed buffered\n                       port switch.')
dot3ChipSetDigital21440 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 6, 6))
if mibBuilder.loadTexts:
    dot3ChipSetDigital21440.setDescription('The authoritative identifier for the Digital\n                       Semiconductor 21440 Multiport 10/100Mbps\n                       Ethernet Controller.')
dot3ChipSetDigital21540 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 6, 7))
if mibBuilder.loadTexts:
    dot3ChipSetDigital21540.setDescription('The authoritative identifier for the Digital\n                       Semiconductor 21540 PCI/CardBus Ethernet LAN\n                       Controller with Modem Interface.')
dot3ChipSetTI = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 7))
dot3ChipSetTIE100 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 7, 1))
if mibBuilder.loadTexts:
    dot3ChipSetTIE100.setDescription('The authoritative identifier for the Texas\n                       Instruments TNETE100 ThunderLAN PCI Fast\n                       Ethernet Controller.')
dot3ChipSetTIE110 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 7, 2))
if mibBuilder.loadTexts:
    dot3ChipSetTIE110.setDescription('The authoritative identifier for the Texas\n                       Instruments TNETE110 ThunderLAN PCI 10BASE-T\n                       Ethernet Adapter.')
dot3ChipSetTIX3100 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 7, 3))
if mibBuilder.loadTexts:
    dot3ChipSetTIX3100.setDescription('The authoritative identifier for the Texas\n                       Instruments TNETX3100 Desktop ThunderSWITCH\n                       8/2.')
dot3ChipSetTIX3150 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 7, 4))
if mibBuilder.loadTexts:
    dot3ChipSetTIX3150.setDescription('The authoritative identifier for the Texas\n                       Instruments TNETX3150 ThunderSWITCH 12/3.')
dot3ChipSetTIX3270 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 7, 5))
if mibBuilder.loadTexts:
    dot3ChipSetTIX3270.setDescription('The authoritative identifier for the Texas\n                       Instruments TNETX3270 ThunderSWITCH 24/3.')
dot3ChipSetToshiba = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 8))
dot3ChipSetToshibaTC35815F = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 8, 1))
if mibBuilder.loadTexts:
    dot3ChipSetToshibaTC35815F.setDescription('The authoritative identifier for the Toshiba\n                       TC35815F PCI-Based 100/10Mbps Ethernet\n                       Controller.')
dot3ChipSetLucent = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 9))
dot3ChipSetLucentATT1MX10 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 9, 1))
if mibBuilder.loadTexts:
    dot3ChipSetLucentATT1MX10.setDescription('The authoritative identifier for the Lucent\n                       Technologies ATT1MX10 (Spinnaker) Quad MAC and\n                       Tranceiver for Ethernet Frame Switching.')
dot3ChipSetLucentLUC3M08 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 9, 2))
if mibBuilder.loadTexts:
    dot3ChipSetLucentLUC3M08.setDescription('The authoritative identifier for the Lucent\n                       Technologies LUC3M08 Eight Ethernet MACs for\n                       10/100 Mbits/s Frame Switching.')
dot3ChipSetGalileo = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 10))
dot3ChipSetGalileoGT48001 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 10, 1))
if mibBuilder.loadTexts:
    dot3ChipSetGalileoGT48001.setDescription('The authoritative identifier for the Galileo\n                       Technology GT-48001A Switched Ethernet\n                       Controller.')
dot3ChipSetGalileoGT48002 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 10, 2))
if mibBuilder.loadTexts:
    dot3ChipSetGalileoGT48002.setDescription('The authoritative identifier for the Galileo\n                       Technology GT-48002A Switched Fast Ethernet\n                       Controller.')
dot3ChipSetGalileoGT48004 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 10, 3))
if mibBuilder.loadTexts:
    dot3ChipSetGalileoGT48004.setDescription('The authoritative identifier for the Galileo\n                       Technology GT-48004A Four Port Fast Ethernet\n                       Switch for Multiport 10/100BASE-X Systems.')
dot3ChipSetGalileoGT48207 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 10, 4))
if mibBuilder.loadTexts:
    dot3ChipSetGalileoGT48207.setDescription('The authoritative identifier for the Galileo\n                       Technology GT-48207 Low-Cost 10 Port Switched\n                       Ethernet Controller for 10+10/100BASE-X.')
dot3ChipSetGalileoGT48208 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 10, 5))
if mibBuilder.loadTexts:
    dot3ChipSetGalileoGT48208.setDescription('The authoritative identifier for the Galileo\n                       Technology GT-48208 Advanced 10 Port Switched\n                       Ethernet Controller for 10+10/100BASE-X.')
dot3ChipSetGalileoGT48212 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 10, 6))
if mibBuilder.loadTexts:
    dot3ChipSetGalileoGT48212.setDescription('The authoritative identifier for the Galileo\n                       Technology GT-48212 Advanced 14 Port Switched\n                       Ethernet Controller for 10+10/100BASE-X.')
dot3ChipSetJato = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 11))
dot3ChipSetJatoJT1001 = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 11, 1))
if mibBuilder.loadTexts:
    dot3ChipSetJatoJT1001.setDescription('The authoritative identifier for the Jato\n                       Technologies JT1001 GigEMAC Server\n                       10/100/1000Mbps Ethernet Controller with PCI\n                       interface.')
dot3ChipSetXaQti = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 7, 8, 12))
dot3ChipSetXaQtiXQ11800FP = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 12, 1))
if mibBuilder.loadTexts:
    dot3ChipSetXaQtiXQ11800FP.setDescription('The authoritative identifier for the XaQTI\n                       XQ11800FP XMAC II Gigabit Ethernet Media Access\n                       Controller.')
dot3ChipSetXaQtiXQ18110FP = ObjectIdentity((1, 3, 6, 1, 2, 1, 10, 7, 8, 12, 2))
if mibBuilder.loadTexts:
    dot3ChipSetXaQtiXQ18110FP.setDescription('The authoritative identifier for the XaQTI\n                       XQ18110FP GigaPower Protocol Accelerator.')
mibBuilder.exportSymbols('ETHER-CHIPSET-MIB', dot3ChipSetNational83902=dot3ChipSetNational83902, dot3ChipSetJato=dot3ChipSetJato, dot3ChipSetAMD=dot3ChipSetAMD, dot3ChipSetIntel82557=dot3ChipSetIntel82557, dot3ChipSetAMD79C970=dot3ChipSetAMD79C970, dot3ChipSetAMD79C940=dot3ChipSetAMD79C940, dot3ChipSetAMD79C960=dot3ChipSetAMD79C960, dot3ChipSetSeeq8100=dot3ChipSetSeeq8100, dot3ChipSetAMD79900=dot3ChipSetAMD79900, dot3ChipSetIntel=dot3ChipSetIntel, dot3ChipSets=dot3ChipSets, dot3ChipSetSeeq84C30=dot3ChipSetSeeq84C30, dot3ChipSetNational83916=dot3ChipSetNational83916, dot3ChipSetFujitsu86965B=dot3ChipSetFujitsu86965B, dot3ChipSetDigital21140=dot3ChipSetDigital21140, dot3ChipSetSeeq=dot3ChipSetSeeq, dot3ChipSetSeeq80C03=dot3ChipSetSeeq80C03, dot3ChipSetTIX3270=dot3ChipSetTIX3270, dot3ChipSetNational=dot3ChipSetNational, dot3ChipSetNational83905=dot3ChipSetNational83905, dot3ChipSetAMD79C971=dot3ChipSetAMD79C971, dot3ChipSetFujitsu86950=dot3ChipSetFujitsu86950, dot3ChipSetDigital21143=dot3ChipSetDigital21143, dot3ChipSetDigital21041=dot3ChipSetDigital21041, dot3ChipSetSeeq84C300=dot3ChipSetSeeq84C300, dot3ChipSetAMD79C961=dot3ChipSetAMD79C961, dot3ChipSetAMD79C972=dot3ChipSetAMD79C972, dot3ChipSetSeeq80C300=dot3ChipSetSeeq80C300, PYSNMP_MODULE_ID=etherChipsetMIB, dot3ChipSetIntel82595=dot3ChipSetIntel82595, dot3ChipSetTIE110=dot3ChipSetTIE110, dot3ChipSetFujitsu86964=dot3ChipSetFujitsu86964, dot3ChipSetLucentATT1MX10=dot3ChipSetLucentATT1MX10, dot3ChipSetAMD79C965=dot3ChipSetAMD79C965, dot3ChipSetNational83901=dot3ChipSetNational83901, dot3ChipSetFujitsu=dot3ChipSetFujitsu, dot3ChipSetNational83934=dot3ChipSetNational83934, dot3ChipSetIntel82596=dot3ChipSetIntel82596, dot3ChipSetIntel82586=dot3ChipSetIntel82586, dot3ChipSetSeeq84302=dot3ChipSetSeeq84302, dot3ChipSetDigital21340=dot3ChipSetDigital21340, dot3ChipSetDigital21440=dot3ChipSetDigital21440, dot3ChipSetSeeq8003=dot3ChipSetSeeq8003, dot3ChipSetTIE100=dot3ChipSetTIE100, dot3ChipSetLucentLUC3M08=dot3ChipSetLucentLUC3M08, dot3ChipSetSeeq8431=dot3ChipSetSeeq8431, dot3ChipSetGalileoGT48208=dot3ChipSetGalileoGT48208, dot3ChipSetGalileoGT48207=dot3ChipSetGalileoGT48207, dot3ChipSetAMD7990=dot3ChipSetAMD7990, dot3ChipSetDigital21540=dot3ChipSetDigital21540, dot3ChipSetDigitalDC21040=dot3ChipSetDigitalDC21040, dot3ChipSetTI=dot3ChipSetTI, dot3ChipSetToshiba=dot3ChipSetToshiba, dot3ChipSetGalileoGT48004=dot3ChipSetGalileoGT48004, dot3ChipSetTIX3100=dot3ChipSetTIX3100, dot3ChipSetXaQti=dot3ChipSetXaQti, dot3ChipSetToshibaTC35815F=dot3ChipSetToshibaTC35815F, dot3ChipSetFujitsu86960=dot3ChipSetFujitsu86960, dot3ChipSetTIX3150=dot3ChipSetTIX3150, dot3ChipSetLucent=dot3ChipSetLucent, dot3ChipSetAMD79C970A=dot3ChipSetAMD79C970A, dot3ChipSetDigital=dot3ChipSetDigital, dot3ChipSetGalileo=dot3ChipSetGalileo, etherChipsetMIB=etherChipsetMIB, dot3ChipSetGalileoGT48002=dot3ChipSetGalileoGT48002, dot3ChipSetAMD79C90=dot3ChipSetAMD79C90, dot3ChipSetNational8390=dot3ChipSetNational8390, dot3ChipSetGalileoGT48212=dot3ChipSetGalileoGT48212, dot3ChipSetNational83936=dot3ChipSetNational83936, dot3ChipSetGalileoGT48001=dot3ChipSetGalileoGT48001, dot3ChipSetXaQtiXQ18110FP=dot3ChipSetXaQtiXQ18110FP, dot3ChipSetAMD79C961A=dot3ChipSetAMD79C961A, dot3ChipSetSeeq84301=dot3ChipSetSeeq84301, dot3ChipSetXaQtiXQ11800FP=dot3ChipSetXaQtiXQ11800FP, dot3ChipSetFujitsu86965A=dot3ChipSetFujitsu86965A, dot3ChipSetNationalSonic=dot3ChipSetNationalSonic, dot3ChipSetIntel82558=dot3ChipSetIntel82558, dot3ChipSetNational83907=dot3ChipSetNational83907, dot3ChipSetJatoJT1001=dot3ChipSetJatoJT1001)