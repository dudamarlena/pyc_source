# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/FC-MGMT-MIB.py
# Compiled at: 2016-02-13 18:12:19
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ValueSizeConstraint, ValueRangeConstraint, ConstraintsIntersection, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ValueSizeConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ConstraintsUnion')
(ifIndex,) = mibBuilder.importSymbols('IF-MIB', 'ifIndex')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(TimeTicks, Counter64, Integer32, iso, Gauge32, IpAddress, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, ModuleIdentity, Bits, transmission, MibIdentifier, NotificationType, Counter32, Unsigned32) = mibBuilder.importSymbols('SNMPv2-SMI', 'TimeTicks', 'Counter64', 'Integer32', 'iso', 'Gauge32', 'IpAddress', 'ObjectIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'ModuleIdentity', 'Bits', 'transmission', 'MibIdentifier', 'NotificationType', 'Counter32', 'Unsigned32')
(DisplayString, TextualConvention, TruthValue) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention', 'TruthValue')
fcMgmtMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 56)).setRevisions(('2005-04-26 00:00', ))
if mibBuilder.loadTexts:
    fcMgmtMIB.setLastUpdated('200504260000Z')
if mibBuilder.loadTexts:
    fcMgmtMIB.setOrganization('IETF IPS (IP-Storage) Working Group')
if mibBuilder.loadTexts:
    fcMgmtMIB.setContactInfo('        Keith McCloghrie\n                        Cisco Systems, Inc.\n                   Tel: +1 408 526-5260\n                E-mail: kzm@cisco.com\n                Postal: 170 West Tasman Drive\n                        San Jose, CA USA 95134\n               ')
if mibBuilder.loadTexts:
    fcMgmtMIB.setDescription('This module defines management information specific to\n               Fibre Channel-attached devices.\n\n\n\n\n               Copyright (C) The Internet Society (2005).  This version\n               of this MIB module is part of RFC 4044;  see the RFC\n               itself for full legal notices.')
fcmgmtObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 56, 1))
fcmgmtNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 56, 2))
fcmgmtNotifPrefix = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 56, 2, 0))
fcmgmtConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 56, 3))

class FcNameIdOrZero(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16))


class FcAddressIdOrZero(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(3, 3))


class FcDomainIdOrZero(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 239)


class FcPortType(Unsigned32, TextualConvention):
    __module__ = __name__


class FcClasses(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('classF', 0), ('class1', 1), ('class2', 2), ('class3',
                                                                            3), ('class4',
                                                                                 4), ('class5',
                                                                                      5), ('class6',
                                                                                           6))


class FcBbCredit(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 32767)


class FcBbCreditModel(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('regular', 1), ('alternate', 2))


class FcDataFieldSize(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(128, 2112)


class FcUnitFunctions(Bits, TextualConvention):
    __module__ = __name__
    namedValues = NamedValues(('other', 0), ('hub', 1), ('switch', 2), ('bridge', 3), ('gateway',
                                                                                       4), ('host',
                                                                                            5), ('storageSubsys',
                                                                                                 6), ('storageAccessDev',
                                                                                                      7), ('nas',
                                                                                                           8), ('wdmux',
                                                                                                                9), ('storageDevice',
                                                                                                                     10))


fcmInstanceTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 1))
if mibBuilder.loadTexts:
    fcmInstanceTable.setDescription('Information about the local Fibre Channel management\n            instances.')
fcmInstanceEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1)).setIndexNames((0,
                                                                                   'FC-MGMT-MIB',
                                                                                   'fcmInstanceIndex'))
if mibBuilder.loadTexts:
    fcmInstanceEntry.setDescription('A list of attributes for a particular local Fibre Channel\n            management instance.')
fcmInstanceIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    fcmInstanceIndex.setDescription('An arbitrary integer value that uniquely identifies this\n            instance amongst all local Fibre Channel management\n            instances.\n\n            It is mandatory to keep this value constant between restarts\n            of the agent, and to make every possible effort to keep it\n            constant across restarts (but note, it is unrealistic to\n            expect it to remain constant across all re-configurations of\n            the local system, e.g., across the replacement of all non-\n            volatile storage).')
fcmInstanceWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 2), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmInstanceWwn.setDescription('If the instance has one (or more) WWN(s), then this object\n            contains that (or one of those) WWN(s).\n\n            If the instance does not have a WWN associated with it, then\n            this object contains the zero-length string.')
fcmInstanceFunctions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 3), FcUnitFunctions()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmInstanceFunctions.setDescription('One (or more) Fibre Channel unit functions being performed\n            by this instance.')
fcmInstancePhysicalIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmInstancePhysicalIndex.setDescription("If this management instance corresponds to a physical\n            component (or to a hierarchy of physical components)\n            identified by the Entity-MIB, then this object's value is\n            the value of the entPhysicalIndex of that component (or of\n            the component at the root of that hierarchy).  If there is\n\n\n\n            no correspondence to a physical component (or no component\n            that has an entPhysicalIndex value), then the value of this\n            object is zero.")
fcmInstanceSoftwareIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmInstanceSoftwareIndex.setDescription("If this management instance corresponds to an installed\n            software module identified in the Host Resources MIB, then\n            this object's value is the value of the hrSWInstalledIndex\n            of that module.  If there is no correspondence to an\n            installed software module (or no module that has a\n            hrSWInstalledIndex value), then the value of this object is\n            zero.")
fcmInstanceStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('unknown',
                                                                                                                                                                                               1), ('ok',
                                                                                                                                                                                                    2), ('warning',
                                                                                                                                                                                                         3), ('failed',
                                                                                                                                                                                                              4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmInstanceStatus.setDescription('Overall status of the Fibre Channel entity/entities managed\n            by this management instance.  The value should reflect the\n            most serious status of such entities.')
fcmInstanceTextName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 7), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 79))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    fcmInstanceTextName.setDescription('A textual name for this management instance and the Fibre\n            Channel entity/entities that it is managing.')
fcmInstanceDescr = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 8), SnmpAdminString()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    fcmInstanceDescr.setDescription('A textual description of this management instance and the\n            Fibre Channel entity/entities that it is managing.')
fcmInstanceFabricId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 1, 1, 9), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmInstanceFabricId.setDescription('The globally unique Fabric Identifier that identifies the\n            fabric to which the Fibre Channel entity/entities managed by\n            this management instance are connected, or, of which they\n            are a part.  This is typically the Node WWN of the principal\n            switch of a Fibre Channel fabric.  The zero-length string\n            indicates that the fabric identifier is unknown (or not\n            applicable).\n\n            In the event that the Fibre Channel entity/entities managed\n            by this management instance is/are connected to multiple\n            fabrics, then this object records the first (known) one.')
fcmSwitchTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 2))
if mibBuilder.loadTexts:
    fcmSwitchTable.setDescription('A table of information about Fibre Channel switches that\n            are managed by Fibre Channel management instances.  Each\n            Fibre Channel management instance can manage one or more\n            Fibre Channel switches.')
fcmSwitchEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 2, 1)).setIndexNames((0,
                                                                                 'FC-MGMT-MIB',
                                                                                 'fcmInstanceIndex'), (0,
                                                                                                       'FC-MGMT-MIB',
                                                                                                       'fcmSwitchIndex'))
if mibBuilder.loadTexts:
    fcmSwitchEntry.setDescription('Information about a particular Fibre Channel switch that is\n\n\n\n            managed by the management instance given by\n            fcmInstanceIndex.')
fcmSwitchIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    fcmSwitchIndex.setDescription('An arbitrary integer that uniquely identifies a Fibre\n            Channel switch amongst those managed by one Fibre Channel\n            management instance.\n\n            It is mandatory to keep this value constant between restarts\n            of the agent, and to make every possible effort to keep it\n            constant across restarts.')
fcmSwitchDomainId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 2, 1, 2), FcDomainIdOrZero()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    fcmSwitchDomainId.setDescription('The Domain Id of this switch.  A value of zero indicates\n            that a switch has not (yet) been assigned a Domain Id.')
fcmSwitchPrincipal = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 2, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmSwitchPrincipal.setDescription('An indication of whether this switch is the principal\n            switch within its fabric.')
fcmSwitchWWN = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 2, 1, 4), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmSwitchWWN.setDescription('The World Wide Name of this switch.')
fcmPortTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 3))
if mibBuilder.loadTexts:
    fcmPortTable.setDescription("Information about Fibre Channel ports.  Each Fibre Channel\n            port is represented by one entry in the IF-MIB's ifTable.")
fcmPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1)).setIndexNames((0, 'IF-MIB',
                                                                               'ifIndex'))
if mibBuilder.loadTexts:
    fcmPortEntry.setDescription('Each entry contains information about a specific port.')
fcmPortInstanceIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortInstanceIndex.setDescription('The value of fcmInstanceIndex by which the Fibre Channel\n            management instance, which manages this port, is identified\n            in the fcmInstanceTable.')
fcmPortWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 2), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortWwn.setDescription('The World Wide Name of the port, or the zero-length string\n            if the port does not have a WWN.')
fcmPortNodeWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 3), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortNodeWwn.setDescription('The World Wide Name of the Node that contains this port, or\n            the zero-length string if the port does not have a node\n            WWN.')
fcmPortAdminType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 4), FcPortType()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    fcmPortAdminType.setDescription('The administratively desired type of this port.')
fcmPortOperType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 5), FcPortType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortOperType.setDescription('The current operational type of this port.')
fcmPortFcCapClass = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 6), FcClasses()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortFcCapClass.setDescription('The classes of service capability of this port.')
fcmPortFcOperClass = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 7), FcClasses()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortFcOperClass.setDescription('The classes of service that are currently operational on\n            this port.  For an FL_Port, this is the union of the classes\n            being supported across all attached NL_Ports.')
fcmPortTransmitterType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('unknown',
                                                                                                                                                                                                          1), ('other',
                                                                                                                                                                                                               2), ('shortwave850nm',
                                                                                                                                                                                                                    3), ('longwave1550nm',
                                                                                                                                                                                                                         4), ('longwave1310nm',
                                                                                                                                                                                                                              5), ('electrical',
                                                                                                                                                                                                                                   6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortTransmitterType.setDescription('The technology of the port transceiver.')
fcmPortConnectorType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9))).clone(namedValues=NamedValues(('unknown',
                                                                                                                                                                                                                 1), ('other',
                                                                                                                                                                                                                      2), ('gbic',
                                                                                                                                                                                                                           3), ('embedded',
                                                                                                                                                                                                                                4), ('glm',
                                                                                                                                                                                                                                     5), ('gbicSerialId',
                                                                                                                                                                                                                                          6), ('gbicNoSerialId',
                                                                                                                                                                                                                                               7), ('sfpSerialId',
                                                                                                                                                                                                                                                    8), ('sfpNoSerialId',
                                                                                                                                                                                                                                                         9)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortConnectorType.setDescription("The module type of the port connector.  This object refers\n            to the hardware implementation of the port.  It will be\n            'embedded' if the hardware equivalent to Gigabit interface\n            card (GBIC) is part of the line card and is unremovable.  It\n            will be 'glm' if it's a gigabit link module (GLM).  It will\n            be 'gbicSerialId' if the GBIC serial id can be read, else it\n            will be 'gbicNoSerialId'.  It will be 'sfpSerialId' if the\n            small form factor (SFP) pluggable GBICs serial id can be\n            read, else it will be 'sfpNoSerialId'.")
fcmPortSerialNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 10), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortSerialNumber.setDescription("The serial number associated with the port (e.g., for a\n            GBIC).  If not applicable, the object's value is a zero-\n            length string.")
fcmPortPhysicalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 11), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortPhysicalNumber.setDescription("This is the port's 'Physical Port Number' as defined by\n            GS-3.")
fcmPortAdminSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(('auto',
                                                                                                                                                                                                            1), ('eighthGbs',
                                                                                                                                                                                                                 2), ('quarterGbs',
                                                                                                                                                                                                                      3), ('halfGbs',
                                                                                                                                                                                                                           4), ('oneGbs',
                                                                                                                                                                                                                                5), ('twoGbs',
                                                                                                                                                                                                                                     6), ('fourGbs',
                                                                                                                                                                                                                                          7), ('tenGbs',
                                                                                                                                                                                                                                               8)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    fcmPortAdminSpeed.setDescription("The speed of the interface:\n\n                'auto'        - auto-negotiation\n                'tenGbs'      - 10Gbs\n                'fourGbs'     -  4Gbs\n                'twoGbs'      -  2Gbs\n                'oneGbs'      -  1Gbs\n                'halfGbs'     - 500Mbs\n                'quarterGbs'  - 250Mbs\n                'eighthGbs'   - 125Mbs")
fcmPortCapProtocols = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 13), Bits().clone(namedValues=NamedValues(('unknown',
                                                                                                                    0), ('loop',
                                                                                                                         1), ('fabric',
                                                                                                                              2), ('scsi',
                                                                                                                                   3), ('tcpIp',
                                                                                                                                        4), ('vi',
                                                                                                                                             5), ('ficon',
                                                                                                                                                  6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortCapProtocols.setDescription('A bit mask specifying the higher level protocols that are\n            capable of running over this port.  Note that for generic\n            Fx_Ports, E_Ports, and B_Ports, this object will indicate\n            all protocols.')
fcmPortOperProtocols = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 3, 1, 14), Bits().clone(namedValues=NamedValues(('unknown',
                                                                                                                     0), ('loop',
                                                                                                                          1), ('fabric',
                                                                                                                               2), ('scsi',
                                                                                                                                    3), ('tcpIp',
                                                                                                                                         4), ('vi',
                                                                                                                                              5), ('ficon',
                                                                                                                                                   6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortOperProtocols.setDescription("A bit mask specifying the higher level protocols that are\n            currently operational on this port.  For Fx_Ports, E_Ports,\n            and B_Ports, this object will typically have the value\n            'unknown'.")
fcmPortStatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 4))
if mibBuilder.loadTexts:
    fcmPortStatsTable.setDescription('A list of statistics for Fibre Channel ports.')
fcmPortStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1))
fcmPortEntry.registerAugmentions(('FC-MGMT-MIB', 'fcmPortStatsEntry'))
fcmPortStatsEntry.setIndexNames(*fcmPortEntry.getIndexNames())
if mibBuilder.loadTexts:
    fcmPortStatsEntry.setDescription('An entry containing statistics for a Fibre Channel port.\n            If any counter in this table suffers a discontinuity, the\n            value of ifCounterDiscontinuityTime (defined in the IF-MIB)\n            must be updated.')
fcmPortBBCreditZeros = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 1), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortBBCreditZeros.setDescription('The number of transitions in/out of the buffer-to-buffer\n            credit zero state.  The other side is not providing any\n            credit.')
fcmPortFullInputBuffers = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 2), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortFullInputBuffers.setDescription('The number of occurrences when all input buffers of a port\n            were full and outbound buffer-to-buffer credit transitioned\n            to zero, i.e., there became no credit to provide to other\n            side.')
fcmPortClass2RxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 3), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2RxFrames.setDescription('The number of Class 2 frames received at this port.')
fcmPortClass2RxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 4), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2RxOctets.setDescription('The number of octets contained in Class 2 frames received\n            at this port.')
fcmPortClass2TxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 5), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2TxFrames.setDescription('The number of Class 2 frames transmitted out of this port.')
fcmPortClass2TxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 6), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2TxOctets.setDescription('The number of octets contained in Class 2 frames\n            transmitted out of this port.')
fcmPortClass2Discards = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 7), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2Discards.setDescription('The number of Class 2 frames that were discarded upon\n            reception at this port.')
fcmPortClass2RxFbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 8), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2RxFbsyFrames.setDescription('The number of times that F_BSY was returned to this port as\n            a result of a Class 2 frame that could not be delivered to\n            the other end of the link.  This can occur when either the\n            fabric or the destination port is temporarily busy.  Note\n            that this counter will never increment for an F_Port.')
fcmPortClass2RxPbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 9), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2RxPbsyFrames.setDescription('The number of times that P_BSY was returned to this port as\n            a result of a Class 2 frame that could not be delivered to\n            the other end of the link.  This can occur when the\n\n\n\n            destination port is temporarily busy.')
fcmPortClass2RxFrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 10), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2RxFrjtFrames.setDescription('The number of times that F_RJT was returned to this port as\n            a result of a Class 2 frame that was rejected by the fabric.\n            Note that this counter will never increment for an F_Port.')
fcmPortClass2RxPrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 11), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2RxPrjtFrames.setDescription('The number of times that P_RJT was returned to this port as\n            a result of a Class 2 frame that was rejected at the\n            destination N_Port.')
fcmPortClass2TxFbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 12), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2TxFbsyFrames.setDescription('The number of times that F_BSY was generated by this port\n            as a result of a Class 2 frame that could not be delivered\n            because either the Fabric or the destination port was\n            temporarily busy.  Note that this counter will never\n            increment for an N_Port.')
fcmPortClass2TxPbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 13), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2TxPbsyFrames.setDescription('The number of times that P_BSY was generated by this port\n            as a result of a Class 2 frame that could not be delivered\n            because the destination port was temporarily busy.  Note\n            that this counter will never increment for an F_Port.')
fcmPortClass2TxFrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 14), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2TxFrjtFrames.setDescription('The number of times that F_RJT was generated by this port\n            as a result of a Class 2 frame being rejected by the fabric.\n            Note that this counter will never increment for an N_Port.')
fcmPortClass2TxPrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 15), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass2TxPrjtFrames.setDescription('The number of times that P_RJT was generated by this port\n            as a result of a Class 2 frame being rejected at the\n            destination N_Port.  Note that this counter will never\n            increment for an F_Port.')
fcmPortClass3RxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 16), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass3RxFrames.setDescription('The number of Class 3 frames received at this port.')
fcmPortClass3RxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 17), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass3RxOctets.setDescription('The number of octets contained in Class 3 frames received\n            at this port.')
fcmPortClass3TxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 18), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass3TxFrames.setDescription('The number of Class 3 frames transmitted out of this port.')
fcmPortClass3TxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 19), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass3TxOctets.setDescription('The number of octets contained in Class 3 frames\n            transmitted out of this port.')
fcmPortClass3Discards = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 20), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClass3Discards.setDescription('The number of Class 3 frames that were discarded upon\n            reception at this port.')
fcmPortClassFRxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 21), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClassFRxFrames.setDescription('The number of Class F frames received at this port.')
fcmPortClassFRxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 22), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClassFRxOctets.setDescription('The number of octets contained in Class F frames received\n            at this port.')
fcmPortClassFTxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 23), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClassFTxFrames.setDescription('The number of Class F frames transmitted out of this port.')
fcmPortClassFTxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 24), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClassFTxOctets.setDescription('The number of octets contained in Class F frames\n            transmitted out of this port.')
fcmPortClassFDiscards = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 4, 1, 25), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortClassFDiscards.setDescription('The number of Class F frames that were discarded upon\n            reception at this port.')
fcmPortLcStatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 5))
if mibBuilder.loadTexts:
    fcmPortLcStatsTable.setDescription('A list of Counter32-based statistics for systems that do\n            not support Counter64.')
fcmPortLcStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1))
fcmPortEntry.registerAugmentions(('FC-MGMT-MIB', 'fcmPortLcStatsEntry'))
fcmPortLcStatsEntry.setIndexNames(*fcmPortEntry.getIndexNames())
if mibBuilder.loadTexts:
    fcmPortLcStatsEntry.setDescription('An entry containing low-capacity (i.e., based on Counter32)\n            statistics for a Fibre Channel port.  If any counter in this\n            table suffers a discontinuity, the value of\n            ifCounterDiscontinuityTime (defined in the IF-MIB) must be\n            updated.')
fcmPortLcBBCreditZeros = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 1), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcBBCreditZeros.setDescription('The number of transitions in/out of the buffer-to-buffer\n            credit zero state.  The other side is not providing any\n            credit.')
fcmPortLcFullInputBuffers = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcFullInputBuffers.setDescription('The number of occurrences when all input buffers of a port\n            were full and outbound buffer-to-buffer credit transitioned\n            to zero, i.e., there became no credit to provide to other\n            side.')
fcmPortLcClass2RxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2RxFrames.setDescription('The number of Class 2 frames received at this port.')
fcmPortLcClass2RxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2RxOctets.setDescription('The number of octets contained in Class 2 frames received\n            at this port.')
fcmPortLcClass2TxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2TxFrames.setDescription('The number of Class 2 frames transmitted out of this port.')
fcmPortLcClass2TxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2TxOctets.setDescription('The number of octets contained in Class 2 frames\n            transmitted out of this port.')
fcmPortLcClass2Discards = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2Discards.setDescription('The number of Class 2 frames that were discarded upon\n            reception at this port.')
fcmPortLcClass2RxFbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2RxFbsyFrames.setDescription('The number of times that F_BSY was returned to this port as\n            a result of a Class 2 frame that could not be delivered to\n            the other end of the link.  This can occur when either the\n            fabric or the destination port is temporarily busy.  Note\n            that this counter will never increment for an F_Port.')
fcmPortLcClass2RxPbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2RxPbsyFrames.setDescription('The number of times that P_BSY was returned to this port as\n            a result of a Class 2 frame that could not be delivered to\n            the other end of the link.  This can occur when the\n            destination port is temporarily busy.')
fcmPortLcClass2RxFrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2RxFrjtFrames.setDescription('The number of times that F_RJT was returned to this port as\n            a result of a Class 2 frame that was rejected by the fabric.\n            Note that this counter will never increment for an F_Port.')
fcmPortLcClass2RxPrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2RxPrjtFrames.setDescription('The number of times that P_RJT was returned to this port as\n            a result of a Class 2 frame that was rejected at the\n            destination N_Port.')
fcmPortLcClass2TxFbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2TxFbsyFrames.setDescription('The number of times that F_BSY was generated by this port\n            as a result of a Class 2 frame that could not be delivered\n            because either the Fabric or the destination port was\n            temporarily busy.  Note that this counter will never\n            increment for an N_Port.')
fcmPortLcClass2TxPbsyFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2TxPbsyFrames.setDescription('The number of times that P_BSY was generated by this port\n            as a result of a Class 2 frame that could not be delivered\n            because the destination port was temporarily busy.  Note\n            that this counter will never increment for an F_Port.')
fcmPortLcClass2TxFrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2TxFrjtFrames.setDescription('The number of times that F_RJT was generated by this port\n            as a result of a Class 2 frame being rejected by the fabric.\n            Note that this counter will never increment for an N_Port.')
fcmPortLcClass2TxPrjtFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 15), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass2TxPrjtFrames.setDescription('The number of times that P_RJT was generated by this port\n            as a result of a Class 2 frame being rejected at the\n            destination N_Port.  Note that this counter will never\n            increment for an F_Port.')
fcmPortLcClass3RxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 16), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass3RxFrames.setDescription('The number of Class 3 frames received at this port.')
fcmPortLcClass3RxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 17), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass3RxOctets.setDescription('The number of octets contained in Class 3 frames received\n            at this port.')
fcmPortLcClass3TxFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 18), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass3TxFrames.setDescription('The number of Class 3 frames transmitted out of this port.')
fcmPortLcClass3TxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 19), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass3TxOctets.setDescription('The number of octets contained in Class 3 frames\n            transmitted out of this port.')
fcmPortLcClass3Discards = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 5, 1, 20), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLcClass3Discards.setDescription('The number of Class 3 frames that were discarded upon\n            reception at this port.')
fcmPortErrorsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 6))
if mibBuilder.loadTexts:
    fcmPortErrorsTable.setDescription('Error counters for Fibre Channel ports.')
fcmPortErrorsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1))
fcmPortEntry.registerAugmentions(('FC-MGMT-MIB', 'fcmPortErrorsEntry'))
fcmPortErrorsEntry.setIndexNames(*fcmPortEntry.getIndexNames())
if mibBuilder.loadTexts:
    fcmPortErrorsEntry.setDescription('Error counters for a Fibre Channel port.  If any counter in\n            this table suffers a discontinuity, the value of\n            ifCounterDiscontinuityTime (defined in the IF-MIB) must be\n            updated.')
fcmPortRxLinkResets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 1), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortRxLinkResets.setDescription('The number of Link Reset (LR) Primitive Sequences\n            received.')
fcmPortTxLinkResets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortTxLinkResets.setDescription('The number of Link Reset (LR) Primitive Sequences\n            transmitted.')
fcmPortLinkResets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLinkResets.setDescription('The number of times the reset link protocol was initiated\n            on this port.  This includes the number of Loop\n            Initialization Primitive (LIP) events on an arbitrated loop\n            port.')
fcmPortRxOfflineSequences = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortRxOfflineSequences.setDescription('The number of Offline (OLS) Primitive Sequences received at\n            this port.')
fcmPortTxOfflineSequences = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortTxOfflineSequences.setDescription('The number of Offline (OLS) Primitive Sequences transmitted\n            by this port.')
fcmPortLinkFailures = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLinkFailures.setDescription("The number of link failures.  This count is part of FC-PH's\n            Link Error Status Block (LESB).")
fcmPortLossofSynchs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLossofSynchs.setDescription("The number of instances of synchronization loss detected at\n            this port.  This count is part of FC-PH's Link Error Status\n            Block (LESB).")
fcmPortLossofSignals = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 8), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortLossofSignals.setDescription("The number of instances of signal loss detected at this\n            port.  This count is part of FC-PH's Link Error Status Block\n            (LESB).")
fcmPortPrimSeqProtocolErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortPrimSeqProtocolErrors.setDescription("The number of primitive sequence protocol errors detected\n            at this port.  This count is part of FC-PH's Link Error\n            Status Block (LESB).")
fcmPortInvalidTxWords = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortInvalidTxWords.setDescription("The number of invalid transmission words received at this\n            port.  This count is part of FC-PH's Link Error Status Block\n            (LESB).")
fcmPortInvalidCRCs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortInvalidCRCs.setDescription("The number of frames received with an invalid CRC.  This\n            count is part of FC-PH's Link Error Status Block (LESB).")
fcmPortInvalidOrderedSets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortInvalidOrderedSets.setDescription('The number of invalid ordered sets received at this port.')
fcmPortFrameTooLongs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortFrameTooLongs.setDescription('The number of frames received at this port for which the\n            frame length was greater than what was agreed to in\n            FLOGI/PLOGI.  This could be caused by losing the end of\n            frame delimiter.')
fcmPortTruncatedFrames = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortTruncatedFrames.setDescription('The number of frames received at this port for which the\n\n\n\n            frame length was less than the minimum indicated by the\n            frame header - normally 24 bytes, but it could be more if\n            the DFCTL field indicates an optional header should have\n            been present.')
fcmPortAddressErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 15), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortAddressErrors.setDescription('The number of frames received with unknown addressing; for\n            example, an unknown SID or DID.')
fcmPortDelimiterErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 16), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortDelimiterErrors.setDescription('The number of invalid frame delimiters received at this\n            port.  An example is a frame with a class 2 start and a\n            class 3 at the end.')
fcmPortEncodingDisparityErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1,
                                                 17), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortEncodingDisparityErrors.setDescription('The number of encoding disparity errors received at this\n            port.')
fcmPortOtherErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 6, 1, 18), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmPortOtherErrors.setDescription('The number of errors that were detected on this port but\n            not counted by any other error counter in this row.')
fcmFxPortTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 7))
if mibBuilder.loadTexts:
    fcmFxPortTable.setDescription('Additional information about Fibre Channel ports that is\n            specific to Fx_Ports.  This table will contain one entry for\n            each fcmPortTable entry that represents an Fx_Port.')
fcmFxPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1)).setIndexNames((0,
                                                                                 'IF-MIB',
                                                                                 'ifIndex'))
if mibBuilder.loadTexts:
    fcmFxPortEntry.setDescription('Each entry contains information about a specific Fx_Port.')
fcmFxPortRatov = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 1), Unsigned32()).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortRatov.setDescription('The Resource_Allocation_Timeout Value configured for this\n            Fx_Port.  This is used as the timeout value for determining\n            when to reuse an Nx_Port resource such as a\n\n\n\n            Recovery_Qualifier.  It represents the Error_Detect_Timeout\n            value (see fcmFxPortEdtov) plus twice the maximum time that\n            a frame may be delayed within the Fabric and still be\n            delivered.')
fcmFxPortEdtov = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 2), Unsigned32()).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortEdtov.setDescription('The Error_Detect_Timeout value configured for this Fx_Port.\n            This is used as the timeout value for detecting an error\n            condition.')
fcmFxPortRttov = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 3), Unsigned32()).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortRttov.setDescription('The Receiver_Transmitter_Timeout value of this Fx_Port.\n            This is used by the receiver logic to detect a Loss of\n            Synchronization.')
fcmFxPortHoldTime = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 4), Unsigned32()).setUnits('microseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortHoldTime.setDescription('The maximum time that this Fx_Port shall hold a frame\n            before discarding the frame if it is unable to deliver the\n            frame.  The value 0 means that this Fx_Port does not support\n            this parameter.')
fcmFxPortCapBbCreditMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 5), FcBbCredit()).setUnits('buffers').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapBbCreditMax.setDescription('The maximum number of receive buffers that this port is\n            capable of making available for holding frames from attached\n\n\n\n            Nx_Port(s).')
fcmFxPortCapBbCreditMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 6), FcBbCredit()).setUnits('buffers').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapBbCreditMin.setDescription('The minimum number of receive buffers that this port is\n            capable of making available for holding frames from attached\n            Nx_Port(s).')
fcmFxPortCapDataFieldSizeMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 7), FcDataFieldSize()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapDataFieldSizeMax.setDescription('The maximum size in bytes of the Data Field in a frame that\n            this Fx_Port is capable of receiving from an attached\n            Nx_Port.')
fcmFxPortCapDataFieldSizeMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 8), FcDataFieldSize()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapDataFieldSizeMin.setDescription('The minimum size in bytes of the Data Field in a frame that\n            this Fx_Port is capable of receiving from an attached\n            Nx_Port.')
fcmFxPortCapClass2SeqDeliv = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 9), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapClass2SeqDeliv.setDescription('An indication of whether this Fx_Port is capable of\n            supporting Class 2 Sequential Delivery.')
fcmFxPortCapClass3SeqDeliv = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 10), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapClass3SeqDeliv.setDescription('An indication of whether this Fx_Port is capable of\n            supporting Class 3 Sequential Delivery.')
fcmFxPortCapHoldTimeMax = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 11), Unsigned32()).setUnits('microseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapHoldTimeMax.setDescription('The maximum holding time that this Fx_Port is capable of\n            supporting.')
fcmFxPortCapHoldTimeMin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 7, 1, 12), Unsigned32()).setUnits('microseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFxPortCapHoldTimeMin.setDescription('The minimum holding time that this Fx_Port is capable of\n            supporting.')
fcmISPortTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 8))
if mibBuilder.loadTexts:
    fcmISPortTable.setDescription('Additional information about E_Ports, B_Ports, and any\n            other type of Fibre Channel port to which inter-switch links\n            can be connected.  This table will contain one entry for\n            each fcmPortTable entry that represents such a port.')
fcmISPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 8, 1)).setIndexNames((0,
                                                                                 'IF-MIB',
                                                                                 'ifIndex'))
if mibBuilder.loadTexts:
    fcmISPortEntry.setDescription('Each entry contains information about a specific port\n            connected to an inter-switch link.')
fcmISPortClassFCredit = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 8, 1, 1), FcBbCredit()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    fcmISPortClassFCredit.setDescription('The maximum number of Class F data frames that can be\n            transmitted by the inter-switch port without receipt of ACK\n            or Link_Response frames.')
fcmISPortClassFDataFieldSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 8, 1, 2), FcDataFieldSize()).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmISPortClassFDataFieldSize.setDescription('The Receive Data Field Size that the inter-switch port has\n            agreed to support for Class F frames to/from this port.  The\n            size specifies the largest Data Field Size for an FT_1\n            frame.')
fcmFLoginTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 9))
if mibBuilder.loadTexts:
    fcmFLoginTable.setDescription('A table that contains one entry for each Nx_Port logged-\n            in/attached to a particular Fx_Port in the switch.  Each\n            entry contains the services parameters established during\n            the most recent Fabric Login, explicit or implicit.  Note\n            that an Fx_Port may have one or more Nx_Ports attached to\n            it.')
fcmFLoginEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1)).setIndexNames((0,
                                                                                 'IF-MIB',
                                                                                 'ifIndex'), (0,
                                                                                              'FC-MGMT-MIB',
                                                                                              'fcmFLoginNxPortIndex'))
if mibBuilder.loadTexts:
    fcmFLoginEntry.setDescription('An entry containing service parameters established from a\n            successful Fabric Login.')
fcmFLoginNxPortIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    fcmFLoginNxPortIndex.setDescription('An arbitrary integer that uniquely identifies an Nx_Port\n            amongst all those attached to the Fx_Port indicated by\n            ifIndex.\n\n            After a value of this object is assigned to a particular\n            Nx_Port, that value can be re-used when and only when it is\n            assigned to the same Nx_Port, or, after a reset of the value\n            of the relevant instance of ifCounterDiscontinuityTime.')
fcmFLoginPortWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 2), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginPortWwn.setDescription('The port name of the attached Nx_Port, or the zero-length\n            string if unknown.')
fcmFLoginNodeWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 3), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginNodeWwn.setDescription('The node name of the attached Nx_Port, or the zero-length\n            string if unknown.')
fcmFLoginBbCreditModel = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 4), FcBbCreditModel()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginBbCreditModel.setDescription('The buffer-to-buffer credit model in use by the Fx_Port.')
fcmFLoginBbCredit = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 5), FcBbCredit()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginBbCredit.setDescription('The number of buffers available for holding frames to be\n\n\n\n            transmitted to the attached Nx_Port.  These buffers are for\n            buffer-to-buffer flow control in the direction from Fx_Port\n            to Nx_Port.')
fcmFLoginClassesAgreed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 6), FcClasses()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginClassesAgreed.setDescription('The Classes of Service that the Fx_Port has agreed to\n            support for this Nx_Port.')
fcmFLoginClass2SeqDelivAgreed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1,
                                                7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginClass2SeqDelivAgreed.setDescription('An indication of whether the Fx_Port has agreed to support\n            Class 2 sequential delivery for this Nx_Port.  This is only\n            meaningful if Class 2 service has been agreed upon.')
fcmFLoginClass2DataFieldSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 8), FcDataFieldSize()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginClass2DataFieldSize.setDescription('The Receive Data Field Size that the Fx_Port has agreed to\n            support for Class 2 frames to/from this Nx_Port.  The size\n            specifies the largest Data Field Size for an FT_1 frame.\n            This is only meaningful if Class 2 service has been agreed\n            upon.')
fcmFLoginClass3SeqDelivAgreed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1,
                                                9), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginClass3SeqDelivAgreed.setDescription('An indication of whether the Fx_Port has agreed to support\n            Class 3 sequential delivery for this Nx_Port.  This is only\n            meaningful if Class 3 service has been agreed upon.')
fcmFLoginClass3DataFieldSize = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 9, 1, 10), FcDataFieldSize()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmFLoginClass3DataFieldSize.setDescription('The Receive Data Field Size that the Fx_Port has agreed to\n            support for Class 3 frames to/from this Nx_Port.  The size\n            specifies the largest Data Field Size for an FT_1 frame.\n            This is only meaningful if Class 3 service has been agreed\n            upon.')
fcmLinkTable = MibTable((1, 3, 6, 1, 2, 1, 10, 56, 1, 10))
if mibBuilder.loadTexts:
    fcmLinkTable.setDescription("A table containing any Fibre Channel link information that\n            is known to local Fibre Channel managed instances.  One end\n            of such a link is typically at a local port, but the table\n            can also contain information on links for which neither end\n            is a local port.\n\n            If one end of a link terminates locally, then that end is\n            termed 'end1'; the other end is termed 'end2'.")
fcmLinkEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1)).setIndexNames((0,
                                                                                'FC-MGMT-MIB',
                                                                                'fcmInstanceIndex'), (0,
                                                                                                      'FC-MGMT-MIB',
                                                                                                      'fcmLinkIndex'))
if mibBuilder.loadTexts:
    fcmLinkEntry.setDescription("An entry containing information that a particular Fibre\n            Channel managed instance has about a Fibre Channel link.\n\n            The two ends of the link are called 'end1' and 'end2'.")
fcmLinkIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    fcmLinkIndex.setDescription('An arbitrary integer that uniquely identifies one link\n            within the set of links about which a particular managed\n            instance has information.')
fcmLinkEnd1NodeWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 2), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd1NodeWwn.setDescription('The node name of end1, or the zero-length string if\n            unknown.')
fcmLinkEnd1PhysPortNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 3), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd1PhysPortNumber.setDescription('The physical port number of end1, or zero if unknown.')
fcmLinkEnd1PortWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 4), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd1PortWwn.setDescription("The port WWN of end1, or the zero-length string if unknown.\n            ('end1' is local if this value is equal to the value of\n            fcmPortWwn in one of the rows of the fcmPortTable.)")
fcmLinkEnd2NodeWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 5), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd2NodeWwn.setDescription('The node name of end2, or the zero-length string if\n            unknown.')
fcmLinkEnd2PhysPortNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 6), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd2PhysPortNumber.setDescription('The physical port number of end2, or zero if unknown.')
fcmLinkEnd2PortWwn = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 7), FcNameIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd2PortWwn.setDescription('The port WWN of end2, or the zero-length string if\n            unknown.')
fcmLinkEnd2AgentAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 8), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd2AgentAddress.setDescription('The address of the management agent for the Fibre Channel\n            Interconnect Element or Platform of which end2 is a part.\n            The GS-4 specification provides some information about\n            management agents.  If the address is unknown, the value of\n            this object is the zero-length string.')
fcmLinkEnd2PortType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 9), FcPortType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd2PortType.setDescription('The port type of end2.')
fcmLinkEnd2UnitType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 10), FcUnitFunctions()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd2UnitType.setDescription('The type of/function(s) performed by the Fibre Channel\n            Interconnect Element or Platform of which end2 is a part.')
fcmLinkEnd2FcAddressId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 56, 1, 10, 1, 11), FcAddressIdOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    fcmLinkEnd2FcAddressId.setDescription('The Fibre Channel Address ID of end2, or the zero-length\n            string if unknown.')
fcmgmtCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 56, 3, 1))
fcmgmtGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 56, 3, 2))
fcmgmtCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 56, 3, 1, 1)).setObjects(*(('FC-MGMT-MIB', 'fcmInstanceBasicGroup'), ('FC-MGMT-MIB', 'fcmPortBasicGroup'), ('FC-MGMT-MIB', 'fcmPortErrorsGroup'), ('FC-MGMT-MIB', 'fcmPortStatsGroup'), ('FC-MGMT-MIB', 'fcmPortClass23StatsGroup'), ('FC-MGMT-MIB', 'fcmPortClassFStatsGroup'), ('FC-MGMT-MIB', 'fcmPortLcStatsGroup'), ('FC-MGMT-MIB', 'fcmSwitchBasicGroup'), ('FC-MGMT-MIB', 'fcmSwitchPortGroup'), ('FC-MGMT-MIB', 'fcmSwitchLoginGroup'), ('FC-MGMT-MIB', 'fcmLinkBasicGroup')))
if mibBuilder.loadTexts:
    fcmgmtCompliance.setDescription('Describes the requirements for compliance to this Fibre\n            Channel Management MIB.')
fcmInstanceBasicGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 1)).setObjects(*(('FC-MGMT-MIB', 'fcmInstanceWwn'), ('FC-MGMT-MIB', 'fcmInstanceFunctions'), ('FC-MGMT-MIB', 'fcmInstancePhysicalIndex'), ('FC-MGMT-MIB', 'fcmInstanceSoftwareIndex'), ('FC-MGMT-MIB', 'fcmInstanceStatus'), ('FC-MGMT-MIB', 'fcmInstanceTextName'), ('FC-MGMT-MIB', 'fcmInstanceDescr'), ('FC-MGMT-MIB', 'fcmInstanceFabricId')))
if mibBuilder.loadTexts:
    fcmInstanceBasicGroup.setDescription('Basic information about Fibre Channel managed instances.')
fcmSwitchBasicGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 2)).setObjects(*(('FC-MGMT-MIB', 'fcmSwitchDomainId'), ('FC-MGMT-MIB', 'fcmSwitchPrincipal'), ('FC-MGMT-MIB', 'fcmSwitchWWN')))
if mibBuilder.loadTexts:
    fcmSwitchBasicGroup.setDescription('Basic information about Fibre Channel switches.')
fcmPortBasicGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 3)).setObjects(*(('FC-MGMT-MIB', 'fcmPortInstanceIndex'), ('FC-MGMT-MIB', 'fcmPortWwn'), ('FC-MGMT-MIB', 'fcmPortNodeWwn'), ('FC-MGMT-MIB', 'fcmPortAdminType'), ('FC-MGMT-MIB', 'fcmPortOperType'), ('FC-MGMT-MIB', 'fcmPortFcCapClass'), ('FC-MGMT-MIB', 'fcmPortFcOperClass'), ('FC-MGMT-MIB', 'fcmPortTransmitterType'), ('FC-MGMT-MIB', 'fcmPortConnectorType'), ('FC-MGMT-MIB', 'fcmPortSerialNumber'), ('FC-MGMT-MIB', 'fcmPortPhysicalNumber'), ('FC-MGMT-MIB', 'fcmPortAdminSpeed'), ('FC-MGMT-MIB', 'fcmPortCapProtocols'), ('FC-MGMT-MIB', 'fcmPortOperProtocols')))
if mibBuilder.loadTexts:
    fcmPortBasicGroup.setDescription('Basic information about Fibre Channel ports.')
fcmPortStatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 4)).setObjects(*(('FC-MGMT-MIB', 'fcmPortBBCreditZeros'), ('FC-MGMT-MIB', 'fcmPortFullInputBuffers')))
if mibBuilder.loadTexts:
    fcmPortStatsGroup.setDescription('Traffic statistics, which are not specific to any one class\n            of service, for Fibre Channel ports.')
fcmPortClass23StatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 5)).setObjects(*(('FC-MGMT-MIB', 'fcmPortClass2RxFrames'), ('FC-MGMT-MIB', 'fcmPortClass2RxOctets'), ('FC-MGMT-MIB', 'fcmPortClass2TxFrames'), ('FC-MGMT-MIB', 'fcmPortClass2TxOctets'), ('FC-MGMT-MIB', 'fcmPortClass2Discards'), ('FC-MGMT-MIB', 'fcmPortClass2RxFbsyFrames'), ('FC-MGMT-MIB', 'fcmPortClass2RxPbsyFrames'), ('FC-MGMT-MIB', 'fcmPortClass2RxFrjtFrames'), ('FC-MGMT-MIB', 'fcmPortClass2RxPrjtFrames'), ('FC-MGMT-MIB', 'fcmPortClass2TxFbsyFrames'), ('FC-MGMT-MIB', 'fcmPortClass2TxPbsyFrames'), ('FC-MGMT-MIB', 'fcmPortClass2TxFrjtFrames'), ('FC-MGMT-MIB', 'fcmPortClass2TxPrjtFrames'), ('FC-MGMT-MIB', 'fcmPortClass3RxFrames'), ('FC-MGMT-MIB', 'fcmPortClass3RxOctets'), ('FC-MGMT-MIB', 'fcmPortClass3TxFrames'), ('FC-MGMT-MIB', 'fcmPortClass3TxOctets'), ('FC-MGMT-MIB', 'fcmPortClass3Discards')))
if mibBuilder.loadTexts:
    fcmPortClass23StatsGroup.setDescription('Traffic statistics for Class 2 and Class 3 traffic on Fibre\n            Channel ports.')
fcmPortClassFStatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 6)).setObjects(*(('FC-MGMT-MIB', 'fcmPortClassFRxFrames'), ('FC-MGMT-MIB', 'fcmPortClassFRxOctets'), ('FC-MGMT-MIB', 'fcmPortClassFTxFrames'), ('FC-MGMT-MIB', 'fcmPortClassFTxOctets'), ('FC-MGMT-MIB', 'fcmPortClassFDiscards')))
if mibBuilder.loadTexts:
    fcmPortClassFStatsGroup.setDescription('Traffic statistics for Class F traffic on Fibre Channel\n            ports.')
fcmPortLcStatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 7)).setObjects(*(('FC-MGMT-MIB', 'fcmPortLcBBCreditZeros'), ('FC-MGMT-MIB', 'fcmPortLcFullInputBuffers'), ('FC-MGMT-MIB', 'fcmPortLcClass2RxFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2RxOctets'), ('FC-MGMT-MIB', 'fcmPortLcClass2TxFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2TxOctets'), ('FC-MGMT-MIB', 'fcmPortLcClass2Discards'), ('FC-MGMT-MIB', 'fcmPortLcClass3Discards'), ('FC-MGMT-MIB', 'fcmPortLcClass3RxFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass3RxOctets'), ('FC-MGMT-MIB', 'fcmPortLcClass3TxFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass3TxOctets'), ('FC-MGMT-MIB', 'fcmPortLcClass2RxFbsyFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2RxPbsyFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2RxFrjtFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2RxPrjtFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2TxFbsyFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2TxPbsyFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2TxFrjtFrames'), ('FC-MGMT-MIB', 'fcmPortLcClass2TxPrjtFrames')))
if mibBuilder.loadTexts:
    fcmPortLcStatsGroup.setDescription('Low-capacity (32-bit) statistics for Fibre Channel ports.')
fcmPortErrorsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 8)).setObjects(*(('FC-MGMT-MIB', 'fcmPortRxLinkResets'), ('FC-MGMT-MIB', 'fcmPortTxLinkResets'), ('FC-MGMT-MIB', 'fcmPortLinkResets'), ('FC-MGMT-MIB', 'fcmPortRxOfflineSequences'), ('FC-MGMT-MIB', 'fcmPortTxOfflineSequences'), ('FC-MGMT-MIB', 'fcmPortLinkFailures'), ('FC-MGMT-MIB', 'fcmPortLossofSynchs'), ('FC-MGMT-MIB', 'fcmPortLossofSignals'), ('FC-MGMT-MIB', 'fcmPortPrimSeqProtocolErrors'), ('FC-MGMT-MIB', 'fcmPortInvalidTxWords'), ('FC-MGMT-MIB', 'fcmPortInvalidCRCs'), ('FC-MGMT-MIB', 'fcmPortInvalidOrderedSets'), ('FC-MGMT-MIB', 'fcmPortFrameTooLongs'), ('FC-MGMT-MIB', 'fcmPortTruncatedFrames'), ('FC-MGMT-MIB', 'fcmPortAddressErrors'), ('FC-MGMT-MIB', 'fcmPortDelimiterErrors'), ('FC-MGMT-MIB', 'fcmPortEncodingDisparityErrors'), ('FC-MGMT-MIB', 'fcmPortOtherErrors')))
if mibBuilder.loadTexts:
    fcmPortErrorsGroup.setDescription('Error statistics for Fibre Channel ports.')
fcmSwitchPortGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 9)).setObjects(*(('FC-MGMT-MIB', 'fcmFxPortRatov'), ('FC-MGMT-MIB', 'fcmFxPortEdtov'), ('FC-MGMT-MIB', 'fcmFxPortRttov'), ('FC-MGMT-MIB', 'fcmFxPortHoldTime'), ('FC-MGMT-MIB', 'fcmFxPortCapBbCreditMax'), ('FC-MGMT-MIB', 'fcmFxPortCapBbCreditMin'), ('FC-MGMT-MIB', 'fcmFxPortCapDataFieldSizeMax'), ('FC-MGMT-MIB', 'fcmFxPortCapDataFieldSizeMin'), ('FC-MGMT-MIB', 'fcmFxPortCapClass2SeqDeliv'), ('FC-MGMT-MIB', 'fcmFxPortCapClass3SeqDeliv'), ('FC-MGMT-MIB', 'fcmFxPortCapHoldTimeMax'), ('FC-MGMT-MIB', 'fcmFxPortCapHoldTimeMin'), ('FC-MGMT-MIB', 'fcmISPortClassFCredit'), ('FC-MGMT-MIB', 'fcmISPortClassFDataFieldSize')))
if mibBuilder.loadTexts:
    fcmSwitchPortGroup.setDescription('Information about ports on a Fibre Channel switch.')
fcmSwitchLoginGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 10)).setObjects(*(('FC-MGMT-MIB', 'fcmFLoginPortWwn'), ('FC-MGMT-MIB', 'fcmFLoginNodeWwn'), ('FC-MGMT-MIB', 'fcmFLoginBbCreditModel'), ('FC-MGMT-MIB', 'fcmFLoginBbCredit'), ('FC-MGMT-MIB', 'fcmFLoginClassesAgreed'), ('FC-MGMT-MIB', 'fcmFLoginClass2SeqDelivAgreed'), ('FC-MGMT-MIB', 'fcmFLoginClass2DataFieldSize'), ('FC-MGMT-MIB', 'fcmFLoginClass3SeqDelivAgreed'), ('FC-MGMT-MIB', 'fcmFLoginClass3DataFieldSize')))
if mibBuilder.loadTexts:
    fcmSwitchLoginGroup.setDescription('Information known to a Fibre Channel switch about\n            attached/logged-in Nx_Ports.')
fcmLinkBasicGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 56, 3, 2, 11)).setObjects(*(('FC-MGMT-MIB', 'fcmLinkEnd1NodeWwn'), ('FC-MGMT-MIB', 'fcmLinkEnd1PhysPortNumber'), ('FC-MGMT-MIB', 'fcmLinkEnd1PortWwn'), ('FC-MGMT-MIB', 'fcmLinkEnd2NodeWwn'), ('FC-MGMT-MIB', 'fcmLinkEnd2PhysPortNumber'), ('FC-MGMT-MIB', 'fcmLinkEnd2PortWwn'), ('FC-MGMT-MIB', 'fcmLinkEnd2AgentAddress'), ('FC-MGMT-MIB', 'fcmLinkEnd2PortType'), ('FC-MGMT-MIB', 'fcmLinkEnd2UnitType'), ('FC-MGMT-MIB', 'fcmLinkEnd2FcAddressId')))
if mibBuilder.loadTexts:
    fcmLinkBasicGroup.setDescription('Information about Fibre Channel links.')
