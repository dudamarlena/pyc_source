# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/BGP4-MIB.py
# Compiled at: 2016-02-13 18:06:31
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ConstraintsUnion', 'SingleValueConstraint')
(ObjectGroup, NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'NotificationGroup', 'ModuleCompliance')
(MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, IpAddress, Counter32, Unsigned32, Bits, Gauge32, Integer32, ModuleIdentity, MibIdentifier, mib_2, TimeTicks, ObjectIdentity, iso, NotificationType) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64', 'IpAddress', 'Counter32', 'Unsigned32', 'Bits', 'Gauge32', 'Integer32', 'ModuleIdentity', 'MibIdentifier', 'mib-2', 'TimeTicks', 'ObjectIdentity', 'iso', 'NotificationType')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
bgp = ModuleIdentity((1, 3, 6, 1, 2, 1, 15)).setRevisions(('2006-01-11 00:00', '1994-05-05 00:00', '1991-10-26 18:39'))
if mibBuilder.loadTexts:
    bgp.setLastUpdated('200601110000Z')
if mibBuilder.loadTexts:
    bgp.setOrganization('IETF IDR Working Group')
if mibBuilder.loadTexts:
    bgp.setContactInfo('E-mail:  idr@ietf.org\n\n                          Jeffrey Haas, Susan Hares  (Editors)\n                          NextHop Technologies\n                          825 Victors Way\n                          Suite 100\n                          Ann Arbor, MI 48108-2738\n                          Tel: +1 734 222-1600\n                          Fax: +1 734 222-1602\n                          E-mail: jhaas@nexthop.com\n                                  skh@nexthop.com')
if mibBuilder.loadTexts:
    bgp.setDescription('The MIB module for the BGP-4 protocol.\n\n                     Copyright (C) The Internet Society (2006).  This\n                     version of this MIB module is part of RFC 4273;\n                     see the RFC itself for full legal notices.')
