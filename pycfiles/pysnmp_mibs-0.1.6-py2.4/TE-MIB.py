# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/TE-MIB.py
# Compiled at: 2016-02-13 18:31:21
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueSizeConstraint, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsIntersection', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueSizeConstraint', 'ValueRangeConstraint')
(TeHopAddress, MplsBitRate, TeHopAddressType) = mibBuilder.importSymbols('MPLS-TC-STD-MIB', 'TeHopAddress', 'MplsBitRate', 'TeHopAddressType')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(ObjectGroup, NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'NotificationGroup', 'ModuleCompliance')
(TimeTicks, NotificationType, iso, ObjectIdentity, MibIdentifier, Bits, IpAddress, mib_2, Unsigned32, ModuleIdentity, Counter32, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, Integer32) = mibBuilder.importSymbols('SNMPv2-SMI', 'TimeTicks', 'NotificationType', 'iso', 'ObjectIdentity', 'MibIdentifier', 'Bits', 'IpAddress', 'mib-2', 'Unsigned32', 'ModuleIdentity', 'Counter32', 'Gauge32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64', 'Integer32')
(TextualConvention, StorageType, TimeStamp, DisplayString, TruthValue, RowStatus) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'StorageType', 'TimeStamp', 'DisplayString', 'TruthValue', 'RowStatus')
teMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 122)).setRevisions(('2005-01-04 00:00',))
if mibBuilder.loadTexts:
    teMIB.setLastUpdated('200501040000Z')
if mibBuilder.loadTexts:
    teMIB.setOrganization('IETF Traffic Engineering Working Group')
if mibBuilder.loadTexts:
    teMIB.setContactInfo('\n                  Editor:         Kireeti Kompella\n                          Postal: Juniper Networks, Inc.\n                                  1194 Mathilda Ave\n\n\n\n                                  Sunnyvale, CA 94089\n                          Tel:    +1 408 745 2000\n                          E-mail: kireeti@juniper.net\n\n                  The IETF Traffic Engineering Working Group is\n                  chaired by Jim Boyle and Ed Kern.\n\n                  WG Mailing List information:\n\n                    General Discussion: te-wg@ops.ietf.org\n                      To Subscribe:     te-wg-request@ops.ietf.org\n                         In Body:       subscribe\n                      Archive:          ftp://ops.ietf.org/pub/lists\n\n                  Comments on the MIB module should be sent to the\n                  mailing list.  The archives for this mailing list\n                  should be consulted for previous discussion on\n                  this MIB.\n                 ')
if mibBuilder.loadTexts:
    teMIB.setDescription('The Traffic Engineering MIB module.\n\n                  Copyright (C) The Internet Society (2005).  This\n                  version of this MIB module is part of RFC 3970;\n                  see the RFC itself for full legal notices.\n                 ')
teMIBNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 122, 0))
teMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 122, 1))
teMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 122, 2))
teInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 122, 1, 1))
teDistProtocol = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 1), Bits().clone(namedValues=NamedValues(('other', 0), ('isis', 1), ('ospf', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teDistProtocol.setDescription('IGP used to distribute Traffic Engineering\n                 information and topology to each device for the\n                 purpose of automatic path computation.  More than\n                 one IGP may be used to distribute TE information.\n                ')
teSignalingProto = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 2), Bits().clone(namedValues=NamedValues(('other', 0), ('rsvpte', 1), ('crldp', 2), ('static', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teSignalingProto.setDescription('Traffic Engineering signaling protocols supported\n                 by this device.  More than one protocol may be\n                 supported.\n                ')
teNotificationEnable = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 3), TruthValue().clone('false')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    teNotificationEnable.setDescription('If this object is true, then it enables the\n                 generation of notifications from this MIB module.\n                 Otherwise notifications are not generated.\n                ')
teNextTunnelIndex = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 4), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teNextTunnelIndex.setDescription('An integer that may be used as a new Index in the\n\n\n\n                 teTunnelTable.\n\n                 The special value of 0 indicates that no more new\n                 entries can be created in that table.\n\n                 When this MIB module is used for configuration, this\n                 object always contains a legal value (if non-zero)\n                 for an index that is not currently used in that\n                 table.  The Command Generator (Network Management\n                 Application) reads this variable and uses the\n                 (non-zero) value read when creating a new row with\n                 an SNMP SET.  When the SET is performed, the Command\n                 Responder (agent) must determine whether the value\n                 is indeed still unused; Two Network Management\n                 Applications may attempt to create a row\n                 (configuration entry) simultaneously and use the\n                 same value.  If it is currently unused, the SET\n                 succeeds, and the Command Responder (agent) changes\n                 the value of this object according to an\n                 implementation-specific algorithm.  If the value is\n                 in use, however, the SET fails.  The Network\n                 Management Application must then re-read this\n                 variable to obtain a new usable value.\n                ')
teNextPathHopIndex = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 5), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teNextPathHopIndex.setDescription('An integer that may be used as a new Index in the\n                 tePathHopTable.\n\n                 The special value of 0 indicates that no more new\n                 entries can be created in that table.\n\n                 When this MIB module is used for configuration, this\n                 object always contains a legal value (if non-zero)\n                 for an index that is not currently used in that\n                 table.  The Command Generator (Network Management\n                 Application) reads this variable and uses the\n                 (non-zero) value read when creating a new row with\n                 an SNMP SET.  When the SET is performed, the Command\n                 Responder (agent) must determine whether the value\n                 is indeed still unused; Two Network Management\n                 Applications may attempt to create a row\n                 (configuration entry) simultaneously and use the\n                 same value.  If it is currently unused, the SET\n\n\n\n                 succeeds, and the Command Responder (agent) changes\n                 the value of this object according to an\n                 implementation-specific algorithm.  If the value is\n                 in use, however, the SET fails.  The Network\n                 Management Application must then re-read this\n                 variable to obtain a new usable value.\n                ')
teConfiguredTunnels = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 6), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teConfiguredTunnels.setDescription('Number of currently configured Tunnels.')
teActiveTunnels = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 7), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teActiveTunnels.setDescription('Number of currently active Tunnels.')
tePrimaryTunnels = MibScalar((1, 3, 6, 1, 2, 1, 122, 1, 1, 8), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    tePrimaryTunnels.setDescription('Number of currently active Tunnels running on\n                 their primary paths.\n                ')
teAdminGroupTable = MibTable((1, 3, 6, 1, 2, 1, 122, 1, 1, 9))
if mibBuilder.loadTexts:
    teAdminGroupTable.setDescription('A mapping of configured administrative groups.  Each\n                 entry represents an Administrative Group and\n                 provides a name and index for the group.\n                 Administrative groups are used to label links in the\n                 Traffic Engineering topology in order to place\n                 constraints (include and exclude) on Tunnel paths.\n\n                 A groupName can only be linked to one group number.\n                 The groupNumber is the number assigned to the\n                 administrative group used in constraints,\n                 such as tePathIncludeAny or tePathIncludeAll.\n                ')
teAdminGroupEntry = MibTableRow((1, 3, 6, 1, 2, 1, 122, 1, 1, 9, 1)).setIndexNames((0, 'TE-MIB', 'teAdminGroupNumber'))
if mibBuilder.loadTexts:
    teAdminGroupEntry.setDescription('A mapping between a configured group number and\n                 its human-readable name.  The group number should\n                 be between 1 and 32, inclusive.  Group number n\n                 represents bit number (n-1) in the bit vector for\n                 Include/Exclude constraints.\n\n                 All entries in this table MUST be kept in stable\n                 storage so that they will re-appear in case of a\n                 restart/reboot.\n                ')
teAdminGroupNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 1, 9, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 32)))
if mibBuilder.loadTexts:
    teAdminGroupNumber.setDescription('Index of the administrative group.')
teAdminGroupName = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 1, 9, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teAdminGroupName.setDescription('Name of the administrative group.')
teAdminGroupRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 1, 9, 1, 3), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teAdminGroupRowStatus.setDescription('The status of this conceptual row.\n\n                 The value of this object has no effect on whether\n                 other objects in this conceptual row can be\n\n\n\n                 modified.\n                ')
teTunnelTable = MibTable((1, 3, 6, 1, 2, 1, 122, 1, 2))
if mibBuilder.loadTexts:
    teTunnelTable.setDescription('Table of Configured Traffic Tunnels.')
teTunnelEntry = MibTableRow((1, 3, 6, 1, 2, 1, 122, 1, 2, 1)).setIndexNames((0, 'TE-MIB', 'teTunnelIndex'))
if mibBuilder.loadTexts:
    teTunnelEntry.setDescription('Entry containing information about a particular\n                 Traffic Tunnel.\n                ')
teTunnelIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    teTunnelIndex.setDescription('A unique index that identifies a Tunnel.  If the TE\n                 Tunnel is considered an interface, then this index\n                 must match the interface index of the corresponding\n                 interface.  Otherwise, this index must be at least\n                 2^24, so that it does not overlap with any existing\n                 interface index.\n                ')
teTunnelName = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teTunnelName.setDescription("Name of the Traffic Tunnel.\n\n                 Note that the name of a Tunnel MUST be unique.\n                 When a SET request contains a name that is already\n                 in use for another entry, then the implementation\n                 must return an inconsistentValue error.\n\n                 The value of this object cannot be changed if the\n                 if the value of the corresponding teTunnelRowStatus\n                 object is 'active'.\n                ")
teTunnelNextPathIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 3), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelNextPathIndex.setDescription('An integer that may be used as a new Index for the\n                 next Path in this Tunnel.\n\n                 The special value of 0 indicates that no more Paths\n                 can be created for this Tunnel, or that no more new\n                 entries can be created in tePathTable.\n\n\n\n\n                 When this MIB module is used for configuration, this\n                 object always contains a legal value (if non-zero)\n                 for an index that is not currently used in that\n                 table.  The Command Generator (Network Management\n                 Application) reads this variable and uses the\n                 (non-zero) value read when creating a new row with\n                 an SNMP SET.  When the SET is performed, the Command\n                 Responder (agent) must determine whether the value\n                 is indeed still unused; Two Network Management\n                 Applications may attempt to create a row\n                 (configuration entry) simultaneously and use the\n                 same value.  If it is currently unused, the SET\n                 succeeds, and the Command Responder (agent) changes\n                 the value of this object according to an\n                 implementation-specific algorithm.  If the value is\n                 in use, however, the SET fails.  The Network\n                 Management Application must then re-read this\n                 variable to obtain a new usable value.\n                ')
teTunnelRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teTunnelRowStatus.setDescription("The status of this conceptual row.\n\n                 When the value of this object is 'active', then\n                 the values for the corresponding objects\n                 teTunnelName, teTunnelSourceAddressType,\n                 teTunnelSourceAddress,\n                 teTunnelDestinationAddressType, and\n                 teTunnelDestinationAddress cannot be changed.\n                ")
teTunnelStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 5), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teTunnelStorageType.setDescription("The storage type for this conceptual row.\n\n                 Conceptual rows having the value 'permanent' need\n                 not allow write-access to any columnar objects\n                 in the row.\n                ")
teTunnelSourceAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 6), TeHopAddressType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teTunnelSourceAddressType.setDescription("The type of Traffic Engineered Tunnel hop address\n                 for the source of this Tunnel.  Typically, this\n                 address type is IPv4 or IPv6, with a prefix length\n                 of 32 or 128, respectively.  If the TE Tunnel path\n                 is being computed by a path computation server,\n                 however, it is possible to use more flexible source\n                 address types, such as AS numbers or prefix lengths\n                 less than host address lengths.\n\n                 The value of this object cannot be changed\n                 if the value of the corresponding teTunnelRowStatus\n                 object is 'active'.\n                ")
teTunnelSourceAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 7), TeHopAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teTunnelSourceAddress.setDescription("The Source Traffic Engineered Tunnel hop address of\n                 this Tunnel.\n\n                 The type of this address is determined by the value\n                 of the corresponding teTunnelSourceAddressType.\n\n                 Note that the source and destination addresses of a\n                 Tunnel can be different address types.\n\n                 The value of this object cannot be changed\n                 if the value of the corresponding teTunnelRowStatus\n                 object is 'active'.\n                ")
teTunnelDestinationAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 8), TeHopAddressType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teTunnelDestinationAddressType.setDescription("The type of Traffic Engineered Tunnel hop address\n                 for the destination of this Tunnel.\n\n                 The value of this object cannot be changed\n                 if the value of the corresponding teTunnelRowStatus\n                 object is 'active'.\n\n\n\n                ")
teTunnelDestinationAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 9), TeHopAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    teTunnelDestinationAddress.setDescription("The Destination Traffic Engineered Tunnel hop\n                 address of this Tunnel.\n\n                 The type of this address is determined by the value\n                 of the corresponding teTunnelDestinationAddressType.\n\n                 Note that source and destination addresses of a\n                 Tunnel can be different address types.\n\n                 The value of this object cannot be changed\n                 if the value of the corresponding teTunnelRowStatus\n                 object is 'active'.\n                ")
teTunnelState = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('unknown', 1), ('up', 2), ('down', 3), ('testing', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelState.setDescription('The operational state of the Tunnel.')
teTunnelDiscontinuityTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 11), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelDiscontinuityTimer.setDescription("The value of sysUpTime on the most recent occasion\n                 at which any one or more of this tunnel's counters\n                 suffered a discontinuity.  The relevant counters\n                 are teTunnelOctets, teTunnelPackets,\n                 teTunnelLPOctets, and teTunnelLPPackets.  If no such\n                 discontinuities have occurred since the last\n                 re-initialization of the local management subsystem\n                 then this object contains a zero value.\n                ")
teTunnelOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 12), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelOctets.setDescription('The number of octets that have been forwarded over\n                 the Tunnel.\n\n                 Discontinuities in the value of this counter can\n                 occur at re-initialization of the management system,\n                 and at other times, as indicated by the value of\n                 teTunnelDiscontinuityTimer.\n                ')
teTunnelPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 13), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelPackets.setDescription('The number of packets that have been forwarded over\n                 the Tunnel.\n\n                 Discontinuities in the value of this counter can\n                 occur at re-initialization of the management system\n                 and at other times, as indicated by the value of\n                 teTunnelDiscontinuityTimer.\n                ')
teTunnelLPOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelLPOctets.setDescription('The number of octets that have been forwarded over\n                 the Tunnel.\n\n                 Discontinuities in the value of this counter can\n                 occur at re-initialization of the management system\n                 and at other times, as indicated by the value of\n                 teTunnelDiscontinuityTimer.\n                ')
teTunnelLPPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 15), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelLPPackets.setDescription('The number of packets that have been forwarded over\n                 the Tunnel.\n\n\n\n                 Discontinuities in the value of this counter can\n                 occur at re-initialization of the management system\n                 and at other times, as indicated by the value of\n                 teTunnelDiscontinuityTimer.\n                ')
teTunnelAge = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 16), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelAge.setDescription('The age (i.e., time from creation of this conceptual\n                 row till now) of this Tunnel in hundredths of a\n                 second.  Note that because TimeTicks wrap in about\n                 16 months, this value is best used in interval\n                 measurements.\n                ')
teTunnelTimeUp = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 17), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelTimeUp.setDescription('The total time in hundredths of a second that this\n                 Tunnel has been operational.  Note that because\n                 TimeTicks wrap in about 16 months, this value is\n                 best used in interval measurements.\n\n                 An example of usage of this object would be to\n                 compute the percentage up time over a period of time\n                 by obtaining values of teTunnelAge and\n                 teTunnelTimeUp at two points in time and computing\n                 the following ratio:\n                 ((teTunnelTimeUp2 - teTunnelTimeUp1)/\n                 (teTunnelAge2 - teTunnelAge1)) * 100 %.  In doing\n                 so, the management station must account for\n                 wrapping of the values of teTunnelAge and\n                 teTunnelTimeUp between the two measurements.\n                ')
teTunnelPrimaryTimeUp = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 18), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelPrimaryTimeUp.setDescription("The total time in hundredths of a second that this\n                 Tunnel's primary path has been operational.  Note\n                 that because TimeTicks wrap in about 16 months, this\n\n\n\n                 value is best used in interval measurements.\n\n                 An example of usage of this field would be to\n                 compute what percentage of time that a TE Tunnel was\n                 on the primary path over a period of time by\n                 computing\n                 ((teTunnelPrimaryTimeUp2 - teTunnelPrimaryTimeUp1)/\n                 (teTunnelTimeUp2 - teTunnelTimeUp1))*100 %.  In\n                 doing so, the management station must account for\n                 wrapping of the values of teTunnelPrimaryTimeUp and\n                 teTunnelTimeUp between the two measurements.\n                ")
teTunnelTransitions = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 19), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelTransitions.setDescription('The number of operational state transitions\n                 (up -> down and down -> up) this Tunnel has\n                 undergone.\n                ')
teTunnelLastTransition = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 20), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelLastTransition.setDescription('The time in hundredths of a second since the last\n                 operational state transition occurred on this\n                 Tunnel.\n\n                 Note that if the last transition was over 16\n                 months ago, this value will be inaccurate.\n                ')
teTunnelPathChanges = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 21), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelPathChanges.setDescription('The number of path changes this Tunnel has had.')
teTunnelLastPathChange = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 22), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelLastPathChange.setDescription('The time in hundredths of a second since the last\n                 path change occurred on this Tunnel.\n\n                 Note that if the last transition was over 16\n                 months ago, this value will be inaccurate.\n\n                 Path changes may be caused by network events or by\n                 reconfiguration that affects the path.\n                ')
teTunnelConfiguredPaths = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 23), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelConfiguredPaths.setDescription('The number of paths configured for this Tunnel.')
teTunnelStandbyPaths = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 24), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelStandbyPaths.setDescription('The number of standby paths configured for this\n                 Tunnel.\n                ')
teTunnelOperationalPaths = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 2, 1, 25), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    teTunnelOperationalPaths.setDescription('The number of operational paths for this Tunnel.\n                 This includes the path currently active, as\n                 well as operational standby paths.\n                ')
tePathTable = MibTable((1, 3, 6, 1, 2, 1, 122, 1, 3))
if mibBuilder.loadTexts:
    tePathTable.setDescription('Table of Configured Traffic Tunnels.')
