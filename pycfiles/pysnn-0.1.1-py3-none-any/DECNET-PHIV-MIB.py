# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/DECNET-PHIV-MIB.py
# Compiled at: 2016-02-13 18:07:15
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueSizeConstraint, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsIntersection', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueSizeConstraint', 'ValueRangeConstraint')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Bits, NotificationType, Counter32, ModuleIdentity, mib_2, Gauge32, ObjectIdentity, IpAddress, Integer32, iso, TimeTicks, Unsigned32, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, Counter64) = mibBuilder.importSymbols('SNMPv2-SMI', 'Bits', 'NotificationType', 'Counter32', 'ModuleIdentity', 'mib-2', 'Gauge32', 'ObjectIdentity', 'IpAddress', 'Integer32', 'iso', 'TimeTicks', 'Unsigned32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'MibIdentifier', 'Counter64')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
phiv = MibIdentifier((1, 3, 6, 1, 2, 1, 18))

class PhivAddr(OctetString):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(2, 2)
    fixedLength = 2


class PhivCounter(Integer32):
    __module__ = __name__


class InterfaceIndex(Integer32):
    __module__ = __name__


phivSystem = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 1))
phivManagement = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 2))
session = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 3))
end = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 4))
routing = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 5))
circuit = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 6))
ddcmp = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 7))
control = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 8))
ethernet = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 9))
counters = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 10))
adjacency = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 11))
line = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 12))
nonBroadcastLine = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 14))
area = MibIdentifier((1, 3, 6, 1, 2, 1, 18, 15))
phivSystemState = MibScalar((1, 3, 6, 1, 2, 1, 18, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('on',
                                                                                                                                                                              1), ('off',
                                                                                                                                                                                   2), ('shut',
                                                                                                                                                                                        3), ('restricted',
                                                                                                                                                                                             4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivSystemState.setDescription('This represents the operational state of the executor\n            node.\n            The possible states are:\n            ON          Allows logical links.\n            OFF         Allows no new links, terminates existing\n                        links, and stops routing traffic through.\n            SHUT        Allows no new logical links, does not\n                        destroy existing logical links, and goes\n                        to the OFF state when all logical links are\n                        gone.\n\n            RESTRICTED  Allows no new incoming logical links from\n                        other nodes.\n\n            NOTE: These values are incremented by one compared to\n            the standard DECnet values in order to maintain\n            compliance with RFC 1155).')
phivExecIdent = MibScalar((1, 3, 6, 1, 2, 1, 18, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 32))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivExecIdent.setDescription("This is a text string that describes the executor node\n            (for example, 'Research Lab').  The string is up to 32\n            characters of any type.")
phivMgmtMgmtVers = MibScalar((1, 3, 6, 1, 2, 1, 18, 2, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivMgmtMgmtVers.setDescription('This is the read-only Network Management Version,\n            consisting of the version number, the Engineering\n            Change Order (ECO) number, and the user ECO number\n            (for example, 3.0.0). This parameter applies to the\n            executor node only.')
phivSessionSystemName = MibScalar((1, 3, 6, 1, 2, 1, 18, 3, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 6))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivSessionSystemName.setDescription('Name to be associated with the node identification.\n            Only one name can be assigned to a node address or a\n            circuit identification. No name should be used more than\n            once in a DECnet network. Node-name is one to six upper\n            case alphanumeric characters with at least one alpha\n            character. A length of 0 indicates no name.')
phivSessionInTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 3, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivSessionInTimer.setDescription('This value represents the maximum duration between the\n            time a connect is received for a process at the\n            executor node and the time that process accepts or\n            rejects it. If the connect is not accepted or rejected\n            by the user within the number of seconds specified,\n            Session Control rejects it for the user.  A value of 0\n            indicates no timer is running.')
phivSessionOutTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 3, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivSessionOutTimer.setDescription('This value represents the duration between the time the\n            executor requests a connect and the time that connect is\n            acknowledged by the destination node. If the connect is\n            not acknowledged within the number of seconds\n            specified, Session Control returns an error.  A value of 0\n            indicates no timer is running.')
phivEndRemoteTable = MibTable((1, 3, 6, 1, 2, 1, 18, 4, 1))
if mibBuilder.loadTexts:
    phivEndRemoteTable.setDescription('Information about the state of sessions between the\n            node under study and the nodes found in the table.')
phivEndRemoteEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 4, 1, 1)).setIndexNames((0,
                                                                                 'DECNET-PHIV-MIB',
                                                                                 'phivEndRemoteHostNodeID'))
if mibBuilder.loadTexts:
    phivEndRemoteEntry.setDescription('Information about a particular remote node as seen\n            from the end communication layer.')
phivEndRemoteHostNodeID = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 1, 1, 1), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndRemoteHostNodeID.setDescription('This value is the address of the remote node to be\n            evaluated.')
phivEndRemoteState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('on',
                                                                                                                                                                                            1), ('off',
                                                                                                                                                                                                 2), ('shut',
                                                                                                                                                                                                      3), ('restricted',
                                                                                                                                                                                                           4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndRemoteState.setDescription('This represents the operational state of the remote node\n            being evaluated.\n            The possible states are:\n\n            ON          Allows logical links.\n            OFF         Allows no new links, terminates existing\n                        links, and stops routing traffic through.\n            SHUT        Allows no new logical links, does not\n                        destroy existing logical links, and goes\n                        to the OFF state when all logical links are\n                        gone.\n            RESTRICTED  Allows no new incoming logical links from\n                        other nodes.\n\n            NOTE: These values are incremented by one compared to\n            the standard DECnet values in order to maintain\n            compliance with RFC 1155.')
phivEndCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCircuitIndex.setDescription('A unique index value for each known circuit used to\n            communicate with the remote node.  This is the same\n            value as phivCircuitIndex.')
phivEndActiveLinks = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndActiveLinks.setDescription('This read-only parameter represents the number of active\n            logical links from the executor to the destination node.')
phivEndDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 1, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndDelay.setDescription('This read-only parameter is the average round trip\n            delay in seconds to the destination node. This\n            parameter is kept on a remote node basis.')
phivEndCountTable = MibTable((1, 3, 6, 1, 2, 1, 18, 4, 2))
if mibBuilder.loadTexts:
    phivEndCountTable.setDescription('Information about the counters associated with each end\n            system that is known to the entity. These counters\n            reflect totals from the perspective of the executor\n            node.')
phivEndCountEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 4, 2, 1)).setIndexNames((0,
                                                                                'DECNET-PHIV-MIB',
                                                                                'phivEndCountHostNodeID'))
if mibBuilder.loadTexts:
    phivEndCountEntry.setDescription('Information about a particular session between two end\n            systems.')
phivEndCountHostNodeID = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 1), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountHostNodeID.setDescription('This value is the address of the remote node to be\n            evaluated.')
phivEndCountSecsLastZeroed = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 2), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountSecsLastZeroed.setDescription('This value is the number of seconds that have elapsed\n            since the counters for the node in this table row were\n            last set to zero. This counter is located in the\n            network management layer, but is returned with the\n            end system information which follows.')
phivEndCountUsrBytesRec = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 3), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountUsrBytesRec.setDescription('Number of user bytes received from the target host.')
phivEndCountUsrBytesSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 4), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountUsrBytesSent.setDescription('Number of user bytes sent to the target host.')
phivEndUCountUsrMessRec = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 5), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndUCountUsrMessRec.setDescription('Number of user messages received from the target host.')
phivEndCountUsrMessSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 6), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountUsrMessSent.setDescription('Number of user messages sent to the target host.')
phivEndCountTotalBytesRec = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 7), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountTotalBytesRec.setDescription('Number of bytes received from the target host.')
phivEndCountTotalBytesSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 8), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountTotalBytesSent.setDescription('Number of bytes sent to the target host.')
phivEndCountTotalMessRec = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 9), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountTotalMessRec.setDescription('Number of messages received from the target host.')
phivEndCountTotalMessSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 10), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountTotalMessSent.setDescription('Number of messages sent to the target host.')
phivEndCountConnectsRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 11), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountConnectsRecd.setDescription('Number of connects received from the target host.')
phivEndCountConnectsSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 12), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountConnectsSent.setDescription('Number of connects sent to the target host.')
phivEndCountReponseTimeouts = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 13), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountReponseTimeouts.setDescription('Number of response timeouts.')
phivEndCountRecdConnectResErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 4, 2, 1, 14), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndCountRecdConnectResErrs.setDescription('Number of received connect resource errors.')
phivEndMaxLinks = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndMaxLinks.setDescription('This value represents the maximum active logical\n            link count allowed for the executor.')
phivEndNSPVers = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 4), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEndNSPVers.setDescription('This read-only parameter represents the version number\n            of the node End Communication S/W. The format is\n            version number, ECO, and user ECO, e.g., 4.1.0')
phivEndRetransmitFactor = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndRetransmitFactor.setDescription('This value represents the maximum number of times the\n            source End Communication at the executor node will\n            restart the retransmission timer when it expires. If\n            the number is exceeded, Session Control disconnects the\n            logical link for the user.')
phivEndDelayFact = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndDelayFact.setDescription('This is the number by which to multiply one sixteenth\n            of the estimated round trip delay to a node to set the\n            retransmission timer to that node.')
phivEndDelayWeight = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndDelayWeight.setDescription('This number represents the weight to apply to a\n            current round trip delay estimate to a remote node\n            when updating the estimated round trip delay to a node.\n            On some systems the number must be 1 less than a power\n            of 2 for computational efficiency.')
phivEndInactivityTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndInactivityTimer.setDescription('This value represents the maximum duration of inactivity\n            (no data in either direction) on a logical link before\n            the node checks to see if the logical link still works.\n            If no activity occurs within the minimum number of\n            seconds, End Communication generates artificial\n            traffic to test the link (End Communication\n            specification).')
phivEndCountZeroCount = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                              1), ('reset',
                                                                                                                                                                                   2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndCountZeroCount.setDescription('When this value is set to 2, all of the counters in\n            the End System Counter Table are set to zero.')
phivEndMaxLinksActive = MibScalar((1, 3, 6, 1, 2, 1, 18, 4, 10), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEndMaxLinksActive.setDescription('This value represents the high water mark for the\n            number of links that were active at any one time.')
phivRouteBroadcastRouteTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteBroadcastRouteTimer.setDescription('This value determines the maximum time in seconds\n             allowed between Routing updates on Ethernet\n             circuits. When this timer expired before a routing\n             update occurs, a routing update is forced.  With a\n             standard calculation, Routing also uses this timer\n             to enforce a minimum delay between routing updates.')
phivRouteBuffSize = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteBuffSize.setDescription('This parameter value determines the maximum size of\n             a Routing message. It therefore determines the maximum\n             size message that can be forwarded.  This size includes\n             protocol overhead down to and including the End\n             Communication layer, plus a constant value of 6. (This\n             value of 6 is included to provide compatibility with\n             the parameter definition in Phase III, which included\n             the Routing overhead.) It does not include Routing or\n             Data link overhead (except for the constant value of\n             6). There is one buffer size for all circuits.\n\n             NOTE: The BUFFER SIZE defines the maximum size messages\n             that the Routing layer can forward. The SEGMENT BUFFER\n             SIZE (defined below) defines the maximum size messages\n             that the End Communication layer can transmit or\n             receive. The SEGMENT BUFFER SIZE is always less than\n             or equal to the BUFFER SIZE. Normally the two\n             parameters will be equal. They may be different to\n             allow the network manager to alter buffer sizes\n             on all nodes without interruption of service. They both\n             include an extra 6 bytes for compatibility with Phase\n             III.')
phivRouteRoutingVers = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteRoutingVers.setDescription("This read-only parameter identifies the executor node's\n            Routing version number.  The format is version number,\n            ECO, and user ECO, e.g., 4.1.0")
phivRouteMaxAddr = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1023))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxAddr.setDescription("This value represents the largest node number and,\n            therefore, number of nodes that can be known about\n            by the executor node's home area.")
phivRouteMaxBdcastNonRouters = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxBdcastNonRouters.setDescription('This value represents the maximum total number of\n            nonrouters the executor node can have on its Ethernet\n            circuits.')
phivRouteMaxBdcastRouters = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxBdcastRouters.setDescription('This value represents the maximum total number of\n            routers the executor node can have on its Ethernet\n            circuits.')
phivRouteMaxBuffs = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxBuffs.setDescription('This value represents the maximum number of transmit\n            buffers that Routing may use for all circuits.')
phivRouteMaxCircuits = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxCircuits.setDescription('This value represents the maximum number of Routing\n            circuits that the executor node can know about.')
phivRouteMaxCost = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1022))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxCost.setDescription("This value represents the maximum total path cost\n            allowed from the executor to any node within an area.\n            The path cost is the sum of the circuit costs along\n            a path between two nodes. This parameter defines the\n            point where the executor node's Routing routing\n            decision algorithm declares another node unreachable\n            because the cost of the least costly path to the\n            other node is excessive. For correct operation, this\n            parameter must not be less than the maximum path cost\n            of the network.")
phivRouteMaxHops = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 30))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxHops.setDescription("This value represents the maximum number of routing hops\n            allowable from the executor to any other reachable node\n            within an area. (A hop is the logical distance over a\n            circuit between two adjacent nodes.) This parameter\n            defines the point where the executor node's Routing\n            routing decision algorithm declares another node\n            unreachable because the length of the shortest path\n            between the two nodes is too long. For correct\n            operation, this parameter must not be less than the\n            network diameter. (The network diameter is the\n            reachability distance between the two nodes of the\n            network having the greatest reachability distance,\n            where reachability distance is the length the shortest\n            path between a given pair of nodes.)")
phivRouteMaxVisits = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 63))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxVisits.setDescription('This value represents the maximum number of nodes a\n            message coming into the executor node can have visited.\n            If the message is not for this node and the MAXIMUM\n            VISITS number is exceeded, the message is discarded.\n            The MAXIMUM VISITS parameter defines the point where\n            the packet lifetime control algorithm discards\n            a packet that has traversed too many nodes. For correct\n            operation, this parameter must not be less than the\n            maximum path length of the network. (The maximum path\n            length is the routing distance between the two nodes of\n            the network having the greatest routing distance, where\n            routing distance is the length of the least costly\n            path between a given pair of nodes.)')
phivRouteRoutingTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteRoutingTimer.setDescription('This value determines the maximum time in seconds\n            allowed between Routing updates on non-Ethernet\n            circuits. When this timer expires before a routing\n            update occurs, a routing update is forced.')
phivRouteSegBuffSize = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 13), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteSegBuffSize.setDescription('This parameter value determines the maximum size of an\n            end-to-end segment. The size is a decimal integer in\n            the range 1-65535. This size is in bytes. This size\n            includes protocol overhead down to and including the\n            End Communication layer, plus a constant value of 6.\n            (This value of 6 is included to provide compatibility\n            with the BUFFER SIZE parameter definition.) It does not\n            include Routing or Data link overhead (except for the\n            constant value of 6).')
phivRouteType = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 14), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('routing-III',
                                                                                                                                                                                1), ('nonrouting-III',
                                                                                                                                                                                     2), ('area',
                                                                                                                                                                                          3), ('routing-IV',
                                                                                                                                                                                               4), ('nonrouting-IV',
                                                                                                                                                                                                    5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteType.setDescription('This parameter indicates the type of the executor\n            node. The node-type is one of the following:\n\n            routing-III\n            nonrouting-III\n            routing-IV\n            ronrouting-IV\n            area\n\n            A routing node has full routing capability. A\n            nonrouting node contains a subset of the Routing\n            routing modules. The III and IV indicate the DNA\n            phase of the node. Nonrouting nodes can deliver\n            and receive packets to and from any node, but cannot\n            route packets from other nodes through to other nodes.\n            An area node routes between areas. Refer to the Routing\n            specification for details.\n            For adjacent nodes, this is a read-only parameter that\n            indicates the type of the reachable adjacent node.\n            NOTE: The ROUTING-III and NONROUTING-III values are\n            incremented by one compared to the standard DECnet\n            values in order to maintain compliance with RFC 1155)')
phivRouteCountAgedPktLoss = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 15), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteCountAgedPktLoss.setDescription('Number of aged packet losses.')
phivRouteCountNodeUnrPktLoss = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 16), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteCountNodeUnrPktLoss.setDescription('Number of node unreachable packet losses.')
phivRouteCountOutRngePktLoss = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 17), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteCountOutRngePktLoss.setDescription('Number of node out-of-range packet losses.')
phivRouteCountOverSzePktLoss = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 18), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteCountOverSzePktLoss.setDescription('Number of Oversized packet losses.')
phivRouteCountPacketFmtErr = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 19), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteCountPacketFmtErr.setDescription('Number of packet format errors.')
phivRouteCountPtlRteUpdtLoss = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 20), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteCountPtlRteUpdtLoss.setDescription('Number of partial routing update losses.')
phivRouteCountVerifReject = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 21), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteCountVerifReject.setDescription('Number of verification rejects.')
phivLevel1RouteTable = MibTable((1, 3, 6, 1, 2, 1, 18, 5, 22))
if mibBuilder.loadTexts:
    phivLevel1RouteTable.setDescription('Information about the currently known DECnet Phase\n            IV Routes.')