bgpVersion = MibScalar((1, 3, 6, 1, 2, 1, 15, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(1, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpVersion.setDescription('Vector of supported BGP protocol version\n                     numbers.  Each peer negotiates the version\n                     from this vector.  Versions are identified\n                     via the string of bits contained within this\n                     object.  The first octet contains bits 0 to\n                     7, the second octet contains bits 8 to 15,\n                     and so on, with the most significant bit\n                     referring to the lowest bit number in the\n                     octet (e.g., the MSB of the first octet\n                     refers to bit 0).  If a bit, i, is present\n                     and set, then the version (i+1) of the BGP\n                     is supported.')
bgpLocalAs = MibScalar((1, 3, 6, 1, 2, 1, 15, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpLocalAs.setDescription('The local autonomous system number.')
bgpPeerTable = MibTable((1, 3, 6, 1, 2, 1, 15, 3))
if mibBuilder.loadTexts:
    bgpPeerTable.setDescription('BGP peer table.  This table contains,\n                     one entry per BGP peer, information about the\n                     connections with BGP peers.')
bgpPeerEntry = MibTableRow((1, 3, 6, 1, 2, 1, 15, 3, 1)).setIndexNames((0, 'BGP4-MIB', 'bgpPeerRemoteAddr'))
if mibBuilder.loadTexts:
    bgpPeerEntry.setDescription('Entry containing information about the\n                     connection with a BGP peer.')
bgpPeerIdentifier = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 1), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerIdentifier.setDescription("The BGP Identifier of this entry's BGP peer.\n                     This entry MUST be 0.0.0.0 unless the\n                     bgpPeerState is in the openconfirm or the\n                     established state.")
bgpPeerState = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('idle', 1), ('connect', 2), ('active', 3), ('opensent', 4), ('openconfirm', 5), ('established', 6)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerState.setDescription('The BGP peer connection state.')
bgpPeerAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('stop', 1), ('start', 2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    bgpPeerAdminStatus.setDescription("The desired state of the BGP connection.\n                     A transition from 'stop' to 'start' will cause\n                     the BGP Manual Start Event to be generated.\n                     A transition from 'start' to 'stop' will cause\n                     the BGP Manual Stop Event to be generated.\n                     This parameter can be used to restart BGP peer\n                     connections.  Care should be used in providing\n                     write access to this object without adequate\n                     authentication.")
bgpPeerNegotiatedVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 4), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerNegotiatedVersion.setDescription('The negotiated version of BGP running between\n                     the two peers.\n\n                     This entry MUST be zero (0) unless the\n                     bgpPeerState is in the openconfirm or the\n                     established state.\n\n                     Note that legal values for this object are\n                     between 0 and 255.')
bgpPeerLocalAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 5), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerLocalAddr.setDescription("The local IP address of this entry's BGP\n                     connection.")
bgpPeerLocalPort = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerLocalPort.setDescription('The local port for the TCP connection between\n                     the BGP peers.')
bgpPeerRemoteAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 7), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerRemoteAddr.setDescription("The remote IP address of this entry's BGP\n                     peer.")
bgpPeerRemotePort = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerRemotePort.setDescription('The remote port for the TCP connection\n                     between the BGP peers.  Note that the\n                     objects bgpPeerLocalAddr,\n                     bgpPeerLocalPort, bgpPeerRemoteAddr, and\n                     bgpPeerRemotePort provide the appropriate\n                     reference to the standard MIB TCP\n                     connection table.')
bgpPeerRemoteAs = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerRemoteAs.setDescription('The remote autonomous system number received in\n                     the BGP OPEN message.')
bgpPeerInUpdates = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 10), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerInUpdates.setDescription('The number of BGP UPDATE messages\n                     received on this connection.')
bgpPeerOutUpdates = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 11), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerOutUpdates.setDescription('The number of BGP UPDATE messages\n                     transmitted on this connection.')
bgpPeerInTotalMessages = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 12), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerInTotalMessages.setDescription('The total number of messages received\n                     from the remote peer on this connection.')
bgpPeerOutTotalMessages = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 13), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerOutTotalMessages.setDescription('The total number of messages transmitted to\n                     the remote peer on this connection.')
bgpPeerLastError = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 14), OctetString().subtype(subtypeSpec=ValueSizeConstraint(2, 2)).setFixedLength(2)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerLastError.setDescription('The last error code and subcode seen by this\n                     peer on this connection.  If no error has\n                     occurred, this field is zero.  Otherwise, the\n                     first byte of this two byte OCTET STRING\n                     contains the error code, and the second byte\n                     contains the subcode.')
bgpPeerFsmEstablishedTransitions = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 15), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerFsmEstablishedTransitions.setDescription('The total number of times the BGP FSM\n                     transitioned into the established state\n                     for this peer.')
bgpPeerFsmEstablishedTime = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 16), Gauge32()).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerFsmEstablishedTime.setDescription('This timer indicates how long (in\n                     seconds) this peer has been in the\n                     established state or how long\n                     since this peer was last in the\n                     established state.  It is set to zero when\n                     a new peer is configured or when the router is\n                     booted.')
bgpPeerConnectRetryInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 17), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    bgpPeerConnectRetryInterval.setDescription('Time interval (in seconds) for the\n                     ConnectRetry timer.  The suggested value\n                     for this timer is 120 seconds.')
bgpPeerHoldTime = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 18), Integer32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0, 0), ValueRangeConstraint(3, 65535)))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerHoldTime.setDescription('Time interval (in seconds) for the Hold\n                     Timer established with the peer.  The\n                     value of this object is calculated by this\n                     BGP speaker, using the smaller of the\n                     values in bgpPeerHoldTimeConfigured and the\n                     Hold Time received in the OPEN message.\n\n                     This value must be at least three seconds\n                     if it is not zero (0).\n\n                     If the Hold Timer has not been established\n                     with the peer this object MUST have a value\n                     of zero (0).\n\n                     If the bgpPeerHoldTimeConfigured object has\n                     a value of (0), then this object MUST have a\n                     value of (0).')
bgpPeerKeepAlive = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 19), Integer32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0, 0), ValueRangeConstraint(1, 21845)))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerKeepAlive.setDescription('Time interval (in seconds) for the KeepAlive\n                     timer established with the peer.  The value\n                     of this object is calculated by this BGP\n                     speaker such that, when compared with\n                     bgpPeerHoldTime, it has the same proportion\n                     that bgpPeerKeepAliveConfigured has,\n                     compared with bgpPeerHoldTimeConfigured.\n\n                     If the KeepAlive timer has not been established\n                     with the peer, this object MUST have a value\n                     of zero (0).\n\n                     If the of bgpPeerKeepAliveConfigured object\n                     has a value of (0), then this object MUST have\n                     a value of (0).')
bgpPeerHoldTimeConfigured = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 20), Integer32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0, 0), ValueRangeConstraint(3, 65535)))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    bgpPeerHoldTimeConfigured.setDescription('Time interval (in seconds) for the Hold Time\n                     configured for this BGP speaker with this\n                     peer.  This value is placed in an OPEN\n                     message sent to this peer by this BGP\n                     speaker, and is compared with the Hold\n                     Time field in an OPEN message received\n                     from the peer when determining the Hold\n                     Time (bgpPeerHoldTime) with the peer.\n                     This value must not be less than three\n                     seconds if it is not zero (0).  If it is\n                     zero (0), the Hold Time is NOT to be\n                     established with the peer.  The suggested\n                     value for this timer is 90 seconds.')
bgpPeerKeepAliveConfigured = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 21), Integer32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0, 0), ValueRangeConstraint(1, 21845)))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    bgpPeerKeepAliveConfigured.setDescription("Time interval (in seconds) for the\n                     KeepAlive timer configured for this BGP\n                     speaker with this peer.  The value of this\n                     object will only determine the\n                     KEEPALIVE messages' frequency relative to\n                     the value specified in\n                     bgpPeerHoldTimeConfigured; the actual\n                     time interval for the KEEPALIVE messages is\n                     indicated by bgpPeerKeepAlive.  A\n                     reasonable maximum value for this timer\n                     would be one third of that of\n                     bgpPeerHoldTimeConfigured.\n                     If the value of this object is zero (0),\n                     no periodical KEEPALIVE messages are sent\n                     to the peer after the BGP connection has\n                     been established.  The suggested value for\n                     this timer is 30 seconds.")
bgpPeerMinASOriginationInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 22), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    bgpPeerMinASOriginationInterval.setDescription('Time interval (in seconds) for the\n                     MinASOriginationInterval timer.\n                     The suggested value for this timer is 15\n                     seconds.')
bgpPeerMinRouteAdvertisementInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 23), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    bgpPeerMinRouteAdvertisementInterval.setDescription('Time interval (in seconds) for the\n                     MinRouteAdvertisementInterval timer.\n                     The suggested value for this timer is 30\n                     seconds for EBGP connections and 5\n                     seconds for IBGP connections.')
bgpPeerInUpdateElapsedTime = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 3, 1, 24), Gauge32()).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPeerInUpdateElapsedTime.setDescription('Elapsed time (in seconds) since the last BGP\n                     UPDATE message was received from the peer.\n                     Each time bgpPeerInUpdates is incremented,\n                     the value of this object is set to zero (0).')
bgpIdentifier = MibScalar((1, 3, 6, 1, 2, 1, 15, 4), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpIdentifier.setDescription('The BGP Identifier of the local system.')
bgpRcvdPathAttrTable = MibTable((1, 3, 6, 1, 2, 1, 15, 5))
if mibBuilder.loadTexts:
    bgpRcvdPathAttrTable.setDescription('The BGP Received Path Attribute Table\n                     contains information about paths to\n                     destination networks, received from all\n                     peers running BGP version 3 or less.')
bgpPathAttrEntry = MibTableRow((1, 3, 6, 1, 2, 1, 15, 5, 1)).setIndexNames((0, 'BGP4-MIB', 'bgpPathAttrDestNetwork'), (0, 'BGP4-MIB', 'bgpPathAttrPeer'))
if mibBuilder.loadTexts:
    bgpPathAttrEntry.setDescription('Information about a path to a network.')
bgpPathAttrPeer = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 5, 1, 1), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPathAttrPeer.setDescription('The IP address of the peer where the path\n                     information was learned.')
bgpPathAttrDestNetwork = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 5, 1, 2), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPathAttrDestNetwork.setDescription('The address of the destination network.')
bgpPathAttrOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 5, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('igp', 1), ('egp', 2), ('incomplete', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPathAttrOrigin.setDescription('The ultimate origin of the path information.')
bgpPathAttrASPath = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 5, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(2, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPathAttrASPath.setDescription('The set of ASes that must be traversed to reach\n                     the network.  This object is probably best\n                     represented as SEQUENCE OF INTEGER.  For SMI\n                     compatibility, though, it is represented as\n                     OCTET STRING.  Each AS is represented as a pair\n                     of octets according to the following algorithm:\n\n                        first-byte-of-pair = ASNumber / 256;\n                        second-byte-of-pair = ASNumber & 255;')
bgpPathAttrNextHop = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 5, 1, 5), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPathAttrNextHop.setDescription('The address of the border router that should\n                     be used for the destination network.')
bgpPathAttrInterASMetric = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 5, 1, 6), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgpPathAttrInterASMetric.setDescription('The optional inter-AS metric.  If this\n                     attribute has not been provided for this route,\n                     the value for this object is 0.')
bgp4PathAttrTable = MibTable((1, 3, 6, 1, 2, 1, 15, 6))
if mibBuilder.loadTexts:
    bgp4PathAttrTable.setDescription('The BGP-4 Received Path Attribute Table\n                     contains information about paths to\n                     destination networks, received from all\n                     BGP4 peers.')
