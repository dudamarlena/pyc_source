# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/L2TP-MIB.py
# Compiled at: 2016-02-13 18:19:42
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint')
(InterfaceIndex,) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndex')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(NotificationGroup, ModuleCompliance, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance', 'ObjectGroup')
(Gauge32, iso, NotificationType, Unsigned32, Counter32, TimeTicks, ObjectIdentity, Integer32, Bits, IpAddress, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, Counter64, transmission) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'iso', 'NotificationType', 'Unsigned32', 'Counter32', 'TimeTicks', 'ObjectIdentity', 'Integer32', 'Bits', 'IpAddress', 'ModuleIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'MibIdentifier', 'Counter64', 'transmission')
(StorageType, DisplayString, TruthValue, TextualConvention, RowStatus) = mibBuilder.importSymbols('SNMPv2-TC', 'StorageType', 'DisplayString', 'TruthValue', 'TextualConvention', 'RowStatus')
l2tp = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 95)).setRevisions(('2002-08-23 00:00',))
if mibBuilder.loadTexts:
    l2tp.setLastUpdated('200208230000Z')
if mibBuilder.loadTexts:
    l2tp.setOrganization('IETF L2TP Working Group')
if mibBuilder.loadTexts:
    l2tp.setContactInfo('Evan Caves\n           Postal: Occam Networks\n                   77 Robin Hill Road\n                   Santa Barbara, CA, 93117\n           Tel:    +1 805692 2900\n           Email:  evan@occamnetworks.com\n\n           Pat R. Calhoun\n\n           Postal: Black Storm Networks\n                   110 Nortech Parkway\n                   San Jose, CA, 95143\n           Tel:    +1 408 941-0500\n           Email:  pcalhoun@bstormnetworks.com\n\n           Ross Wheeler\n           Postal: DoubleWide Software, Inc.\n                   2953 Bunker Hill Lane\n                   Suite 101\n                   Santa Clara, CA 95054\n           Tel:    +1 6509260599\n           Email:  ross@doublewidesoft.com\n\n           Layer Two Tunneling Protocol Extensions WG\n           Working Group Area:    Internet\n           Working Group Name:    l2tpext\n           General Discussion:    l2tp@l2tp.net')
if mibBuilder.loadTexts:
    l2tp.setDescription('The MIB module that describes managed objects of\n            general use by the Layer Two Transport Protocol.')

class L2tpMilliSeconds(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd-3'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 2147483646)


l2tpNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 0))
l2tpObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 1))
l2tpTransports = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 3))
l2tpConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 4))
l2tpScalar = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 1, 1))
l2tpConfig = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 1))
l2tpStats = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 2))
l2tpTransportIpUdp = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 3, 1))
l2tpIpUdpObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 3, 1, 1))
l2tpIpUdpTraps = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 3, 1, 2))
l2tpAdminState = MibScalar((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled', 1), ('disabled', 2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpAdminState.setDescription("This object defines the administrative state of\n            the L2TP protocol. Setting this object to\n            'disabled' causes all tunnels to be immediately\n            disconnected and no further tunnels to be either\n            initiated or accepted. The value of this object\n            must be maintained in non-volatile memory.")
l2tpDrainTunnels = MibScalar((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 1, 2), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpDrainTunnels.setDescription("Setting this object to 'true' will prevent any new\n            tunnels and/or sessions to be either initiated or\n            accepted but does NOT disconnect any active\n            tunnels/sessions. Setting this object to true(1)\n            causes all domains and their respective tunnels\n            to transition to the draining state. Note that\n            when this occurs the 'xxxDraining' status objects\n            of the domains and their tunnels should reflect\n            that they are 'draining'. Setting this object has\n            no affect on the domains or their tunnels\n            'xxxDrainTunnels' configuration objects. To cancel\n            a drain this object should be set to false(2).\n            The object l2tpDrainingTunnels reflects\n            the current L2TP draining state. The value of\n            this object must be maintained in non-volatile\n            memory.")
l2tpProtocolVersions = MibScalar((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 2, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(2, 256))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpProtocolVersions.setDescription('Vector of supported L2TP protocol version and\n             revision numbers. Supported versions are identified\n             via a two octet pairing where the first octet indicates\n             the version and the second octet contains the revision.')
l2tpVendorName = MibScalar((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 2, 2), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpVendorName.setDescription('This object identifies the Vendor name of the L2TP\n            protocol stack.')
l2tpFirmwareRev = MibScalar((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 2, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpFirmwareRev.setDescription('This object defines the firmware revision for the\n            L2TP protocol stack.')
l2tpDrainingTunnels = MibScalar((1, 3, 6, 1, 2, 1, 10, 95, 1, 1, 2, 4), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDrainingTunnels.setDescription('This object indicates if the local L2TP is draining\n            off sessions from all tunnels.')
l2tpDomainConfigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 1, 2))
if mibBuilder.loadTexts:
    l2tpDomainConfigTable.setDescription('The L2TP Domain configuration table. This table\n            contains objects that can be used to configure\n            the operational characteristics of a tunnel\n            domain. There is a 1-1 correspondence between\n            conceptual rows of this table and conceptual\n            rows of the l2tpDomainStatsTable.')
l2tpDomainConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1)).setIndexNames((0, 'L2TP-MIB', 'l2tpDomainConfigId'))
if mibBuilder.loadTexts:
    l2tpDomainConfigEntry.setDescription('An L2TP Domain configuration entry. An entry in this\n            table may correspond to a single endpoint or a group\n            of tunnel endpoints.')
l2tpDomainConfigId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 80)))
if mibBuilder.loadTexts:
    l2tpDomainConfigId.setDescription("The identifier, usually in the form of a Domain\n            Name (full or partial), describing a single tunnel\n            endpoint or a domain of tunnel endpoints. This is\n            typically used as a 'handle' to identify the\n            tunnel configuration requirements for both incoming\n            and outgoing tunnel connection attempts. Both the\n            LAC and  LNS could use information provided in the\n            Host Name AVP attribute however the tunnel initiator\n            could use other means not specified to identify\n            the domain's tunnel configuration requirements.\n            For example; three rows in this table have\n            l2tpDomainConfigId values of 'lac1.isp.com',\n\n            'isp.com' and 'com'. A tunnel endpoint then identifies\n            itself as 'lac1.isp.com' which would match the\n            'lac1.isp.com' entry in this table. A second tunnel\n            endpoint then identifies itself as 'lac2.isp.com'.\n            This endpoint is then associated with the 'isp.com'\n            entry of this table.")
l2tpDomainConfigAdminState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled', 1), ('disabled', 2))).clone('enabled')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigAdminState.setDescription('This object defines the administrative state of this\n            tunnel domain. Setting this object to disabled(2)\n            causes all tunnels to be immediately disconnected\n            and no further tunnels to be either initiated or\n            accepted. Note that all columnar objects corresponding\n            to this conceptual row cannot be modified when\n            the administrative state is enabled EXCEPT those\n            objects which specifically state otherwise.')
l2tpDomainConfigDrainTunnels = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 3), TruthValue().clone('false')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigDrainTunnels.setDescription("Setting this object to 'true' will prevent any new\n            tunnels and/or sessions from being either initiated\n            or accepted but does NOT disconnect any active\n            tunnels/sessions for this tunnel domain. Setting\n            this object to true(1) causes all tunnels within\n            this domain to transition to the draining state.\n            Note that when this occurs the\n            l2tpTunnelStatsDrainingTunnel status objects of\n            all of this domain's tunnels should reflect that\n            they are 'draining'. Setting this object has no\n            effect on this domain's associated tunnels\n            l2tpTunnelConfigDrainTunnel configuration objects.\n            To cancel a drain this object should be set to\n            false(2).  Setting this object to false(2) when\n            the L2TP object l2tpDrainTunnels is true(1) has\n            no affect, all domains and their tunnels will\n\n            continue to drain.")
l2tpDomainConfigAuth = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none', 1), ('simple', 2), ('challenge', 3))).clone('none')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigAuth.setDescription('This object describes how tunnel peers belonging\n            to this domain are to be authenticated. The value\n            simple(2) indicates that peers are authenticated\n            simply by their host name as described in the Host\n            Name AVP.  The value challenge(3) indicates that\n            all peers are challenged to prove their identification.\n            This mechanism is described in the L2TP protocol.')
l2tpDomainConfigSecret = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 5), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigSecret.setDescription('This object is used to configure the shared secret\n            used during the tunnel authentication phase of\n            tunnel establishment. This object MUST be accessible\n            only via requests using both authentication and\n            privacy. The agent MUST report an empty string in\n            response to get, get-next and get-bulk requests.')
l2tpDomainConfigTunnelSecurity = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none', 1), ('other', 2), ('ipSec', 3))).clone('none')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigTunnelSecurity.setDescription('This object defines whether this tunnel domain\n            requires that all tunnels are to be secured. The\n\n            value of ipsec(3) indicates that all tunnel packets,\n            control and session, have IP Security headers. The\n            type of IP Security headers (AH, ESP etc) and how\n            they are further described is outside the scope of\n            this document.')
l2tpDomainConfigTunnelHelloInt = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 3600)).clone(60)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigTunnelHelloInt.setDescription('This object defines the interval in which Hello\n            (or keep-alive) packets are to be sent by local\n            peers belonging to this tunnel domain. The value\n            zero effectively disables the sending of Hello\n            packets. This object may be modified when the\n            administrative state is enabled for this conceptual\n            row.')
l2tpDomainConfigTunnelIdleTO = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 86400))).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigTunnelIdleTO.setDescription('This object defines the period of time that an\n            established tunnel belonging to this tunnel\n            domain with no active sessions will wait before\n            disconnecting the tunnel. A value of zero indicates\n            that the tunnel will disconnect immediately after the\n            last session disconnects. A value of -1 leaves the\n            tunnel up indefinitely. This object may be modified\n            when the administrative state is enabled for this\n            conceptual row.')
l2tpDomainConfigControlRWS = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)).clone(4)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigControlRWS.setDescription('This object defines the control channel receive\n\n            window size for tunnels belonging to this domain. It\n            specifies the maximum number of packets the tunnel\n            peer belonging to this domain can send without waiting\n            for an acknowledgement from this peer.')
l2tpDomainConfigControlMaxRetx = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 32)).clone(5)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigControlMaxRetx.setDescription('This object defines the maximum number of retransmissions\n            which the L2TP stack will attempt for tunnels belonging\n            to this domain before assuming that the peer is no\n            longer responding.')
l2tpDomainConfigControlMaxRetxTO = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 32)).clone(16)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigControlMaxRetxTO.setDescription('This object defines the maximum retransmission timeout\n            interval which the L2TP stack will wait for tunnels\n            belonging to this domain before retransmitting a\n            control packet that has not been acknowledged.')
l2tpDomainConfigPayloadSeq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('onDemand', 1), ('never', 2), ('always', 3))).clone('onDemand')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigPayloadSeq.setDescription('This object determines whether or not session payload\n            packets will be requested to be sent with sequence\n            numbers from tunnel peers belonging to this domain.\n            The value onDemand(1) allows the L2TP implementation\n            to initiate payload sequencing when necessary based\n            on local information (e.g: during LCP/NCP negotiations\n            or for CCP). The value never(2) indicates that L2TP\n\n            will never initiate sequencing but will do sequencing\n            if asked. The value always(3) indicates that L2TP\n            will send the Sequencing Required AVP during session\n            establishment.')
l2tpDomainConfigReassemblyTO = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 13), L2tpMilliSeconds()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigReassemblyTO.setDescription('This object defines the number of milliseconds that\n            local peers of this tunnel domain will wait before\n            processing payload packets that were received out of\n            sequence (which are waiting for the packet(s) to put\n            them in sequence).  A low value increases the chance\n            of delayed packets to be discarded (which MAY cause\n            the PPP decompression engine to reset) while a high\n            value may cause more queuing and possibly degrade\n            throughput if packets are truly lost. The default\n            value for this object is zero which will result in\n            all delayed packets being lost.')
l2tpDomainConfigProxyPPPAuth = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 14), TruthValue().clone('true')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigProxyPPPAuth.setDescription("This object is used to configure the sending\n            or acceptance of the PPP Proxy Authentication\n            AVP's on the LAC or LNS.")
l2tpDomainConfigStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 15), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigStorageType.setDescription("The storage type for this conceptual row.\n\n            Conceptual rows having the value 'permanent' must\n            allow write-access at a minimum to:\n\n            - l2tpDomainConfigAdminState and\n\n              l2tpDomainConfigDrainTunnels at all times\n            - l2tpDomainConfigSecret if l2tpDomainConfigAuth\n              has been configured as 'challenge'\n\n            It is an implementation issue to decide if a SET for\n            a readOnly or permanent row is accepted at all. In some\n            contexts this may make sense, in others it may not. If\n            a SET for a readOnly or permanent row is not accepted\n            at all, then a 'wrongValue' error must be returned.")
l2tpDomainConfigStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 2, 1, 16), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpDomainConfigStatus.setDescription("The status of this Domain entry. Columnar objects\n            corresponding to this conceptual row may be modified\n            according to their description clauses when this\n            RowStatus object is 'active'.")
l2tpDomainStatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 1, 3))
if mibBuilder.loadTexts:
    l2tpDomainStatsTable.setDescription('The L2TP Domain Status and Statistics table. This\n            table contains objects that can be used to describe\n            the current status and statistics of a tunnel domain.\n            There is a 1-1 correspondence between conceptual\n            rows of this table and conceptual rows of the\n            l2tpDomainConfigTable.')