phivLevel1RouteEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 5, 22, 1)).setIndexNames((0,
                                                                                    'DECNET-PHIV-MIB',
                                                                                    'phivLevel1RouteNodeAddr'))
if mibBuilder.loadTexts:
    phivLevel1RouteEntry.setDescription('Information about the currently known DECnet Phase\n            IV Routes.')
phivLevel1RouteNodeAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 5, 22, 1, 1), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLevel1RouteNodeAddr.setDescription('This value is the address of the node about which\n            routing information is contained in this level 1\n            routing table.')
phivLevel1RouteCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 5, 22, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLevel1RouteCircuitIndex.setDescription('A unique index value for each known circuit. This is\n            the index to the circuit state table and is the same\n            value as phivCircuitIndex.')
phivLevel1RouteCost = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 5, 22, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLevel1RouteCost.setDescription('This read-only parameter represents the total cost\n            over the current path to the destination node. Cost is\n            a positive integer value associated with using a\n            circuit. Routing routes messages (data) along the path\n            between two nodes with the smallest cost. COST is kept\n            on a remote node basis.')
phivLevel1RouteHops = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 5, 22, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 127))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLevel1RouteHops.setDescription('This read-only parameter represents the number of hops\n            over to a destination node. A hop is Routing value\n            representing the logical distance between two nodes in\n            a network. HOPS is kept on a remote node basis.')
phivLevel1RouteNextNode = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 5, 22, 1, 5), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLevel1RouteNextNode.setDescription('This read-only value indicates the next node on the\n            circuit used to get to the node under scrutiny\n            (next hop).')
phivRouteCountZeroCount = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 23), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                 1), ('reset',
                                                                                                                                                                                      2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteCountZeroCount.setDescription('When this value is set to 2, the following objects are\n            set to Zero: phivRouteCountAgedPktLoss,\n            phivRouteCountNodeUnrPktLoss,\n            phivRouteCountOutRngePktLoss,\n            phivRouteCountOverSzePktLoss,\n            phivRouteCountPacketFmtErr,\n            phivRouteCountPtlRteUpdtLoss, and\n            phivRouteCountVerifReject.')
phivRouteSystemAddr = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 24), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivRouteSystemAddr.setDescription('DECnet Phase IV node address.')
phivRouteRoutingType = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 25), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('routing-III',
                                                                                                                                                                                       1), ('nonrouting-III',
                                                                                                                                                                                            2), ('area',
                                                                                                                                                                                                 3), ('routing-IV',
                                                                                                                                                                                                      4), ('nonrouting-IV',
                                                                                                                                                                                                           5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteRoutingType.setDescription('This read-write parameter indicates the type of the executor\n            node. The node-type is one of the following:\n\n            routing-III\n            nonrouting-III\n            routing-IV\n            ronrouting-IV\n            area\n\n            A routing node has full routing capability. A\n            nonrouting node contains a subset of the Routing\n            routing modules. The III and IV indicate the DNA\n            phase of the node. Nonrouting nodes can deliver\n            and receive packets to and from any node, but cannot\n            route packets from other nodes through to other nodes.\n            An area node routes between areas. Refer to the Routing\n            specification for details.\n\n            For adjacent nodes, this is a read-only parameter that\n            indicates the type of the reachable adjacent node.\n            NOTE: The ROUTING-III and NONROUTING-III values are\n            incremented by one compared to the standard DECnet\n            values in order to maintain compliance with RFC 1155)')
phivRouteSystemAddress = MibScalar((1, 3, 6, 1, 2, 1, 18, 5, 26), PhivAddr()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteSystemAddress.setDescription('DECnet Phase IV node address.')
phivCircuitParametersTable = MibTable((1, 3, 6, 1, 2, 1, 18, 6, 1))
if mibBuilder.loadTexts:
    phivCircuitParametersTable.setDescription('Information about the parameters associated with all\n            circuits currently known.')
phivCircuitParametersEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 6, 1, 1)).setIndexNames((0,
                                                                                         'DECNET-PHIV-MIB',
                                                                                         'phivCircuitIndex'))