bgp4PathAttrEntry = MibTableRow((1, 3, 6, 1, 2, 1, 15, 6, 1)).setIndexNames((0, 'BGP4-MIB', 'bgp4PathAttrIpAddrPrefix'), (0, 'BGP4-MIB', 'bgp4PathAttrIpAddrPrefixLen'), (0, 'BGP4-MIB', 'bgp4PathAttrPeer'))
if mibBuilder.loadTexts:
    bgp4PathAttrEntry.setDescription('Information about a path to a network.')
bgp4PathAttrPeer = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 1), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrPeer.setDescription('The IP address of the peer where the path\n                     information was learned.')
bgp4PathAttrIpAddrPrefixLen = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 32))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrIpAddrPrefixLen.setDescription('Length in bits of the IP address prefix in\n                     the Network Layer Reachability\n                     Information field.')
bgp4PathAttrIpAddrPrefix = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 3), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrIpAddrPrefix.setDescription('An IP address prefix in the Network Layer\n                     Reachability Information field.  This object\n                     is an IP address containing the prefix with\n                     length specified by\n                     bgp4PathAttrIpAddrPrefixLen.\n                     Any bits beyond the length specified by\n                     bgp4PathAttrIpAddrPrefixLen are zeroed.')
bgp4PathAttrOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('igp', 1), ('egp', 2), ('incomplete', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrOrigin.setDescription('The ultimate origin of the path\n                     information.')
bgp4PathAttrASPathSegment = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(2, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrASPathSegment.setDescription('The sequence of AS path segments.  Each AS\n                     path segment is represented by a triple\n                     <type, length, value>.\n\n                     The type is a 1-octet field that has two\n                     possible values:\n                         1      AS_SET: unordered set of ASes that a\n                                     route in the UPDATE message\n                                     has traversed\n\n                         2      AS_SEQUENCE: ordered set of ASes that\n                                     a route in the UPDATE message\n                                     has traversed.\n\n                     The length is a 1-octet field containing the\n                     number of ASes in the value field.\n\n                     The value field contains one or more AS\n                     numbers.  Each AS is represented in the octet\n                     string as a pair of octets according to the\n                     following algorithm:\n\n                        first-byte-of-pair = ASNumber / 256;\n                        second-byte-of-pair = ASNumber & 255;\n\n                     Known Issues:\n                     o BGP Confederations will result in\n                       a type of either 3 or 4.\n                     o An AS Path may be longer than 255 octets.\n                       This may result in this object containing\n                       a truncated AS Path.')
bgp4PathAttrNextHop = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 6), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrNextHop.setDescription('The address of the border router that\n                     should be used for the destination\n                     network.  This address is the NEXT_HOP\n                     address received in the UPDATE packet.')
bgp4PathAttrMultiExitDisc = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrMultiExitDisc.setDescription('This metric is used to discriminate\n                     between multiple exit points to an\n                     adjacent autonomous system.  A value of -1\n                     indicates the absence of this attribute.\n\n                     Known Issues:\n                     o The BGP-4 specification uses an\n                       unsigned 32 bit number.  Thus, this\n                       object cannot represent the full\n                       range of the protocol.')
bgp4PathAttrLocalPref = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrLocalPref.setDescription("The originating BGP4 speaker's degree of\n                     preference for an advertised route.  A\n                     value of -1 indicates the absence of this\n                     attribute.\n\n                     Known Issues:\n                     o The BGP-4 specification uses an\n                       unsigned 32 bit number and thus this\n                       object cannot represent the full\n                       range of the protocol.")
bgp4PathAttrAtomicAggregate = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('lessSpecificRouteNotSelected', 1), ('lessSpecificRouteSelected', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrAtomicAggregate.setDescription("If the ATOMIC_AGGREGATE attribute is present\n                     in the Path Attributes then this object MUST\n                     have a value of 'lessSpecificRouteNotSelected'.\n\n                     If the ATOMIC_AGGREGATE attribute is missing\n                     in the Path Attributes then this object MUST\n                     have a value of 'lessSpecificRouteSelected'.\n\n                     Note that ATOMIC_AGGREGATE is now a primarily\n                     informational attribute.")
bgp4PathAttrAggregatorAS = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrAggregatorAS.setDescription('The AS number of the last BGP4 speaker that\n                     performed route aggregation.  A value of\n                     zero (0) indicates the absence of this\n                     attribute.\n\n                     Note that propagation of AS of zero is illegal\n                     in the Internet.')
bgp4PathAttrAggregatorAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 11), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrAggregatorAddr.setDescription('The IP address of the last BGP4 speaker\n                     that performed route aggregation.  A\n                     value of 0.0.0.0 indicates the absence\n                     of this attribute.')
bgp4PathAttrCalcLocalPref = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrCalcLocalPref.setDescription('The degree of preference calculated by the\n                     receiving BGP4 speaker for an advertised\n                     route.  A value of -1 indicates the\n                     absence of this attribute.\n\n                     Known Issues:\n                     o The BGP-4 specification uses an\n                       unsigned 32 bit number and thus this\n                       object cannot represent the full\n                       range of the protocol.')
bgp4PathAttrBest = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 13), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('false', 1), ('true', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrBest.setDescription('An indication of whether this route\n                     was chosen as the best BGP4 route for this\n                     destination.')
bgp4PathAttrUnknown = MibTableColumn((1, 3, 6, 1, 2, 1, 15, 6, 1, 14), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    bgp4PathAttrUnknown.setDescription('One or more path attributes not understood by\n                     this BGP4 speaker.\n\n                     Path attributes are recorded in the Update Path\n                     attribute format of type, length, value.\n\n                     Size zero (0) indicates the absence of such\n                     attributes.\n\n                     Octets beyond the maximum size, if any, are not\n                     recorded by this object.\n\n                     Known Issues:\n                     o Attributes understood by this speaker, but not\n                       represented in this MIB, are unavailable to\n                       the agent.')
bgpNotification = MibIdentifier((1, 3, 6, 1, 2, 1, 15, 0))
bgpEstablishedNotification = NotificationType((1, 3, 6, 1, 2, 1, 15, 0, 1)).setObjects(*(('BGP4-MIB', 'bgpPeerRemoteAddr'), ('BGP4-MIB', 'bgpPeerLastError'), ('BGP4-MIB', 'bgpPeerState')))
if mibBuilder.loadTexts:
    bgpEstablishedNotification.setDescription('The bgpEstablishedNotification event is generated\n                     when the BGP FSM enters the established state.\n\n                     This Notification replaces the bgpEstablished\n                     Notification.')
bgpBackwardTransNotification = NotificationType((1, 3, 6, 1, 2, 1, 15, 0, 2)).setObjects(*(('BGP4-MIB', 'bgpPeerRemoteAddr'), ('BGP4-MIB', 'bgpPeerLastError'), ('BGP4-MIB', 'bgpPeerState')))
if mibBuilder.loadTexts:
    bgpBackwardTransNotification.setDescription('The bgpBackwardTransNotification event is\n                     generated when the BGP FSM moves from a higher\n                     numbered state to a lower numbered state.\n\n                     This Notification replaces the\n                     bgpBackwardsTransition Notification.')
bgpTraps = MibIdentifier((1, 3, 6, 1, 2, 1, 15, 7))
bgpEstablished = NotificationType((1, 3, 6, 1, 2, 1, 15, 7, 1)).setObjects(*(('BGP4-MIB', 'bgpPeerLastError'), ('BGP4-MIB', 'bgpPeerState')))
if mibBuilder.loadTexts:
    bgpEstablished.setDescription('The bgpEstablished event is generated when\n                     the BGP FSM enters the established state.\n\n                     This Notification has been replaced by the\n                     bgpEstablishedNotification Notification.')
bgpBackwardTransition = NotificationType((1, 3, 6, 1, 2, 1, 15, 7, 2)).setObjects(*(('BGP4-MIB', 'bgpPeerLastError'), ('BGP4-MIB', 'bgpPeerState')))
if mibBuilder.loadTexts:
    bgpBackwardTransition.setDescription('The bgpBackwardTransition event is generated\n                     when the BGP FSM moves from a higher numbered\n                     state to a lower numbered state.\n\n                     This Notification has been replaced by the\n                     bgpBackwardTransNotification Notification.')
bgp4MIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 15, 8))
bgp4MIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 15, 8, 1))
bgp4MIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 15, 8, 2))
bgp4MIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 15, 8, 1, 1)).setObjects(*(('BGP4-MIB', 'bgp4MIBGlobalsGroup'), ('BGP4-MIB', 'bgp4MIBPeerGroup'), ('BGP4-MIB', 'bgp4MIBPathAttrGroup'), ('BGP4-MIB', 'bgp4MIBNotificationGroup')))
if mibBuilder.loadTexts:
    bgp4MIBCompliance.setDescription('The compliance statement for entities which\n                     implement the BGP4 mib.')