l2tpDomainStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1))
l2tpDomainConfigEntry.registerAugmentions(('L2TP-MIB', 'l2tpDomainStatsEntry'))
l2tpDomainStatsEntry.setIndexNames(*l2tpDomainConfigEntry.getIndexNames())
if mibBuilder.loadTexts:
    l2tpDomainStatsEntry.setDescription('An L2TP Domain Stats entry. An entry in this table\n            may correspond to a single endpoint or a group of\n            tunnel endpoints.')
l2tpDomainStatsTotalTunnels = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 1), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsTotalTunnels.setDescription('This object returns the total number of tunnels\n            that have successfully reached the established\n            state for this tunnel domain.')
l2tpDomainStatsFailedTunnels = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 2), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsFailedTunnels.setDescription("This object returns the number of tunnels that\n            failed (eg: connection timeout, unsupported\n            or malformed AVP's etc) to reach the established\n            state for this tunnel domain.")
l2tpDomainStatsFailedAuths = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsFailedAuths.setDescription('This object returns the number of failed tunnel\n            connection attempts for this domain because the\n            tunnel peer failed authentication.')
l2tpDomainStatsActiveTunnels = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 4), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsActiveTunnels.setDescription('This object returns the number of tunnels that\n            are currently active for this domain.')
l2tpDomainStatsTotalSessions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsTotalSessions.setDescription('This object returns the total number of sessions\n            that have successfully reached the established\n            state for this tunnel domain.')
l2tpDomainStatsFailedSessions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 6), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsFailedSessions.setDescription("This object returns the number of sessions that\n            failed (eg: connection timeout, unsupported\n            or malformed AVP's etc) to reach the established\n            state for this tunnel domain.")
l2tpDomainStatsActiveSessions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 7), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsActiveSessions.setDescription('This object returns the number of sessions that\n            are currently active for this domain.')
l2tpDomainStatsDrainingTunnels = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsDrainingTunnels.setDescription('This object indicates if this domain is draining\n            off sessions from all tunnels.')
l2tpDomainStatsControlRxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 9), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlRxOctets.setDescription('This object returns the number of control channel\n            octets received for this tunnel domain.')
l2tpDomainStatsControlRxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlRxPkts.setDescription('This object returns the number of control packets\n            received for this tunnel domain.')
l2tpDomainStatsControlTxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlTxOctets.setDescription('This object returns the number of control channel\n            octets that were transmitted to tunnel endpoints\n            for this domain.')
l2tpDomainStatsControlTxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlTxPkts.setDescription('This object returns the number of control packets\n            that were transmitted to tunnel endpoints for\n            this domain.')
l2tpDomainStatsPayloadRxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadRxOctets.setDescription('This object returns the number of payload channel\n            octets that were received for this tunnel domain.')
l2tpDomainStatsPayloadRxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadRxPkts.setDescription('This object returns the number of payload packets\n            that were received for this tunnel domain.')
l2tpDomainStatsPayloadRxDiscs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 15), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadRxDiscs.setDescription('This object returns the number of received payload\n            packets that were discarded by this tunnel domain.')
l2tpDomainStatsPayloadTxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 16), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadTxOctets.setDescription('This object returns the number of payload channel\n            octets that were transmitted to tunnel peers\n            within this tunnel domain.')
l2tpDomainStatsPayloadTxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 17), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadTxPkts.setDescription('This object returns the number of payload packets\n            that were transmitted to tunnel peers within\n            this tunnel domain.')
l2tpDomainStatsControlHCRxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 18), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlHCRxOctets.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsControlRxOctets.')
l2tpDomainStatsControlHCRxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 19), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlHCRxPkts.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsControlRxPkts.')
l2tpDomainStatsControlHCTxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 20), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlHCTxOctets.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsControlTxOctets.')
l2tpDomainStatsControlHCTxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 21), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsControlHCTxPkts.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsControlTxPkts.')
l2tpDomainStatsPayloadHCRxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 22), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadHCRxOctets.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsPayloadRxOctets.')
l2tpDomainStatsPayloadHCRxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 23), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadHCRxPkts.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsPayloadRxPkts.')
l2tpDomainStatsPayloadHCRxDiscs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 24), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadHCRxDiscs.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsPayloadRxDiscs.')
l2tpDomainStatsPayloadHCTxOctets = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 25), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadHCTxOctets.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsPayloadTxOctets.')
l2tpDomainStatsPayloadHCTxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 3, 1, 26), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpDomainStatsPayloadHCTxPkts.setDescription('This object is a 64-bit version of\n            l2tpDomainStatsPayloadTxPkts.')
l2tpTunnelConfigTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 1, 4))
if mibBuilder.loadTexts:
    l2tpTunnelConfigTable.setDescription('The L2TP tunnel configuration table. This\n            table contains objects that can be used to\n            (re)configure the operational characteristics\n            of a single L2TP tunnel. There is a 1-1\n            correspondence between conceptual rows of\n            this table and conceptual rows of the\n            l2tpTunnelStatsTable. Entries in this table\n            have the same persistency characteristics as\n            that of the tunnelConfigTable.')