if mibBuilder.loadTexts:
    phivCircuitParametersEntry.setDescription('Parameters information about all circuits currently\n             known.')
phivCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitIndex.setDescription('A unique index value for each known circuit.')
phivCircuitLineIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 2), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitLineIndex.setDescription('The line on which this circuit is active.  This is\n             the same as the ifIndex.')
phivCircuitCommonState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('on',
                                                                                                                                                                                                1), ('off',
                                                                                                                                                                                                     2), ('service',
                                                                                                                                                                                                          3), ('cleared',
                                                                                                                                                                                                               4)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivCircuitCommonState.setDescription("This value represents the circuit's Network Management\n            operational state. NOTE: These values are incremented\n            by one compared to the standard DECnet values in order\n            to maintain compliance with RFC 1155.")
phivCircuitCommonSubState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))).clone(namedValues=NamedValues(('starting',
                                                                                                                                                                                                                                  1), ('reflecting',
                                                                                                                                                                                                                                       2), ('looping',
                                                                                                                                                                                                                                            3), ('loading',
                                                                                                                                                                                                                                                 4), ('dumping',
                                                                                                                                                                                                                                                      5), ('triggering',
                                                                                                                                                                                                                                                           6), ('autoservice',
                                                                                                                                                                                                                                                                7), ('autoloading',
                                                                                                                                                                                                                                                                     8), ('autodumping',
                                                                                                                                                                                                                                                                          9), ('autotriggering',
                                                                                                                                                                                                                                                                               10), ('synchronizing',
                                                                                                                                                                                                                                                                                     11), ('failed',
                                                                                                                                                                                                                                                                                           12), ('running',
                                                                                                                                                                                                                                                                                                 13)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCommonSubState.setDescription("This value represents the circuit's Network Management\n            operational and service substate. NOTE: These values are\n            incremented by one compared to the standard DECnet values\n            in order to maintain compliance with RFC 1155.")
phivCircuitCommonName = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 5), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 16))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCommonName.setDescription('The name of the circuit entry in the table, for example,\n             SVA-0 or in a level 2 router ASYNC-8 or ETHER-1).')
phivCircuitExecRecallTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivCircuitExecRecallTimer.setDescription('This parameter represents the minimum number of\n            seconds to wait before restarting the circuit.  A\n            value of 0 indicates not timer is running.')
phivCircuitCommonType = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15))).clone(namedValues=NamedValues(('ddcmp-point',
                                                                                                                                                                                                                      1), ('ddcmp-control',
                                                                                                                                                                                                                           2), ('ddcmp-tributary',
                                                                                                                                                                                                                                3), ('x25',
                                                                                                                                                                                                                                     4), ('ddcmp-dmc',
                                                                                                                                                                                                                                          5), ('ethernet',
                                                                                                                                                                                                                                               6), ('ci',
                                                                                                                                                                                                                                                    7), ('qp2-dte20',
                                                                                                                                                                                                                                                         8), ('bisync',
                                                                                                                                                                                                                                                              9), ('other',
                                                                                                                                                                                                                                                                   14), ('fddi',
                                                                                                                                                                                                                                                                         15)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCommonType.setDescription('Represents the type of the circuit. For X.25 circuits,\n            the value must be set to X25. For DDCMP and Ethernet\n            circuits it is read only and is the same value as the\n            protocol of the associated line.\n            NOTE: Values 1 - 5 are incremented by one compared to the\n            standard DECnet values in order to maintain compliance\n            with RFC 1155.')
phivCircuitService = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                      1), ('disabled',
                                                                                                                                                                                           2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivCircuitService.setDescription('This value indicates whether or not Network Management\n            allows service operations on a circuit. The values for\n            service-control are as follows:\n\n            ENABLED     SERVICE state and/or service functions are\n                        allowed.\n\n            DISABLED    SERVICE state and/or service functions are not\n                        allowed.\n\n            NOTE: These values are incremented by one compared to the\n            standard DECnet values in order to maintain compliance\n            with RFC 1155.')
phivCircuitExecCost = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 25))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivCircuitExecCost.setDescription('This value represents the routing cost of the circuit.\n            Routing sends messages along the path between two nodes\n            having the smallest cost.')
phivCircuitExecHelloTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 8191))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivCircuitExecHelloTimer.setDescription('This value determines the frequency of Routing Hello\n            messages sent to the adjacent node on the circuit.')
phivCircuitCountTable = MibTable((1, 3, 6, 1, 2, 1, 18, 6, 2))
if mibBuilder.loadTexts:
    phivCircuitCountTable.setDescription('Information about the counters associated with all\n            circuits currently known.')
phivCircuitCountEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 6, 2, 1)).setIndexNames((0,
                                                                                    'DECNET-PHIV-MIB',
                                                                                    'phivCircuitIndex'))
if mibBuilder.loadTexts:
    phivCircuitCountEntry.setDescription('Counter information about all circuits currently known')
phivCircuitCountSecLastZeroed = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 1), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountSecLastZeroed.setDescription('Number of seconds since the circuit counters for this\n            circuit were last zeroed.')
phivCircuitCountTermPacketsRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 2), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountTermPacketsRecd.setDescription('Number of terminating packets received on this circuit.')
phivCircuitCountOriginPackSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 3), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountOriginPackSent.setDescription('Number of originating packets sent on this circuit.')
phivCircuitCountTermCongLoss = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 4), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountTermCongLoss.setDescription('Number of terminating congestion losses on this\n            circuit.')
phivCircuitCountCorruptLoss = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 5), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountCorruptLoss.setDescription('Number of corruption losses on this circuit.')
phivCircuitCountTransitPksRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 6), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountTransitPksRecd.setDescription('Number of Transit packets received on this circuit.')
phivCircuitCountTransitPkSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 7), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountTransitPkSent.setDescription('Number of transit packets sent on this circuit.')
phivCircuitCountTransitCongestLoss = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1,
                                                     8), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountTransitCongestLoss.setDescription('Number of transit congestion losses on this circuit.')