tePathEntry = MibTableRow((1, 3, 6, 1, 2, 1, 122, 1, 3, 1)).setIndexNames((0, 'TE-MIB', 'teTunnelIndex'), (0, 'TE-MIB', 'tePathIndex'))
if mibBuilder.loadTexts:
    tePathEntry.setDescription('Entry containing information about a particular\n                 Traffic Tunnel.  Each Traffic Tunnel can have zero\n                 or more Traffic Paths.\n\n                 As a Traffic Path can only exist over an existing\n                 Traffic Tunnel, all tePathEntries with\n                 a value of n for teTunnelIndex MUST be removed by\n                 the implementation when the corresponding\n                 teTunnelEntry with a value of n for teTunnelIndex\n                 is removed.\n                ')
tePathIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    tePathIndex.setDescription('An index that uniquely identifies a path within\n                 a Tunnel.\n\n\n\n                 The combination of <teTunnelIndex, tePathIndex> thus\n                 uniquely identifies a path among all paths on this\n                 router.\n                ')
tePathName = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathName.setDescription("The name of this path.\n\n                 A pathName must be unique within the set of paths\n                 over a single tunnel.  If a SET request is received\n                 with a duplicate name, then the implementation MUST\n                 return an inconsistentValue error.\n\n                 The value of this object cannot be changed\n                 if the value of the corresponding teTunnelRowStatus\n                 object is 'active'.\n                ")
tePathRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 3), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathRowStatus.setDescription("The status of this conceptual row.\n\n                 When the value of this object is 'active', then\n                 the value of tePathName cannot be changed.  All\n                 other writable objects may be changed; however,\n                 these changes may affect traffic going over the TE\n                 tunnel or require the path to be computed and/or\n                 re-signaled.\n                ")
tePathStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 4), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathStorageType.setDescription("The storage type for this conceptual row.\n\n                 Conceptual rows having the value 'permanent' need\n                 not allow write-access to any columnar objects\n                 in the row.\n                ")
tePathType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('other', 1), ('primary', 2), ('standby', 3), ('secondary', 4)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathType.setDescription('The type for this PathEntry; i.e., whether this path\n                 is a primary path, a standby path, or a secondary\n                 path.\n                ')
tePathConfiguredRoute = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 6), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathConfiguredRoute.setDescription('The route that this TE path is configured to follow;\n                 i.e., an ordered list of hops.  The value of this\n                 object gives the primary index into the Hop Table.\n                 The secondary index is the hop count in the path, so\n                 to get the route, one could get the first hop with\n                 index <tePathConfiguredRoute, 1> in the Hop Table\n                 and do a getnext to get subsequent hops.\n                ')
tePathBandwidth = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 7), MplsBitRate()).setUnits('Kilobits per second').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathBandwidth.setDescription('The configured bandwidth for this Tunnel,\n                 in units of thousands of bits per second (Kbps).\n                ')
tePathIncludeAny = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 8), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathIncludeAny.setDescription('This is a configured set of administrative groups\n                 specified as a bit vector (i.e., bit n is 1 if group\n\n\n\n                 n is in the set, where n = 0 is the LSB).  For each\n                 link that this path goes through, the link must have\n                 at least one of the groups specified in IncludeAny\n                 to be acceptable.  If IncludeAny is zero, all links\n                 are acceptable.\n                ')
tePathIncludeAll = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 9), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathIncludeAll.setDescription('This is a configured set of administrative groups\n                 specified as a bit vector (i.e., bit n is 1 if group\n                 n is in the set, where n = 0 is the LSB).  For each\n                 link that this path goes through, the link must have\n                 all of the groups specified in IncludeAll to be\n                 acceptable.  If IncludeAll is zero, all links are\n                 acceptable.\n                ')
tePathExclude = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 10), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathExclude.setDescription("This is a configured set of administrative groups\n                 specified as a bit vector (i.e., bit n is 1 if group\n                 n is in the set, where n = 0 is the LSB).  For each\n                 link that this path goes through, the link MUST have\n                 groups associated with it, and the intersection of\n                 the link's groups and the 'exclude' set MUST be\n                 null.\n                ")
tePathSetupPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7)).clone(7)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathSetupPriority.setDescription('The setup priority configured for this path, with 0\n                 as the highest priority and 7 as the lowest.\n                ')
tePathHoldPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 7))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathHoldPriority.setDescription('The hold priority configured for this path, with 0\n                 as the highest priority and 7 as the lowest.\n                ')
tePathProperties = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 13), Bits().clone(namedValues=NamedValues(('recordRoute', 0), ('cspf', 1), ('makeBeforeBreak', 2), ('mergeable', 3), ('fastReroute', 4), ('protected', 5)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathProperties.setDescription("The set of configured properties for this path,\n                 expressed as a bit map.  For example, if the path\n                 supports 'make before break', then bit 2 is set.\n                ")
tePathOperStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 14), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('unknown', 0), ('down', 1), ('testing', 2), ('dormant', 3), ('ready', 4), ('operational', 5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    tePathOperStatus.setDescription('The operational status of the path:\n                 unknown:\n                 down:        Signaling failed.\n                 testing:     Administratively set aside for testing.\n                 dormant:     Not signaled (for a backup tunnel).\n                 ready:       Signaled but not yet carrying traffic.\n                 operational: Signaled and carrying traffic.\n                ')
tePathAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 15), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('normal', 1), ('testing', 2)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathAdminStatus.setDescription('The operational status of the path:\n                 normal:      Used normally for forwarding.\n                 testing:     Administratively set aside for testing.\n                ')
tePathComputedRoute = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 16), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    tePathComputedRoute.setDescription('The route computed for this path, perhaps using\n                 some form of Constraint-based Routing.  The\n                 algorithm is implementation dependent.\n\n                 This object returns the computed route as an ordered\n                 list of hops.  The value of this object gives the\n                 primary index into the Hop Table.  The secondary\n                 index is the hop count in the path, so to get the\n                 route, one could get the first hop with index\n                 <tePathComputedRoute, 1> in the Hop Table and do a\n                 getnext to get subsequent hops.\n\n                 A value of zero (0) means there is no computedRoute.\n                ')
tePathRecordedRoute = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 3, 1, 17), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    tePathRecordedRoute.setDescription('The route actually used for this path, as recorded\n                 by the signaling protocol.  This is again an ordered\n                 list of hops; each hop is expected to be strict.\n\n                 The value of this object gives the primary index\n                 into the Hop Table.  The secondary index is the hop\n                 count in the path, so to get the route, one can get\n                 the first hop with index <tePathRecordedRoute, 1>\n                 in the Hop Table and do a getnext to get subsequent\n\n\n\n                 hops.\n\n                 A value of zero (0) means there is no recordedRoute.\n                ')
tePathHopTable = MibTable((1, 3, 6, 1, 2, 1, 122, 1, 4))
if mibBuilder.loadTexts:
    tePathHopTable.setDescription('Table of Tunnel Path Hops.')