l2tpTunnelConfigEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1)).setIndexNames((0, 'L2TP-MIB', 'l2tpTunnelConfigIfIndex'))
if mibBuilder.loadTexts:
    l2tpTunnelConfigEntry.setDescription("A L2TP tunnel interface configuration entry.\n            Entries in this table come and go as a result\n            of protocol interactions or on management\n            operations. The latter occurs when a row is\n            instantiated in the tunnelConfigTable row\n            and the encapsulation method is 'l2tp'.")
l2tpTunnelConfigIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    l2tpTunnelConfigIfIndex.setDescription('This value for this object is equal to the value\n            of ifIndex of the Interfaces MIB for tunnel\n            interfaces of type L2TP.')
l2tpTunnelConfigDomainId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 80))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigDomainId.setDescription('The tunnel domain that this tunnel belongs\n            to. A LNS tunnel endpoint will typically inherit\n            this value from the endpoint domain table. A\n            LAC may be provided with this information during\n            tunnel setup. When a zero length string is returned\n            this tunnel does not belong belong to any particular\n            domain.')
l2tpTunnelConfigAuth = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none', 1), ('simple', 2), ('challenge', 3))).clone('none')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigAuth.setDescription("This object describes how L2TP tunnel peers are\n            to be authenticated. The value 'simple' indicates\n            that peers are authenticated simply by their host\n            name as described in the Host Name AVP. The value\n            'challenge' indicates that all peers are challenged\n            to prove their identification. This mechanism is\n            described in the L2TP protocol. This object cannot\n            be modified when the tunnel is in a connecting or\n            connected state.")
l2tpTunnelConfigSecret = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 4), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigSecret.setDescription('This object is used to configure the shared secret\n            used during the tunnel authentication phase of\n\n            tunnel establishment. This object cannot be modified\n            when the tunnel is in a connecting or connected\n            state. This object MUST be accessible only via\n            requests using both authentication and privacy.\n            The agent MUST report an empty string in response\n            to get, get-next and get-bulk requests.')
l2tpTunnelConfigSecurity = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none', 1), ('other', 2), ('ipsec', 3))).clone('none')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigSecurity.setDescription("This object defines whether this tunnel is to be\n            secured. The value of 'ipSec' indicates that all\n            tunnel packets, control and session, have IP\n            Security headers. The type of IP Security headers\n            (AH, ESP etc) and how they are further described\n            is outside the scope of this document. This object\n            cannot be modified when the tunnel is in a connecting\n            or connected state.")
l2tpTunnelConfigHelloInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 3600)).clone(60)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigHelloInterval.setDescription('This object defines the interval in which Hello\n            (or keep-alive) packets are to be sent to the\n            tunnel peer.  The value zero effectively disables\n            the sending of Hello packets. Modifications to this\n            object have immediate effect.')
l2tpTunnelConfigIdleTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 86400))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigIdleTimeout.setDescription('This object defines the period of time that an\n            established tunnel with no sessions will wait\n            before disconnecting the tunnel. A value of\n            zero indicates that the tunnel will disconnect\n            immediately after the last session disconnects.\n            A value of -1 leaves the tunnel up indefinitely.\n            Modifications to this object have immediate\n            effect.')
l2tpTunnelConfigControlRWS = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)).clone(4)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigControlRWS.setDescription('This object defines the control channel receive\n            window size. It specifies the maximum number of\n            packets the tunnel peer can send without waiting\n            for an acknowledgement from this peer. This object\n            cannot be modified when the tunnel is in a con-\n            necting or connected state.')
l2tpTunnelConfigControlMaxRetx = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 32)).clone(5)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigControlMaxRetx.setDescription('This object defines the number of retransmissions\n            which the tunnel will attempt before assuming that\n            the peer is no longer responding. A value of zero\n            indicates that this peer will not attempt to\n            retransmit an unacknowledged control packet.\n            Modifications to this object have immediate\n            effect.')
l2tpTunnelConfigControlMaxRetxTO = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 32)).clone(16)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigControlMaxRetxTO.setDescription('This object defines the maximum retransmission timeout\n            interval which the tunnel will wait before retrans-\n\n            mitting a control packet that has not been acknowledged.\n            Modifications to this object have immediate effect.')
l2tpTunnelConfigPayloadSeq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('onDemand', 1), ('never', 2), ('always', 3))).clone('onDemand')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigPayloadSeq.setDescription('This object determines whether or not session payload\n            packets will be requested to be sent with sequence\n            numbers from tunnel peers belonging to this domain.\n            The value onDemand(1) allows the L2TP implementation\n            to initiate payload sequencing when necessary based\n            on local information (e.g: during LCP/NCP negotiations\n            or for CCP). The value never(2) indicates that L2TP\n            will never initiate sequencing but will do sequencing\n            if asked. The value always(3) indicates that L2TP\n            will send the Sequencing Required AVP during session\n            establishment. Modifications to this object have\n            immediate effect.')
l2tpTunnelConfigReassemblyTO = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 12), L2tpMilliSeconds()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigReassemblyTO.setDescription('This object defines the number of milliseconds that\n            this tunnel will wait before processing payload packets\n            that were received out of sequence (which are waiting\n            for the packet(s) to put them in sequence).  A low value\n            increases the chance of delayed packets to be discarded\n            (which MAY cause the PPP decompression engine to\n            reset) while a high value may cause more queuing and\n            possibly degrade throughput if packets are truly lost.\n            The default value for this object is zero which will\n            result in all delayed packets being lost. Modifications\n            to this object have immediate effect.')
l2tpTunnelConfigTransport = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 13), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('other', 1), ('none', 2), ('udpIp', 3), ('frameRelay', 4), ('atm', 5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigTransport.setDescription("This object defines the underlying transport media\n            that is in use for this tunnel entry. Different tunnel\n            transports may define MIB extensions to the L2TP tunnel\n            table to realize the transport layer. For example if the\n            value of this object is 'udpIp' then the value of ifIndex\n            for this table may be used to determine state from the\n            l2tpUdpStatsTable. This object cannot be modified when\n            the tunnel is in a connecting or connected state.")
l2tpTunnelConfigDrainTunnel = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 14), TruthValue().clone('false')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigDrainTunnel.setDescription("Setting this object to 'true' will prevent any new\n            session from being either initiated or accepted but\n            does NOT disconnect any active sessions for this\n            tunnel. Note that when this occurs the\n            l2tpTunnelStatsDrainingTunnel status object of\n            this tunnel should reflect that it is 'draining'.\n            To cancel a drain this object should be set to\n            false(2).  Setting this object to false(2) when\n            the L2TP objects l2tpDrainTunnels or\n            l2tpDomainConfigDrainTunnels is true(1) has\n            no affect, this tunnels will continue to drain.")
l2tpTunnelConfigProxyPPPAuth = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 4, 1, 15), TruthValue().clone('true')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    l2tpTunnelConfigProxyPPPAuth.setDescription("This object is used to configure the sending\n            or acceptance of the session PPP Proxy\n            Authentication AVP's on the LAC or LNS.")
l2tpTunnelStatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 1, 5))
if mibBuilder.loadTexts:
    l2tpTunnelStatsTable.setDescription('The L2TP tunnel status and statistics table. This\n            table contains objects that can be used to describe\n            the current status and statistics of a single L2TP\n            tunnel. There is a 1-1 correspondence between\n            conceptual rows of this table and conceptual rows of\n            the l2tpTunnelConfigTable.')