phivCircuitCountCircuitDown = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 9), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountCircuitDown.setDescription('Number of circuit downs on this circuit.')
phivCircuitCountInitFailure = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 10), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountInitFailure.setDescription('Number of Initialization failures on this circuit.')
phivCircuitCountAdjDown = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 11), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountAdjDown.setDescription('This counter indicates the number of adjacency losses\n            that result from any of the following:\n                 Node listener timeout\n                 Invalid data received at node listener\n                 Unexpected control (initialization or verification)\n                     message received\n                 Routing message received with a checksum error\n                 Node identification from a routing message or a\n                 Hello message that is not the one expected Hello\n                 message received indicating that connectivity\n                 became one-way\n                 Adjacency idled.')
phivCircuitCountPeakAdj = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 12), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountPeakAdj.setDescription('This counter indicates the maximum number of nodes\n            that are up on the circuit.')
phivCircuitCountBytesRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 13), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountBytesRecd.setDescription('Number of bytes received on this circuit.')
phivCircuitCountBytesSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 14), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountBytesSent.setDescription('Number of bytes sent on this circuit.')
phivCircuitCountDataBlocksRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 15), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountDataBlocksRecd.setDescription('Number of data blocks received on this circuit.')
phivCircuitCountDataBlocksSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 16), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountDataBlocksSent.setDescription('Number of data blocks sent on this circuit.')
phivCircuitCountUsrBuffUnav = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 6, 2, 1, 17), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCircuitCountUsrBuffUnav.setDescription('Number of user buffer unavailable errors.')
phivCircuitOrigQueueLimit = MibScalar((1, 3, 6, 1, 2, 1, 18, 6, 3), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivCircuitOrigQueueLimit.setDescription('This parameter indicates the maximum number of\n            originating packets that may be outstanding on this\n            circuit. This does not include route-thru traffic.')
phivCircuitCountZeroCount = MibScalar((1, 3, 6, 1, 2, 1, 18, 6, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                  1), ('reset',
                                                                                                                                                                                       2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivCircuitCountZeroCount.setDescription('When this value is set to 2, all of the counters in the\n            Circuit Counter Table are set to zero.')
phivDDCMPCircuitParametersTable = MibTable((1, 3, 6, 1, 2, 1, 18, 7, 1))
if mibBuilder.loadTexts:
    phivDDCMPCircuitParametersTable.setDescription('Information about DDCMP circuit parameters.')
phivDDCMPCircuitParametersEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 7, 1, 1)).setIndexNames((0,
                                                                                              'DECNET-PHIV-MIB',
                                                                                              'phivDDCMPCircuitIndex'))
if mibBuilder.loadTexts:
    phivDDCMPCircuitParametersEntry.setDescription('Parameters information about DDCMP circuits currently\n             known.')
phivDDCMPCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitIndex.setDescription('A unique index value for each known DDCMP circuit.\n            This is the same value as phivCircuitIndex.')
phivDDCMPCircuitAdjNodeAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 1, 1, 2), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitAdjNodeAddr.setDescription('The address of the adjacent node.')
phivDDCMPCircuitTributary = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitTributary.setDescription('This value represents the Data Link physical tributary\n            address of the circuit.')
phivDDCMPCircuitCountTable = MibTable((1, 3, 6, 1, 2, 1, 18, 7, 2))
if mibBuilder.loadTexts:
    phivDDCMPCircuitCountTable.setDescription('Information about the DDCMP counters associated with all\n            circuits currently known.')
phivDDCMPCircuitCountEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 7, 2, 1)).setIndexNames((0,
                                                                                         'DECNET-PHIV-MIB',
                                                                                         'phivCircuitIndex'))
if mibBuilder.loadTexts:
    phivDDCMPCircuitCountEntry.setDescription('Counter information about DDCMP circuits now known')
phivDDCMPCircuitErrorsInbd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1, 1), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitErrorsInbd.setDescription('Number of Data errors inbound.')
phivDDCMPCircuitErrorsOutbd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1, 2), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitErrorsOutbd.setDescription('Number of outbound data errors.')
phivDDCMPCircuitRmteReplyTimeouts = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1,
                                                    3), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitRmteReplyTimeouts.setDescription('Number of remote reply timeouts.')
phivDDCMPCircuitLocalReplyTimeouts = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1,
                                                     4), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitLocalReplyTimeouts.setDescription('Number of local Reply timeouts.')
phivDDCMPCircuitRmteBuffErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1, 5), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitRmteBuffErrors.setDescription('Number of remote reply time out errors.')
phivDDCMPCircuitLocalBuffErrors = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1, 6), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitLocalBuffErrors.setDescription('Number of local buffer errors.')
phivDDCMPCircuitSelectIntervalsElap = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1,
                                                      7), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitSelectIntervalsElap.setDescription('Selection intervals that have elapsed.')
phivDDCMPCircuitSelectTimeouts = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 2, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPCircuitSelectTimeouts.setDescription('Number of selection timeouts.')
phivDDCMPLineCountTable = MibTable((1, 3, 6, 1, 2, 1, 18, 7, 3))
if mibBuilder.loadTexts:
    phivDDCMPLineCountTable.setDescription('The DDCMP Line Count Table.')
phivDDCMPLineCountEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 7, 3, 1)).setIndexNames((0,
                                                                                      'DECNET-PHIV-MIB',
                                                                                      'phivDDCMPLineCountIndex'))
if mibBuilder.loadTexts:
    phivDDCMPLineCountEntry.setDescription('There is one entry in the table for each line.')
phivDDCMPLineCountIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 3, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPLineCountIndex.setDescription("The line on which this entry's equivalence is\n            effective. The interface identified by a particular\n            value of this index is the same interface as\n            identified by the same value of phivLineIndex.\n            This value is the ifIndex.")
phivDDCMPLineCountDataErrsIn = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 3, 1, 2), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPLineCountDataErrsIn.setDescription('Number of data errors inbound.')
phivDDCMPLineCountRmteStationErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 3, 1,
                                                    3), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPLineCountRmteStationErrs.setDescription('Number of remote station errors.')
phivDDCMPLineCountLocalStationErrs = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 7, 3, 1,
                                                     4), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivDDCMPLineCountLocalStationErrs.setDescription('Number of local station errors.')
phivControlSchedTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 8, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(50, 65535)).clone(200)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivControlSchedTimer.setDescription('This value represents the number of milliseconds\n            between recalculation of tributary polling priorities.')
phivControlDeadTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 8, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)).clone(10000)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivControlDeadTimer.setDescription('This value represents the number of milliseconds\n            between polls of one of the set of dead\n            tributaries.')
phivControlDelayTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 8, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivControlDelayTimer.setDescription('This value represents the minimum number of\n            milliseconds to delay between polls. The delay timer\n            limits the effect of a very fast control station on\n            slow tributaries.')
phivControlStreamTimer = MibScalar((1, 3, 6, 1, 2, 1, 18, 8, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(6000)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivControlStreamTimer.setDescription('This value represents the number of milliseconds a\n            tributary or a half duplex remote station is\n            allowed to hold the line.\n\n            NOTE: This parameter can also be applied to\n            half-duplex lines of type DDCMP POINT.')
phivControlParametersTable = MibTable((1, 3, 6, 1, 2, 1, 18, 8, 5))
if mibBuilder.loadTexts:
    phivControlParametersTable.setDescription('Information about control circuit parameters.')
phivControlParametersEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 8, 5, 1)).setIndexNames((0,
                                                                                         'DECNET-PHIV-MIB',
                                                                                         'phivControlCircuitIndex'))
if mibBuilder.loadTexts:
    phivControlParametersEntry.setDescription('Parameters information about control circuits\n            currently known.')
phivControlCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivControlCircuitIndex.setDescription('A unique index value for each known multipoint\n            control circuit.\n            This is the same value as phivCircuitIndex.')
phivControlBabbleTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)).clone(6000)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlBabbleTimer.setDescription('This value represents the number of milliseconds that a\n            selected tributary or remote half-duplex station is\n            allowed to transmit.')
phivControlMaxBuffs = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 254))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlMaxBuffs.setDescription('This value represents the maximum number of buffers the\n            tributary can use from a common buffer pool. If not\n            set, there is no common buffer pool and buffers are\n            explicitly supplied by the higher level. Count is a\n            decimal integer in the range 1-254.')
phivControlMaxTransmits = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 255)).clone(4)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlMaxTransmits.setDescription('This value represents the maximum number of data\n            messages that can be transmitted at one time. Count\n            is a decimal integer in the range 1-255.')
phivControlDyingBase = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlDyingBase.setDescription('This value represents the base priority to which a\n            tributary is reset each time it has been polled. A\n            separate base can be set for each of the indicated\n            polling states. Base is a decimal integer in the range\n            0-255.  If not set, the defaults are: active, 255;\n            inactive, 0; and dying, 0.')
phivControlDyingIncrement = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlDyingIncrement.setDescription('This value represents the increment added to the\n            tributary priority each time the scheduling timer\n            expires.  If not set, the defaults are: active, 0;\n            inactive, 64; and dying, 16.')
phivControlDeadThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)).clone(8)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlDeadThreshold.setDescription('This value represents the number of times to poll the\n            active, inactive, or dying tributary before changing\n            its polling state to dead because of receive timeouts.\n            Count is a decimal integer in the range 0-255.')
phivControlDyingThreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)).clone(2)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlDyingThreshold.setDescription('This value represents the number of times to poll the\n            active or inactive tributary before changing its\n            polling state to dying because of receive timeouts.\n            Count is a decimal integer in the range 0-255.')
phivControlInactTreshold = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)).clone(8)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlInactTreshold.setDescription('This value represents the number of times to poll the\n            active tributary before changing its polling state to\n            inactive because of no data response. Count is a\n            decimal integer in the range\n            0-255.')
phivControlPollingState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('automatic',
                                                                                                                                                                                                     1), ('active',
                                                                                                                                                                                                          2), ('inactive',
                                                                                                                                                                                                               3), ('dying',
                                                                                                                                                                                                                    4), ('dead',
                                                                                                                                                                                                                         5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlPollingState.setDescription("This value represents the state of the tributary\n            relative to the multipoint polling algorithm.  If not\n            set the default is AUTOMATIC. The possible states are:\n            AUTOMATIC\n\n              The tributary's state is allowed to vary according to\n              the operation of the polling algorithm.\n\n            ACTIVE/INACTIVE/DYING/DEAD\n\n              The tributary is locked in the specified state.\n\n             NOTE: These values are incremented by one compared to\n             the standard DECnet values in order to maintain\n             compliance with RFC 1155.")
phivControlPollingSubState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('active',
                                                                                                                                                                                                     1), ('inactive',
                                                                                                                                                                                                          2), ('dying',
                                                                                                                                                                                                               3), ('dead',
                                                                                                                                                                                                                    4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivControlPollingSubState.setDescription("This value represents the tributary's state as\n            determined by the polling algorithm.  This applies\n            only when the polling state is AUTOMATIC and is\n            read-only to Network Management.  Polling-substate is\n            one of ACTIVE, INACTIVE, DYING, or DEAD.  It is\n            displayed as a tag on the polling state, for example:\n            AUTOMATIC-INACTIVE.")
phivControlTransTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 8, 5, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivControlTransTimer.setDescription('This value represents the number of milliseconds to\n            delay between data message transmits. Milliseconds is\n            a decimal integer in the range 0-65535.')
phivEthLinkParametersTable = MibTable((1, 3, 6, 1, 2, 1, 18, 9, 1))
if mibBuilder.loadTexts:
    phivEthLinkParametersTable.setDescription('Information about ethernet link parameters.')
phivEthLinkParametersEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 9, 1, 1)).setIndexNames((0,
                                                                                         'DECNET-PHIV-MIB',
                                                                                         'phivEthLinkIndex'))