mibBuilder.exportSymbols('FC-MGMT-MIB', fcmgmtCompliances=fcmgmtCompliances, fcmSwitchDomainId=fcmSwitchDomainId, fcmLinkEnd1NodeWwn=fcmLinkEnd1NodeWwn, fcmFLoginNodeWwn=fcmFLoginNodeWwn, fcmPortClass3RxFrames=fcmPortClass3RxFrames, fcmPortLinkResets=fcmPortLinkResets, fcmFxPortCapClass3SeqDeliv=fcmFxPortCapClass3SeqDeliv, fcmPortLcClass2TxFrjtFrames=fcmPortLcClass2TxFrjtFrames, fcmPortStatsEntry=fcmPortStatsEntry, fcmFxPortCapBbCreditMin=fcmFxPortCapBbCreditMin, fcmISPortTable=fcmISPortTable, fcmPortSerialNumber=fcmPortSerialNumber, fcmPortLcStatsEntry=fcmPortLcStatsEntry, fcmPortClassFRxFrames=fcmPortClassFRxFrames, fcmSwitchWWN=fcmSwitchWWN, fcmSwitchTable=fcmSwitchTable, fcmPortConnectorType=fcmPortConnectorType, fcmPortLcClass2Discards=fcmPortLcClass2Discards, fcmFxPortCapClass2SeqDeliv=fcmFxPortCapClass2SeqDeliv, fcmPortErrorsGroup=fcmPortErrorsGroup, fcmPortTransmitterType=fcmPortTransmitterType, fcmPortClass2RxFrjtFrames=fcmPortClass2RxFrjtFrames, fcmPortLcClass2TxFbsyFrames=fcmPortLcClass2TxFbsyFrames, fcmPortBBCreditZeros=fcmPortBBCreditZeros, fcmLinkEntry=fcmLinkEntry, fcmPortLcClass2TxOctets=fcmPortLcClass2TxOctets, fcmPortLcBBCreditZeros=fcmPortLcBBCreditZeros, fcmFLoginBbCredit=fcmFLoginBbCredit, fcmPortFrameTooLongs=fcmPortFrameTooLongs, fcmLinkTable=fcmLinkTable, fcmPortLcClass2RxFrames=fcmPortLcClass2RxFrames, fcmInstanceTable=fcmInstanceTable, fcmPortErrorsEntry=fcmPortErrorsEntry, fcmLinkEnd2PortWwn=fcmLinkEnd2PortWwn, fcmInstanceStatus=fcmInstanceStatus, fcmPortClass2TxFrames=fcmPortClass2TxFrames, fcmPortLcClass2TxPrjtFrames=fcmPortLcClass2TxPrjtFrames, fcmPortLcClass2TxFrames=fcmPortLcClass2TxFrames, fcmPortInvalidOrderedSets=fcmPortInvalidOrderedSets, fcmPortLcClass2RxPbsyFrames=fcmPortLcClass2RxPbsyFrames, fcmPortInstanceIndex=fcmPortInstanceIndex, fcmSwitchLoginGroup=fcmSwitchLoginGroup, fcmPortNodeWwn=fcmPortNodeWwn, fcmPortCapProtocols=fcmPortCapProtocols, fcmPortBasicGroup=fcmPortBasicGroup, fcmLinkEnd1PortWwn=fcmLinkEnd1PortWwn, fcmPortLinkFailures=fcmPortLinkFailures, fcmFLoginTable=fcmFLoginTable, fcmgmtConformance=fcmgmtConformance, fcmPortFcOperClass=fcmPortFcOperClass, fcmFxPortTable=fcmFxPortTable, fcmPortEncodingDisparityErrors=fcmPortEncodingDisparityErrors, fcmFLoginEntry=fcmFLoginEntry, fcmLinkEnd2UnitType=fcmLinkEnd2UnitType, fcmPortClass2TxPrjtFrames=fcmPortClass2TxPrjtFrames, fcmPortLcClass3TxFrames=fcmPortLcClass3TxFrames, fcmPortLcClass3Discards=fcmPortLcClass3Discards, fcmPortClass2RxPrjtFrames=fcmPortClass2RxPrjtFrames, fcmSwitchBasicGroup=fcmSwitchBasicGroup, fcmInstancePhysicalIndex=fcmInstancePhysicalIndex, fcmPortClass2TxFrjtFrames=fcmPortClass2TxFrjtFrames, fcmPortClassFTxFrames=fcmPortClassFTxFrames, fcmInstanceBasicGroup=fcmInstanceBasicGroup, fcmPortDelimiterErrors=fcmPortDelimiterErrors, fcmPortOperProtocols=fcmPortOperProtocols, fcmFxPortCapHoldTimeMin=fcmFxPortCapHoldTimeMin, fcmInstanceFabricId=fcmInstanceFabricId, fcmPortClassFRxOctets=fcmPortClassFRxOctets, fcmFxPortCapDataFieldSizeMax=fcmFxPortCapDataFieldSizeMax, fcmFLoginClass3SeqDelivAgreed=fcmFLoginClass3SeqDelivAgreed, fcmPortEntry=fcmPortEntry, fcmPortClass2Discards=fcmPortClass2Discards, fcmFLoginClassesAgreed=fcmFLoginClassesAgreed, fcmISPortClassFCredit=fcmISPortClassFCredit, fcmPortLcFullInputBuffers=fcmPortLcFullInputBuffers, fcmPortLcClass2RxPrjtFrames=fcmPortLcClass2RxPrjtFrames, fcmPortLcClass2TxPbsyFrames=fcmPortLcClass2TxPbsyFrames, fcmLinkEnd1PhysPortNumber=fcmLinkEnd1PhysPortNumber, fcmPortLcStatsTable=fcmPortLcStatsTable, fcmInstanceSoftwareIndex=fcmInstanceSoftwareIndex, fcmPortOperType=fcmPortOperType, FcPortType=FcPortType, fcmPortClass2TxFbsyFrames=fcmPortClass2TxFbsyFrames, fcmPortInvalidTxWords=fcmPortInvalidTxWords, fcmPortStatsGroup=fcmPortStatsGroup, fcmLinkEnd2PhysPortNumber=fcmLinkEnd2PhysPortNumber, FcUnitFunctions=FcUnitFunctions, fcmFLoginBbCreditModel=fcmFLoginBbCreditModel, fcmLinkEnd2NodeWwn=fcmLinkEnd2NodeWwn, fcmISPortEntry=fcmISPortEntry, PYSNMP_MODULE_ID=fcMgmtMIB, fcmPortLcClass3RxOctets=fcmPortLcClass3RxOctets, fcmPortAddressErrors=fcmPortAddressErrors, fcmPortLcClass2RxOctets=fcmPortLcClass2RxOctets, fcmPortPrimSeqProtocolErrors=fcmPortPrimSeqProtocolErrors, fcmFLoginPortWwn=fcmFLoginPortWwn, fcmPortStatsTable=fcmPortStatsTable, FcDomainIdOrZero=FcDomainIdOrZero, fcmFxPortCapHoldTimeMax=fcmFxPortCapHoldTimeMax, fcMgmtMIB=fcMgmtMIB, fcmPortLcClass2RxFbsyFrames=fcmPortLcClass2RxFbsyFrames, FcBbCreditModel=FcBbCreditModel, fcmInstanceTextName=fcmInstanceTextName, fcmSwitchPrincipal=fcmSwitchPrincipal, fcmSwitchPortGroup=fcmSwitchPortGroup, fcmFLoginClass2SeqDelivAgreed=fcmFLoginClass2SeqDelivAgreed, fcmInstanceWwn=fcmInstanceWwn, FcClasses=FcClasses, fcmPortAdminType=fcmPortAdminType, fcmgmtCompliance=fcmgmtCompliance, fcmPortErrorsTable=fcmPortErrorsTable, fcmPortLcClass3TxOctets=fcmPortLcClass3TxOctets, fcmPortTable=fcmPortTable, fcmFxPortRttov=fcmFxPortRttov, fcmLinkEnd2FcAddressId=fcmLinkEnd2FcAddressId, FcDataFieldSize=FcDataFieldSize, fcmPortLossofSynchs=fcmPortLossofSynchs, fcmPortOtherErrors=fcmPortOtherErrors, fcmPortClass3RxOctets=fcmPortClass3RxOctets, fcmInstanceEntry=fcmInstanceEntry, fcmPortClass2TxPbsyFrames=fcmPortClass2TxPbsyFrames, fcmLinkBasicGroup=fcmLinkBasicGroup, fcmFxPortRatov=fcmFxPortRatov, fcmPortClass2RxFrames=fcmPortClass2RxFrames, fcmPortRxOfflineSequences=fcmPortRxOfflineSequences, fcmgmtObjects=fcmgmtObjects, fcmPortClass2RxOctets=fcmPortClass2RxOctets, fcmFLoginNxPortIndex=fcmFLoginNxPortIndex, fcmPortClassFTxOctets=fcmPortClassFTxOctets, fcmPortWwn=fcmPortWwn, fcmInstanceFunctions=fcmInstanceFunctions, fcmgmtNotifications=fcmgmtNotifications, fcmLinkEnd2PortType=fcmLinkEnd2PortType, fcmPortPhysicalNumber=fcmPortPhysicalNumber, fcmPortClass3TxOctets=fcmPortClass3TxOctets, fcmPortClassFDiscards=fcmPortClassFDiscards, FcBbCredit=FcBbCredit, fcmLinkEnd2AgentAddress=fcmLinkEnd2AgentAddress, fcmPortClass2RxPbsyFrames=fcmPortClass2RxPbsyFrames, fcmFxPortEntry=fcmFxPortEntry, fcmFLoginClass3DataFieldSize=fcmFLoginClass3DataFieldSize, fcmFxPortCapBbCreditMax=fcmFxPortCapBbCreditMax, fcmgmtNotifPrefix=fcmgmtNotifPrefix, FcNameIdOrZero=FcNameIdOrZero, FcAddressIdOrZero=FcAddressIdOrZero, fcmPortFcCapClass=fcmPortFcCapClass, fcmPortFullInputBuffers=fcmPortFullInputBuffers, fcmPortClass2TxOctets=fcmPortClass2TxOctets, fcmPortLcClass2RxFrjtFrames=fcmPortLcClass2RxFrjtFrames, fcmPortInvalidCRCs=fcmPortInvalidCRCs, fcmInstanceDescr=fcmInstanceDescr, fcmPortClass3Discards=fcmPortClass3Discards, fcmPortLcStatsGroup=fcmPortLcStatsGroup, fcmPortLcClass3RxFrames=fcmPortLcClass3RxFrames, fcmPortClass3TxFrames=fcmPortClass3TxFrames, fcmInstanceIndex=fcmInstanceIndex, fcmFxPortCapDataFieldSizeMin=fcmFxPortCapDataFieldSizeMin, fcmSwitchEntry=fcmSwitchEntry, fcmPortRxLinkResets=fcmPortRxLinkResets, fcmPortAdminSpeed=fcmPortAdminSpeed, fcmPortTxOfflineSequences=fcmPortTxOfflineSequences, fcmgmtGroups=fcmgmtGroups, fcmFLoginClass2DataFieldSize=fcmFLoginClass2DataFieldSize, fcmPortTxLinkResets=fcmPortTxLinkResets, fcmSwitchIndex=fcmSwitchIndex, fcmFxPortEdtov=fcmFxPortEdtov, fcmPortTruncatedFrames=fcmPortTruncatedFrames, fcmPortLossofSignals=fcmPortLossofSignals, fcmPortClass2RxFbsyFrames=fcmPortClass2RxFbsyFrames, fcmFxPortHoldTime=fcmFxPortHoldTime, fcmPortClass23StatsGroup=fcmPortClass23StatsGroup, fcmLinkIndex=fcmLinkIndex, fcmPortClassFStatsGroup=fcmPortClassFStatsGroup, fcmISPortClassFDataFieldSize=fcmISPortClassFDataFieldSize)