l2tpTunnelStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1))
l2tpTunnelConfigEntry.registerAugmentions(('L2TP-MIB', 'l2tpTunnelStatsEntry'))
l2tpTunnelStatsEntry.setIndexNames(*l2tpTunnelConfigEntry.getIndexNames())
if mibBuilder.loadTexts:
    l2tpTunnelStatsEntry.setDescription('An L2TP tunnel interface stats entry.')
l2tpTunnelStatsLocalTID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsLocalTID.setDescription('This object contains the local tunnel Identifier.')
l2tpTunnelStatsRemoteTID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsRemoteTID.setDescription('This object contains the remote tunnel Identifier.')
l2tpTunnelStatsState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('tunnelIdle', 1), ('tunnelConnecting', 2), ('tunnelEstablished', 3), ('tunnelDisconnecting', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsState.setDescription('This field contains the current state of the\n            control tunnel.')
l2tpTunnelStatsInitiated = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('locally', 1), ('remotely', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsInitiated.setDescription('This object indicates whether the tunnel was\n            initiated locally or by the remote tunnel peer.')
l2tpTunnelStatsRemoteHostName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 5), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsRemoteHostName.setDescription('This object contains the host name as discovered\n\n            during the tunnel establishment phase (via the Host\n            Name AVP) of the L2TP peer. If the tunnel is idle\n            this object should maintain its value from the last\n            time it was connected.')
l2tpTunnelStatsRemoteVendorName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 6), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsRemoteVendorName.setDescription("This object identifies the vendor name of the peer's\n            L2TP implementation. If the tunnel is idle this\n            object should maintain its value from the last time\n            it was connected.")
l2tpTunnelStatsRemoteFirmwareRev = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsRemoteFirmwareRev.setDescription("This object contains the tunnel peer's firmware\n            revision number. If the tunnel is idle this object\n            should maintain its value from the last time it\n            was connected.")
l2tpTunnelStatsRemoteProtocolVer = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 8), OctetString().subtype(subtypeSpec=ValueSizeConstraint(2, 2)).setFixedLength(2)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsRemoteProtocolVer.setDescription('This object describes the protocol version and\n            revision of the tunnel peers implementation. The\n            first octet contains the protocol version. The\n            second octet contains the protocol revision.')
l2tpTunnelStatsInitialRemoteRWS = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsInitialRemoteRWS.setDescription("This object contains the initial remote peer's\n            receive window size as indicated by the tunnel peer\n            (in the RWS AVP) during the tunnel establishment\n            phase. If the tunnel is idle this object should\n\n            maintain its value from the last time it was\n            connected.")
l2tpTunnelStatsBearerCaps = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('none', 1), ('digital', 2), ('analog', 3), ('digitalAnalog', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsBearerCaps.setDescription('This object describes the Bearer Capabilities of\n            the tunnel peer. If the tunnel is idle this object\n            should maintain its value from the last time it was\n            connected.')
l2tpTunnelStatsFramingCaps = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('none', 1), ('sync', 2), ('async', 3), ('syncAsync', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsFramingCaps.setDescription('This object describes the Framing Capabilities of\n            the tunnel peer. If the tunnel is idle this object\n            should maintain its value from the last time it was\n            connected.')
l2tpTunnelStatsControlRxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsControlRxPkts.setDescription('This object contains the number of control packets\n            received on the tunnel.')
l2tpTunnelStatsControlRxZLB = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsControlRxZLB.setDescription('This object returns a count of the number of Zero\n            Length Body control packet acknowledgement packets\n            that were received.')
l2tpTunnelStatsControlOutOfSeq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 14), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsControlOutOfSeq.setDescription('This object returns a count of the number of\n            control packets that were not received in the\n            correct order (as per the sequence number)\n            on this tunnel including out of window\n            packets.')
l2tpTunnelStatsControlOutOfWin = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 15), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsControlOutOfWin.setDescription('This object contains the number of control\n            packets that were received outside of the\n            offered receive window. It is implementation\n            specific as to whether these packets are queued\n            or discarded.')
l2tpTunnelStatsControlTxPkts = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 16), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsControlTxPkts.setDescription('This object contains the number of control\n            packets that were transmitted to the tunnel\n            peer.')
l2tpTunnelStatsControlTxZLB = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 17), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsControlTxZLB.setDescription('This object contains the number of Zero Length\n            Body control packets transmitted to the tunnel\n\n            peer.')
l2tpTunnelStatsControlAckTO = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 18), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsControlAckTO.setDescription('This object returns a count of the number of\n            control packet timeouts due to the lack of a\n            timely acknowledgement from the tunnel peer.')
l2tpTunnelStatsCurrentRemoteRWS = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 19), Gauge32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsCurrentRemoteRWS.setDescription('This object contains the current remote receive\n            window size as determined by the local flow\n            control mechanism employed.')
l2tpTunnelStatsTxSeq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 20), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsTxSeq.setDescription('This object contains the next send sequence number\n            for the control channel.')
l2tpTunnelStatsTxSeqAck = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 21), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsTxSeqAck.setDescription('This object contains the send sequence number that\n            the tunnel peer has acknowledged for the control\n            channel. The flow control state can be determined\n            by subtracting the l2tpTunnelStatsTxSeq from\n            l2tpTunnelStatsTxSeqAck and comparing this value\n            to l2tpTunnelStatsCurrentRemoteRWS (taking into\n            consideration sequence number wraps).')
l2tpTunnelStatsRxSeq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 22), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsRxSeq.setDescription('This object contains the next receive sequence\n            number expected to be received on this control\n            channel.')
l2tpTunnelStatsRxSeqAck = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 23), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsRxSeqAck.setDescription('This object contains the last receive sequence\n            number that was acknowledged back to the tunnel\n            peer for the control channel.')
l2tpTunnelStatsTotalSessions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 24), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsTotalSessions.setDescription('This object contains the total number of sessions\n            that this tunnel has successfully connected through\n            to its tunnel peer since this tunnel was created.')
l2tpTunnelStatsFailedSessions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 25), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsFailedSessions.setDescription('This object contains the total number of sessions\n            that were initiated but failed to reach the\n            established phase.')
l2tpTunnelStatsActiveSessions = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 26), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsActiveSessions.setDescription('This object contains the total number of sessions\n            in the established state for this tunnel.')
l2tpTunnelStatsLastResultCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 27), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsLastResultCode.setDescription('This object contains the last value of the result\n            code as described in the Result Code AVP which\n            caused the tunnel to disconnect.')
l2tpTunnelStatsLastErrorCode = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 28), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsLastErrorCode.setDescription('This object contains the last value of the error\n            code as described in the Result Code AVP which\n            caused the tunnel to disconnect.')
l2tpTunnelStatsLastErrorMessage = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 29), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsLastErrorMessage.setDescription('This object contains the last value of the optional\n            message as described in the Result Code AVP which\n            caused the tunnel to disconnect.')
l2tpTunnelStatsDrainingTunnel = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 5, 1, 30), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelStatsDrainingTunnel.setDescription('This object indicates if this tunnel is draining\n            off sessions. This object will return false(2) when\n            the tunnel is not draining sessions or after the\n            last session has disconnected when the tunnel is in\n            the draining state.')
l2tpSessionStatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 1, 7))
if mibBuilder.loadTexts:
    l2tpSessionStatsTable.setDescription('The L2TP session status and statistics table. This\n            table contains the objects that can be used to\n            describe the current status and statistics of a\n            single L2TP tunneled session.')
l2tpSessionStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1)).setIndexNames((0, 'L2TP-MIB', 'l2tpSessionStatsTunnelIfIndex'), (0, 'L2TP-MIB', 'l2tpSessionStatsLocalSID'))
if mibBuilder.loadTexts:
    l2tpSessionStatsEntry.setDescription('An L2TP session interface stats entry.')
l2tpSessionStatsTunnelIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    l2tpSessionStatsTunnelIfIndex.setDescription("This object identifies the session's associated\n            L2TP tunnel ifIndex value.")
l2tpSessionStatsIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 2), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsIfIndex.setDescription('This object identifies the ifIndex value of the\n            interface from which PPP packets are being tunneled.\n            For example this could be a DS0 ifIndex on a\n            LAC or it would be the PPP ifIndex on the LNS.')
l2tpSessionStatsLocalSID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    l2tpSessionStatsLocalSID.setDescription('This object contains the local assigned session\n            identifier for this session.')
l2tpSessionStatsRemoteSID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsRemoteSID.setDescription('This object contains the remote assigned session\n            identifier for this session. When a session is\n            starting this value may be zero until the remote\n            tunnel endpoint has responded.')
l2tpSessionStatsUserName = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 5), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsUserName.setDescription('This object identifies the peer session name on\n            this interface. This is typically the login name\n            of the remote user. If the user name is unknown to\n            the local tunnel peer then this object will contain\n            a null string.')
l2tpSessionStatsState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('sessionIdle', 1), ('sessionConnecting', 2), ('sessionEstablished', 3), ('sessionDisconnecting', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsState.setDescription('This object contains the current state of the\n            session.')
l2tpSessionStatsCallType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('lacIncoming', 1), ('lnsIncoming', 2), ('lacOutgoing', 3), ('lnsOutgoing', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsCallType.setDescription('This object indicates the type of call and the\n            role this tunnel peer is providing for this\n            session. For example, lacIncoming(1) indicates\n            that this tunnel peer is acting as a LAC and\n            generated a Incoming-Call-Request to the tunnel\n            peer (the LNS). Note that tunnel peers can be\n            both LAC and LNS simultaneously.')
l2tpSessionStatsCallSerialNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 8), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsCallSerialNumber.setDescription('This object contains the serial number that has\n            been assigned to this  session.')
l2tpSessionStatsTxConnectSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 9), Unsigned32()).setUnits('bits per second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsTxConnectSpeed.setDescription('This object returns the last known transmit\n            baud rate for this session.')
l2tpSessionStatsRxConnectSpeed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 10), Unsigned32()).setUnits('bits per second').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsRxConnectSpeed.setDescription('This object returns the last known receive\n            baud rate for this session established.')
l2tpSessionStatsCallBearerType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none', 1), ('digital', 2), ('analog', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsCallBearerType.setDescription('This object describes the bearer type of this\n            session.')
l2tpSessionStatsFramingType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('none', 1), ('sync', 2), ('async', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsFramingType.setDescription('This object describes the framing type of this\n            session.')
l2tpSessionStatsPhysChanId = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 13), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsPhysChanId.setDescription('This object contains the physical channel\n            identifier for the session.')
l2tpSessionStatsDNIS = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 14), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsDNIS.setDescription('This object identifies the Dialed Number\n            Information String that the LAC obtained from\n            the network for the session. If no DNIS was\n            provided then a null string will be returned.')
l2tpSessionStatsCLID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 15), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsCLID.setDescription('This object identifies the Calling Line ID\n            that the LAC obtained from the network for\n            the session. If no CLID was provided then a\n            null string will be returned.')
l2tpSessionStatsSubAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 16), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsSubAddress.setDescription('This object identifies the Sub Address that\n            the LAC obtained from the network for the\n            session. If no Sub Address was provided then\n            a null string will be returned.')
l2tpSessionStatsPrivateGroupID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 17), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsPrivateGroupID.setDescription('This object identifies the Private Group\n            Identifier used for this tunneled session.\n            If no Private Group Identifier was provided\n            then a null string will be returned.')
l2tpSessionStatsProxyLcp = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 18), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsProxyLcp.setDescription('Indicates whether the LAC performed proxy LCP\n            for this session.')
l2tpSessionStatsAuthMethod = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 19), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(('none', 1), ('text', 2), ('pppChap', 3), ('pppPap', 4), ('pppEap', 5), ('pppMsChapV1', 6), ('pppMsChapV2', 7), ('other', 8)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsAuthMethod.setDescription('This object contains the proxy authentication\n            method employed by the LAC for the session. If\n            l2tpSessionProxyLcp is false(2) this object\n            should not be interpreted.')
l2tpSessionStatsSequencingState = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 20), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('none', 1), ('remote', 2), ('local', 3), ('both', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsSequencingState.setDescription('This object defines which tunnel peers have\n            requested payload sequencing. The value of\n            both(4) indicates that both peers have requested\n            payload sequencing.')
l2tpSessionStatsOutSequence = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 21), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsOutSequence.setDescription('This object returns the total number of packets\n            received for this session which were received out\n            of sequence.')
l2tpSessionStatsReassemblyTO = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 22), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsReassemblyTO.setDescription('This object returns the number of reassembly\n            timeouts that have occurred for this session.')
l2tpSessionStatsTxSeq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 23), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsTxSeq.setDescription('This object contains the next send sequence number\n            for for this session.')
l2tpSessionStatsRxSeq = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 7, 1, 24), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionStatsRxSeq.setDescription('This object contains the next receive sequence\n            number expected to be received on this session.')
l2tpTunnelMapTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 1, 8))
if mibBuilder.loadTexts:
    l2tpTunnelMapTable.setDescription('The L2TP Tunnel index mapping table. This table\n            is intended to assist management applications\n            to quickly determine what the ifIndex value is\n            for a given local tunnel identifier.')
l2tpTunnelMapEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 1, 8, 1)).setIndexNames((0, 'L2TP-MIB', 'l2tpTunnelMapLocalTID'))
if mibBuilder.loadTexts:
    l2tpTunnelMapEntry.setDescription('An L2TP tunnel index map entry.')
l2tpTunnelMapLocalTID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 8, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    l2tpTunnelMapLocalTID.setDescription('This object contains the local tunnel Identifier.')
l2tpTunnelMapIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 8, 1, 2), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpTunnelMapIfIndex.setDescription('This value for this object is equal to the value\n            of ifIndex of the Interfaces MIB for tunnel\n            interfaces of type L2TP.')
l2tpSessionMapTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 1, 9))
if mibBuilder.loadTexts:
    l2tpSessionMapTable.setDescription('The L2TP Session index mapping table. This table\n            is intended to assist management applications\n            to map interfaces to a tunnel and session\n            identifier.')
l2tpSessionMapEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 1, 9, 1)).setIndexNames((0, 'L2TP-MIB', 'l2tpSessionMapIfIndex'))
if mibBuilder.loadTexts:
    l2tpSessionMapEntry.setDescription('An L2TP Session index map entry.')
l2tpSessionMapIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 9, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    l2tpSessionMapIfIndex.setDescription('This object identifies the ifIndex value of the\n            interface which is receiving or sending its packets\n            over an L2TP tunnel. For example this could be a DS0\n            ifIndex on a LAC or a PPP ifIndex on the LNS.')
l2tpSessionMapTunnelIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 9, 1, 2), InterfaceIndex()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpSessionMapTunnelIfIndex.setDescription('This object identifies the sessions associated\n            L2TP tunnel ifIndex value. When this object is\n            set it provides a binding between a particular\n            interface identified by l2tpSessionMapIfIndex\n            to a particular tunnel.')
l2tpSessionMapLocalSID = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 9, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpSessionMapLocalSID.setDescription('This object contains the local assigned session\n            identifier for this session.')
l2tpSessionMapStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 1, 9, 1, 4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    l2tpSessionMapStatus.setDescription('The status of this session map entry.')
l2tpUdpStatsTable = MibTable((1, 3, 6, 1, 2, 1, 10, 95, 3, 1, 1, 2))
if mibBuilder.loadTexts:
    l2tpUdpStatsTable.setDescription('The L2TP UDP/IP transport stats table. This table\n            contains objects that can be used to describe the\n            current status and statistics of the UDP/IP L2TP\n            tunnel transport.')
l2tpUdpStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 95, 3, 1, 1, 2, 1)).setIndexNames((0, 'L2TP-MIB', 'l2tpUdpStatsIfIndex'))
if mibBuilder.loadTexts:
    l2tpUdpStatsEntry.setDescription('An L2TP UDP/IP transport stats entry.')
l2tpUdpStatsIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 3, 1, 1, 2, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    l2tpUdpStatsIfIndex.setDescription('This value for this object is equal to the\n            value of ifIndex of the Interfaces MIB for\n            tunnel interfaces of type L2TP and which have\n            a L2TP transport of UDP/IP.')
l2tpUdpStatsPeerPort = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 3, 1, 1, 2, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpUdpStatsPeerPort.setDescription("This object reflects the peer's UDP port number\n            used for this tunnel. When not known a value of\n            zero should be returned.")
l2tpUdpStatsLocalPort = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 95, 3, 1, 1, 2, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    l2tpUdpStatsLocalPort.setDescription('This object reflects the local UDP port number\n            that this tunnel is bound to.')
l2tpTunnelAuthFailure = NotificationType((1, 3, 6, 1, 2, 1, 10, 95, 0, 1)).setObjects(*(('L2TP-MIB', 'l2tpTunnelStatsInitiated'), ('L2TP-MIB', 'l2tpTunnelStatsRemoteHostName')))
if mibBuilder.loadTexts:
    l2tpTunnelAuthFailure.setDescription('A l2tpTunnelAuthFailure trap signifies that an\n            attempt to establish a tunnel to a remote peer\n            has failed authentication.')