if mibBuilder.loadTexts:
    phivEthLinkParametersEntry.setDescription('Parameter information about ethernet links currently\n            known.')
phivEthLinkIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 9, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEthLinkIndex.setDescription('The circuit over which this links information is\n            collected.  This is the same as phivCircuitIndex.')
phivEthDesigRouterNodeAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 9, 1, 1, 2), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEthDesigRouterNodeAddr.setDescription('This value is the address of the designated router.')
phivEthMaxRouters = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 9, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEthMaxRouters.setDescription('This parameter is the maximum number of routers (other\n             than the executor itself) allowed on the circuit by\n             Routing for circuits that are owned by the executor\n             node.')
phivEthRouterPri = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 9, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 127)).clone(64)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivEthRouterPri.setDescription('This parameter is the priority that this router is to\n             have in the selection of designated router for the\n             circuit on circuits that are owned by the executor\n             node.')
phivEthHardwareAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 9, 1, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(6, 6)).setFixedLength(6)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivEthHardwareAddr.setDescription('This read-only parameter is the address that is\n            associated with the line device hardware as seen by\n            the DECnet Software.  This value is not the same as\n            ifPhysAddress.')
phivCountersCountTable = MibTable((1, 3, 6, 1, 2, 1, 18, 10, 1))
if mibBuilder.loadTexts:
    phivCountersCountTable.setDescription('Information about ethernet link counters.')
phivCountersCountEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 10, 1, 1)).setIndexNames((0,
                                                                                      'DECNET-PHIV-MIB',
                                                                                      'phivCountersIndex'))
if mibBuilder.loadTexts:
    phivCountersCountEntry.setDescription('Counter information about ethernet links currently\n            known.')
phivCountersIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersIndex.setDescription('The interface to which these counters apply.  This is\n            the same interface as identified by the same value of\n            phivLineIndex. This value is the ifIndex.')
phivCountersCountBytesRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 2), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountBytesRecd.setDescription('Number of bytes received over this link.')
phivCountersCountBytesSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 3), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountBytesSent.setDescription('Number of bytes sent over this link.')
phivCountersCountDataBlocksRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 4), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountDataBlocksRecd.setDescription('Number of data blocks received over this link.')
phivCountersCountDataBlocksSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 5), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountDataBlocksSent.setDescription('Number of data blocks sent over this link.')
phivCountersCountEthUsrBuffUnav = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 6), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountEthUsrBuffUnav.setDescription('Number of user buffer unavailable errors over this\n            link.')
phivCountersCountMcastBytesRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 7), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountMcastBytesRecd.setDescription('Number of multicast bytes received over this link.')
phivCountersCountDataBlksRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 8), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountDataBlksRecd.setDescription('Number of data blocks received over this link.')
phivCountersCountDataBlksSent = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 9), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountDataBlksSent.setDescription('Number of data blocks sent over this link.')
phivCountersCountMcastBlksRecd = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 10), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountMcastBlksRecd.setDescription('Number of multicast blocks received over this link.')
phivCountersCountBlksSentDef = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 11), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountBlksSentDef.setDescription('Number of blocks sent, initially deferred over this\n            link.')
phivCountersCountBlksSentSingleCol = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1,
                                                     12), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountBlksSentSingleCol.setDescription('Number of blocks sent, single collision over this link.')
phivCountersCountBlksSentMultCol = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1,
                                                   13), PhivCounter().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountBlksSentMultCol.setDescription('Number of blocks sent, multiple collisions over this\n            link.')
phivCountersCountSendFailure = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 14), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountSendFailure.setDescription('Number of send failures over this link.')
phivCountersCountCollDetectFailure = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1,
                                                     15), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountCollDetectFailure.setDescription('Number of collision detect check failures over this\n             link.')
phivCountersCountReceiveFailure = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 16), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountReceiveFailure.setDescription('Number of receive failures over this link.')
phivCountersCountUnrecFrameDest = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 17), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountUnrecFrameDest.setDescription('Number of unrecognized frame destinations over this\n            link.')
phivCountersCountDataOver = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 18), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountDataOver.setDescription('Number of data overruns over this link.')
phivCountersCountSysBuffUnav = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 19), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountSysBuffUnav.setDescription('Number of system buffer unavailables over this link.')
phivCountersCountUsrBuffUnav = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 10, 1, 1, 20), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivCountersCountUsrBuffUnav.setDescription('Number of user buffer unavailables.')
phivAdjTable = MibTable((1, 3, 6, 1, 2, 1, 18, 11, 1))
if mibBuilder.loadTexts:
    phivAdjTable.setDescription('The Adjacency Table.')
phivAdjEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 11, 1, 1)).setIndexNames((0, 'DECNET-PHIV-MIB',
                                                                            'phivAdjCircuitIndex'))
if mibBuilder.loadTexts:
    phivAdjEntry.setDescription('There is one entry in the table for each adjacency.')
phivAdjCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 1), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjCircuitIndex.setDescription('A unique index value for each known circuit.')
phivAdjNodeAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 2), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodeAddr.setDescription('The address of the adjacent node.')
phivAdjBlockSize = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjBlockSize.setDescription('This read-only parameter is the block size that was\n            negotiated with the adjacent Routing layer during Routing\n            initialization over a particular circuit. It includes the\n            routing header, but excludes the data link header. This\n            parameter is qualified by ADJACENT NODE.')
phivAdjListenTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjListenTimer.setDescription('This value determines the maximum number of seconds\n            allowed to elapse before Routing receives some message\n            (either a Hello message or a user message) from the\n            adjacent node on the circuit. It was agreed during\n            Routing initialization with the adjacent Routing layer.\n            This parameter is qualified by ADJACENT NODE.')
phivAdjCircuitEtherServPhysAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(6, 6)).setFixedLength(6)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjCircuitEtherServPhysAddr.setDescription('This parameter indicates the Ethernet physical address\n            of an adjacent node that is being serviced on this\n            circuit. This parameter is a qualifier for SERVICE\n            SUBSTATE.')
phivAdjType = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('routing-III',
                                                                                                                                                                                         1), ('nonrouting-III',
                                                                                                                                                                                              2), ('area',
                                                                                                                                                                                                   3), ('routing-IV',
                                                                                                                                                                                                        4), ('nonrouting-IV',
                                                                                                                                                                                                             5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjType.setDescription('This parameter indicates the type of adjacency.\n\n            For adjacent nodes, this is a read-only parameter that\n            indicates the type of the reachable adjacent node.\n            NOTE: The routing-III and nonrouting-III values are\n            incremented by one compared to the standard DECnet\n            values in order to maintain compliance with RFC 1155)')
phivAdjState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))).clone(namedValues=NamedValues(('initializing',
                                                                                                                                                                                                          1), ('up',
                                                                                                                                                                                                               2), ('run',
                                                                                                                                                                                                                    3), ('circuit-rejected',
                                                                                                                                                                                                                         4), ('data-link-start',
                                                                                                                                                                                                                              5), ('routing-layer-initialize',
                                                                                                                                                                                                                                   6), ('routing-layer-verify',
                                                                                                                                                                                                                                        7), ('routing-layer-complete',
                                                                                                                                                                                                                                             8), ('off',
                                                                                                                                                                                                                                                  9), ('halt',
                                                                                                                                                                                                                                                       10)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjState.setDescription('This value indicates the state of a router adjacency.\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) Ethernet, CI, or FDDI, with an\n            adjacent node of type (phivAdjType) ROUTING IV or AREA,\n            this variable is the state of the Ethernet\n            Initialization Layer for this adjacency, and can have\n            values INITIALIZING or UP. (See Section 9.1.1 of\n            DECnet Phase IV Routing Layer Functional Specification.)\n\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) Ethernet, CI, or FDDI, with an\n            adjacent node of type (phivAdjType) NONROUTING IV,\n            this variable will always take on the value UP.\n\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) DDCMP POINT, DDCMP CONTROL,\n            DDCMP TRIBUTARY, DDCMP DMC, or X.25, this variable is\n            the state of the Routing Layer Initialization Circuit\n            State. (See section 7.3, ibid.)  It can have values\n            between RUN and HALT.\n\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) OTHER, this variable may be\n            used in a manner consistent with the Initialization\n            Layer used on that circuit.')
phivAdjPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjPriority.setDescription('Priority assigned by the adjacent node for this\n            circuit.')
phivAdjExecListenTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjExecListenTimer.setDescription('This read-only value determines the maximum number of\n            seconds allowed to elapse before Routing receives some\n            message (either a Hello message or a user message) from\n            the adjacent node on the circuit. It was agreed during\n            Routing initialization with the adjacent Routing layer.')
phivAdjNodeTable = MibTable((1, 3, 6, 1, 2, 1, 18, 11, 2))
if mibBuilder.loadTexts:
    phivAdjNodeTable.setDescription('The Adjacent Node Table.')
phivAdjNodeEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 11, 2, 1)).setIndexNames((0,
                                                                                'DECNET-PHIV-MIB',
                                                                                'phivAdjNodeCircuitIndex'), (0,
                                                                                                             'DECNET-PHIV-MIB',
                                                                                                             'phivAdjAddr'))