bgp4MIBDeprecatedCompliances = ModuleCompliance((1, 3, 6, 1, 2, 1, 15, 8, 1, 2)).setObjects(*(('BGP4-MIB', 'bgp4MIBTrapGroup'),))
if mibBuilder.loadTexts:
    bgp4MIBDeprecatedCompliances.setDescription('The compliance statement documenting deprecated\n                     objects in the BGP4 mib.')
bgp4MIBObsoleteCompliances = ModuleCompliance((1, 3, 6, 1, 2, 1, 15, 8, 1, 3)).setObjects(*(('BGP4-MIB', 'bgpRcvdPathAttrGroup'),))
if mibBuilder.loadTexts:
    bgp4MIBObsoleteCompliances.setDescription('The compliance statement documenting obsolete\n                     objects in the BGP4 mib.')
bgp4MIBGlobalsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 15, 8, 2, 1)).setObjects(*(('BGP4-MIB', 'bgpVersion'), ('BGP4-MIB', 'bgpLocalAs'), ('BGP4-MIB', 'bgpIdentifier')))
if mibBuilder.loadTexts:
    bgp4MIBGlobalsGroup.setDescription('A collection of objects providing\n                     information on global BGP state.')
bgp4MIBPeerGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 15, 8, 2, 2)).setObjects(*(('BGP4-MIB', 'bgpPeerIdentifier'), ('BGP4-MIB', 'bgpPeerState'), ('BGP4-MIB', 'bgpPeerAdminStatus'), ('BGP4-MIB', 'bgpPeerNegotiatedVersion'), ('BGP4-MIB', 'bgpPeerLocalAddr'), ('BGP4-MIB', 'bgpPeerLocalPort'), ('BGP4-MIB', 'bgpPeerRemoteAddr'), ('BGP4-MIB', 'bgpPeerRemotePort'), ('BGP4-MIB', 'bgpPeerRemoteAs'), ('BGP4-MIB', 'bgpPeerInUpdates'), ('BGP4-MIB', 'bgpPeerOutUpdates'), ('BGP4-MIB', 'bgpPeerInTotalMessages'), ('BGP4-MIB', 'bgpPeerOutTotalMessages'), ('BGP4-MIB', 'bgpPeerLastError'), ('BGP4-MIB', 'bgpPeerFsmEstablishedTransitions'), ('BGP4-MIB', 'bgpPeerFsmEstablishedTime'), ('BGP4-MIB', 'bgpPeerConnectRetryInterval'), ('BGP4-MIB', 'bgpPeerHoldTime'), ('BGP4-MIB', 'bgpPeerKeepAlive'), ('BGP4-MIB', 'bgpPeerHoldTimeConfigured'), ('BGP4-MIB', 'bgpPeerKeepAliveConfigured'), ('BGP4-MIB', 'bgpPeerMinASOriginationInterval'), ('BGP4-MIB', 'bgpPeerMinRouteAdvertisementInterval'), ('BGP4-MIB', 'bgpPeerInUpdateElapsedTime')))
if mibBuilder.loadTexts:
    bgp4MIBPeerGroup.setDescription('A collection of objects for managing\n                     BGP peers.')
bgpRcvdPathAttrGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 15, 8, 2, 3)).setObjects(*(('BGP4-MIB', 'bgpPathAttrPeer'), ('BGP4-MIB', 'bgpPathAttrDestNetwork'), ('BGP4-MIB', 'bgpPathAttrOrigin'), ('BGP4-MIB', 'bgpPathAttrASPath'), ('BGP4-MIB', 'bgpPathAttrNextHop'), ('BGP4-MIB', 'bgpPathAttrInterASMetric')))
if mibBuilder.loadTexts:
    bgpRcvdPathAttrGroup.setDescription('A collection of objects for managing BGP-3 and\n                    earlier path entries.\n\n                    This conformance group, like BGP-3, is obsolete.')
bgp4MIBPathAttrGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 15, 8, 2, 4)).setObjects(*(('BGP4-MIB', 'bgp4PathAttrPeer'), ('BGP4-MIB', 'bgp4PathAttrIpAddrPrefixLen'), ('BGP4-MIB', 'bgp4PathAttrIpAddrPrefix'), ('BGP4-MIB', 'bgp4PathAttrOrigin'), ('BGP4-MIB', 'bgp4PathAttrASPathSegment'), ('BGP4-MIB', 'bgp4PathAttrNextHop'), ('BGP4-MIB', 'bgp4PathAttrMultiExitDisc'), ('BGP4-MIB', 'bgp4PathAttrLocalPref'), ('BGP4-MIB', 'bgp4PathAttrAtomicAggregate'), ('BGP4-MIB', 'bgp4PathAttrAggregatorAS'), ('BGP4-MIB', 'bgp4PathAttrAggregatorAddr'), ('BGP4-MIB', 'bgp4PathAttrCalcLocalPref'), ('BGP4-MIB', 'bgp4PathAttrBest'), ('BGP4-MIB', 'bgp4PathAttrUnknown')))
if mibBuilder.loadTexts:
    bgp4MIBPathAttrGroup.setDescription('A collection of objects for managing\n                     BGP path entries.')