l2tpGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 4, 1))
l2tpCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 95, 4, 2))
l2tpMIBFullCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 95, 4, 2, 1)).setObjects(*(('L2TP-MIB', 'l2tpConfigGroup'), ('L2TP-MIB', 'l2tpStatsGroup'), ('L2TP-MIB', 'l2tpTrapGroup'), ('L2TP-MIB', 'l2tpIpUdpGroup'), ('L2TP-MIB', 'l2tpDomainGroup'), ('L2TP-MIB', 'l2tpMappingGroup'), ('L2TP-MIB', 'l2tpSecurityGroup'), ('L2TP-MIB', 'l2tpHCPacketGroup')))
if mibBuilder.loadTexts:
    l2tpMIBFullCompliance.setDescription('When this MIB is implemented with support for\n            read-create and read-write, then such an\n\n            implementation can claim full compliance. Such\n            an implementation can then be both monitored\n            and configured with this MIB.')
l2tpMIBReadOnlyCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 95, 4, 2, 2)).setObjects(*(('L2TP-MIB', 'l2tpConfigGroup'), ('L2TP-MIB', 'l2tpStatsGroup'), ('L2TP-MIB', 'l2tpTrapGroup')))
if mibBuilder.loadTexts:
    l2tpMIBReadOnlyCompliance.setDescription('When this MIB is implemented without support for\n            read-create and read-write (i.e. in read-only mode),\n            then such an implementation can claim read-only\n            compliance. Such an implementation can then be\n            monitored but can not be configured with this MIB.')
l2tpConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 1)).setObjects(*(('L2TP-MIB', 'l2tpAdminState'), ('L2TP-MIB', 'l2tpDrainTunnels'), ('L2TP-MIB', 'l2tpTunnelConfigDomainId'), ('L2TP-MIB', 'l2tpTunnelConfigHelloInterval'), ('L2TP-MIB', 'l2tpTunnelConfigIdleTimeout'), ('L2TP-MIB', 'l2tpTunnelConfigControlRWS'), ('L2TP-MIB', 'l2tpTunnelConfigControlMaxRetx'), ('L2TP-MIB', 'l2tpTunnelConfigControlMaxRetxTO'), ('L2TP-MIB', 'l2tpTunnelConfigPayloadSeq'), ('L2TP-MIB', 'l2tpTunnelConfigReassemblyTO'), ('L2TP-MIB', 'l2tpTunnelConfigTransport'), ('L2TP-MIB', 'l2tpTunnelConfigDrainTunnel'), ('L2TP-MIB', 'l2tpTunnelConfigProxyPPPAuth')))
if mibBuilder.loadTexts:
    l2tpConfigGroup.setDescription('A collection of objects providing configuration\n            information of the L2TP protocol, tunnels and\n            sessions.')
l2tpStatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 2)).setObjects(*(('L2TP-MIB', 'l2tpProtocolVersions'), ('L2TP-MIB', 'l2tpVendorName'), ('L2TP-MIB', 'l2tpFirmwareRev'), ('L2TP-MIB', 'l2tpDrainingTunnels'), ('L2TP-MIB', 'l2tpTunnelStatsLocalTID'), ('L2TP-MIB', 'l2tpTunnelStatsRemoteTID'), ('L2TP-MIB', 'l2tpTunnelStatsState'), ('L2TP-MIB', 'l2tpTunnelStatsInitiated'), ('L2TP-MIB', 'l2tpTunnelStatsRemoteHostName'), ('L2TP-MIB', 'l2tpTunnelStatsRemoteVendorName'), ('L2TP-MIB', 'l2tpTunnelStatsRemoteFirmwareRev'), ('L2TP-MIB', 'l2tpTunnelStatsRemoteProtocolVer'), ('L2TP-MIB', 'l2tpTunnelStatsInitialRemoteRWS'), ('L2TP-MIB', 'l2tpTunnelStatsBearerCaps'), ('L2TP-MIB', 'l2tpTunnelStatsFramingCaps'), ('L2TP-MIB', 'l2tpTunnelStatsControlRxPkts'), ('L2TP-MIB', 'l2tpTunnelStatsControlRxZLB'), ('L2TP-MIB', 'l2tpTunnelStatsControlOutOfSeq'), ('L2TP-MIB', 'l2tpTunnelStatsControlOutOfWin'), ('L2TP-MIB', 'l2tpTunnelStatsControlTxPkts'), ('L2TP-MIB', 'l2tpTunnelStatsControlTxZLB'), ('L2TP-MIB', 'l2tpTunnelStatsControlAckTO'), ('L2TP-MIB', 'l2tpTunnelStatsCurrentRemoteRWS'), ('L2TP-MIB', 'l2tpTunnelStatsTxSeq'), ('L2TP-MIB', 'l2tpTunnelStatsTxSeqAck'), ('L2TP-MIB', 'l2tpTunnelStatsRxSeq'), ('L2TP-MIB', 'l2tpTunnelStatsRxSeqAck'), ('L2TP-MIB', 'l2tpTunnelStatsTotalSessions'), ('L2TP-MIB', 'l2tpTunnelStatsFailedSessions'), ('L2TP-MIB', 'l2tpTunnelStatsActiveSessions'), ('L2TP-MIB', 'l2tpTunnelStatsLastResultCode'), ('L2TP-MIB', 'l2tpTunnelStatsLastErrorCode'), ('L2TP-MIB', 'l2tpTunnelStatsLastErrorMessage'), ('L2TP-MIB', 'l2tpTunnelStatsDrainingTunnel'), ('L2TP-MIB', 'l2tpSessionStatsIfIndex'), ('L2TP-MIB', 'l2tpSessionStatsRemoteSID'), ('L2TP-MIB', 'l2tpSessionStatsUserName'), ('L2TP-MIB', 'l2tpSessionStatsState'), ('L2TP-MIB', 'l2tpSessionStatsCallType'), ('L2TP-MIB', 'l2tpSessionStatsCallSerialNumber'), ('L2TP-MIB', 'l2tpSessionStatsTxConnectSpeed'), ('L2TP-MIB', 'l2tpSessionStatsRxConnectSpeed'), ('L2TP-MIB', 'l2tpSessionStatsCallBearerType'), ('L2TP-MIB', 'l2tpSessionStatsFramingType'), ('L2TP-MIB', 'l2tpSessionStatsPhysChanId'), ('L2TP-MIB', 'l2tpSessionStatsDNIS'), ('L2TP-MIB', 'l2tpSessionStatsCLID'), ('L2TP-MIB', 'l2tpSessionStatsSubAddress'), ('L2TP-MIB', 'l2tpSessionStatsPrivateGroupID'), ('L2TP-MIB', 'l2tpSessionStatsProxyLcp'), ('L2TP-MIB', 'l2tpSessionStatsAuthMethod'), ('L2TP-MIB', 'l2tpSessionStatsSequencingState'), ('L2TP-MIB', 'l2tpSessionStatsOutSequence'), ('L2TP-MIB', 'l2tpSessionStatsReassemblyTO'), ('L2TP-MIB', 'l2tpSessionStatsTxSeq'), ('L2TP-MIB', 'l2tpSessionStatsRxSeq')))
if mibBuilder.loadTexts:
    l2tpStatsGroup.setDescription('A collection of objects providing status and\n            statistics of the L2TP protocol, tunnels and\n            sessions.')
l2tpIpUdpGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 3)).setObjects(*(('L2TP-MIB', 'l2tpUdpStatsPeerPort'), ('L2TP-MIB', 'l2tpUdpStatsLocalPort')))
if mibBuilder.loadTexts:
    l2tpIpUdpGroup.setDescription('A collection of objects providing status and\n            statistics of the L2TP UDP/IP transport layer.')