if mibBuilder.loadTexts:
    phivAdjNodeEntry.setDescription('There is one entry in the table for each adjacency.')
phivAdjNodeCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodeCircuitIndex.setDescription('A unique index value for each known circuit.  This\n            value is the same as phivCircuitIndex and identifies the\n            circuit over which the adjacency is realized.')
phivAdjAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2, 1, 2), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjAddr.setDescription('The address of the adjacent node.')
phivAdjNodeBlockSize = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2, 1, 3), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodeBlockSize.setDescription('This read-only parameter is the block size that was\n            negotiated with the adjacent Routing layer during Routing\n            initialization over a particular circuit. It includes the\n            routing header, but excludes the data link header. This\n            parameter is qualified by ADJACENT NODE.')
phivAdjNodeListenTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodeListenTimer.setDescription('This value determines the maximum number of seconds\n            allowed to elapse before Routing receives some message\n            (either a Hello message or a user message) from the\n            adjacent node on the circuit. It was agreed during\n            Routing initialization with the adjacent Routing layer.\n            This parameter is qualified by ADJACENT NODE.')
phivAdjNodeCircuitEtherServPhysAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2,
                                                      1, 5), OctetString().subtype(subtypeSpec=ValueSizeConstraint(6, 6)).setFixedLength(6)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodeCircuitEtherServPhysAddr.setDescription('This parameter indicates the Ethernet physical address\n            of an adjacent node that is being serviced on this\n            circuit. This parameter is a qualifier for SERVICE\n            SUBSTATE.')
phivAdjNodeType = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('routing-III',
                                                                                                                                                                                             1), ('nonrouting-III',
                                                                                                                                                                                                  2), ('area',
                                                                                                                                                                                                       3), ('routing-IV',
                                                                                                                                                                                                            4), ('nonrouting-IV',
                                                                                                                                                                                                                 5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodeType.setDescription('This parameter indicates the type of adjacency.\n\n            For adjacent nodes, this is a read-only parameter that\n            indicates the type of the reachable adjacent node.\n            NOTE: The routing-III and nonrouting-III values are\n            incremented by one compared to the standard DECnet\n            values in order to maintain compliance with RFC 1155)')
phivAdjNodeState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))).clone(namedValues=NamedValues(('initializing',
                                                                                                                                                                                                              1), ('up',
                                                                                                                                                                                                                   2), ('run',
                                                                                                                                                                                                                        3), ('circuit-rejected',
                                                                                                                                                                                                                             4), ('data-link-start',
                                                                                                                                                                                                                                  5), ('routing-layer-initialize',
                                                                                                                                                                                                                                       6), ('routing-layer-verify',
                                                                                                                                                                                                                                            7), ('routing-layer-complete',
                                                                                                                                                                                                                                                 8), ('off',
                                                                                                                                                                                                                                                      9), ('halt',
                                                                                                                                                                                                                                                           10)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodeState.setDescription('This value indicates the state of a router adjacency.\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) Ethernet, CI, or FDDI, with an\n            adjacent node of type (phivAdjNodeType) ROUTING IV or AREA,\n            this variable is the state of the Ethernet\n            Initialization Layer for this adjacency, and can have\n            values INITIALIZING or UP. (See Section 9.1.1 of\n            DECnet Phase IV Routing Layer Functional Specification.)\n\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) Ethernet, CI, or FDDI, with an\n            adjacent node of type (phivAdjNodeType) NONROUTING IV,\n            this variable will always take on the value UP.\n\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) DDCMP POINT, DDCMP CONTROL,\n            DDCMP TRIBUTARY, DDCMP DMC, or X.25, this variable is\n            the state of the Routing Layer Initialization Circuit\n            State. (See section 7.3, ibid.)  It can have values\n            between RUN and HALT.\n\n            On adjacencies over a circuit of type\n            (phivCircuitCommonType) OTHER, this variable may be\n            used in a manner consistent with the Initialization\n            Layer used on that circuit.')
phivAdjNodePriority = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 11, 2, 1, 8), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAdjNodePriority.setDescription('Priority assigned by the adjacent node for this\n            circuit.')
phivLineTable = MibTable((1, 3, 6, 1, 2, 1, 18, 12, 1))
if mibBuilder.loadTexts:
    phivLineTable.setDescription('The Line Table.')
phivLineEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 12, 1, 1)).setIndexNames((0, 'DECNET-PHIV-MIB',
                                                                             'phivLineIndex'))
if mibBuilder.loadTexts:
    phivLineEntry.setDescription('There is one entry in the table for each line.')
phivLineIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineIndex.setDescription("The line on which this entry's equivalence is effective.\n            This is the same as the ifIndex.")
phivLineName = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 16))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineName.setDescription('The name of the line on this row of the table.')
phivLineState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('on',
                                                                                                                                                                                        1), ('off',
                                                                                                                                                                                             2), ('service',
                                                                                                                                                                                                  3), ('cleared',
                                                                                                                                                                                                       4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineState.setDescription('This value represents Network Management operational\n            state.\n            NOTE that these values are incremented by one compared to\n            the standard DECnet values.')
phivLineSubstate = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))).clone(namedValues=NamedValues(('starting',
                                                                                                                                                                                                                          1), ('reflecting',
                                                                                                                                                                                                                               2), ('looping',
                                                                                                                                                                                                                                    3), ('loading',
                                                                                                                                                                                                                                         4), ('dumping',
                                                                                                                                                                                                                                              5), ('triggering',
                                                                                                                                                                                                                                                   6), ('auto-service',
                                                                                                                                                                                                                                                        7), ('auto-loading',
                                                                                                                                                                                                                                                             8), ('auto-dumping',
                                                                                                                                                                                                                                                                  9), ('auto-triggering',
                                                                                                                                                                                                                                                                       10), ('synchronizing',
                                                                                                                                                                                                                                                                             11), ('failed',
                                                                                                                                                                                                                                                                                   12), ('running',
                                                                                                                                                                                                                                                                                         13)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineSubstate.setDescription("This value represents the line's read-only Network\n            Management substate.\n            NOTE that these values are incremented by one compared to\n            the standard DECnet values.")
phivLineService = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('starting',
                                                                                                                                                                                          1), ('reflecting',
                                                                                                                                                                                               2), ('looping',
                                                                                                                                                                                                    3), ('other',
                                                                                                                                                                                                         4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineService.setDescription("This value represents the line's read-only Network\n            Management service.\n            NOTE that these values are incremented by one compared to\n            the standard DECnet values and OTHER is a new addition.")
phivLineDevice = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 16))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineDevice.setDescription('This value represents the Physical Link device to be\n            used on the line.')
phivLineReceiveBuffs = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineReceiveBuffs.setDescription('This value represents the number of receive buffers\n            reserved for the line. It is a decimal number in\n            the range 0-65535.  0 is supported for those vendors\n            that do not reserve buffers on a per line basis and\n            use a pool of buffers that can be used by any line.')
phivLineProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 14, 15))).clone(namedValues=NamedValues(('ddcmp-point',
                                                                                                                                                                                                                  1), ('ddcmp-control',
                                                                                                                                                                                                                       2), ('ddcmp-tributary',
                                                                                                                                                                                                                            3), ('reserved',
                                                                                                                                                                                                                                 4), ('ddcmp-dmc',
                                                                                                                                                                                                                                      5), ('olapb',
                                                                                                                                                                                                                                           6), ('ethernet',
                                                                                                                                                                                                                                                7), ('ci',
                                                                                                                                                                                                                                                     8), ('qp2',
                                                                                                                                                                                                                                                          9), ('other',
                                                                                                                                                                                                                                                               14), ('fddi',
                                                                                                                                                                                                                                                                     15)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineProtocol.setDescription('This value represents the protocol used on the line\n            device.  Note that these values are incremented by\n            one compared to the standard DECnet values.')
phivLineServiceTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 9), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineServiceTimer.setDescription('This value represents the amount of time in\n            milliseconds allowed to elapse before a Data Link\n            receive request completes while doing service\n            operations.')
phivLineMaxBlock = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 12, 1, 1, 10), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivLineMaxBlock.setDescription('This value represents the Data Link maximum block\n            size on the line.')
phivNonBroadcastTable = MibTable((1, 3, 6, 1, 2, 1, 18, 14, 1))
if mibBuilder.loadTexts:
    phivNonBroadcastTable.setDescription('The Non Broadcast Table.')
phivNonBroadcastEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 14, 1, 1)).setIndexNames((0,
                                                                                     'DECNET-PHIV-MIB',
                                                                                     'phivNonBroadcastIndex'))
if mibBuilder.loadTexts:
    phivNonBroadcastEntry.setDescription('There is one entry in the table for each\n            Non Broadcast line.')
phivNonBroadcastIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 14, 1, 1, 1), InterfaceIndex()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivNonBroadcastIndex.setDescription("The Non Broadcast line on which this entry's\n            equivalence is effective.  This is the same value\n            as the ifIndex.")
phivNonBroadcastController = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 14, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('normal',
                                                                                                                                                                                                  1), ('loopback',
                                                                                                                                                                                                       2), ('other',
                                                                                                                                                                                                            3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivNonBroadcastController.setDescription('This value represents the Physical Link hardware\n            controller mode for the line device. The values\n            for controller-mode are:\n\n            NORMAL  For normal controller operating mode.\n\n            LOOPBACK For software controllable loopback of the\n            controller. On those devices that can support this\n            mode, it causes all transmitted messages to be looped\n            back from within the controller itself. This is\n            accomplished without any manual intervention other\n            than the setting of this parameter value.\n\n            OTHER indicates function is not supported\n            Note that these values are incremented by one compared to\n            the standard DECnet values.')
phivNonBroadcastDuplex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 14, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('full',
                                                                                                                                                                                           1), ('half',
                                                                                                                                                                                                2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivNonBroadcastDuplex.setDescription('This value represents the Physical Link hardware\n            duplex mode of the line device. The possible modes\n            are:\n\n            FULL   Full-duplex\n            HALF   Half-duplex\n\n            Note that these values are incremented by one compared to\n            the standard DECnet values.')
phivNonBroadcastClock = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 14, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('external',
                                                                                                                                                                                             1), ('internal',
                                                                                                                                                                                                  2), ('other',
                                                                                                                                                                                                       3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivNonBroadcastClock.setDescription('This value represents the Physical Link hardware clock\n            mode for the line device. The values for clock-mode are:\n            INTERNAL For software controllable loopback use of\n            the clock. On those devices that can support this\n            mode, it causes the device to supply a clock signal\n            such that a transmitted messages can be looped\n            back from outside the device. This may require manual\n            intervention other than the setting of this parameter\n            value. For example, the operator may have to connect\n            a loopback plug in place of the normal line.\n\n            EXTERNAL For normal clock operating mode, where the\n            clock signal is supplied externally to the controller.\n            Note that these values are incremented by one compared to\n            the standard DECnet values.')
phivNonBroadcastRetransmitTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 14, 1, 1, 5), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)).clone(3000)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivNonBroadcastRetransmitTimer.setDescription('This value represents number of milliseconds before\n            the Data Link retransmits a block on the line. On\n            half-duplex lines, this parameter is the select timer.')
phivAreaTable = MibTable((1, 3, 6, 1, 2, 1, 18, 15, 1))
if mibBuilder.loadTexts:
    phivAreaTable.setDescription('Table of information kept on all areas known to\n            this unit.')
phivAreaEntry = MibTableRow((1, 3, 6, 1, 2, 1, 18, 15, 1, 1)).setIndexNames((0, 'DECNET-PHIV-MIB',
                                                                             'phivAreaNum'))
if mibBuilder.loadTexts:
    phivAreaEntry.setDescription('The area routing information.')