bgp4MIBTrapGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 15, 8, 2, 5)).setObjects(*(('BGP4-MIB', 'bgpEstablished'), ('BGP4-MIB', 'bgpBackwardTransition')))
if mibBuilder.loadTexts:
    bgp4MIBTrapGroup.setDescription('A collection of notifications for signaling\n                     changes in BGP peer relationships.\n\n                     Obsoleted by bgp4MIBNotificationGroup')
bgp4MIBNotificationGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 15, 8, 2, 6)).setObjects(*(('BGP4-MIB', 'bgpEstablishedNotification'), ('BGP4-MIB', 'bgpBackwardTransNotification')))
if mibBuilder.loadTexts:
    bgp4MIBNotificationGroup.setDescription('A collection of notifications for signaling\n                     changes in BGP peer relationships.\n\n                     Obsoletes bgp4MIBTrapGroup.')
mibBuilder.exportSymbols('BGP4-MIB', bgpTraps=bgpTraps, bgp4PathAttrASPathSegment=bgp4PathAttrASPathSegment, bgpPeerLocalAddr=bgpPeerLocalAddr, bgp4MIBGlobalsGroup=bgp4MIBGlobalsGroup, bgpNotification=bgpNotification, bgpEstablished=bgpEstablished, bgp=bgp, bgpPeerRemoteAs=bgpPeerRemoteAs, bgpPeerMinASOriginationInterval=bgpPeerMinASOriginationInterval, bgp4PathAttrBest=bgp4PathAttrBest, bgpPathAttrEntry=bgpPathAttrEntry, bgpPeerLocalPort=bgpPeerLocalPort, bgpPeerFsmEstablishedTransitions=bgpPeerFsmEstablishedTransitions, bgpPeerLastError=bgpPeerLastError, bgpPeerInUpdates=bgpPeerInUpdates, bgpPeerKeepAlive=bgpPeerKeepAlive, bgpPeerInTotalMessages=bgpPeerInTotalMessages, bgpPeerRemotePort=bgpPeerRemotePort, bgpVersion=bgpVersion, bgp4PathAttrIpAddrPrefix=bgp4PathAttrIpAddrPrefix, bgpPeerTable=bgpPeerTable, bgpPeerHoldTimeConfigured=bgpPeerHoldTimeConfigured, bgpPathAttrDestNetwork=bgpPathAttrDestNetwork, bgp4PathAttrCalcLocalPref=bgp4PathAttrCalcLocalPref, bgpBackwardTransition=bgpBackwardTransition, bgpPeerFsmEstablishedTime=bgpPeerFsmEstablishedTime, bgp4MIBCompliance=bgp4MIBCompliance, bgpPeerOutTotalMessages=bgpPeerOutTotalMessages, bgp4PathAttrIpAddrPrefixLen=bgp4PathAttrIpAddrPrefixLen, bgpPeerEntry=bgpPeerEntry, bgp4PathAttrOrigin=bgp4PathAttrOrigin, bgp4MIBCompliances=bgp4MIBCompliances, bgp4PathAttrLocalPref=bgp4PathAttrLocalPref, bgp4MIBDeprecatedCompliances=bgp4MIBDeprecatedCompliances, bgp4PathAttrUnknown=bgp4PathAttrUnknown, bgpLocalAs=bgpLocalAs, bgpPathAttrNextHop=bgpPathAttrNextHop, bgp4MIBPeerGroup=bgp4MIBPeerGroup, bgpPathAttrASPath=bgpPathAttrASPath, bgpPeerNegotiatedVersion=bgpPeerNegotiatedVersion, bgp4PathAttrNextHop=bgp4PathAttrNextHop, bgpPeerState=bgpPeerState, bgpRcvdPathAttrGroup=bgpRcvdPathAttrGroup, bgp4MIBObsoleteCompliances=bgp4MIBObsoleteCompliances, bgpRcvdPathAttrTable=bgpRcvdPathAttrTable, bgp4PathAttrAggregatorAddr=bgp4PathAttrAggregatorAddr, bgpPeerInUpdateElapsedTime=bgpPeerInUpdateElapsedTime, bgpPeerRemoteAddr=bgpPeerRemoteAddr, bgp4PathAttrTable=bgp4PathAttrTable, bgp4MIBPathAttrGroup=bgp4MIBPathAttrGroup, bgpPeerOutUpdates=bgpPeerOutUpdates, bgpPeerMinRouteAdvertisementInterval=bgpPeerMinRouteAdvertisementInterval, bgpPathAttrInterASMetric=bgpPathAttrInterASMetric, bgpPeerKeepAliveConfigured=bgpPeerKeepAliveConfigured, bgpPeerConnectRetryInterval=bgpPeerConnectRetryInterval, bgp4PathAttrMultiExitDisc=bgp4PathAttrMultiExitDisc, bgp4MIBNotificationGroup=bgp4MIBNotificationGroup, bgp4MIBConformance=bgp4MIBConformance, bgpPathAttrPeer=bgpPathAttrPeer, bgp4PathAttrEntry=bgp4PathAttrEntry, bgpPathAttrOrigin=bgpPathAttrOrigin, bgp4MIBTrapGroup=bgp4MIBTrapGroup, bgpBackwardTransNotification=bgpBackwardTransNotification, PYSNMP_MODULE_ID=bgp, bgpPeerIdentifier=bgpPeerIdentifier, bgpIdentifier=bgpIdentifier, bgp4PathAttrAggregatorAS=bgp4PathAttrAggregatorAS, bgp4PathAttrPeer=bgp4PathAttrPeer, bgpEstablishedNotification=bgpEstablishedNotification, bgp4MIBGroups=bgp4MIBGroups, bgp4PathAttrAtomicAggregate=bgp4PathAttrAtomicAggregate, bgpPeerHoldTime=bgpPeerHoldTime, bgpPeerAdminStatus=bgpPeerAdminStatus)