l2tpDomainGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 4)).setObjects(*(('L2TP-MIB', 'l2tpDomainConfigAdminState'), ('L2TP-MIB', 'l2tpDomainConfigDrainTunnels'), ('L2TP-MIB', 'l2tpDomainConfigTunnelHelloInt'), ('L2TP-MIB', 'l2tpDomainConfigTunnelIdleTO'), ('L2TP-MIB', 'l2tpDomainConfigControlRWS'), ('L2TP-MIB', 'l2tpDomainConfigControlMaxRetx'), ('L2TP-MIB', 'l2tpDomainConfigControlMaxRetxTO'), ('L2TP-MIB', 'l2tpDomainConfigPayloadSeq'), ('L2TP-MIB', 'l2tpDomainConfigReassemblyTO'), ('L2TP-MIB', 'l2tpDomainConfigProxyPPPAuth'), ('L2TP-MIB', 'l2tpDomainConfigStorageType'), ('L2TP-MIB', 'l2tpDomainConfigStatus'), ('L2TP-MIB', 'l2tpDomainStatsTotalTunnels'), ('L2TP-MIB', 'l2tpDomainStatsFailedTunnels'), ('L2TP-MIB', 'l2tpDomainStatsFailedAuths'), ('L2TP-MIB', 'l2tpDomainStatsActiveTunnels'), ('L2TP-MIB', 'l2tpDomainStatsTotalSessions'), ('L2TP-MIB', 'l2tpDomainStatsFailedSessions'), ('L2TP-MIB', 'l2tpDomainStatsActiveSessions'), ('L2TP-MIB', 'l2tpDomainStatsDrainingTunnels'), ('L2TP-MIB', 'l2tpDomainStatsControlRxOctets'), ('L2TP-MIB', 'l2tpDomainStatsControlRxPkts'), ('L2TP-MIB', 'l2tpDomainStatsControlTxOctets'), ('L2TP-MIB', 'l2tpDomainStatsControlTxPkts'), ('L2TP-MIB', 'l2tpDomainStatsPayloadRxOctets'), ('L2TP-MIB', 'l2tpDomainStatsPayloadRxPkts'), ('L2TP-MIB', 'l2tpDomainStatsPayloadRxDiscs'), ('L2TP-MIB', 'l2tpDomainStatsPayloadTxOctets'), ('L2TP-MIB', 'l2tpDomainStatsPayloadTxPkts')))
if mibBuilder.loadTexts:
    l2tpDomainGroup.setDescription('A collection of objects providing configuration,\n            status and statistics of L2TP tunnel domains.')
l2tpMappingGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 5)).setObjects(*(('L2TP-MIB', 'l2tpTunnelMapIfIndex'), ('L2TP-MIB', 'l2tpSessionMapTunnelIfIndex'), ('L2TP-MIB', 'l2tpSessionMapLocalSID'), ('L2TP-MIB', 'l2tpSessionMapStatus')))
if mibBuilder.loadTexts:
    l2tpMappingGroup.setDescription('A collection of objects providing index mapping.')
l2tpSecurityGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 6)).setObjects(*(('L2TP-MIB', 'l2tpDomainConfigAuth'), ('L2TP-MIB', 'l2tpDomainConfigSecret'), ('L2TP-MIB', 'l2tpDomainConfigTunnelSecurity'), ('L2TP-MIB', 'l2tpTunnelConfigAuth'), ('L2TP-MIB', 'l2tpTunnelConfigSecret'), ('L2TP-MIB', 'l2tpTunnelConfigSecurity')))
if mibBuilder.loadTexts:
    l2tpSecurityGroup.setDescription('A collection of objects providing L2TP security\n            configuration.')
l2tpTrapGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 7)).setObjects(*(('L2TP-MIB', 'l2tpTunnelAuthFailure'),))
if mibBuilder.loadTexts:
    l2tpTrapGroup.setDescription('A collection of L2TP trap events as specified\n            in NOTIFICATION-TYPE constructs.')
l2tpHCPacketGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 95, 4, 1, 8)).setObjects(*(('L2TP-MIB', 'l2tpDomainStatsControlHCRxOctets'), ('L2TP-MIB', 'l2tpDomainStatsControlHCRxPkts'), ('L2TP-MIB', 'l2tpDomainStatsControlHCTxOctets'), ('L2TP-MIB', 'l2tpDomainStatsControlHCTxPkts'), ('L2TP-MIB', 'l2tpDomainStatsPayloadHCRxOctets'), ('L2TP-MIB', 'l2tpDomainStatsPayloadHCRxPkts'), ('L2TP-MIB', 'l2tpDomainStatsPayloadHCRxDiscs'), ('L2TP-MIB', 'l2tpDomainStatsPayloadHCTxOctets'), ('L2TP-MIB', 'l2tpDomainStatsPayloadHCTxPkts')))
if mibBuilder.loadTexts:
    l2tpHCPacketGroup.setDescription('A collection of objects providing High Capacity\n            64-bit counter objects.')