phivAreaNum = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 15, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 64))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAreaNum.setDescription('This value indicates the area number of this entry.')
phivAreaState = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 15, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(4, 5))).clone(namedValues=NamedValues(('reachable',
                                                                                                                                                                                  4), ('unreachable',
                                                                                                                                                                                       5)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAreaState.setDescription('This value indicates the state of the area')
phivAreaCost = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 15, 1, 1, 3), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAreaCost.setDescription('The total cost over the current path to the\n             destination area. Cost is a value associated with\n             using a circuit. Routing routes messages (data)\n             along the path between 2 areas with the smallest\n             cost.')
phivAreaHops = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 15, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAreaHops.setDescription('The number of hops to a destination area. A hop is\n            the routing value representing the logical distance\n            between two areas in network.')
phivAreaNextNode = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 15, 1, 1, 5), PhivAddr()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAreaNextNode.setDescription('The next node on the circuit used to get to the\n            area under scrutiny.')
phivAreaCircuitIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 18, 15, 1, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    phivAreaCircuitIndex.setDescription('A unique index value for each known circuit.')
phivAreaMaxCost = MibScalar((1, 3, 6, 1, 2, 1, 18, 15, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1022))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivAreaMaxCost.setDescription('This value represents the maximum total path cost\n            allowed from the executor to any other level 2 routing\n            node. The AREA MAXIMUM COST number is decimal in the\n            range 1-1022. This parameter is only applicable if\n            the executor node is of type AREA.')
phivAreaMaxHops = MibScalar((1, 3, 6, 1, 2, 1, 18, 15, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 30))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivAreaMaxHops.setDescription('This value represents the maximum number of routing hops\n            allowable from the executor to any other level 2\n            routing node.  This parameter is only applicable if the\n            executor node is of type AREA.')
phivRouteMaxArea = MibScalar((1, 3, 6, 1, 2, 1, 18, 15, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 63))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    phivRouteMaxArea.setDescription("This value represents the largest area number and,\n            therefore, number of areas that can be known about\n            by the executor node's Routing. This parameter is only\n            applicable if the executor node is of type AREA.")
mibBuilder.exportSymbols('DECNET-PHIV-MIB', phivDDCMPCircuitIndex=phivDDCMPCircuitIndex, phivEthDesigRouterNodeAddr=phivEthDesigRouterNodeAddr, phivControlDeadThreshold=phivControlDeadThreshold, phivEthLinkParametersEntry=phivEthLinkParametersEntry, phivDDCMPCircuitCountEntry=phivDDCMPCircuitCountEntry, routing=routing, phivDDCMPCircuitRmteBuffErrors=phivDDCMPCircuitRmteBuffErrors, phivAdjTable=phivAdjTable, phivEndInactivityTimer=phivEndInactivityTimer, phivSessionInTimer=phivSessionInTimer, phivCountersCountReceiveFailure=phivCountersCountReceiveFailure, phivLineMaxBlock=phivLineMaxBlock, phivControlSchedTimer=phivControlSchedTimer, phivEndRemoteEntry=phivEndRemoteEntry, phivDDCMPCircuitSelectTimeouts=phivDDCMPCircuitSelectTimeouts, phivDDCMPLineCountRmteStationErrs=phivDDCMPLineCountRmteStationErrs, phivDDCMPCircuitSelectIntervalsElap=phivDDCMPCircuitSelectIntervalsElap, control=control, phivRouteSegBuffSize=phivRouteSegBuffSize, phivAdjListenTimer=phivAdjListenTimer, phivLevel1RouteNextNode=phivLevel1RouteNextNode, phivSystem=phivSystem, phivRouteCountOverSzePktLoss=phivRouteCountOverSzePktLoss, phivCountersCountTable=phivCountersCountTable, phivCircuitCountTermCongLoss=phivCircuitCountTermCongLoss, phivCircuitCountSecLastZeroed=phivCircuitCountSecLastZeroed, phivLevel1RouteHops=phivLevel1RouteHops, phivCountersCountDataBlksRecd=phivCountersCountDataBlksRecd, phivRouteRoutingType=phivRouteRoutingType, phivAdjNodeBlockSize=phivAdjNodeBlockSize, phivAreaCost=phivAreaCost, phivCircuitCountCorruptLoss=phivCircuitCountCorruptLoss, phivAdjNodeEntry=phivAdjNodeEntry, phivControlPollingSubState=phivControlPollingSubState, line=line, phivCountersIndex=phivCountersIndex, phivLineProtocol=phivLineProtocol, phivSystemState=phivSystemState, phivCountersCountEntry=phivCountersCountEntry, phivRouteCountPacketFmtErr=phivRouteCountPacketFmtErr, phivRouteBuffSize=phivRouteBuffSize, phivLineSubstate=phivLineSubstate, phivRouteCountPtlRteUpdtLoss=phivRouteCountPtlRteUpdtLoss, phivEndCountTable=phivEndCountTable, phivCircuitCountAdjDown=phivCircuitCountAdjDown, phivAdjPriority=phivAdjPriority, phivEndCountUsrBytesRec=phivEndCountUsrBytesRec, phivEndDelay=phivEndDelay, phivDDCMPLineCountIndex=phivDDCMPLineCountIndex, phivControlDeadTimer=phivControlDeadTimer, phivEndDelayFact=phivEndDelayFact, phivCircuitCountTermPacketsRecd=phivCircuitCountTermPacketsRecd, phivLineReceiveBuffs=phivLineReceiveBuffs, phivLineState=phivLineState, phivEndRemoteState=phivEndRemoteState, PhivCounter=PhivCounter, phivEthRouterPri=phivEthRouterPri, phivEthLinkIndex=phivEthLinkIndex, phivCircuitIndex=phivCircuitIndex, ddcmp=ddcmp, phivDDCMPCircuitParametersTable=phivDDCMPCircuitParametersTable, phivLevel1RouteTable=phivLevel1RouteTable, phivRouteCountZeroCount=phivRouteCountZeroCount, phivEndCountRecdConnectResErrs=phivEndCountRecdConnectResErrs, phivDDCMPLineCountEntry=phivDDCMPLineCountEntry, phivAreaHops=phivAreaHops, phivNonBroadcastController=phivNonBroadcastController, phivCountersCountSendFailure=phivCountersCountSendFailure, phivCountersCountUnrecFrameDest=phivCountersCountUnrecFrameDest, phivCountersCountDataOver=phivCountersCountDataOver, phivRouteMaxHops=phivRouteMaxHops, phivLevel1RouteCost=phivLevel1RouteCost, phivAreaMaxHops=phivAreaMaxHops, phivCountersCountBlksSentMultCol=phivCountersCountBlksSentMultCol, phivCircuitCountCircuitDown=phivCircuitCountCircuitDown, nonBroadcastLine=nonBroadcastLine, phivCircuitParametersTable=phivCircuitParametersTable, phivCircuitParametersEntry=phivCircuitParametersEntry, phivAdjNodeListenTimer=phivAdjNodeListenTimer, phivAreaCircuitIndex=phivAreaCircuitIndex, phivAdjCircuitIndex=phivAdjCircuitIndex, phivDDCMPCircuitAdjNodeAddr=phivDDCMPCircuitAdjNodeAddr, PhivAddr=PhivAddr, phivAdjBlockSize=phivAdjBlockSize, phivRouteMaxCost=phivRouteMaxCost, phivCountersCountBlksSentSingleCol=phivCountersCountBlksSentSingleCol, phivAdjCircuitEtherServPhysAddr=phivAdjCircuitEtherServPhysAddr, phivNonBroadcastRetransmitTimer=phivNonBroadcastRetransmitTimer, phivCountersCountMcastBlksRecd=phivCountersCountMcastBlksRecd, phivExecIdent=phivExecIdent, phivRouteBroadcastRouteTimer=phivRouteBroadcastRouteTimer, phivDDCMPCircuitParametersEntry=phivDDCMPCircuitParametersEntry, phivRouteCountVerifReject=phivRouteCountVerifReject, phivControlDelayTimer=phivControlDelayTimer, phivControlBabbleTimer=phivControlBabbleTimer, phivCircuitCountTransitCongestLoss=phivCircuitCountTransitCongestLoss, phivEthLinkParametersTable=phivEthLinkParametersTable, session=session, phivAreaNum=phivAreaNum, phivCircuitCommonSubState=phivCircuitCommonSubState, phivCircuitCountDataBlocksRecd=phivCircuitCountDataBlocksRecd, phivControlDyingBase=phivControlDyingBase, phivEndUCountUsrMessRec=phivEndUCountUsrMessRec, phivDDCMPLineCountTable=phivDDCMPLineCountTable, phivLevel1RouteCircuitIndex=phivLevel1RouteCircuitIndex, end=end, phivEndCountUsrMessSent=phivEndCountUsrMessSent, phivEndCountUsrBytesSent=phivEndCountUsrBytesSent, phivCountersCountDataBlocksRecd=phivCountersCountDataBlocksRecd, phivRouteMaxArea=phivRouteMaxArea, phivCountersCountBytesRecd=phivCountersCountBytesRecd, phivEndCountTotalMessSent=phivEndCountTotalMessSent, phivEndActiveLinks=phivEndActiveLinks, phivEndCountSecsLastZeroed=phivEndCountSecsLastZeroed, phivAdjExecListenTimer=phivAdjExecListenTimer, phivAdjAddr=phivAdjAddr, phivControlMaxBuffs=phivControlMaxBuffs, phivControlStreamTimer=phivControlStreamTimer, phivAreaTable=phivAreaTable, phivEndMaxLinks=phivEndMaxLinks, phivEndRemoteTable=phivEndRemoteTable, phivAdjNodeCircuitIndex=phivAdjNodeCircuitIndex, phivCountersCountBlksSentDef=phivCountersCountBlksSentDef, phivCircuitCountDataBlocksSent=phivCircuitCountDataBlocksSent, phivCircuitCountOriginPackSent=phivCircuitCountOriginPackSent, phivDDCMPCircuitLocalBuffErrors=phivDDCMPCircuitLocalBuffErrors, phivLineService=phivLineService, phiv=phiv, phivCircuitCommonName=phivCircuitCommonName, phivDDCMPLineCountDataErrsIn=phivDDCMPLineCountDataErrsIn, phivEndDelayWeight=phivEndDelayWeight, phivDDCMPCircuitLocalReplyTimeouts=phivDDCMPCircuitLocalReplyTimeouts, phivRouteCountOutRngePktLoss=phivRouteCountOutRngePktLoss, phivLevel1RouteEntry=phivLevel1RouteEntry, phivAdjNodeAddr=phivAdjNodeAddr, phivCountersCountEthUsrBuffUnav=phivCountersCountEthUsrBuffUnav, phivCircuitLineIndex=phivCircuitLineIndex, phivCircuitCountUsrBuffUnav=phivCircuitCountUsrBuffUnav, phivAreaNextNode=phivAreaNextNode, phivControlMaxTransmits=phivControlMaxTransmits, phivAreaState=phivAreaState, phivEndCountEntry=phivEndCountEntry, phivRouteMaxCircuits=phivRouteMaxCircuits, phivAdjState=phivAdjState, phivAreaMaxCost=phivAreaMaxCost, phivCircuitCountInitFailure=phivCircuitCountInitFailure, phivRouteRoutingVers=phivRouteRoutingVers, phivCircuitExecCost=phivCircuitExecCost, phivCircuitCountTransitPkSent=phivCircuitCountTransitPkSent, phivAdjEntry=phivAdjEntry, phivLineDevice=phivLineDevice, phivSessionOutTimer=phivSessionOutTimer, phivCountersCountMcastBytesRecd=phivCountersCountMcastBytesRecd, phivRouteCountAgedPktLoss=phivRouteCountAgedPktLoss, phivLineIndex=phivLineIndex, phivMgmtMgmtVers=phivMgmtMgmtVers, phivRouteMaxVisits=phivRouteMaxVisits, phivDDCMPCircuitErrorsOutbd=phivDDCMPCircuitErrorsOutbd, phivAdjNodeState=phivAdjNodeState, phivRouteMaxBuffs=phivRouteMaxBuffs, phivDDCMPCircuitTributary=phivDDCMPCircuitTributary, phivRouteSystemAddr=phivRouteSystemAddr, phivCircuitExecHelloTimer=phivCircuitExecHelloTimer, phivCountersCountCollDetectFailure=phivCountersCountCollDetectFailure, phivDDCMPLineCountLocalStationErrs=phivDDCMPLineCountLocalStationErrs, phivControlInactTreshold=phivControlInactTreshold, phivEndCountHostNodeID=phivEndCountHostNodeID, phivEndRetransmitFactor=phivEndRetransmitFactor, phivControlCircuitIndex=phivControlCircuitIndex, phivLineName=phivLineName, phivEndCountConnectsRecd=phivEndCountConnectsRecd, phivControlDyingIncrement=phivControlDyingIncrement, circuit=circuit, phivEthMaxRouters=phivEthMaxRouters, phivCountersCountSysBuffUnav=phivCountersCountSysBuffUnav, phivEndCountTotalBytesRec=phivEndCountTotalBytesRec, phivAdjNodePriority=phivAdjNodePriority, phivNonBroadcastEntry=phivNonBroadcastEntry, phivControlPollingState=phivControlPollingState, phivEndCountConnectsSent=phivEndCountConnectsSent, phivEndNSPVers=phivEndNSPVers, phivAdjNodeType=phivAdjNodeType, phivCircuitCommonState=phivCircuitCommonState, phivCircuitCountEntry=phivCircuitCountEntry, phivRouteCountNodeUnrPktLoss=phivRouteCountNodeUnrPktLoss, phivEndCircuitIndex=phivEndCircuitIndex, phivNonBroadcastTable=phivNonBroadcastTable, phivCircuitCountBytesSent=phivCircuitCountBytesSent, phivCountersCountDataBlocksSent=phivCountersCountDataBlocksSent, phivSessionSystemName=phivSessionSystemName, phivLineTable=phivLineTable, phivLineServiceTimer=phivLineServiceTimer, phivCircuitOrigQueueLimit=phivCircuitOrigQueueLimit, phivControlTransTimer=phivControlTransTimer, phivRouteMaxBdcastRouters=phivRouteMaxBdcastRouters, phivControlParametersEntry=phivControlParametersEntry, phivCountersCountDataBlksSent=phivCountersCountDataBlksSent, phivCircuitCommonType=phivCircuitCommonType, phivControlDyingThreshold=phivControlDyingThreshold, phivAreaEntry=phivAreaEntry, phivLevel1RouteNodeAddr=phivLevel1RouteNodeAddr, phivCircuitCountPeakAdj=phivCircuitCountPeakAdj, phivRouteMaxBdcastNonRouters=phivRouteMaxBdcastNonRouters, phivEndMaxLinksActive=phivEndMaxLinksActive, adjacency=adjacency, phivEndCountTotalBytesSent=phivEndCountTotalBytesSent, InterfaceIndex=InterfaceIndex, ethernet=ethernet, phivEndCountZeroCount=phivEndCountZeroCount, phivCircuitCountTable=phivCircuitCountTable, phivManagement=phivManagement, phivCountersCountBytesSent=phivCountersCountBytesSent, phivCircuitCountTransitPksRecd=phivCircuitCountTransitPksRecd, area=area, phivEndCountTotalMessRec=phivEndCountTotalMessRec, phivCircuitService=phivCircuitService, phivDDCMPCircuitCountTable=phivDDCMPCircuitCountTable, phivNonBroadcastIndex=phivNonBroadcastIndex, phivEndRemoteHostNodeID=phivEndRemoteHostNodeID, phivDDCMPCircuitRmteReplyTimeouts=phivDDCMPCircuitRmteReplyTimeouts, phivNonBroadcastDuplex=phivNonBroadcastDuplex, phivNonBroadcastClock=phivNonBroadcastClock, phivControlParametersTable=phivControlParametersTable, phivEndCountReponseTimeouts=phivEndCountReponseTimeouts, phivEthHardwareAddr=phivEthHardwareAddr, phivCircuitExecRecallTimer=phivCircuitExecRecallTimer, phivAdjType=phivAdjType, phivAdjNodeTable=phivAdjNodeTable, phivRouteSystemAddress=phivRouteSystemAddress, counters=counters, phivRouteMaxAddr=phivRouteMaxAddr, phivLineEntry=phivLineEntry, phivRouteRoutingTimer=phivRouteRoutingTimer, phivRouteType=phivRouteType, phivDDCMPCircuitErrorsInbd=phivDDCMPCircuitErrorsInbd, phivAdjNodeCircuitEtherServPhysAddr=phivAdjNodeCircuitEtherServPhysAddr, phivCircuitCountZeroCount=phivCircuitCountZeroCount, phivCircuitCountBytesRecd=phivCircuitCountBytesRecd, phivCountersCountUsrBuffUnav=phivCountersCountUsrBuffUnav)