tePathHopEntry = MibTableRow((1, 3, 6, 1, 2, 1, 122, 1, 4, 1)).setIndexNames((0, 'TE-MIB', 'teHopListIndex'), (0, 'TE-MIB', 'tePathHopIndex'))
if mibBuilder.loadTexts:
    tePathHopEntry.setDescription('Entry containing information about a particular\n                 hop.\n                ')
teHopListIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 4, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    teHopListIndex.setDescription('An index that identifies a list of hops.  This is\n                 the primary index to access hops.\n                ')
tePathHopIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 4, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    tePathHopIndex.setDescription('An index that identifies a particular hop among the\n                 list of hops for a path.  An index of i identifies\n                 the ith hop.  This is the secondary index for a hop\n                 entry.\n                ')
tePathHopRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 4, 1, 3), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathHopRowStatus.setDescription("The status of this conceptual row.\n\n                 Any field in this table can be changed, even if the\n                 value of this object is 'active'.  However, such a\n                 change may cause traffic to be rerouted or even\n                 disrupted.\n                ")
tePathHopStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 4, 1, 4), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathHopStorageType.setDescription("The storage type for this conceptual row.\n\n                 Conceptual rows having the value 'permanent' need\n                 not allow write-access to any columnar objects\n                 in the row.\n                ")
tePathHopAddrType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 4, 1, 5), TeHopAddressType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathHopAddrType.setDescription("The type of Traffic Engineered Tunnel hop Address\n                 of this hop.\n\n                 The value of this object cannot be changed\n                 if the value of the corresponding tePathRowStatus\n                 object is 'active'.\n                ")
tePathHopAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 4, 1, 6), TeHopAddress()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    tePathHopAddress.setDescription("The Traffic Engineered Tunnel hop Address of this\n                 hop.\n\n                 The type of this address is determined by the value\n                 of the corresponding tePathHopAddressType.\n\n                 The value of this object cannot be changed\n                 if the value of the corresponding teTunnelRowStatus\n                 object is 'active'.\n                ")
tePathHopType = MibTableColumn((1, 3, 6, 1, 2, 1, 122, 1, 4, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2))).clone(namedValues=NamedValues(('unknown', 0), ('loose', 1), ('strict', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    tePathHopType.setDescription('The type of hop:\n                 unknown:\n                 loose:    This hop is a LOOSE hop.\n                 strict:   This hop is a STRICT hop.\n                ')
teTunnelUp = NotificationType((1, 3, 6, 1, 2, 1, 122, 0, 1)).setObjects(*(('TE-MIB', 'teTunnelName'), ('TE-MIB', 'tePathName')))
if mibBuilder.loadTexts:
    teTunnelUp.setDescription("A teTunnelUp notification is generated when the\n                 Tunnel indexed by teTunnelName transitions to the\n                 'up' state.\n\n                 A tunnel is up when at least one of its paths is up.\n                 The tePathName is the name of the path whose\n                 transition to up made the tunnel go up.\n\n\n\n\n                 This notification MUST be limited to at most one\n                 every minute, in case the tunnel flaps up and down.\n                ")
teTunnelDown = NotificationType((1, 3, 6, 1, 2, 1, 122, 0, 2)).setObjects(*(('TE-MIB', 'teTunnelName'), ('TE-MIB', 'tePathName')))
if mibBuilder.loadTexts:
    teTunnelDown.setDescription("A teTunnelDown notification is generated when the\n                 Tunnel indexed by teTunnelName transitions to the\n                 'down' state.\n\n                 A tunnel is up when at least one of its paths is up.\n                 The tePathName is the name of the path whose\n                 transition to down made the tunnel go down.\n\n                 This notification MUST be limited to at most one\n                 every minute, in case the tunnel flaps up and down.\n                ")
teTunnelChanged = NotificationType((1, 3, 6, 1, 2, 1, 122, 0, 3)).setObjects(*(('TE-MIB', 'teTunnelName'), ('TE-MIB', 'tePathName')))
if mibBuilder.loadTexts:
    teTunnelChanged.setDescription('A teTunnelChanged notification is generated when an\n                 active path on the Tunnel indexed by teTunnelName\n                 changes or a new path becomes active.  The value\n                 of tePathName is the new active path.\n\n                 This notification MUST be limited to at most one\n                 every minute, in case the tunnel changes quickly.\n                ')
teTunnelRerouted = NotificationType((1, 3, 6, 1, 2, 1, 122, 0, 4)).setObjects(*(('TE-MIB', 'teTunnelName'), ('TE-MIB', 'tePathName')))
if mibBuilder.loadTexts:
    teTunnelRerouted.setDescription('A teTunnelRerouted notification is generated when\n                 an active path for the Tunnel indexed by\n                 teTunnelName stays the same, but its route changes.\n\n                 This notification MUST be limited to at most one\n                 every minute, in case the tunnel reroutes quickly.\n                ')
teGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 122, 2, 1))
teModuleCompliance = MibIdentifier((1, 3, 6, 1, 2, 1, 122, 2, 2))
teTrafficEngineeringGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 122, 2, 1, 1)).setObjects(*(('TE-MIB', 'teTunnelName'), ('TE-MIB', 'teTunnelNextPathIndex'), ('TE-MIB', 'teTunnelRowStatus'), ('TE-MIB', 'teTunnelStorageType'), ('TE-MIB', 'teTunnelSourceAddressType'), ('TE-MIB', 'teTunnelSourceAddress'), ('TE-MIB', 'teTunnelDestinationAddressType'), ('TE-MIB', 'teTunnelDestinationAddress'), ('TE-MIB', 'teTunnelState'), ('TE-MIB', 'teTunnelDiscontinuityTimer'), ('TE-MIB', 'teTunnelOctets'), ('TE-MIB', 'teTunnelPackets'), ('TE-MIB', 'teTunnelLPOctets'), ('TE-MIB', 'teTunnelLPPackets'), ('TE-MIB', 'teTunnelAge'), ('TE-MIB', 'teTunnelTimeUp'), ('TE-MIB', 'teTunnelPrimaryTimeUp'), ('TE-MIB', 'teTunnelTransitions'), ('TE-MIB', 'teTunnelLastTransition'), ('TE-MIB', 'teTunnelPathChanges'), ('TE-MIB', 'teTunnelLastPathChange'), ('TE-MIB', 'teTunnelConfiguredPaths'), ('TE-MIB', 'teTunnelStandbyPaths'), ('TE-MIB', 'teTunnelOperationalPaths'), ('TE-MIB', 'tePathBandwidth'), ('TE-MIB', 'tePathIncludeAny'), ('TE-MIB', 'tePathIncludeAll'), ('TE-MIB', 'tePathExclude'), ('TE-MIB', 'tePathSetupPriority'), ('TE-MIB', 'tePathHoldPriority'), ('TE-MIB', 'tePathProperties'), ('TE-MIB', 'tePathOperStatus'), ('TE-MIB', 'tePathAdminStatus'), ('TE-MIB', 'tePathComputedRoute'), ('TE-MIB', 'tePathRecordedRoute'), ('TE-MIB', 'teDistProtocol'), ('TE-MIB', 'teSignalingProto'), ('TE-MIB', 'teNotificationEnable'), ('TE-MIB', 'teNextTunnelIndex'), ('TE-MIB', 'teNextPathHopIndex'), ('TE-MIB', 'teAdminGroupName'), ('TE-MIB', 'teAdminGroupRowStatus'), ('TE-MIB', 'teConfiguredTunnels'), ('TE-MIB', 'teActiveTunnels'), ('TE-MIB', 'tePrimaryTunnels'), ('TE-MIB', 'tePathName'), ('TE-MIB', 'tePathType'), ('TE-MIB', 'tePathRowStatus'), ('TE-MIB', 'tePathStorageType'), ('TE-MIB', 'tePathConfiguredRoute'), ('TE-MIB', 'tePathHopRowStatus'), ('TE-MIB', 'tePathHopStorageType'), ('TE-MIB', 'tePathHopAddrType'), ('TE-MIB', 'tePathHopAddress'), ('TE-MIB', 'tePathHopType')))
if mibBuilder.loadTexts:
    teTrafficEngineeringGroup.setDescription('Objects for Traffic Engineering in this MIB module.')
teNotificationGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 122, 2, 1, 2)).setObjects(*(('TE-MIB', 'teTunnelUp'), ('TE-MIB', 'teTunnelDown'), ('TE-MIB', 'teTunnelChanged'), ('TE-MIB', 'teTunnelRerouted')))
if mibBuilder.loadTexts:
    teNotificationGroup.setDescription('Notifications specified in this MIB module.')
teModuleReadOnlyCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 122, 2, 2, 1)).setObjects(*(('TE-MIB', 'teTrafficEngineeringGroup'), ('TE-MIB', 'teNotificationGroup')))
if mibBuilder.loadTexts:
    teModuleReadOnlyCompliance.setDescription('When this MIB module is implemented without support\n                 for read-create (i.e., in read-only mode), then such\n                 an implementation can claim read-only compliance.\n                 Such a device can be monitored but cannot be\n                 configured with this MIB module.\n                ')
teModuleFullCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 122, 2, 2, 2)).setObjects(*(('TE-MIB', 'teTrafficEngineeringGroup'), ('TE-MIB', 'teNotificationGroup')))
if mibBuilder.loadTexts:
    teModuleFullCompliance.setDescription('When this MIB module is implemented with support for\n                 read-create, then the implementation can claim\n                 full compliance.  Such devices can be both\n\n\n\n                 monitored and configured with this MIB module.\n                ')
teModuleServerReadOnlyCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 122, 2, 2, 3)).setObjects(*(('TE-MIB', 'teTrafficEngineeringGroup'), ('TE-MIB', 'teNotificationGroup')))
if mibBuilder.loadTexts:
    teModuleServerReadOnlyCompliance.setDescription('When this MIB module is implemented by a path\n                 computation server without support for read-create\n                 (i.e., in read-only mode), then the implementation\n                 can claim read-only compliance.  Such\n                 a device can be monitored but cannot be\n                 configured with this MIB module.\n                ')
teModuleServerFullCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 122, 2, 2, 4)).setObjects(*(('TE-MIB', 'teTrafficEngineeringGroup'), ('TE-MIB', 'teNotificationGroup')))
if mibBuilder.loadTexts:
    teModuleServerFullCompliance.setDescription('When this MIB module is implemented by a path\n                 computation server with support for read-create,\n                 then the implementation can claim full\n                 compliance.\n                ')
mibBuilder.exportSymbols('TE-MIB', teMIBObjects=teMIBObjects, teTunnelPrimaryTimeUp=teTunnelPrimaryTimeUp, tePathComputedRoute=tePathComputedRoute, teMIBNotifications=teMIBNotifications, teTunnelTimeUp=teTunnelTimeUp, teTunnelStandbyPaths=teTunnelStandbyPaths, teTunnelDestinationAddressType=teTunnelDestinationAddressType, tePathHopAddrType=tePathHopAddrType, tePathEntry=tePathEntry, tePathSetupPriority=tePathSetupPriority, tePathHoldPriority=tePathHoldPriority, teTunnelPackets=teTunnelPackets, teSignalingProto=teSignalingProto, teTunnelState=teTunnelState, teTunnelEntry=teTunnelEntry, teTunnelLPOctets=teTunnelLPOctets, tePathStorageType=tePathStorageType, tePathType=tePathType, tePathHopIndex=tePathHopIndex, teTunnelPathChanges=teTunnelPathChanges, teModuleServerFullCompliance=teModuleServerFullCompliance, tePathHopAddress=tePathHopAddress, teTunnelLastTransition=teTunnelLastTransition, tePathTable=tePathTable, teTunnelLastPathChange=teTunnelLastPathChange, teMIBConformance=teMIBConformance, teTunnelLPPackets=teTunnelLPPackets, teTunnelIndex=teTunnelIndex, teTunnelAge=teTunnelAge, teTunnelConfiguredPaths=teTunnelConfiguredPaths, teAdminGroupTable=teAdminGroupTable, teTunnelTransitions=teTunnelTransitions, teTunnelTable=teTunnelTable, tePathHopRowStatus=tePathHopRowStatus, tePrimaryTunnels=tePrimaryTunnels, teTunnelOctets=teTunnelOctets, tePathName=tePathName, PYSNMP_MODULE_ID=teMIB, teNotificationGroup=teNotificationGroup, teTrafficEngineeringGroup=teTrafficEngineeringGroup, teTunnelSourceAddress=teTunnelSourceAddress, teTunnelSourceAddressType=teTunnelSourceAddressType, teGroups=teGroups, teTunnelUp=teTunnelUp, teActiveTunnels=teActiveTunnels, tePathHopTable=tePathHopTable, tePathHopType=tePathHopType, tePathProperties=tePathProperties, teTunnelDestinationAddress=teTunnelDestinationAddress, teInfo=teInfo, teModuleServerReadOnlyCompliance=teModuleServerReadOnlyCompliance, teHopListIndex=teHopListIndex, teAdminGroupNumber=teAdminGroupNumber, teTunnelStorageType=teTunnelStorageType, teModuleCompliance=teModuleCompliance, tePathHopEntry=tePathHopEntry, teAdminGroupEntry=teAdminGroupEntry, tePathAdminStatus=tePathAdminStatus, teNextPathHopIndex=teNextPathHopIndex, teMIB=teMIB, teModuleReadOnlyCompliance=teModuleReadOnlyCompliance, teAdminGroupRowStatus=teAdminGroupRowStatus, teTunnelRowStatus=teTunnelRowStatus, teTunnelNextPathIndex=teTunnelNextPathIndex, tePathIncludeAny=tePathIncludeAny, tePathIndex=tePathIndex, tePathExclude=tePathExclude, teDistProtocol=teDistProtocol, teNotificationEnable=teNotificationEnable, tePathOperStatus=tePathOperStatus, tePathRecordedRoute=tePathRecordedRoute, teAdminGroupName=teAdminGroupName, tePathRowStatus=tePathRowStatus, teConfiguredTunnels=teConfiguredTunnels, tePathIncludeAll=tePathIncludeAll, teModuleFullCompliance=teModuleFullCompliance, teTunnelDiscontinuityTimer=teTunnelDiscontinuityTimer, teTunnelOperationalPaths=teTunnelOperationalPaths, teTunnelChanged=teTunnelChanged, teTunnelDown=teTunnelDown, tePathHopStorageType=tePathHopStorageType, teTunnelName=teTunnelName, teNextTunnelIndex=teNextTunnelIndex, teTunnelRerouted=teTunnelRerouted, tePathBandwidth=tePathBandwidth, tePathConfiguredRoute=tePathConfiguredRoute)