mibBuilder.exportSymbols('L2TP-MIB', l2tpSessionStatsEntry=l2tpSessionStatsEntry, l2tpDomainConfigPayloadSeq=l2tpDomainConfigPayloadSeq, l2tpMIBFullCompliance=l2tpMIBFullCompliance, l2tpDomainConfigStatus=l2tpDomainConfigStatus, l2tpDomainStatsActiveSessions=l2tpDomainStatsActiveSessions, l2tpDomainStatsPayloadRxDiscs=l2tpDomainStatsPayloadRxDiscs, l2tpTunnelStatsControlTxPkts=l2tpTunnelStatsControlTxPkts, l2tpUdpStatsEntry=l2tpUdpStatsEntry, l2tpDomainConfigStorageType=l2tpDomainConfigStorageType, l2tpTunnelStatsControlRxZLB=l2tpTunnelStatsControlRxZLB, l2tpTunnelStatsLastErrorCode=l2tpTunnelStatsLastErrorCode, l2tpTunnelStatsEntry=l2tpTunnelStatsEntry, l2tpTunnelStatsFailedSessions=l2tpTunnelStatsFailedSessions, l2tpSessionStatsCallBearerType=l2tpSessionStatsCallBearerType, l2tpDomainStatsFailedSessions=l2tpDomainStatsFailedSessions, l2tpDomainConfigAuth=l2tpDomainConfigAuth, l2tpSessionStatsUserName=l2tpSessionStatsUserName, l2tpConformance=l2tpConformance, l2tpSessionStatsTxConnectSpeed=l2tpSessionStatsTxConnectSpeed, l2tpTunnelMapLocalTID=l2tpTunnelMapLocalTID, l2tpAdminState=l2tpAdminState, l2tpSessionMapTunnelIfIndex=l2tpSessionMapTunnelIfIndex, l2tpDomainConfigControlMaxRetxTO=l2tpDomainConfigControlMaxRetxTO, l2tpTunnelStatsDrainingTunnel=l2tpTunnelStatsDrainingTunnel, l2tpDomainStatsPayloadHCRxOctets=l2tpDomainStatsPayloadHCRxOctets, l2tpSessionMapStatus=l2tpSessionMapStatus, l2tpDomainStatsPayloadHCRxDiscs=l2tpDomainStatsPayloadHCRxDiscs, l2tpTunnelConfigReassemblyTO=l2tpTunnelConfigReassemblyTO, l2tpTunnelStatsRemoteFirmwareRev=l2tpTunnelStatsRemoteFirmwareRev, l2tpTunnelStatsRemoteVendorName=l2tpTunnelStatsRemoteVendorName, l2tpUdpStatsIfIndex=l2tpUdpStatsIfIndex, l2tpScalar=l2tpScalar, l2tpDomainStatsControlHCTxOctets=l2tpDomainStatsControlHCTxOctets, l2tpTunnelMapEntry=l2tpTunnelMapEntry, L2tpMilliSeconds=L2tpMilliSeconds, l2tpDomainStatsPayloadTxOctets=l2tpDomainStatsPayloadTxOctets, l2tpDomainConfigId=l2tpDomainConfigId, l2tpSessionStatsTxSeq=l2tpSessionStatsTxSeq, l2tpTunnelConfigTransport=l2tpTunnelConfigTransport, l2tpGroups=l2tpGroups, l2tpDomainConfigDrainTunnels=l2tpDomainConfigDrainTunnels, l2tpDomainStatsPayloadHCTxPkts=l2tpDomainStatsPayloadHCTxPkts, l2tpTunnelStatsControlTxZLB=l2tpTunnelStatsControlTxZLB, l2tpDomainStatsTable=l2tpDomainStatsTable, l2tpTunnelConfigHelloInterval=l2tpTunnelConfigHelloInterval, l2tpTunnelConfigDrainTunnel=l2tpTunnelConfigDrainTunnel, l2tpDomainConfigTunnelIdleTO=l2tpDomainConfigTunnelIdleTO, l2tpTunnelMapTable=l2tpTunnelMapTable, l2tpDomainStatsControlHCRxOctets=l2tpDomainStatsControlHCRxOctets, l2tpObjects=l2tpObjects, l2tpDomainStatsEntry=l2tpDomainStatsEntry, l2tpDomainStatsPayloadTxPkts=l2tpDomainStatsPayloadTxPkts, l2tpDomainConfigTable=l2tpDomainConfigTable, l2tpTunnelConfigSecurity=l2tpTunnelConfigSecurity, l2tpVendorName=l2tpVendorName, l2tpSessionStatsTunnelIfIndex=l2tpSessionStatsTunnelIfIndex, l2tpTunnelConfigProxyPPPAuth=l2tpTunnelConfigProxyPPPAuth, l2tpTrapGroup=l2tpTrapGroup, l2tpCompliances=l2tpCompliances, l2tpDomainConfigProxyPPPAuth=l2tpDomainConfigProxyPPPAuth, l2tpDomainGroup=l2tpDomainGroup, l2tpDomainConfigEntry=l2tpDomainConfigEntry, l2tpTunnelStatsTable=l2tpTunnelStatsTable, l2tpTunnelStatsRxSeqAck=l2tpTunnelStatsRxSeqAck, l2tpSessionStatsAuthMethod=l2tpSessionStatsAuthMethod, l2tpDomainConfigSecret=l2tpDomainConfigSecret, l2tpTunnelStatsActiveSessions=l2tpTunnelStatsActiveSessions, l2tpSessionStatsRxSeq=l2tpSessionStatsRxSeq, l2tpDomainStatsFailedTunnels=l2tpDomainStatsFailedTunnels, l2tpDomainStatsPayloadRxOctets=l2tpDomainStatsPayloadRxOctets, l2tpDomainStatsPayloadHCRxPkts=l2tpDomainStatsPayloadHCRxPkts, l2tpTunnelStatsCurrentRemoteRWS=l2tpTunnelStatsCurrentRemoteRWS, l2tpTunnelConfigPayloadSeq=l2tpTunnelConfigPayloadSeq, l2tpTunnelConfigControlMaxRetx=l2tpTunnelConfigControlMaxRetx, l2tpDomainStatsControlTxPkts=l2tpDomainStatsControlTxPkts, l2tpTunnelStatsLocalTID=l2tpTunnelStatsLocalTID, l2tpDomainConfigControlMaxRetx=l2tpDomainConfigControlMaxRetx, l2tpDomainStatsTotalSessions=l2tpDomainStatsTotalSessions, l2tpSessionStatsTable=l2tpSessionStatsTable, l2tpTunnelStatsLastResultCode=l2tpTunnelStatsLastResultCode, l2tpNotifications=l2tpNotifications, l2tpDomainStatsTotalTunnels=l2tpDomainStatsTotalTunnels, l2tpDomainStatsActiveTunnels=l2tpDomainStatsActiveTunnels, l2tpTunnelStatsTxSeq=l2tpTunnelStatsTxSeq, l2tpSessionStatsProxyLcp=l2tpSessionStatsProxyLcp, l2tpMappingGroup=l2tpMappingGroup, l2tpDomainConfigTunnelSecurity=l2tpDomainConfigTunnelSecurity, l2tpIpUdpGroup=l2tpIpUdpGroup, l2tpDomainStatsControlRxPkts=l2tpDomainStatsControlRxPkts, l2tpSessionStatsLocalSID=l2tpSessionStatsLocalSID, PYSNMP_MODULE_ID=l2tp, l2tpHCPacketGroup=l2tpHCPacketGroup, l2tpDomainStatsPayloadHCTxOctets=l2tpDomainStatsPayloadHCTxOctets, l2tpSessionStatsReassemblyTO=l2tpSessionStatsReassemblyTO, l2tpDomainConfigAdminState=l2tpDomainConfigAdminState, l2tpConfigGroup=l2tpConfigGroup, l2tpTunnelStatsBearerCaps=l2tpTunnelStatsBearerCaps, l2tpDomainStatsControlRxOctets=l2tpDomainStatsControlRxOctets, l2tpIpUdpObjects=l2tpIpUdpObjects, l2tpTunnelConfigEntry=l2tpTunnelConfigEntry, l2tpSessionStatsPrivateGroupID=l2tpSessionStatsPrivateGroupID, l2tpDrainTunnels=l2tpDrainTunnels, l2tpDomainStatsDrainingTunnels=l2tpDomainStatsDrainingTunnels, l2tpTunnelConfigControlRWS=l2tpTunnelConfigControlRWS, l2tpDomainStatsPayloadRxPkts=l2tpDomainStatsPayloadRxPkts, l2tpTunnelStatsControlAckTO=l2tpTunnelStatsControlAckTO, l2tpStatsGroup=l2tpStatsGroup, l2tpSessionMapEntry=l2tpSessionMapEntry, l2tpSessionStatsFramingType=l2tpSessionStatsFramingType, l2tpMIBReadOnlyCompliance=l2tpMIBReadOnlyCompliance, l2tpTunnelStatsRemoteTID=l2tpTunnelStatsRemoteTID, l2tpSessionStatsPhysChanId=l2tpSessionStatsPhysChanId, l2tpSessionStatsRemoteSID=l2tpSessionStatsRemoteSID, l2tpDomainStatsFailedAuths=l2tpDomainStatsFailedAuths, l2tpUdpStatsPeerPort=l2tpUdpStatsPeerPort, l2tpSessionStatsOutSequence=l2tpSessionStatsOutSequence, l2tpProtocolVersions=l2tpProtocolVersions, l2tpConfig=l2tpConfig, l2tpSessionMapIfIndex=l2tpSessionMapIfIndex, l2tpTunnelConfigControlMaxRetxTO=l2tpTunnelConfigControlMaxRetxTO, l2tpSessionStatsSubAddress=l2tpSessionStatsSubAddress, l2tpSessionStatsDNIS=l2tpSessionStatsDNIS, l2tpTunnelAuthFailure=l2tpTunnelAuthFailure, l2tpTunnelConfigSecret=l2tpTunnelConfigSecret, l2tpTunnelConfigDomainId=l2tpTunnelConfigDomainId, l2tpTunnelStatsFramingCaps=l2tpTunnelStatsFramingCaps, l2tpTunnelStatsControlRxPkts=l2tpTunnelStatsControlRxPkts, l2tpTunnelStatsRemoteProtocolVer=l2tpTunnelStatsRemoteProtocolVer, l2tpSessionStatsState=l2tpSessionStatsState, l2tpTunnelStatsLastErrorMessage=l2tpTunnelStatsLastErrorMessage, l2tpSessionStatsCLID=l2tpSessionStatsCLID, l2tpDrainingTunnels=l2tpDrainingTunnels, l2tpTunnelConfigTable=l2tpTunnelConfigTable, l2tpSessionStatsCallSerialNumber=l2tpSessionStatsCallSerialNumber, l2tpStats=l2tpStats, l2tpDomainConfigReassemblyTO=l2tpDomainConfigReassemblyTO, l2tpDomainConfigControlRWS=l2tpDomainConfigControlRWS, l2tpTunnelConfigAuth=l2tpTunnelConfigAuth, l2tpTunnelStatsRemoteHostName=l2tpTunnelStatsRemoteHostName, l2tpSessionMapLocalSID=l2tpSessionMapLocalSID, l2tpTunnelStatsInitialRemoteRWS=l2tpTunnelStatsInitialRemoteRWS, l2tpTunnelStatsInitiated=l2tpTunnelStatsInitiated, l2tpSessionStatsSequencingState=l2tpSessionStatsSequencingState, l2tpDomainStatsControlHCRxPkts=l2tpDomainStatsControlHCRxPkts, l2tpUdpStatsTable=l2tpUdpStatsTable, l2tpTunnelConfigIdleTimeout=l2tpTunnelConfigIdleTimeout, l2tpTunnelStatsRxSeq=l2tpTunnelStatsRxSeq, l2tpTunnelStatsTotalSessions=l2tpTunnelStatsTotalSessions, l2tpDomainConfigTunnelHelloInt=l2tpDomainConfigTunnelHelloInt, l2tpFirmwareRev=l2tpFirmwareRev, l2tpTunnelStatsControlOutOfSeq=l2tpTunnelStatsControlOutOfSeq, l2tpTunnelStatsState=l2tpTunnelStatsState, l2tpUdpStatsLocalPort=l2tpUdpStatsLocalPort, l2tpTransportIpUdp=l2tpTransportIpUdp, l2tpSecurityGroup=l2tpSecurityGroup, l2tpSessionStatsIfIndex=l2tpSessionStatsIfIndex, l2tpDomainStatsControlHCTxPkts=l2tpDomainStatsControlHCTxPkts, l2tpTunnelStatsControlOutOfWin=l2tpTunnelStatsControlOutOfWin, l2tpSessionStatsRxConnectSpeed=l2tpSessionStatsRxConnectSpeed, l2tpIpUdpTraps=l2tpIpUdpTraps, l2tpDomainStatsControlTxOctets=l2tpDomainStatsControlTxOctets, l2tpSessionStatsCallType=l2tpSessionStatsCallType, l2tpTransports=l2tpTransports, l2tpTunnelConfigIfIndex=l2tpTunnelConfigIfIndex, l2tpSessionMapTable=l2tpSessionMapTable, l2tpTunnelMapIfIndex=l2tpTunnelMapIfIndex, l2tpTunnelStatsTxSeqAck=l2tpTunnelStatsTxSeqAck, l2tp=l2tp)