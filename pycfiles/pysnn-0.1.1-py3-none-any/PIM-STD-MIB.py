# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/PIM-STD-MIB.py
# Compiled at: 2016-02-13 18:23:42
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsUnion, ValueSizeConstraint, ValueRangeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueSizeConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection')
(IANAipRouteProtocol,) = mibBuilder.importSymbols('IANA-RTPROTO-MIB', 'IANAipRouteProtocol')
(InterfaceIndex, InterfaceIndexOrZero) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndex', 'InterfaceIndexOrZero')
(InetAddress, InetVersion, InetAddressPrefixLength, InetAddressType) = mibBuilder.importSymbols('INET-ADDRESS-MIB', 'InetAddress', 'InetVersion', 'InetAddressPrefixLength', 'InetAddressType')
(ObjectGroup, NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'NotificationGroup', 'ModuleCompliance')
(iso, Gauge32, TimeTicks, Unsigned32, mib_2, Counter64, MibIdentifier, IpAddress, NotificationType, ModuleIdentity, Integer32, Counter32, Bits, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn) = mibBuilder.importSymbols('SNMPv2-SMI', 'iso', 'Gauge32', 'TimeTicks', 'Unsigned32', 'mib-2', 'Counter64', 'MibIdentifier', 'IpAddress', 'NotificationType', 'ModuleIdentity', 'Integer32', 'Counter32', 'Bits', 'ObjectIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn')
(TruthValue, DisplayString, TextualConvention, StorageType, RowStatus) = mibBuilder.importSymbols('SNMPv2-TC', 'TruthValue', 'DisplayString', 'TextualConvention', 'StorageType', 'RowStatus')
pimStdMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 157)).setRevisions(('2007-11-02 00:00',))
if mibBuilder.loadTexts:
    pimStdMIB.setLastUpdated('200711020000Z')
if mibBuilder.loadTexts:
    pimStdMIB.setOrganization('IETF Protocol Independent Multicast (PIM) Working Group')
if mibBuilder.loadTexts:
    pimStdMIB.setContactInfo('Email: pim@ietf.org\n            WG charter:\n\n            http://www.ietf.org/html.charters/pim-charter.html')
if mibBuilder.loadTexts:
    pimStdMIB.setDescription('The MIB module for management of PIM routers.\n\n            Copyright (C) The IETF Trust (2007).  This version of this\n            MIB module is part of RFC 5060; see the RFC itself for full\n            legal notices.')

class PimMode(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))
    namedValues = NamedValues(('none', 1), ('ssm', 2), ('asm', 3), ('bidir', 4), ('dm',
                                                                                  5), ('other',
                                                                                       6))


class PimGroupMappingOriginType(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7))
    namedValues = NamedValues(('fixed', 1), ('configRp', 2), ('configSsm', 3), ('bsr',
                                                                                4), ('autoRP',
                                                                                     5), ('embedded',
                                                                                          6), ('other',
                                                                                               7))


pimNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 157, 0))
pim = MibIdentifier((1, 3, 6, 1, 2, 1, 157, 1))
pimKeepalivePeriod = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 14), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(210)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimKeepalivePeriod.setDescription('The duration of the Keepalive Timer.  This is the period\n            during which the PIM router will maintain (S,G) state in the\n            absence of explicit (S,G) local membership or (S,G) join\n            messages received to maintain it.  This timer period is\n            called the Keepalive_Period in the PIM-SM specification.  It\n            is called the SourceLifetime in the PIM-DM specification.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.')
pimRegisterSuppressionTime = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 15), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(60)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimRegisterSuppressionTime.setDescription('The duration of the Register Suppression Timer.  This is\n            the period during which a PIM Designated Router (DR) stops\n            sending Register-encapsulated data to the Rendezvous Point\n            (RP) after receiving a Register-Stop message.  This object\n            is used to run timers both at the DR and at the RP.  This\n            timer period is called the Register_Suppression_Time in the\n            PIM-SM specification.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.')
pimStarGEntries = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 16), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGEntries.setDescription('The number of entries in the pimStarGTable.')
pimStarGIEntries = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 17), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIEntries.setDescription('The number of entries in the pimStarGITable.')
pimSGEntries = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 18), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGEntries.setDescription('The number of entries in the pimSGTable.')
pimSGIEntries = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 19), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIEntries.setDescription('The number of entries in the pimSGITable.')
pimSGRptEntries = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 20), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptEntries.setDescription('The number of entries in the pimSGRptTable.')
pimSGRptIEntries = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 21), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptIEntries.setDescription('The number of entries in the pimSGRptITable.')
pimOutAsserts = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 22), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimOutAsserts.setDescription('The number of Asserts sent by this router.\n\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, for example,\n            when the device is rebooted.')
pimInAsserts = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 23), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInAsserts.setDescription('The number of Asserts received by this router.  Asserts\n            are multicast to all routers on a network.  This counter is\n            incremented by all routers that receive an assert, not only\n            those routers that are contesting the assert.\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, for example,\n            when the device is rebooted.')
pimLastAssertInterface = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 24), InterfaceIndexOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimLastAssertInterface.setDescription('The interface on which this router most recently sent or\n            received an assert, or zero if this router has not sent or\n            received an assert.')
pimLastAssertGroupAddressType = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 25), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimLastAssertGroupAddressType.setDescription('The address type of the multicast group address in the most\n            recently sent or received assert.  If this router has not\n            sent or received an assert, then this object is set to\n            unknown(0).')
pimLastAssertGroupAddress = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 26), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimLastAssertGroupAddress.setDescription('The multicast group address in the most recently sent or\n            received assert.  The InetAddressType is given by the\n            pimLastAssertGroupAddressType object.')
pimLastAssertSourceAddressType = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 27), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimLastAssertSourceAddressType.setDescription('The address type of the source address in the most recently\n            sent or received assert.  If the most recent assert was\n            (*,G), or if this router has not sent or received an assert,\n            then this object is set to unknown(0).')
pimLastAssertSourceAddress = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 28), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimLastAssertSourceAddress.setDescription('The source address in the most recently sent or received\n            assert.  The InetAddressType is given by the\n            pimLastAssertSourceAddressType object.')
pimNeighborLossNotificationPeriod = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 29), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimNeighborLossNotificationPeriod.setDescription("The minimum time that must elapse between pimNeighborLoss\n            notifications originated by this router.  The maximum value\n            65535 represents an 'infinite' time, in which case, no\n            pimNeighborLoss notifications are ever sent.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.")
pimNeighborLossCount = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 30), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborLossCount.setDescription('The number of neighbor loss events that have occurred.\n\n            This counter is incremented when the neighbor timer expires,\n            and the router has no other neighbors on the same interface\n            with the same IP version and a lower IP address than itself.\n\n            This counter is incremented whenever a pimNeighborLoss\n            notification would be generated.\n\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, for example,\n            when the device is rebooted.')
pimInvalidRegisterNotificationPeriod = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 31), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(10, 65535)).clone(65535)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimInvalidRegisterNotificationPeriod.setDescription("The minimum time that must elapse between\n            pimInvalidRegister notifications originated by this router.\n            The default value of 65535 represents an 'infinite' time, in\n            which case, no pimInvalidRegister notifications are ever\n            sent.\n\n            The non-zero minimum allowed value provides resilience\n            against propagation of denial-of-service attacks from the\n            data and control planes to the network management plane.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.")
pimInvalidRegisterMsgsRcvd = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 32), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidRegisterMsgsRcvd.setDescription('The number of invalid PIM Register messages that have been\n            received by this device.\n\n            A PIM Register message is invalid if either\n\n            o the destination address of the Register message does not\n              match the Group to RP mapping on this device, or\n\n            o this device believes the group address to be within an\n              SSM address range, but this Register implies ASM usage.\n\n            These conditions can occur transiently while RP mapping\n            changes propagate through the network.  If this counter is\n            incremented repeatedly over several minutes, then there is a\n            persisting configuration error that requires correction.\n\n            The active Group to RP mapping on this device is specified\n            by the object pimGroupMappingPimMode.  If there is no such\n            mapping, then the object pimGroupMappingPimMode is absent.\n            The RP address contained in the invalid Register is\n            pimInvalidRegisterRp.\n\n            Multicast data carried by invalid Register messages is\n            discarded.  The discarded data is from a source directly\n            connected to pimInvalidRegisterOrigin, and is addressed to\n            pimInvalidRegisterGroup.\n\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, for example,\n            when the device is rebooted.')
pimInvalidRegisterAddressType = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 33), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidRegisterAddressType.setDescription('The address type stored in pimInvalidRegisterOrigin,\n            pimInvalidRegisterGroup, and pimInvalidRegisterRp.\n\n            If no invalid Register messages have been received, then\n            this object is set to unknown(0).')
pimInvalidRegisterOrigin = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 34), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidRegisterOrigin.setDescription('The source address of the last invalid Register message\n            received by this device.')
pimInvalidRegisterGroup = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 35), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidRegisterGroup.setDescription('The IP multicast group address to which the last invalid\n            Register message received by this device was addressed.')
pimInvalidRegisterRp = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 36), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidRegisterRp.setDescription('The RP address to which the last invalid Register message\n            received by this device was delivered.')
pimInvalidJoinPruneNotificationPeriod = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 37), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(10, 65535)).clone(65535)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimInvalidJoinPruneNotificationPeriod.setDescription("The minimum time that must elapse between\n            pimInvalidJoinPrune notifications originated by this router.\n            The default value of 65535 represents an 'infinite' time, in\n            which case, no pimInvalidJoinPrune notifications are ever\n            sent.\n\n            The non-zero minimum allowed value provides resilience\n            against propagation of denial-of-service attacks from the\n            control plane to the network management plane.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.")
pimInvalidJoinPruneMsgsRcvd = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 38), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidJoinPruneMsgsRcvd.setDescription('The number of invalid PIM Join/Prune messages that have\n            been received by this device.\n\n            A PIM Join/Prune message is invalid if either\n\n            o the Group to RP mapping specified by this message does not\n              match the Group to RP mapping on this device, or\n\n            o this device believes the group address to be within an\n              SSM address range, but this Join/Prune (*,G) or (S,G,rpt)\n              implies ASM usage.\n\n            These conditions can occur transiently while RP mapping\n            changes propagate through the network.  If this counter is\n            incremented repeatedly over several minutes, then there is a\n            persisting configuration error that requires correction.\n\n            The active Group to RP mapping on this device is specified\n            by the object pimGroupMappingPimMode.  If there is no such\n            mapping, then the object pimGroupMappingPimMode is absent.\n            The RP address contained in the invalid Join/Prune is\n            pimInvalidJoinPruneRp.\n            Invalid Join/Prune messages are discarded.  This may result\n            in loss of multicast data affecting listeners downstream of\n            pimInvalidJoinPruneOrigin, for multicast data addressed to\n            pimInvalidJoinPruneGroup.\n\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, for example,\n            when the device is rebooted.')
pimInvalidJoinPruneAddressType = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 39), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidJoinPruneAddressType.setDescription('The address type stored in pimInvalidJoinPruneOrigin,\n            pimInvalidJoinPruneGroup, and pimInvalidJoinPruneRp.\n\n            If no invalid Join/Prune messages have been received, this\n            object is set to unknown(0).')
pimInvalidJoinPruneOrigin = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 40), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidJoinPruneOrigin.setDescription('The source address of the last invalid Join/Prune message\n            received by this device.')
pimInvalidJoinPruneGroup = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 41), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidJoinPruneGroup.setDescription('The IP multicast group address carried in the last\n            invalid Join/Prune message received by this device.')
pimInvalidJoinPruneRp = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 42), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInvalidJoinPruneRp.setDescription('The RP address carried in the last invalid Join/Prune\n            message received by this device.')
pimRPMappingNotificationPeriod = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 43), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(65535)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimRPMappingNotificationPeriod.setDescription("The minimum time that must elapse between\n            pimRPMappingChange notifications originated by this router.\n            The default value of 65535 represents an 'infinite' time, in\n            which case, no pimRPMappingChange notifications are ever\n            sent.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.")
pimRPMappingChangeCount = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 44), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimRPMappingChangeCount.setDescription('The number of changes to active RP mappings on this device.\n\n            Information about active RP mappings is available in\n            pimGroupMappingTable.  Only changes to active mappings cause\n            this counter to be incremented.  That is, changes that\n            modify the pimGroupMappingEntry with the highest precedence\n            for a group (lowest value of pimGroupMappingPrecedence).\n\n            Such changes may result from manual configuration of this\n            device, or from automatic RP mapping discovery methods\n            including the PIM Bootstrap Router (BSR) mechanism.\n\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, for example,\n            when the device is rebooted.')
pimInterfaceElectionNotificationPeriod = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 45), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(65535)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimInterfaceElectionNotificationPeriod.setDescription("The minimum time that must elapse between\n            pimInterfaceElection notifications originated by this\n            router.  The default value of 65535 represents an 'infinite'\n            time, in which case, no pimInterfaceElection notifications\n            are ever sent.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.")
pimInterfaceElectionWinCount = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 46), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceElectionWinCount.setDescription('The number of times this device has been elected DR or DF\n            on any interface.\n\n            Elections occur frequently on newly-active interfaces, as\n            triggered Hellos establish adjacencies.  This counter is not\n            incremented for elections on an interface until the first\n            periodic Hello has been sent.  If this router is the DR or\n            DF at the time of sending the first periodic Hello after\n            interface activation, then this counter is incremented\n            (once) at that time.\n\n            Discontinuities in the value of this counter can occur at\n            re-initialization of the management system, for example,\n            when the device is rebooted.')
pimRefreshInterval = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 47), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(60)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimRefreshInterval.setDescription('The interval between successive State Refresh messages sent\n            by an Originator.  This timer period is called the\n            RefreshInterval in the PIM-DM specification.  This object is\n            used only by PIM-DM.\n\n            The storage type of this object is determined by\n            pimDeviceConfigStorageType.')
pimDeviceConfigStorageType = MibScalar((1, 3, 6, 1, 2, 1, 157, 1, 48), StorageType().clone('nonVolatile')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    pimDeviceConfigStorageType.setDescription("The storage type used for the global PIM configuration of\n            this device, comprised of the objects listed below.  If this\n            storage type takes the value 'permanent', write-access to\n            the listed objects need not be allowed.\n\n            The objects described by this storage type are:\n            pimKeepalivePeriod, pimRegisterSuppressionTime,\n            pimNeighborLossNotificationPeriod,\n            pimInvalidRegisterNotificationPeriod,\n            pimInvalidJoinPruneNotificationPeriod,\n            pimRPMappingNotificationPeriod,\n            pimInterfaceElectionNotificationPeriod, and\n            pimRefreshInterval.")
pimInterfaceTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 1))
if mibBuilder.loadTexts:
    pimInterfaceTable.setDescription("The (conceptual) table listing the router's PIM interfaces.\n            PIM is enabled on all interfaces listed in this table.")
pimInterfaceEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 1, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimInterfaceIfIndex'), (0, 'PIM-STD-MIB', 'pimInterfaceIPVersion'))
if mibBuilder.loadTexts:
    pimInterfaceEntry.setDescription('An entry (conceptual row) in the pimInterfaceTable.  This\n            entry is preserved on agent restart.')
pimInterfaceIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    pimInterfaceIfIndex.setDescription('The ifIndex value of this PIM interface.')
pimInterfaceIPVersion = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 2), InetVersion())
if mibBuilder.loadTexts:
    pimInterfaceIPVersion.setDescription('The IP version of this PIM interface.  A physical interface\n            may be configured in multiple modes concurrently, e.g., IPv4\n            and IPv6; however, the traffic is considered to be logically\n            separate.')
pimInterfaceAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 3), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceAddressType.setDescription('The address type of this PIM interface.')
pimInterfaceAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 4), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceAddress.setDescription('The primary IP address of this router on this PIM\n            interface.  The InetAddressType is given by the\n            pimInterfaceAddressType object.')
pimInterfaceGenerationIDValue = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 5), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceGenerationIDValue.setDescription('The value of the Generation ID this router inserted in the\n            last PIM Hello message it sent on this interface.')
pimInterfaceDR = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 6), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceDR.setDescription('The primary IP address of the Designated Router on this PIM\n            interface.  The InetAddressType is given by the\n            pimInterfaceAddressType object.')
pimInterfaceDRPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 7), Unsigned32().clone(1)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceDRPriority.setDescription('The Designated Router Priority value inserted into the DR\n            Priority option in PIM Hello messages transmitted on this\n            interface.  Numerically higher values for this object\n            indicate higher priorities.')
pimInterfaceDRPriorityEnabled = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceDRPriorityEnabled.setDescription('Evaluates to TRUE if all routers on this interface are\n            using the DR Priority option.')
pimInterfaceHelloInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 9), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 18000)).clone(30)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceHelloInterval.setDescription("The frequency at which PIM Hello messages are transmitted\n            on this interface.  This object corresponds to the\n            'Hello_Period' timer value defined in the PIM-SM\n            specification.  A value of zero represents an 'infinite'\n            interval, and indicates that periodic PIM Hello messages\n            should not be sent on this interface.")
pimInterfaceTrigHelloInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 10), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 60)).clone(5)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceTrigHelloInterval.setDescription("The maximum time before this router sends a triggered PIM\n            Hello message on this interface.  This object corresponds to\n            the 'Trigered_Hello_Delay' timer value defined in the PIM-SM\n            specification.  A value of zero has no special meaning and\n            indicates that triggered PIM Hello messages should always be\n            sent immediately.")
pimInterfaceHelloHoldtime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 11), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(105)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceHelloHoldtime.setDescription("The value set in the Holdtime field of PIM Hello messages\n            transmitted on this interface.  A value of 65535 represents\n            an 'infinite' holdtime.  Implementations are recommended\n            to use a holdtime that is 3.5 times the value of\n            pimInterfaceHelloInterval, or 65535 if\n            pimInterfaceHelloInterval is set to zero.")
pimInterfaceJoinPruneInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 12), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 18000)).clone(60)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceJoinPruneInterval.setDescription("The frequency at which this router sends PIM Join/Prune\n            messages on this PIM interface.  This object corresponds to\n            the 't_periodic' timer value defined in the PIM-SM\n            specification.  A value of zero represents an 'infinite'\n            interval, and indicates that periodic PIM Join/Prune\n            messages should not be sent on this interface.")
pimInterfaceJoinPruneHoldtime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 13), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(210)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceJoinPruneHoldtime.setDescription("The value inserted into the Holdtime field of a PIM\n            Join/Prune message sent on this interface.  A value of 65535\n            represents an 'infinite' holdtime.  Implementations are\n            recommended to use a holdtime that is 3.5 times the value of\n            pimInterfaceJoinPruneInterval, or 65535 if\n            pimInterfaceJoinPruneInterval is set to zero.  PIM-DM\n            implementations are recommended to use the value of\n            pimInterfacePruneLimitInterval.")
pimInterfaceDFElectionRobustness = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 14), Unsigned32().clone(3)).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceDFElectionRobustness.setDescription('The minimum number of PIM DF-Election messages that must be\n            lost in order for DF election on this interface to fail.')
pimInterfaceLanDelayEnabled = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 15), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceLanDelayEnabled.setDescription('Evaluates to TRUE if all routers on this interface are\n            using the LAN Prune Delay option.')
pimInterfacePropagationDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 16), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 32767)).clone(500)).setUnits('milliseconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfacePropagationDelay.setDescription('The expected propagation delay between PIM routers on this\n            network or link.\n\n            This router inserts this value into the Propagation_Delay\n            field of the LAN Prune Delay option in the PIM Hello\n            messages sent on this interface.  Implementations SHOULD\n            enforce a lower bound on the permitted values for this\n            object to allow for scheduling and processing delays within\n            the local router.')
pimInterfaceOverrideInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 17), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(2500)).setUnits('milliseconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceOverrideInterval.setDescription('The value this router inserts into the Override_Interval\n            field of the LAN Prune Delay option in the PIM Hello\n            messages it sends on this interface.\n\n            When overriding a prune, PIM routers pick a random timer\n            duration up to the value of this object.  The more PIM\n            routers that are active on a network, the more likely it is\n            that the prune will be overridden after a small proportion\n            of this time has elapsed.\n\n            The more PIM routers are active on this network, the larger\n            this object should be to obtain an optimal spread of prune\n            override latencies.')
pimInterfaceEffectPropagDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 18), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 32767))).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceEffectPropagDelay.setDescription('The Effective Propagation Delay on this interface.  This\n            object is always 500 if pimInterfaceLanDelayEnabled is\n            FALSE.')
pimInterfaceEffectOverrideIvl = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 19), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setUnits('milliseconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceEffectOverrideIvl.setDescription('The Effective Override Interval on this interface.  This\n            object is always 2500 if pimInterfaceLanDelayEnabled is\n            FALSE.')
pimInterfaceSuppressionEnabled = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 20), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceSuppressionEnabled.setDescription('Whether join suppression is enabled on this interface.\n            This object is always TRUE if pimInterfaceLanDelayEnabled is\n            FALSE.')
pimInterfaceBidirCapable = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 21), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceBidirCapable.setDescription('Evaluates to TRUE if all routers on this interface are\n            using the Bidirectional-PIM Capable option.')
pimInterfaceDomainBorder = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 22), TruthValue().clone('false')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceDomainBorder.setDescription('Whether or not this interface is a PIM domain border.  This\n            includes acting as a border for PIM Bootstrap Router (BSR)\n            messages, if the BSR mechanism is in use.')
pimInterfaceStubInterface = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 23), TruthValue().clone('false')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceStubInterface.setDescription("Whether this interface is a 'stub interface'.  If this\n            object is set to TRUE, then no PIM packets are sent out this\n            interface, and any received PIM packets are ignored.\n\n            Setting this object to TRUE is a security measure for\n            interfaces towards untrusted hosts.  This allows an\n            interface to be configured for use with IGMP (Internet Group\n            Management Protocol) or MLD (Multicast Listener Discovery)\n            only, which protects the PIM router from forged PIM messages\n            on the interface.\n\n            To communicate with other PIM routers using this interface,\n            this object must remain set to FALSE.\n\n            Changing the value of this object while the interface is\n            operational causes PIM to be disabled and then re-enabled on\n            this interface.")
pimInterfacePruneLimitInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 24), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(60)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfacePruneLimitInterval.setDescription("The minimum interval that must transpire between two\n            successive Prunes sent by a router.  This object corresponds\n            to the 't_limit' timer value defined in the PIM-DM\n            specification.  This object is used only by PIM-DM.")
pimInterfaceGraftRetryInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 25), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)).clone(3)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceGraftRetryInterval.setDescription("The minimum interval that must transpire between two\n            successive Grafts sent by a router.  This object corresponds\n            to the 'Graft_Retry_Period' timer value defined in the\n            PIM-DM specification.  This object is used only by PIM-DM.")
pimInterfaceSRPriorityEnabled = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 26), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimInterfaceSRPriorityEnabled.setDescription('Evaluates to TRUE if all routers on this interface are\n            using the State Refresh option.  This object is used only by\n            PIM-DM.')
pimInterfaceStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 27), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceStatus.setDescription('The status of this entry.  Creating the entry enables PIM\n            on the interface; destroying the entry disables PIM on the\n            interface.\n\n            This status object can be set to active(1) without setting\n            any other columnar objects in this entry.\n\n            All writable objects in this entry can be modified when the\n            status of this entry is active(1).')
pimInterfaceStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 1, 1, 28), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimInterfaceStorageType.setDescription("The storage type for this row.  Rows having the value\n            'permanent' need not allow write-access to any columnar\n            objects in the row.")
pimNeighborTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 2))
if mibBuilder.loadTexts:
    pimNeighborTable.setDescription("The (conceptual) table listing the router's PIM neighbors.")
pimNeighborEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 2, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimNeighborIfIndex'), (0, 'PIM-STD-MIB', 'pimNeighborAddressType'), (0, 'PIM-STD-MIB', 'pimNeighborAddress'))
if mibBuilder.loadTexts:
    pimNeighborEntry.setDescription('An entry (conceptual row) in the pimNeighborTable.')
pimNeighborIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    pimNeighborIfIndex.setDescription('The value of ifIndex for the interface used to reach this\n            PIM neighbor.')
pimNeighborAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 2), InetAddressType())
if mibBuilder.loadTexts:
    pimNeighborAddressType.setDescription('The address type of this PIM neighbor.')
pimNeighborAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 3), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimNeighborAddress.setDescription('The primary IP address of this PIM neighbor.  The\n            InetAddressType is given by the pimNeighborAddressType\n            object.')
pimNeighborGenerationIDPresent = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 4), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborGenerationIDPresent.setDescription('Evaluates to TRUE if this neighbor is using the Generation\n            ID option.')
pimNeighborGenerationIDValue = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 5), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborGenerationIDValue.setDescription('The value of the Generation ID from the last PIM Hello\n            message received from this neighbor.  This object is always\n            zero if pimNeighborGenerationIDPresent is FALSE.')
pimNeighborUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 6), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborUpTime.setDescription('The time since this PIM neighbor (last) became a neighbor\n            of the local router.')
pimNeighborExpiryTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 7), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborExpiryTime.setDescription('The minimum time remaining before this PIM neighbor will\n            time out.  The value zero indicates that this PIM neighbor\n            will never time out.')
pimNeighborDRPriorityPresent = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborDRPriorityPresent.setDescription('Evaluates to TRUE if this neighbor is using the DR Priority\n            option.')
pimNeighborDRPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 9), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborDRPriority.setDescription('The value of the Designated Router Priority from the last\n            PIM Hello message received from this neighbor.  This object\n            is always zero if pimNeighborDRPriorityPresent is FALSE.')
pimNeighborLanPruneDelayPresent = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 10), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborLanPruneDelayPresent.setDescription('Evaluates to TRUE if this neighbor is using the LAN Prune\n            Delay option.')
pimNeighborTBit = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 11), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborTBit.setDescription('Whether the T bit was set in the LAN Prune Delay option\n            received from this neighbor.  The T bit specifies the\n            ability of the neighbor to disable join suppression.  This\n            object is always TRUE if pimNeighborLanPruneDelayPresent is\n            FALSE.')
pimNeighborPropagationDelay = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 12), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 32767))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborPropagationDelay.setDescription('The value of the Propagation_Delay field of the LAN Prune\n            Delay option received from this neighbor.  This object is\n            always zero if pimNeighborLanPruneDelayPresent is FALSE.')
pimNeighborOverrideInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 13), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborOverrideInterval.setDescription('The value of the Override_Interval field of the LAN Prune\n            Delay option received from this neighbor.  This object is\n            always zero if pimNeighborLanPruneDelayPresent is FALSE.')
pimNeighborBidirCapable = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 14), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborBidirCapable.setDescription('Evaluates to TRUE if this neighbor is using the\n            Bidirectional-PIM Capable option.')
pimNeighborSRCapable = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 2, 1, 15), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNeighborSRCapable.setDescription('Evaluates to TRUE if this neighbor is using the State\n            Refresh Capable option.  This object is used only by\n            PIM-DM.')
pimNbrSecAddressTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 3))
if mibBuilder.loadTexts:
    pimNbrSecAddressTable.setDescription('The (conceptual) table listing the secondary addresses\n            advertised by each PIM neighbor (on a subset of the rows of\n            the pimNeighborTable defined above).')
pimNbrSecAddressEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 3, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimNbrSecAddressIfIndex'), (0, 'PIM-STD-MIB', 'pimNbrSecAddressType'), (0, 'PIM-STD-MIB', 'pimNbrSecAddressPrimary'), (0, 'PIM-STD-MIB', 'pimNbrSecAddress'))
if mibBuilder.loadTexts:
    pimNbrSecAddressEntry.setDescription('An entry (conceptual row) in the pimNbrSecAddressTable.')
pimNbrSecAddressIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 3, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    pimNbrSecAddressIfIndex.setDescription('The value of ifIndex for the interface used to reach this\n            PIM neighbor.')
pimNbrSecAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 3, 1, 2), InetAddressType())
if mibBuilder.loadTexts:
    pimNbrSecAddressType.setDescription('The address type of this PIM neighbor.')
pimNbrSecAddressPrimary = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 3, 1, 3), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimNbrSecAddressPrimary.setDescription('The primary IP address of this PIM neighbor.  The\n            InetAddressType is given by the pimNbrSecAddressType\n            object.')
pimNbrSecAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 3, 1, 4), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimNbrSecAddress.setDescription('The secondary IP address of this PIM neighbor.  The\n            InetAddressType is given by the pimNbrSecAddressType\n            object.')
pimStarGTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 4))
if mibBuilder.loadTexts:
    pimStarGTable.setDescription('The (conceptual) table listing the non-interface specific\n            (*,G) state that PIM has.')
pimStarGEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 4, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimStarGAddressType'), (0, 'PIM-STD-MIB', 'pimStarGGrpAddress'))
if mibBuilder.loadTexts:
    pimStarGEntry.setDescription('An entry (conceptual row) in the pimStarGTable.')
pimStarGAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 1), InetAddressType())
if mibBuilder.loadTexts:
    pimStarGAddressType.setDescription('The address type of this multicast group.')
pimStarGGrpAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 2), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimStarGGrpAddress.setDescription('The multicast group address.  The InetAddressType is given\n            by the pimStarGAddressType object.')
pimStarGUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 3), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGUpTime.setDescription('The time since this entry was created by the local router.')
pimStarGPimMode = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 4), PimMode().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(3, 4))).clone(namedValues=NamedValues(('asm', 3), ('bidir', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGPimMode.setDescription('Whether this entry represents an ASM (Any Source Multicast,\n            used with PIM-SM) or BIDIR-PIM group.')
pimStarGRPAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 5), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPAddressType.setDescription('The address type of the Rendezvous Point (RP), or\n            unknown(0) if the RP address is unknown.')
pimStarGRPAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 6), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPAddress.setDescription('The address of the Rendezvous Point (RP) for the group.\n            The InetAddressType is given by the pimStarGRPAddressType.')
pimStarGPimModeOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 7), PimGroupMappingOriginType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGPimModeOrigin.setDescription('The mechanism by which the PIM mode and RP for the group\n            were learned.')
pimStarGRPIsLocal = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPIsLocal.setDescription('Whether the local router is the RP for the group.')
pimStarGUpstreamJoinState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('notJoined', 1), ('joined', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGUpstreamJoinState.setDescription('Whether the local router should join the RP tree for the\n            group.  This corresponds to the state of the upstream (*,G)\n            state machine in the PIM-SM specification.')
pimStarGUpstreamJoinTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 10), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGUpstreamJoinTimer.setDescription('The time remaining before the local router next sends a\n            periodic (*,G) Join message on pimStarGRPFIfIndex.  This\n            timer is called the (*,G) Upstream Join Timer in the PIM-SM\n            specification.  This object is zero if the timer is not\n            running.')
pimStarGUpstreamNeighborType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 11), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGUpstreamNeighborType.setDescription('The primary address type of the upstream neighbor, or\n            unknown(0) if the upstream neighbor address is unknown or is\n            not a PIM neighbor.')
pimStarGUpstreamNeighbor = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 12), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGUpstreamNeighbor.setDescription("The primary address of the neighbor on pimStarGRPFIfIndex\n            that the local router is sending periodic (*,G) Join\n            messages to.  The InetAddressType is given by the\n            pimStarGUpstreamNeighborType object.  This address is called\n            RPF'(*,G) in the PIM-SM specification.")
pimStarGRPFIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 13), InterfaceIndexOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFIfIndex.setDescription('The value of ifIndex for the Reverse Path Forwarding\n            (RPF) interface towards the RP, or zero if the RPF\n            interface is unknown.')
pimStarGRPFNextHopType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 14), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFNextHopType.setDescription('The address type of the RPF next hop towards the RP, or\n            unknown(0) if the RPF next hop is unknown.')
pimStarGRPFNextHop = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 15), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFNextHop.setDescription('The address of the RPF next hop towards the RP.  The\n            InetAddressType is given by the pimStarGRPFNextHopType\n            object.  This address is called MRIB.next_hop(RP(G))\n            in the PIM-SM specification.')
pimStarGRPFRouteProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 16), IANAipRouteProtocol()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFRouteProtocol.setDescription('The routing mechanism via which the route used to find the\n            RPF interface towards the RP was learned.')
pimStarGRPFRouteAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 17), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFRouteAddress.setDescription('The IP address that, when combined with the corresponding\n            value of pimStarGRPFRoutePrefixLength, identifies the route\n            used to find the RPF interface towards the RP.  The\n            InetAddressType is given by the pimStarGRPFNextHopType\n            object.\n\n            This address object is only significant up to\n            pimStarGRPFRoutePrefixLength bits.  The remainder of the\n            address bits are zero.')
pimStarGRPFRoutePrefixLength = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 18), InetAddressPrefixLength()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFRoutePrefixLength.setDescription('The prefix length that, when combined with the\n            corresponding value of pimStarGRPFRouteAddress, identifies\n            the route used to find the RPF interface towards the RP.\n            The InetAddressType is given by the pimStarGRPFNextHopType\n            object.')
pimStarGRPFRouteMetricPref = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 19), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFRouteMetricPref.setDescription('The metric preference of the route used to find the RPF\n            interface towards the RP.')
pimStarGRPFRouteMetric = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 4, 1, 20), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGRPFRouteMetric.setDescription('The routing metric of the route used to find the RPF\n            interface towards the RP.')
pimStarGITable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 5))
if mibBuilder.loadTexts:
    pimStarGITable.setDescription('The (conceptual) table listing the interface-specific (*,G)\n            state that PIM has.')
pimStarGIEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 5, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimStarGAddressType'), (0, 'PIM-STD-MIB', 'pimStarGGrpAddress'), (0, 'PIM-STD-MIB', 'pimStarGIIfIndex'))
if mibBuilder.loadTexts:
    pimStarGIEntry.setDescription('An entry (conceptual row) in the pimStarGITable.')
pimStarGIIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    pimStarGIIfIndex.setDescription('The ifIndex of the interface that this entry corresponds\n            to.')
pimStarGIUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 2), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIUpTime.setDescription('The time since this entry was created by the local router.')
pimStarGILocalMembership = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGILocalMembership.setDescription('Whether the local router has (*,G) local membership on this\n            interface (resulting from a mechanism such as IGMP or MLD).\n            This corresponds to local_receiver_include(*,G,I) in the\n            PIM-SM specification.')
pimStarGIJoinPruneState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('noInfo', 1), ('join', 2), ('prunePending', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIJoinPruneState.setDescription('The state resulting from (*,G) Join/Prune messages\n            received on this interface.  This corresponds to the state\n            of the downstream per-interface (*,G) state machine in the\n            PIM-SM specification.')
pimStarGIPrunePendingTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 5), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIPrunePendingTimer.setDescription('The time remaining before the local router acts on a (*,G)\n            Prune message received on this interface, during which the\n            router is waiting to see whether another downstream router\n            will override the Prune message.  This timer is called the\n            (*,G) Prune-Pending Timer in the PIM-SM specification.  This\n            object is zero if the timer is not running.')
pimStarGIJoinExpiryTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 6), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIJoinExpiryTimer.setDescription("The time remaining before (*,G) Join state for this\n            interface expires.  This timer is called the (*,G) Join\n            Expiry Timer in the PIM-SM specification.  This object is\n            zero if the timer is not running.  A value of 'FFFFFFFF'h\n            indicates an infinite expiry time.")
pimStarGIAssertState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('noInfo', 1), ('iAmAssertWinner', 2), ('iAmAssertLoser', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIAssertState.setDescription("The (*,G) Assert state for this interface.  This\n            corresponds to the state of the per-interface (*,G) Assert\n            state machine in the PIM-SM specification.  If\n            pimStarGPimMode is 'bidir', this object must be 'noInfo'.")
pimStarGIAssertTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 8), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIAssertTimer.setDescription("If pimStarGIAssertState is 'iAmAssertWinner', this is the\n            time remaining before the local router next sends a (*,G)\n            Assert message on this interface.  If pimStarGIAssertState\n            is 'iAmAssertLoser', this is the time remaining before the\n            (*,G) Assert state expires.  If pimStarGIAssertState is\n            'noInfo', this is zero.  This timer is called the (*,G)\n            Assert Timer in the PIM-SM specification.")
pimStarGIAssertWinnerAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 9), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIAssertWinnerAddressType.setDescription("If pimStarGIAssertState is 'iAmAssertLoser', this is the\n            address type of the assert winner; otherwise, this object is\n            unknown(0).")
pimStarGIAssertWinnerAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 10), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIAssertWinnerAddress.setDescription("If pimStarGIAssertState is 'iAmAssertLoser', this is the\n            address of the assert winner.  The InetAddressType is given\n            by the pimStarGIAssertWinnerAddressType object.")
pimStarGIAssertWinnerMetricPref = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 11), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIAssertWinnerMetricPref.setDescription("If pimStarGIAssertState is 'iAmAssertLoser', this is the\n            metric preference of the route to the RP advertised by the\n            assert winner; otherwise, this object is zero.")
pimStarGIAssertWinnerMetric = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 5, 1, 12), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimStarGIAssertWinnerMetric.setDescription("If pimStarGIAssertState is 'iAmAssertLoser', this is the\n            routing metric of the route to the RP advertised by the\n            assert winner; otherwise, this object is zero.")
pimSGTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 6))
if mibBuilder.loadTexts:
    pimSGTable.setDescription('The (conceptual) table listing the non-interface specific\n            (S,G) state that PIM has.')
pimSGEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 6, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimSGAddressType'), (0, 'PIM-STD-MIB', 'pimSGGrpAddress'), (0, 'PIM-STD-MIB', 'pimSGSrcAddress'))
if mibBuilder.loadTexts:
    pimSGEntry.setDescription('An entry (conceptual row) in the pimSGTable.')
pimSGAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 1), InetAddressType())
if mibBuilder.loadTexts:
    pimSGAddressType.setDescription('The address type of the source and multicast group for this\n            entry.')
pimSGGrpAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 2), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimSGGrpAddress.setDescription('The multicast group address for this entry.  The\n            InetAddressType is given by the pimSGAddressType object.')
pimSGSrcAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 3), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimSGSrcAddress.setDescription('The source address for this entry.  The InetAddressType is\n            given by the pimSGAddressType object.')
pimSGUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 4), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGUpTime.setDescription('The time since this entry was created by the local router.')
pimSGPimMode = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 5), PimMode().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(2, 3))).clone(namedValues=NamedValues(('ssm', 2), ('asm', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGPimMode.setDescription('Whether pimSGGrpAddress is an SSM (Source Specific\n            Multicast, used with PIM-SM) or ASM (Any Source Multicast,\n            used with PIM-SM) group.')
pimSGUpstreamJoinState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('notJoined', 1), ('joined', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGUpstreamJoinState.setDescription('Whether the local router should join the shortest-path tree\n            for the source and group represented by this entry.  This\n            corresponds to the state of the upstream (S,G) state machine\n            in the PIM-SM specification.')
pimSGUpstreamJoinTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 7), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGUpstreamJoinTimer.setDescription('The time remaining before the local router next sends a\n            periodic (S,G) Join message on pimSGRPFIfIndex.  This timer\n            is called the (S,G) Upstream Join Timer in the PIM-SM\n            specification.  This object is zero if the timer is not\n            running.')
pimSGUpstreamNeighbor = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 8), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGUpstreamNeighbor.setDescription("The primary address of the neighbor on pimSGRPFIfIndex that\n            the local router is sending periodic (S,G) Join messages to.\n            This is zero if the RPF next hop is unknown or is not a\n            PIM neighbor.  The InetAddressType is given by the\n            pimSGAddressType object.  This address is called RPF'(S,G)\n            in the PIM-SM specification.")
pimSGRPFIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 9), InterfaceIndexOrZero()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFIfIndex.setDescription('The value of ifIndex for the RPF interface towards the\n            source, or zero if the RPF interface is unknown.')
pimSGRPFNextHopType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 10), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFNextHopType.setDescription('The address type of the RPF next hop towards the source, or\n            unknown(0) if the RPF next hop is unknown.')
pimSGRPFNextHop = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 11), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFNextHop.setDescription('The address of the RPF next hop towards the source.  The\n            InetAddressType is given by the pimSGRPFNextHopType.  This\n            address is called MRIB.next_hop(S) in the PIM-SM\n            specification.')
pimSGRPFRouteProtocol = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 12), IANAipRouteProtocol()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFRouteProtocol.setDescription('The routing mechanism via which the route used to find the\n            RPF interface towards the source was learned.')
pimSGRPFRouteAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 13), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFRouteAddress.setDescription('The IP address that, when combined with the corresponding\n            value of pimSGRPFRoutePrefixLength, identifies the route\n            used to find the RPF interface towards the source.  The\n            InetAddressType is given by the pimSGRPFNextHopType object.\n\n            This address object is only significant up to\n            pimSGRPFRoutePrefixLength bits.  The remainder of the\n            address bits are zero.')
pimSGRPFRoutePrefixLength = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 14), InetAddressPrefixLength()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFRoutePrefixLength.setDescription('The prefix length that, when combined with the\n            corresponding value of pimSGRPFRouteAddress, identifies the\n            route used to find the RPF interface towards the source.\n            The InetAddressType is given by the pimSGRPFNextHopType\n            object.')
pimSGRPFRouteMetricPref = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 15), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFRouteMetricPref.setDescription('The metric preference of the route used to find the RPF\n            interface towards the source.')
pimSGRPFRouteMetric = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 16), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPFRouteMetric.setDescription('The routing metric of the route used to find the RPF\n            interface towards the source.')
pimSGSPTBit = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 17), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGSPTBit.setDescription('Whether the SPT bit is set; and therefore whether\n            forwarding is taking place on the shortest-path tree.')
pimSGKeepaliveTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 18), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGKeepaliveTimer.setDescription('The time remaining before this (S,G) state expires, in\n            the absence of explicit (S,G) local membership or (S,G)\n            Join messages received to maintain it.  This timer is\n            called the (S,G) Keepalive Timer in the PIM-SM\n            specification.')
pimSGDRRegisterState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 19), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('noInfo', 1), ('join', 2), ('joinPending', 3), ('prune', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGDRRegisterState.setDescription("Whether the local router should encapsulate (S,G) data\n            packets in Register messages and send them to the RP.  This\n            corresponds to the state of the per-(S,G) Register state\n            machine in the PIM-SM specification.  This object is always\n            'noInfo' unless pimSGPimMode is 'asm'.")
pimSGDRRegisterStopTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 20), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGDRRegisterStopTimer.setDescription("If pimSGDRRegisterState is 'prune', this is the time\n            remaining before the local router sends a Null-Register\n            message to the RP.  If pimSGDRRegisterState is\n            'joinPending', this is the time remaining before the local\n            router resumes encapsulating data packets and sending them\n            to the RP.  Otherwise, this is zero.  This timer is called\n            the Register-Stop Timer in the PIM-SM specification.")
pimSGRPRegisterPMBRAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 21), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPRegisterPMBRAddressType.setDescription('The address type of the first PIM Multicast Border Router\n            to send a Register message with the Border bit set.  This\n            object is unknown(0) if the local router is not the RP for\n            the group.')
pimSGRPRegisterPMBRAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 22), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRPRegisterPMBRAddress.setDescription('The IP address of the first PIM Multicast Border Router to\n            send a Register message with the Border bit set.  The\n            InetAddressType is given by the\n            pimSGRPRegisterPMBRAddressType object.')
pimSGUpstreamPruneState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 23), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('forwarding', 1), ('ackpending', 2), ('pruned', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGUpstreamPruneState.setDescription('Whether the local router has pruned itself from the tree.\n            This corresponds to the state of the upstream prune (S,G)\n            state machine in the PIM-DM specification.  This object is\n            used only by PIM-DM.')
pimSGUpstreamPruneLimitTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 24), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGUpstreamPruneLimitTimer.setDescription('The time remaining before the local router may send a (S,G)\n            Prune message on pimSGRPFIfIndex.  This timer is called the\n            (S,G) Prune Limit Timer in the PIM-DM specification.  This\n            object is zero if the timer is not running.  This object is\n            used only by PIM-DM.')
pimSGOriginatorState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 25), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('notOriginator', 1), ('originator', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGOriginatorState.setDescription('Whether the router is an originator for an (S,G) message\n            flow.  This corresponds to the state of the per-(S,G)\n            Originator state machine in the PIM-DM specification.  This\n            object is used only by PIM-DM.')
pimSGSourceActiveTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 26), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGSourceActiveTimer.setDescription("If pimSGOriginatorState is 'originator', this is the time\n            remaining before the local router reverts to a notOriginator\n            state.  Otherwise, this is zero.  This timer is called the\n            Source Active Timer in the PIM-DM specification.  This\n            object is used only by PIM-DM.")
pimSGStateRefreshTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 6, 1, 27), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGStateRefreshTimer.setDescription("If pimSGOriginatorState is 'originator', this is the time\n            remaining before the local router sends a State Refresh\n            message.  Otherwise, this is zero.  This timer is called the\n            State Refresh Timer in the PIM-DM specification.  This\n            object is used only by PIM-DM.")
pimSGITable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 7))
if mibBuilder.loadTexts:
    pimSGITable.setDescription('The (conceptual) table listing the interface-specific (S,G)\n            state that PIM has.')
pimSGIEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 7, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimSGAddressType'), (0, 'PIM-STD-MIB', 'pimSGGrpAddress'), (0, 'PIM-STD-MIB', 'pimSGSrcAddress'), (0, 'PIM-STD-MIB', 'pimSGIIfIndex'))
if mibBuilder.loadTexts:
    pimSGIEntry.setDescription('An entry (conceptual row) in the pimSGITable.')
pimSGIIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    pimSGIIfIndex.setDescription('The ifIndex of the interface that this entry corresponds\n            to.')
pimSGIUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 2), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIUpTime.setDescription('The time since this entry was created by the local router.')
pimSGILocalMembership = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGILocalMembership.setDescription('Whether the local router has (S,G) local membership on this\n            interface (resulting from a mechanism such as IGMP or MLD).\n            This corresponds to local_receiver_include(S,G,I) in the\n            PIM-SM specification.')
pimSGIJoinPruneState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('noInfo', 1), ('join', 2), ('prunePending', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIJoinPruneState.setDescription('The state resulting from (S,G) Join/Prune messages\n            received on this interface.  This corresponds to the state\n            of the downstream per-interface (S,G) state machine in the\n            PIM-SM and PIM-DM specification.')
pimSGIPrunePendingTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 5), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIPrunePendingTimer.setDescription('The time remaining before the local router acts on an (S,G)\n            Prune message received on this interface, during which the\n            router is waiting to see whether another downstream router\n            will override the Prune message.  This timer is called the\n            (S,G) Prune-Pending Timer in the PIM-SM specification.  This\n            object is zero if the timer is not running.')
pimSGIJoinExpiryTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 6), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIJoinExpiryTimer.setDescription("The time remaining before (S,G) Join state for this\n            interface expires.  This timer is called the (S,G) Join\n            Expiry Timer in the PIM-SM specification.  This object is\n            zero if the timer is not running.  A value of 'FFFFFFFF'h\n            indicates an infinite expiry time.  This timer is called the\n            (S,G) Prune Timer in the PIM-DM specification.")
pimSGIAssertState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('noInfo', 1), ('iAmAssertWinner', 2), ('iAmAssertLoser', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIAssertState.setDescription('The (S,G) Assert state for this interface.  This\n            corresponds to the state of the per-interface (S,G) Assert\n            state machine in the PIM-SM specification.')
pimSGIAssertTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 8), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIAssertTimer.setDescription("If pimSGIAssertState is 'iAmAssertWinner', this is the time\n            remaining before the local router next sends a (S,G) Assert\n            message on this interface.  If pimSGIAssertState is\n            'iAmAssertLoser', this is the time remaining before the\n            (S,G) Assert state expires.  If pimSGIAssertState is\n            'noInfo', this is zero.  This timer is called the (S,G)\n            Assert Timer in the PIM-SM specification.")
pimSGIAssertWinnerAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 9), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIAssertWinnerAddressType.setDescription("If pimSGIAssertState is 'iAmAssertLoser', this is the\n            address type of the assert winner; otherwise, this object is\n            unknown(0).")
pimSGIAssertWinnerAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 10), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIAssertWinnerAddress.setDescription("If pimSGIAssertState is 'iAmAssertLoser', this is the\n            address of the assert winner.  The InetAddressType is given\n            by the pimSGIAssertWinnerAddressType object.")
pimSGIAssertWinnerMetricPref = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 11), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIAssertWinnerMetricPref.setDescription("If pimSGIAssertState is 'iAmAssertLoser', this is the\n            metric preference of the route to the source advertised by\n            the assert winner; otherwise, this object is zero.")
pimSGIAssertWinnerMetric = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 7, 1, 12), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGIAssertWinnerMetric.setDescription("If pimSGIAssertState is 'iAmAssertLoser', this is the\n            routing metric of the route to the source advertised by the\n            assert winner; otherwise, this object is zero.")
pimSGRptTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 8))
if mibBuilder.loadTexts:
    pimSGRptTable.setDescription('The (conceptual) table listing the non-interface specific\n            (S,G,rpt) state that PIM has.')
pimSGRptEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 8, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimStarGAddressType'), (0, 'PIM-STD-MIB', 'pimStarGGrpAddress'), (0, 'PIM-STD-MIB', 'pimSGRptSrcAddress'))
if mibBuilder.loadTexts:
    pimSGRptEntry.setDescription('An entry (conceptual row) in the pimSGRptTable.')
pimSGRptSrcAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 8, 1, 1), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimSGRptSrcAddress.setDescription('The source address for this entry.  The InetAddressType is\n            given by the pimStarGAddressType object.')
pimSGRptUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 8, 1, 2), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptUpTime.setDescription('The time since this entry was created by the local router.')
pimSGRptUpstreamPruneState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 8, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('rptNotJoined', 1), ('pruned', 2), ('notPruned', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptUpstreamPruneState.setDescription('Whether the local router should prune the source off the RP\n            tree.  This corresponds to the state of the upstream\n            (S,G,rpt) state machine for triggered messages in the PIM-SM\n            specification.')
pimSGRptUpstreamOverrideTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 8, 1, 4), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptUpstreamOverrideTimer.setDescription('The time remaining before the local router sends a\n            triggered (S,G,rpt) Join message on pimStarGRPFIfIndex.\n            This timer is called the (S,G,rpt) Upstream Override Timer\n            in the PIM-SM specification.  This object is zero if the\n            timer is not running.')
pimSGRptITable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 9))
if mibBuilder.loadTexts:
    pimSGRptITable.setDescription('The (conceptual) table listing the interface-specific\n            (S,G,rpt) state that PIM has.')
pimSGRptIEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 9, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimStarGAddressType'), (0, 'PIM-STD-MIB', 'pimStarGGrpAddress'), (0, 'PIM-STD-MIB', 'pimSGRptSrcAddress'), (0, 'PIM-STD-MIB', 'pimSGRptIIfIndex'))
if mibBuilder.loadTexts:
    pimSGRptIEntry.setDescription('An entry (conceptual row) in the pimSGRptITable.')
pimSGRptIIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 9, 1, 1), InterfaceIndex())
if mibBuilder.loadTexts:
    pimSGRptIIfIndex.setDescription('The ifIndex of the interface that this entry corresponds\n            to.')
pimSGRptIUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 9, 1, 2), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptIUpTime.setDescription('The time since this entry was created by the local router.')
pimSGRptILocalMembership = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 9, 1, 3), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptILocalMembership.setDescription('Whether the local router has both (*,G) include local\n            membership and (S,G) exclude local membership on this\n            interface (resulting from a mechanism such as IGMP or MLD).\n            This corresponds to local_receiver_exclude(S,G,I) in the\n            PIM-SM specification.')
pimSGRptIJoinPruneState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 9, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('noInfo', 1), ('prune', 2), ('prunePending', 3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptIJoinPruneState.setDescription('The state resulting from (S,G,rpt) Join/Prune messages\n            received on this interface.  This corresponds to the state\n            of the downstream per-interface (S,G,rpt) state machine in\n            the PIM-SM specification.')
pimSGRptIPrunePendingTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 9, 1, 5), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptIPrunePendingTimer.setDescription('The time remaining before the local router starts pruning\n            this source off the RP tree.  This timer is called the\n            (S,G,rpt) Prune-Pending Timer in the PIM-SM specification.\n            This object is zero if the timer is not running.')
pimSGRptIPruneExpiryTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 9, 1, 6), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimSGRptIPruneExpiryTimer.setDescription("The time remaining before (S,G,rpt) Prune state for this\n            interface expires.  This timer is called the (S,G,rpt)\n            Prune Expiry Timer in the PIM-SM specification.  This object\n            is zero if the timer is not running.  A value of 'FFFFFFFF'h\n            indicates an infinite expiry time.")
pimBidirDFElectionTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 10))
if mibBuilder.loadTexts:
    pimBidirDFElectionTable.setDescription('The (conceptual) table listing the per-RP Designated\n            Forwarder (DF) Election state for each interface for all the\n            RPs in BIDIR mode.')
pimBidirDFElectionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 10, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimBidirDFElectionAddressType'), (0, 'PIM-STD-MIB', 'pimBidirDFElectionRPAddress'), (0, 'PIM-STD-MIB', 'pimBidirDFElectionIfIndex'))
if mibBuilder.loadTexts:
    pimBidirDFElectionEntry.setDescription('An entry (conceptual row) in the pimBidirDFElectionTable.')
pimBidirDFElectionAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 1), InetAddressType())
if mibBuilder.loadTexts:
    pimBidirDFElectionAddressType.setDescription('The address type of the RP for which the DF state is being\n            maintained.')
pimBidirDFElectionRPAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 2), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimBidirDFElectionRPAddress.setDescription('The IP address of the RP for which the DF state is being\n            maintained.  The InetAddressType is given by the\n            pimBidirDFElectionAddressType object.')
pimBidirDFElectionIfIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 3), InterfaceIndex())
if mibBuilder.loadTexts:
    pimBidirDFElectionIfIndex.setDescription('The value of ifIndex for the interface for which the DF\n            state is being maintained.')
pimBidirDFElectionWinnerAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 4), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimBidirDFElectionWinnerAddressType.setDescription('The primary address type of the winner of the DF Election\n            process.  A value of unknown(0) indicates there is currently\n            no DF.')
pimBidirDFElectionWinnerAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 5), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimBidirDFElectionWinnerAddress.setDescription('The primary IP address of the winner of the DF Election\n            process.  The InetAddressType is given by the\n            pimBidirDFElectionWinnerAddressType object.')
pimBidirDFElectionWinnerUpTime = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 6), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimBidirDFElectionWinnerUpTime.setDescription('The time since the current winner (last) became elected as\n            the DF for this RP.')
pimBidirDFElectionWinnerMetricPref = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 7), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimBidirDFElectionWinnerMetricPref.setDescription('The metric preference advertised by the DF Winner, or zero\n            if there is currently no DF.')
pimBidirDFElectionWinnerMetric = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 8), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimBidirDFElectionWinnerMetric.setDescription('The metric advertised by the DF Winner, or zero if there is\n            currently no DF.')
pimBidirDFElectionState = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('dfOffer', 1), ('dfLose', 2), ('dfWinner', 3), ('dfBackoff', 4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimBidirDFElectionState.setDescription('The state of this interface with respect to DF-Election for\n            this RP.  The states correspond to the ones defined in the\n            BIDIR-PIM specification.')
pimBidirDFElectionStateTimer = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 10, 1, 10), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimBidirDFElectionStateTimer.setDescription('The minimum time remaining after which the local router\n            will expire the current DF state represented by\n            pimBidirDFElectionState.')
pimStaticRPTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 11))
if mibBuilder.loadTexts:
    pimStaticRPTable.setDescription('This table is used to manage static configuration of RPs.\n\n            If the group prefixes configured for two or more rows in\n            this table overlap, the row with the greatest value of\n            pimStaticRPGrpPrefixLength is used for the overlapping\n            range.')
pimStaticRPEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 11, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimStaticRPAddressType'), (0, 'PIM-STD-MIB', 'pimStaticRPGrpAddress'), (0, 'PIM-STD-MIB', 'pimStaticRPGrpPrefixLength'))
if mibBuilder.loadTexts:
    pimStaticRPEntry.setDescription('An entry (conceptual row) in the pimStaticRPTable.  This\n            entry is preserved on agent restart.')
pimStaticRPAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 1), InetAddressType())
if mibBuilder.loadTexts:
    pimStaticRPAddressType.setDescription('The address type of this entry.')
pimStaticRPGrpAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 2), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimStaticRPGrpAddress.setDescription('The multicast group address that, when combined with\n            pimStaticRPGrpPrefixLength, gives the group prefix for this\n            entry.  The InetAddressType is given by the\n            pimStaticRPAddressType object.\n\n            This address object is only significant up to\n            pimStaticRPGrpPrefixLength bits.  The remainder of the\n            address bits are zero.  This is especially important for\n            this index field, which is part of the index of this entry.\n            Any non-zero bits would signify an entirely different\n            entry.')
pimStaticRPGrpPrefixLength = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 3), InetAddressPrefixLength().subtype(subtypeSpec=ValueRangeConstraint(4, 128)))
if mibBuilder.loadTexts:
    pimStaticRPGrpPrefixLength.setDescription("The multicast group prefix length that, when combined\n            with pimStaticRPGrpAddress, gives the group prefix for this\n            entry.  The InetAddressType is given by the\n            pimStaticRPAddressType object.  If pimStaticRPAddressType is\n            'ipv4' or 'ipv4z', this object must be in the range 4..32.\n            If pimStaticRPGrpAddressType is 'ipv6' or 'ipv6z', this\n            object must be in the range 8..128.")
pimStaticRPRPAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 4), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimStaticRPRPAddress.setDescription('The IP address of the RP to be used for groups within this\n            group prefix.  The InetAddressType is given by the\n            pimStaticRPAddressType object.')
pimStaticRPPimMode = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 5), PimMode().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(2, 3, 4))).clone(namedValues=NamedValues(('ssm', 2), ('asm', 3), ('bidir', 4))).clone('asm')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimStaticRPPimMode.setDescription('The PIM mode to be used for groups in this group prefix.\n\n            If this object is set to ssm(2), then pimStaticRPRPAddress\n            must be set to zero.  No RP operations are ever possible for\n            PIM Mode SSM.')
pimStaticRPOverrideDynamic = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 6), TruthValue().clone('false')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimStaticRPOverrideDynamic.setDescription('Whether this static RP configuration will override other\n            group mappings in this group prefix.  If this object is\n            TRUE, then it will override:\n\n            -  RP information learned dynamically for groups in this\n            group prefix.\n\n            -  RP information configured in pimStaticRPTable with\n            pimStaticRPOverrideDynamic set to FALSE.\n\n            See pimGroupMappingTable for details.')
pimStaticRPPrecedence = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 7), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimStaticRPPrecedence.setDescription('The value for pimGroupMappingPrecedence to be used for this\n            static RP configuration.  This allows fine control over\n            which configuration is overridden by this static\n            configuration.\n\n            If pimStaticRPOverrideDynamic is set to TRUE, all dynamic RP\n            configuration is overridden by this static configuration,\n            whatever the value of this object.\n\n            The absolute values of this object have a significance only\n            on the local router and do not need to be coordinated with\n            other routers.  A setting of this object may have different\n            effects when applied to other routers.\n\n            Do not use this object unless fine control of static RP\n            behavior on the local router is required.')
pimStaticRPRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 8), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimStaticRPRowStatus.setDescription('The status of this row, by which rows in this table can\n            be created and destroyed.\n\n            This status object cannot be set to active(1) before a valid\n            value has been written to pimStaticRPRPAddress.\n\n            All writable objects in this entry can be modified when the\n            status of this entry is active(1).')
pimStaticRPStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 11, 1, 9), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimStaticRPStorageType.setDescription("The storage type for this row.  Rows having the value\n            'permanent' need not allow write-access to any columnar\n            objects in the row.")
pimAnycastRPSetTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 12))
if mibBuilder.loadTexts:
    pimAnycastRPSetTable.setDescription('This table is used to manage Anycast-RP via PIM Register\n            messages, as opposed to via other protocols such as MSDP\n            (Multicast Source Discovery Protocol).\n\n            Entries must be configured in this table if and only if the\n            local router is a member of one or more Anycast-RP sets,\n            that is, one or more Anycast-RP addresses are assigned to\n            the local router.  Note that if using static RP\n            configuration, this is in addition to, not instead of, the\n            pimStaticRPTable entries that must be configured for the\n            Anycast-RPs.\n\n            The set of rows with the same values of both\n            pimAnycastRPSetAddressType and pimAnycastRPSetAnycastAddress\n            corresponds to the Anycast-RP set for that Anycast-RP\n            address.\n\n            When an Anycast-RP set configuration is active, one entry\n            per pimAnycastRPSetAnycastAddress corresponds to the local\n            router.  The local router is identified by the\n            pimAnycastRpSetLocalRouter object.  That entry determines\n            the source address used by the local router when forwarding\n            PIM Register messages within the Anycast-RP set.')
pimAnycastRPSetEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 12, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimAnycastRPSetAddressType'), (0, 'PIM-STD-MIB', 'pimAnycastRPSetAnycastAddress'), (0, 'PIM-STD-MIB', 'pimAnycastRPSetRouterAddress'))
if mibBuilder.loadTexts:
    pimAnycastRPSetEntry.setDescription('An entry corresponds to a single router within a particular\n            Anycast-RP set.  This entry is preserved on agent restart.')
pimAnycastRPSetAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 12, 1, 1), InetAddressType())
if mibBuilder.loadTexts:
    pimAnycastRPSetAddressType.setDescription('The address type of the Anycast-RP address and router\n            address.')
pimAnycastRPSetAnycastAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 12, 1, 2), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimAnycastRPSetAnycastAddress.setDescription('The Anycast-RP address.  The InetAddressType is given by\n            the pimAnycastRPSetAddressType object.')
pimAnycastRPSetRouterAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 12, 1, 3), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimAnycastRPSetRouterAddress.setDescription('The address of a router that is a member of the Anycast-RP\n            set.  The InetAddressType is given by the\n            pimAnycastRPSetAddressType object.\n\n            This address differs from pimAnycastRPSetAnycastAddress.\n            Equal values for these two addresses in a single entry are\n            not permitted.  That would cause a Register loop.')
pimAnycastRPSetLocalRouter = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 12, 1, 4), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimAnycastRPSetLocalRouter.setDescription('Whether this entry corresponds to the local router.')
pimAnycastRPSetRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 12, 1, 5), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimAnycastRPSetRowStatus.setDescription('The status of this row, by which rows in this table can\n            be created and destroyed.\n\n            This status object can be set to active(1) without setting\n            any other columnar objects in this entry.\n\n            All writable objects in this entry can be modified when the\n            status of this entry is active(1).')
pimAnycastRPSetStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 12, 1, 6), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    pimAnycastRPSetStorageType.setDescription("The storage type for this row.  Rows having the value\n            'permanent' need not allow write-access to any columnar\n            objects in the row.")
pimGroupMappingTable = MibTable((1, 3, 6, 1, 2, 1, 157, 1, 13))
if mibBuilder.loadTexts:
    pimGroupMappingTable.setDescription("The (conceptual) table listing mappings from multicast\n            group prefixes to the PIM mode and RP address to use for\n            groups within that group prefix.\n\n            Rows in this table are created for a variety of reasons,\n            indicated by the value of the pimGroupMappingOrigin object.\n\n            -  Rows with a pimGroupMappingOrigin value of 'fixed' are\n               created automatically by the router at startup, to\n               correspond to the well-defined prefixes of link-local and\n               unroutable group addresses.  These rows are never\n               destroyed.\n\n            -  Rows with a pimGroupMappingOrigin value of 'embedded' are\n               created by the router to correspond to group prefixes\n               that are to be treated as being in Embedded-RP format.\n\n            -  Rows with a pimGroupMappingOrigin value of 'configRp' are\n               created and destroyed as a result of rows in the\n               pimStaticRPTable being created and destroyed.\n\n            -  Rows with a pimGroupMappingOrigin value of 'configSsm'\n               are created and destroyed as a result of configuration of\n               SSM address ranges to the local router.\n\n            -  Rows with a pimGroupMappingOrigin value of 'bsr' are\n               created as a result of running the PIM Bootstrap Router\n               (BSR) mechanism.  If the local router is not the elected\n               BSR, these rows are created to correspond to group\n               prefixes in the PIM Bootstrap messages received from the\n               elected BSR.  If the local router is the elected BSR,\n               these rows are created to correspond to group prefixes in\n               the PIM Bootstrap messages that the local router sends.\n               In either case, these rows are destroyed when the group\n               prefixes are timed out by the BSR mechanism.\n\n            -  Rows with a pimGroupMappingOrigin value of 'other' are\n               created and destroyed according to some other mechanism\n               not specified here.\n\n            Given the collection of rows in this table at any point in\n            time, the PIM mode and RP address to use for a particular\n            group is determined using the following algorithm.\n\n            1. From the set of all rows, the subset whose group prefix\n               contains the group in question are selected.\n\n            2. If there are no such rows, then the group mapping is\n               undefined.\n\n            3. If there are multiple selected rows, and a subset is\n               defined by pimStaticRPTable (pimGroupMappingOrigin value\n               of 'configRp') with pimStaticRPOverrideDynamic set to\n               TRUE, then this subset is selected.\n\n            4. From the selected subset of rows, the subset that have\n               the greatest value of pimGroupMappingGrpPrefixLength are\n               selected.\n\n            5. If there are still multiple selected rows, the subset\n               that has the highest precedence (the lowest numerical\n               value for pimGroupMappingPrecedence) is selected.\n\n            6. If there are still multiple selected rows, the row\n               selected is implementation dependent; the implementation\n               might or might not apply the PIM hash function to select\n               the row.\n\n            7. The group mode to use is given by the value of\n               pimGroupMappingPimMode from the single selected row; the\n               RP to use is given by the value of\n               pimGroupMappingRPAddress, unless pimGroupMappingOrigin is\n               'embedded', in which case, the RP is extracted from the\n               group address in question.")
pimGroupMappingEntry = MibTableRow((1, 3, 6, 1, 2, 1, 157, 1, 13, 1)).setIndexNames((0, 'PIM-STD-MIB', 'pimGroupMappingOrigin'), (0, 'PIM-STD-MIB', 'pimGroupMappingAddressType'), (0, 'PIM-STD-MIB', 'pimGroupMappingGrpAddress'), (0, 'PIM-STD-MIB', 'pimGroupMappingGrpPrefixLength'), (0, 'PIM-STD-MIB', 'pimGroupMappingRPAddressType'), (0, 'PIM-STD-MIB', 'pimGroupMappingRPAddress'))
if mibBuilder.loadTexts:
    pimGroupMappingEntry.setDescription('An entry (conceptual row) in the pimGroupMappingTable.')
pimGroupMappingOrigin = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 1), PimGroupMappingOriginType())
if mibBuilder.loadTexts:
    pimGroupMappingOrigin.setDescription('The mechanism by which this group mapping was learned.')
pimGroupMappingAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 2), InetAddressType())
if mibBuilder.loadTexts:
    pimGroupMappingAddressType.setDescription('The address type of the IP multicast group prefix.')
pimGroupMappingGrpAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 3), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimGroupMappingGrpAddress.setDescription('The IP multicast group address that, when combined with\n            pimGroupMappingGrpPrefixLength, gives the group prefix for\n            this mapping.  The InetAddressType is given by the\n            pimGroupMappingAddressType object.\n\n            This address object is only significant up to\n            pimGroupMappingGrpPrefixLength bits.  The remainder of the\n            address bits are zero.  This is especially important for\n            this index field, which is part of the index of this entry.\n            Any non-zero bits would signify an entirely different\n            entry.')
pimGroupMappingGrpPrefixLength = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 4), InetAddressPrefixLength().subtype(subtypeSpec=ValueRangeConstraint(4, 128)))
if mibBuilder.loadTexts:
    pimGroupMappingGrpPrefixLength.setDescription("The multicast group prefix length that, when combined\n            with pimGroupMappingGrpAddress, gives the group prefix for\n            this mapping.  The InetAddressType is given by the\n            pimGroupMappingAddressType object.  If\n            pimGroupMappingAddressType is 'ipv4' or 'ipv4z', this\n            object must be in the range 4..32.  If\n            pimGroupMappingAddressType is 'ipv6' or 'ipv6z', this object\n            must be in the range 8..128.")
pimGroupMappingRPAddressType = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 5), InetAddressType())
if mibBuilder.loadTexts:
    pimGroupMappingRPAddressType.setDescription('The address type of the RP to be used for groups within\n            this group prefix, or unknown(0) if no RP is to be used or\n            if the RP address is unknown.  This object must be\n            unknown(0) if pimGroupMappingPimMode is ssm(2), or if\n            pimGroupMappingOrigin is embedded(6).')
pimGroupMappingRPAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 6), InetAddress().subtype(subtypeSpec=ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(4, 4), ValueSizeConstraint(8, 8), ValueSizeConstraint(16, 16), ValueSizeConstraint(20, 20))))
if mibBuilder.loadTexts:
    pimGroupMappingRPAddress.setDescription('The IP address of the RP to be used for groups within this\n            group prefix.  The InetAddressType is given by the\n            pimGroupMappingRPAddressType object.')
pimGroupMappingPimMode = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 7), PimMode()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimGroupMappingPimMode.setDescription('The PIM mode to be used for groups in this group prefix.')
pimGroupMappingPrecedence = MibTableColumn((1, 3, 6, 1, 2, 1, 157, 1, 13, 1, 8), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    pimGroupMappingPrecedence.setDescription('The precedence of this row, used in the algorithm that\n            determines which row applies to a given group address\n            (described above).  Numerically higher values for this\n            object indicate lower precedences, with the value zero\n            denoting the highest precedence.\n\n            The absolute values of this object have a significance only\n            on the local router and do not need to be coordinated with\n            other routers.')
pimNeighborLoss = NotificationType((1, 3, 6, 1, 2, 1, 157, 0, 1)).setObjects(*(('PIM-STD-MIB', 'pimNeighborUpTime'),))
if mibBuilder.loadTexts:
    pimNeighborLoss.setDescription('A pimNeighborLoss notification signifies the loss of an\n            adjacency with a neighbor.  This notification should be\n            generated when the neighbor timer expires, and the router\n            has no other neighbors on the same interface with the same\n            IP version and a lower IP address than itself.\n\n            This notification is generated whenever the counter\n            pimNeighborLossCount is incremented, subject\n            to the rate limit specified by\n            pimNeighborLossNotificationPeriod.')
pimInvalidRegister = NotificationType((1, 3, 6, 1, 2, 1, 157, 0, 2)).setObjects(*(('PIM-STD-MIB', 'pimGroupMappingPimMode'), ('PIM-STD-MIB', 'pimInvalidRegisterAddressType'), ('PIM-STD-MIB', 'pimInvalidRegisterOrigin'), ('PIM-STD-MIB', 'pimInvalidRegisterGroup'), ('PIM-STD-MIB', 'pimInvalidRegisterRp')))
if mibBuilder.loadTexts:
    pimInvalidRegister.setDescription('A pimInvalidRegister notification signifies that an invalid\n            PIM Register message was received by this device.\n\n            This notification is generated whenever the counter\n            pimInvalidRegisterMsgsRcvd is incremented, subject to the\n            rate limit specified by\n            pimInvalidRegisterNotificationPeriod.')
pimInvalidJoinPrune = NotificationType((1, 3, 6, 1, 2, 1, 157, 0, 3)).setObjects(*(('PIM-STD-MIB', 'pimGroupMappingPimMode'), ('PIM-STD-MIB', 'pimInvalidJoinPruneAddressType'), ('PIM-STD-MIB', 'pimInvalidJoinPruneOrigin'), ('PIM-STD-MIB', 'pimInvalidJoinPruneGroup'), ('PIM-STD-MIB', 'pimInvalidJoinPruneRp'), ('PIM-STD-MIB', 'pimNeighborUpTime')))
if mibBuilder.loadTexts:
    pimInvalidJoinPrune.setDescription('A pimInvalidJoinPrune notification signifies that an\n            invalid PIM Join/Prune message was received by this device.\n\n            This notification is generated whenever the counter\n            pimInvalidJoinPruneMsgsRcvd is incremented, subject to the\n            rate limit specified by\n            pimInvalidJoinPruneNotificationPeriod.')
pimRPMappingChange = NotificationType((1, 3, 6, 1, 2, 1, 157, 0, 4)).setObjects(*(('PIM-STD-MIB', 'pimGroupMappingPimMode'), ('PIM-STD-MIB', 'pimGroupMappingPrecedence')))
if mibBuilder.loadTexts:
    pimRPMappingChange.setDescription('A pimRPMappingChange notification signifies a change to the\n            active RP mapping on this device.\n\n            This notification is generated whenever the counter\n            pimRPMappingChangeCount is incremented, subject to the\n            rate limit specified by\n            pimRPMappingChangeNotificationPeriod.')
pimInterfaceElection = NotificationType((1, 3, 6, 1, 2, 1, 157, 0, 5)).setObjects(*(('PIM-STD-MIB', 'pimInterfaceAddressType'), ('PIM-STD-MIB', 'pimInterfaceAddress')))
if mibBuilder.loadTexts:
    pimInterfaceElection.setDescription('A pimInterfaceElection notification signifies that a new DR\n            or DF has been elected on a network.\n\n            This notification is generated whenever the counter\n            pimInterfaceElectionWinCount is incremented, subject to the\n            rate limit specified by\n            pimInterfaceElectionNotificationPeriod.')
pimMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 157, 2))
pimMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 157, 2, 1))
pimMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 157, 2, 2))
pimMIBComplianceAsm = ModuleCompliance((1, 3, 6, 1, 2, 1, 157, 2, 1, 1)).setObjects(*(('PIM-STD-MIB', 'pimTopologyGroup'), ('PIM-STD-MIB', 'pimSsmGroup'), ('PIM-STD-MIB', 'pimRPConfigGroup'), ('PIM-STD-MIB', 'pimSmGroup'), ('PIM-STD-MIB', 'pimNotificationGroup'), ('PIM-STD-MIB', 'pimTuningParametersGroup'), ('PIM-STD-MIB', 'pimRouterStatisticsGroup'), ('PIM-STD-MIB', 'pimAnycastRpGroup'), ('PIM-STD-MIB', 'pimStaticRPPrecedenceGroup'), ('PIM-STD-MIB', 'pimNetMgmtNotificationObjects'), ('PIM-STD-MIB', 'pimNetMgmtNotificationGroup'), ('PIM-STD-MIB', 'pimDiagnosticsGroup'), ('PIM-STD-MIB', 'pimDeviceStorageGroup')))
if mibBuilder.loadTexts:
    pimMIBComplianceAsm.setDescription('The compliance statement for routers which are running\n             PIM-SM (Sparse Mode).')
pimMIBComplianceBidir = ModuleCompliance((1, 3, 6, 1, 2, 1, 157, 2, 1, 2)).setObjects(*(('PIM-STD-MIB', 'pimTopologyGroup'), ('PIM-STD-MIB', 'pimRPConfigGroup'), ('PIM-STD-MIB', 'pimSmGroup'), ('PIM-STD-MIB', 'pimBidirGroup'), ('PIM-STD-MIB', 'pimNotificationGroup'), ('PIM-STD-MIB', 'pimTuningParametersGroup'), ('PIM-STD-MIB', 'pimRouterStatisticsGroup'), ('PIM-STD-MIB', 'pimAnycastRpGroup'), ('PIM-STD-MIB', 'pimStaticRPPrecedenceGroup'), ('PIM-STD-MIB', 'pimNetMgmtNotificationObjects'), ('PIM-STD-MIB', 'pimNetMgmtNotificationGroup'), ('PIM-STD-MIB', 'pimDiagnosticsGroup'), ('PIM-STD-MIB', 'pimDeviceStorageGroup')))
if mibBuilder.loadTexts:
    pimMIBComplianceBidir.setDescription('The compliance statement for routers which are running\n            Bidir-PIM.')
pimMIBComplianceSsm = ModuleCompliance((1, 3, 6, 1, 2, 1, 157, 2, 1, 3)).setObjects(*(('PIM-STD-MIB', 'pimTopologyGroup'), ('PIM-STD-MIB', 'pimSsmGroup'), ('PIM-STD-MIB', 'pimNotificationGroup'), ('PIM-STD-MIB', 'pimTuningParametersGroup'), ('PIM-STD-MIB', 'pimRouterStatisticsGroup'), ('PIM-STD-MIB', 'pimNetMgmtNotificationObjects'), ('PIM-STD-MIB', 'pimNetMgmtNotificationGroup'), ('PIM-STD-MIB', 'pimDiagnosticsGroup'), ('PIM-STD-MIB', 'pimDeviceStorageGroup')))
if mibBuilder.loadTexts:
    pimMIBComplianceSsm.setDescription('The compliance statement for routers which are running\n             PIM SSM (Source Specific Multicast).')
pimMIBComplianceDm = ModuleCompliance((1, 3, 6, 1, 2, 1, 157, 2, 1, 4)).setObjects(*(('PIM-STD-MIB', 'pimTopologyGroup'), ('PIM-STD-MIB', 'pimSsmGroup'), ('PIM-STD-MIB', 'pimRPConfigGroup'), ('PIM-STD-MIB', 'pimSmGroup'), ('PIM-STD-MIB', 'pimDmGroup'), ('PIM-STD-MIB', 'pimNotificationGroup'), ('PIM-STD-MIB', 'pimTuningParametersGroup'), ('PIM-STD-MIB', 'pimRouterStatisticsGroup'), ('PIM-STD-MIB', 'pimAnycastRpGroup'), ('PIM-STD-MIB', 'pimStaticRPPrecedenceGroup'), ('PIM-STD-MIB', 'pimNetMgmtNotificationObjects'), ('PIM-STD-MIB', 'pimNetMgmtNotificationGroup'), ('PIM-STD-MIB', 'pimDiagnosticsGroup'), ('PIM-STD-MIB', 'pimDeviceStorageGroup')))
if mibBuilder.loadTexts:
    pimMIBComplianceDm.setDescription('The compliance statement for routers which are running\n            PIM-DM (Dense Mode).')
pimTopologyGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 1)).setObjects(*(('PIM-STD-MIB', 'pimInterfaceAddressType'), ('PIM-STD-MIB', 'pimInterfaceAddress'), ('PIM-STD-MIB', 'pimInterfaceGenerationIDValue'), ('PIM-STD-MIB', 'pimInterfaceDR'), ('PIM-STD-MIB', 'pimInterfaceDRPriorityEnabled'), ('PIM-STD-MIB', 'pimInterfaceHelloHoldtime'), ('PIM-STD-MIB', 'pimInterfaceJoinPruneHoldtime'), ('PIM-STD-MIB', 'pimInterfaceLanDelayEnabled'), ('PIM-STD-MIB', 'pimInterfaceEffectPropagDelay'), ('PIM-STD-MIB', 'pimInterfaceEffectOverrideIvl'), ('PIM-STD-MIB', 'pimInterfaceSuppressionEnabled'), ('PIM-STD-MIB', 'pimInterfaceBidirCapable'), ('PIM-STD-MIB', 'pimNeighborGenerationIDPresent'), ('PIM-STD-MIB', 'pimNeighborGenerationIDValue'), ('PIM-STD-MIB', 'pimNeighborUpTime'), ('PIM-STD-MIB', 'pimNeighborExpiryTime'), ('PIM-STD-MIB', 'pimNeighborDRPriorityPresent'), ('PIM-STD-MIB', 'pimNeighborDRPriority'), ('PIM-STD-MIB', 'pimNeighborLanPruneDelayPresent'), ('PIM-STD-MIB', 'pimNeighborTBit'), ('PIM-STD-MIB', 'pimNeighborPropagationDelay'), ('PIM-STD-MIB', 'pimNeighborOverrideInterval'), ('PIM-STD-MIB', 'pimNeighborBidirCapable'), ('PIM-STD-MIB', 'pimNbrSecAddress')))
if mibBuilder.loadTexts:
    pimTopologyGroup.setDescription('A collection of read-only objects used to report local PIM\n            topology.')
pimNotificationGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 2)).setObjects(*(('PIM-STD-MIB', 'pimNeighborLoss'),))
if mibBuilder.loadTexts:
    pimNotificationGroup.setDescription('A collection of notifications for signaling important PIM\n            events.')
pimTuningParametersGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 3)).setObjects(*(('PIM-STD-MIB', 'pimKeepalivePeriod'), ('PIM-STD-MIB', 'pimRegisterSuppressionTime'), ('PIM-STD-MIB', 'pimInterfaceDRPriority'), ('PIM-STD-MIB', 'pimInterfaceHelloInterval'), ('PIM-STD-MIB', 'pimInterfaceTrigHelloInterval'), ('PIM-STD-MIB', 'pimInterfaceJoinPruneInterval'), ('PIM-STD-MIB', 'pimInterfacePropagationDelay'), ('PIM-STD-MIB', 'pimInterfaceOverrideInterval'), ('PIM-STD-MIB', 'pimInterfaceDomainBorder'), ('PIM-STD-MIB', 'pimInterfaceStubInterface'), ('PIM-STD-MIB', 'pimInterfaceStatus'), ('PIM-STD-MIB', 'pimInterfaceStorageType')))
if mibBuilder.loadTexts:
    pimTuningParametersGroup.setDescription('A collection of writable objects used to configure PIM\n            behavior and to tune performance.')
pimRouterStatisticsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 4)).setObjects(*(('PIM-STD-MIB', 'pimStarGEntries'), ('PIM-STD-MIB', 'pimStarGIEntries'), ('PIM-STD-MIB', 'pimSGEntries'), ('PIM-STD-MIB', 'pimSGIEntries'), ('PIM-STD-MIB', 'pimSGRptEntries'), ('PIM-STD-MIB', 'pimSGRptIEntries')))
if mibBuilder.loadTexts:
    pimRouterStatisticsGroup.setDescription('A collection of statistics global to the PIM router.')
pimSsmGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 5)).setObjects(*(('PIM-STD-MIB', 'pimSGUpTime'), ('PIM-STD-MIB', 'pimSGPimMode'), ('PIM-STD-MIB', 'pimSGUpstreamJoinState'), ('PIM-STD-MIB', 'pimSGUpstreamJoinTimer'), ('PIM-STD-MIB', 'pimSGUpstreamNeighbor'), ('PIM-STD-MIB', 'pimSGRPFIfIndex'), ('PIM-STD-MIB', 'pimSGRPFNextHopType'), ('PIM-STD-MIB', 'pimSGRPFNextHop'), ('PIM-STD-MIB', 'pimSGRPFRouteProtocol'), ('PIM-STD-MIB', 'pimSGRPFRouteAddress'), ('PIM-STD-MIB', 'pimSGRPFRoutePrefixLength'), ('PIM-STD-MIB', 'pimSGRPFRouteMetricPref'), ('PIM-STD-MIB', 'pimSGRPFRouteMetric'), ('PIM-STD-MIB', 'pimSGSPTBit'), ('PIM-STD-MIB', 'pimSGKeepaliveTimer'), ('PIM-STD-MIB', 'pimSGDRRegisterState'), ('PIM-STD-MIB', 'pimSGDRRegisterStopTimer'), ('PIM-STD-MIB', 'pimSGRPRegisterPMBRAddressType'), ('PIM-STD-MIB', 'pimSGRPRegisterPMBRAddress'), ('PIM-STD-MIB', 'pimSGIUpTime'), ('PIM-STD-MIB', 'pimSGILocalMembership'), ('PIM-STD-MIB', 'pimSGIJoinPruneState'), ('PIM-STD-MIB', 'pimSGIPrunePendingTimer'), ('PIM-STD-MIB', 'pimSGIJoinExpiryTimer'), ('PIM-STD-MIB', 'pimSGIAssertState'), ('PIM-STD-MIB', 'pimSGIAssertTimer'), ('PIM-STD-MIB', 'pimSGIAssertWinnerAddressType'), ('PIM-STD-MIB', 'pimSGIAssertWinnerAddress'), ('PIM-STD-MIB', 'pimSGIAssertWinnerMetricPref'), ('PIM-STD-MIB', 'pimSGIAssertWinnerMetric')))
if mibBuilder.loadTexts:
    pimSsmGroup.setDescription('A collection of objects to support management of PIM\n            routers running the PIM SSM (Source Specific Multicast)\n            protocol, in PIM mode SM (Sparse Mode).')
pimRPConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 6)).setObjects(*(('PIM-STD-MIB', 'pimStaticRPRPAddress'), ('PIM-STD-MIB', 'pimStaticRPPimMode'), ('PIM-STD-MIB', 'pimStaticRPOverrideDynamic'), ('PIM-STD-MIB', 'pimStaticRPRowStatus'), ('PIM-STD-MIB', 'pimStaticRPStorageType'), ('PIM-STD-MIB', 'pimGroupMappingPimMode'), ('PIM-STD-MIB', 'pimGroupMappingPrecedence')))
if mibBuilder.loadTexts:
    pimRPConfigGroup.setDescription('A collection of objects to support configuration of RPs\n            (Rendezvous Points) and Group Mappings.')
pimSmGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 7)).setObjects(*(('PIM-STD-MIB', 'pimStarGUpTime'), ('PIM-STD-MIB', 'pimStarGPimMode'), ('PIM-STD-MIB', 'pimStarGRPAddressType'), ('PIM-STD-MIB', 'pimStarGRPAddress'), ('PIM-STD-MIB', 'pimStarGPimModeOrigin'), ('PIM-STD-MIB', 'pimStarGRPIsLocal'), ('PIM-STD-MIB', 'pimStarGUpstreamJoinState'), ('PIM-STD-MIB', 'pimStarGUpstreamJoinTimer'), ('PIM-STD-MIB', 'pimStarGUpstreamNeighborType'), ('PIM-STD-MIB', 'pimStarGUpstreamNeighbor'), ('PIM-STD-MIB', 'pimStarGRPFIfIndex'), ('PIM-STD-MIB', 'pimStarGRPFNextHopType'), ('PIM-STD-MIB', 'pimStarGRPFNextHop'), ('PIM-STD-MIB', 'pimStarGRPFRouteProtocol'), ('PIM-STD-MIB', 'pimStarGRPFRouteAddress'), ('PIM-STD-MIB', 'pimStarGRPFRoutePrefixLength'), ('PIM-STD-MIB', 'pimStarGRPFRouteMetricPref'), ('PIM-STD-MIB', 'pimStarGRPFRouteMetric'), ('PIM-STD-MIB', 'pimStarGIUpTime'), ('PIM-STD-MIB', 'pimStarGILocalMembership'), ('PIM-STD-MIB', 'pimStarGIJoinPruneState'), ('PIM-STD-MIB', 'pimStarGIPrunePendingTimer'), ('PIM-STD-MIB', 'pimStarGIJoinExpiryTimer'), ('PIM-STD-MIB', 'pimStarGIAssertState'), ('PIM-STD-MIB', 'pimStarGIAssertTimer'), ('PIM-STD-MIB', 'pimStarGIAssertWinnerAddressType'), ('PIM-STD-MIB', 'pimStarGIAssertWinnerAddress'), ('PIM-STD-MIB', 'pimStarGIAssertWinnerMetricPref'), ('PIM-STD-MIB', 'pimStarGIAssertWinnerMetric'), ('PIM-STD-MIB', 'pimSGRptUpTime'), ('PIM-STD-MIB', 'pimSGRptUpstreamPruneState'), ('PIM-STD-MIB', 'pimSGRptUpstreamOverrideTimer'), ('PIM-STD-MIB', 'pimSGRptIUpTime'), ('PIM-STD-MIB', 'pimSGRptILocalMembership'), ('PIM-STD-MIB', 'pimSGRptIJoinPruneState'), ('PIM-STD-MIB', 'pimSGRptIPrunePendingTimer'), ('PIM-STD-MIB', 'pimSGRptIPruneExpiryTimer')))
if mibBuilder.loadTexts:
    pimSmGroup.setDescription('A collection of objects to support management of PIM\n            routers running PIM-SM (Sparse Mode).  The groups\n            pimSsmGroup and pimRPConfigGroup are also required.')
pimBidirGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 8)).setObjects(*(('PIM-STD-MIB', 'pimInterfaceDFElectionRobustness'), ('PIM-STD-MIB', 'pimBidirDFElectionWinnerAddressType'), ('PIM-STD-MIB', 'pimBidirDFElectionWinnerAddress'), ('PIM-STD-MIB', 'pimBidirDFElectionWinnerUpTime'), ('PIM-STD-MIB', 'pimBidirDFElectionWinnerMetricPref'), ('PIM-STD-MIB', 'pimBidirDFElectionWinnerMetric'), ('PIM-STD-MIB', 'pimBidirDFElectionState'), ('PIM-STD-MIB', 'pimBidirDFElectionStateTimer')))
if mibBuilder.loadTexts:
    pimBidirGroup.setDescription('A collection of objects to support management of PIM\n            routers running BIDIR mode.  The groups pimSsmGroup,\n            pimSmGroup and pimRPConfigGroup are also required.')
pimAnycastRpGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 9)).setObjects(*(('PIM-STD-MIB', 'pimAnycastRPSetLocalRouter'), ('PIM-STD-MIB', 'pimAnycastRPSetRowStatus'), ('PIM-STD-MIB', 'pimAnycastRPSetStorageType')))
if mibBuilder.loadTexts:
    pimAnycastRpGroup.setDescription('A collection of objects to support management of the PIM\n            Anycast-RP mechanism.')
pimStaticRPPrecedenceGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 10)).setObjects(*(('PIM-STD-MIB', 'pimStaticRPPrecedence'),))
if mibBuilder.loadTexts:
    pimStaticRPPrecedenceGroup.setDescription('A collection of objects to allow fine control of\n            interactions between static RP configuration and\n            dynamically acquired group to RP mappings.')
pimNetMgmtNotificationObjects = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 11)).setObjects(*(('PIM-STD-MIB', 'pimInvalidRegisterNotificationPeriod'), ('PIM-STD-MIB', 'pimInvalidRegisterMsgsRcvd'), ('PIM-STD-MIB', 'pimInvalidRegisterAddressType'), ('PIM-STD-MIB', 'pimInvalidRegisterOrigin'), ('PIM-STD-MIB', 'pimInvalidRegisterGroup'), ('PIM-STD-MIB', 'pimInvalidRegisterRp'), ('PIM-STD-MIB', 'pimInvalidJoinPruneNotificationPeriod'), ('PIM-STD-MIB', 'pimInvalidJoinPruneMsgsRcvd'), ('PIM-STD-MIB', 'pimInvalidJoinPruneAddressType'), ('PIM-STD-MIB', 'pimInvalidJoinPruneOrigin'), ('PIM-STD-MIB', 'pimInvalidJoinPruneGroup'), ('PIM-STD-MIB', 'pimInvalidJoinPruneRp'), ('PIM-STD-MIB', 'pimRPMappingNotificationPeriod'), ('PIM-STD-MIB', 'pimRPMappingChangeCount'), ('PIM-STD-MIB', 'pimInterfaceElectionNotificationPeriod'), ('PIM-STD-MIB', 'pimInterfaceElectionWinCount')))
if mibBuilder.loadTexts:
    pimNetMgmtNotificationObjects.setDescription('A collection of objects to support notification of PIM\n            network management events.')
pimNetMgmtNotificationGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 12)).setObjects(*(('PIM-STD-MIB', 'pimInvalidRegister'), ('PIM-STD-MIB', 'pimInvalidJoinPrune'), ('PIM-STD-MIB', 'pimRPMappingChange'), ('PIM-STD-MIB', 'pimInterfaceElection')))
if mibBuilder.loadTexts:
    pimNetMgmtNotificationGroup.setDescription('A collection of notifications for signaling PIM network\n            management events.')
pimDiagnosticsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 13)).setObjects(*(('PIM-STD-MIB', 'pimInAsserts'), ('PIM-STD-MIB', 'pimOutAsserts'), ('PIM-STD-MIB', 'pimLastAssertInterface'), ('PIM-STD-MIB', 'pimLastAssertGroupAddressType'), ('PIM-STD-MIB', 'pimLastAssertGroupAddress'), ('PIM-STD-MIB', 'pimLastAssertSourceAddressType'), ('PIM-STD-MIB', 'pimLastAssertSourceAddress'), ('PIM-STD-MIB', 'pimNeighborLossNotificationPeriod'), ('PIM-STD-MIB', 'pimNeighborLossCount')))
if mibBuilder.loadTexts:
    pimDiagnosticsGroup.setDescription('Objects providing additional diagnostics related to a PIM\n            router.')
pimDmGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 14)).setObjects(*(('PIM-STD-MIB', 'pimRefreshInterval'), ('PIM-STD-MIB', 'pimInterfacePruneLimitInterval'), ('PIM-STD-MIB', 'pimInterfaceGraftRetryInterval'), ('PIM-STD-MIB', 'pimInterfaceSRPriorityEnabled'), ('PIM-STD-MIB', 'pimNeighborSRCapable'), ('PIM-STD-MIB', 'pimSGUpstreamPruneState'), ('PIM-STD-MIB', 'pimSGUpstreamPruneLimitTimer'), ('PIM-STD-MIB', 'pimSGOriginatorState'), ('PIM-STD-MIB', 'pimSGSourceActiveTimer'), ('PIM-STD-MIB', 'pimSGStateRefreshTimer')))
if mibBuilder.loadTexts:
    pimDmGroup.setDescription('A collection of objects required for management of PIM\n            Dense Mode (PIM-DM) function.  The groups pimSsmGroup and\n            pimSmGroup are also required.')
pimDeviceStorageGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 157, 2, 2, 15)).setObjects(*(('PIM-STD-MIB', 'pimDeviceConfigStorageType'),))
if mibBuilder.loadTexts:
    pimDeviceStorageGroup.setDescription('An object that specifies the volatility of global PIM\n            configuration settings on this device.')
mibBuilder.exportSymbols('PIM-STD-MIB', pimSGUpTime=pimSGUpTime, pimKeepalivePeriod=pimKeepalivePeriod, pimStarGTable=pimStarGTable, pimStarGRPFRouteMetricPref=pimStarGRPFRouteMetricPref, pimTopologyGroup=pimTopologyGroup, pimLastAssertGroupAddress=pimLastAssertGroupAddress, pimSGAddressType=pimSGAddressType, pimGroupMappingPimMode=pimGroupMappingPimMode, pimGroupMappingRPAddressType=pimGroupMappingRPAddressType, pimStarGIUpTime=pimStarGIUpTime, pimLastAssertSourceAddressType=pimLastAssertSourceAddressType, pimStarGPimMode=pimStarGPimMode, pimInterfaceIfIndex=pimInterfaceIfIndex, pimInterfaceOverrideInterval=pimInterfaceOverrideInterval, pimStarGIAssertTimer=pimStarGIAssertTimer, pimBidirDFElectionIfIndex=pimBidirDFElectionIfIndex, pimGroupMappingEntry=pimGroupMappingEntry, pimNbrSecAddressEntry=pimNbrSecAddressEntry, pimMIBComplianceSsm=pimMIBComplianceSsm, pimMIBComplianceDm=pimMIBComplianceDm, pimDeviceStorageGroup=pimDeviceStorageGroup, pimSGRPFIfIndex=pimSGRPFIfIndex, pimInterfaceHelloInterval=pimInterfaceHelloInterval, pimNotificationGroup=pimNotificationGroup, pimAnycastRPSetAnycastAddress=pimAnycastRPSetAnycastAddress, pimSGITable=pimSGITable, pimRPMappingChangeCount=pimRPMappingChangeCount, pimInvalidRegisterRp=pimInvalidRegisterRp, pimInvalidJoinPruneNotificationPeriod=pimInvalidJoinPruneNotificationPeriod, pimInterfaceStatus=pimInterfaceStatus, pimStarGUpstreamNeighbor=pimStarGUpstreamNeighbor, pimStarGRPFNextHopType=pimStarGRPFNextHopType, pimSGTable=pimSGTable, pimInterfacePruneLimitInterval=pimInterfacePruneLimitInterval, pimStarGIAssertWinnerAddress=pimStarGIAssertWinnerAddress, pimStarGILocalMembership=pimStarGILocalMembership, pimSGIEntry=pimSGIEntry, pimNeighborEntry=pimNeighborEntry, pimNeighborExpiryTime=pimNeighborExpiryTime, pimBidirDFElectionWinnerAddressType=pimBidirDFElectionWinnerAddressType, pimStarGIJoinPruneState=pimStarGIJoinPruneState, pimSGSPTBit=pimSGSPTBit, pimStaticRPEntry=pimStaticRPEntry, pimSGRptIPrunePendingTimer=pimSGRptIPrunePendingTimer, pimInterfaceEffectOverrideIvl=pimInterfaceEffectOverrideIvl, pimSGDRRegisterStopTimer=pimSGDRRegisterStopTimer, pimSGRPFNextHop=pimSGRPFNextHop, pimGroupMappingGrpPrefixLength=pimGroupMappingGrpPrefixLength, pimDmGroup=pimDmGroup, pimSGEntries=pimSGEntries, pimLastAssertSourceAddress=pimLastAssertSourceAddress, pimInterfaceBidirCapable=pimInterfaceBidirCapable, pimSGIAssertWinnerAddress=pimSGIAssertWinnerAddress, pimSGRPFRoutePrefixLength=pimSGRPFRoutePrefixLength, pimOutAsserts=pimOutAsserts, pimSGUpstreamPruneLimitTimer=pimSGUpstreamPruneLimitTimer, pimSGRptTable=pimSGRptTable, pimBidirDFElectionWinnerUpTime=pimBidirDFElectionWinnerUpTime, pimNeighborLoss=pimNeighborLoss, pimNbrSecAddressIfIndex=pimNbrSecAddressIfIndex, pimNbrSecAddressPrimary=pimNbrSecAddressPrimary, pimStarGITable=pimStarGITable, pimSGIJoinPruneState=pimSGIJoinPruneState, pimStaticRPStorageType=pimStaticRPStorageType, pimStarGPimModeOrigin=pimStarGPimModeOrigin, pimStarGIAssertState=pimStarGIAssertState, pimStarGRPFRoutePrefixLength=pimStarGRPFRoutePrefixLength, pimInterfaceDRPriority=pimInterfaceDRPriority, pimStarGIPrunePendingTimer=pimStarGIPrunePendingTimer, pimStarGUpTime=pimStarGUpTime, pimInterfaceElection=pimInterfaceElection, pimInAsserts=pimInAsserts, pimInterfaceDR=pimInterfaceDR, pimNeighborGenerationIDValue=pimNeighborGenerationIDValue, pimInterfaceSRPriorityEnabled=pimInterfaceSRPriorityEnabled, pim=pim, pimStarGIEntry=pimStarGIEntry, pimSGStateRefreshTimer=pimSGStateRefreshTimer, pimSGIAssertWinnerMetric=pimSGIAssertWinnerMetric, pimRouterStatisticsGroup=pimRouterStatisticsGroup, pimInvalidJoinPruneRp=pimInvalidJoinPruneRp, pimSGRPFNextHopType=pimSGRPFNextHopType, pimInvalidJoinPruneAddressType=pimInvalidJoinPruneAddressType, pimSGRPRegisterPMBRAddressType=pimSGRPRegisterPMBRAddressType, pimSGIUpTime=pimSGIUpTime, pimStaticRPPimMode=pimStaticRPPimMode, pimInterfaceAddressType=pimInterfaceAddressType, pimSGRPFRouteMetricPref=pimSGRPFRouteMetricPref, pimInvalidJoinPruneGroup=pimInvalidJoinPruneGroup, pimInterfaceGraftRetryInterval=pimInterfaceGraftRetryInterval, pimInterfaceStorageType=pimInterfaceStorageType, pimSGRptIJoinPruneState=pimSGRptIJoinPruneState, pimStarGRPFRouteAddress=pimStarGRPFRouteAddress, pimDeviceConfigStorageType=pimDeviceConfigStorageType, pimStarGRPAddress=pimStarGRPAddress, pimMIBConformance=pimMIBConformance, pimMIBCompliances=pimMIBCompliances, pimSGRPFRouteProtocol=pimSGRPFRouteProtocol, pimSGEntry=pimSGEntry, pimStarGIEntries=pimStarGIEntries, pimInterfaceAddress=pimInterfaceAddress, pimStarGEntry=pimStarGEntry, pimMIBComplianceAsm=pimMIBComplianceAsm, pimBidirDFElectionStateTimer=pimBidirDFElectionStateTimer, pimInvalidRegisterGroup=pimInvalidRegisterGroup, pimNbrSecAddress=pimNbrSecAddress, pimSGGrpAddress=pimSGGrpAddress, pimSGIAssertTimer=pimSGIAssertTimer, pimMIBGroups=pimMIBGroups, pimBidirDFElectionAddressType=pimBidirDFElectionAddressType, pimSGRptILocalMembership=pimSGRptILocalMembership, pimStarGGrpAddress=pimStarGGrpAddress, pimRPConfigGroup=pimRPConfigGroup, pimNeighborTable=pimNeighborTable, pimSmGroup=pimSmGroup, pimBidirGroup=pimBidirGroup, pimSGSourceActiveTimer=pimSGSourceActiveTimer, pimInterfaceStubInterface=pimInterfaceStubInterface, pimSGUpstreamJoinTimer=pimSGUpstreamJoinTimer, pimInterfaceLanDelayEnabled=pimInterfaceLanDelayEnabled, pimSGRptIIfIndex=pimSGRptIIfIndex, pimBidirDFElectionRPAddress=pimBidirDFElectionRPAddress, pimSGRptEntry=pimSGRptEntry, pimAnycastRPSetTable=pimAnycastRPSetTable, pimNetMgmtNotificationGroup=pimNetMgmtNotificationGroup, pimInterfaceElectionNotificationPeriod=pimInterfaceElectionNotificationPeriod, pimAnycastRPSetStorageType=pimAnycastRPSetStorageType, pimMIBComplianceBidir=pimMIBComplianceBidir, pimSGPimMode=pimSGPimMode, pimInterfaceHelloHoldtime=pimInterfaceHelloHoldtime, pimNeighborAddress=pimNeighborAddress, pimNeighborTBit=pimNeighborTBit, pimSGILocalMembership=pimSGILocalMembership, pimAnycastRpGroup=pimAnycastRpGroup, pimLastAssertInterface=pimLastAssertInterface, pimInterfaceGenerationIDValue=pimInterfaceGenerationIDValue, pimStarGRPFNextHop=pimStarGRPFNextHop, pimInvalidJoinPruneOrigin=pimInvalidJoinPruneOrigin, pimInterfacePropagationDelay=pimInterfacePropagationDelay, PimMode=PimMode, pimSGOriginatorState=pimSGOriginatorState, pimAnycastRPSetLocalRouter=pimAnycastRPSetLocalRouter, pimSGIPrunePendingTimer=pimSGIPrunePendingTimer, pimStaticRPTable=pimStaticRPTable, pimInvalidJoinPruneMsgsRcvd=pimInvalidJoinPruneMsgsRcvd, pimInterfaceEntry=pimInterfaceEntry, pimNbrSecAddressType=pimNbrSecAddressType, pimSGKeepaliveTimer=pimSGKeepaliveTimer, pimInterfaceDomainBorder=pimInterfaceDomainBorder, pimTuningParametersGroup=pimTuningParametersGroup, pimBidirDFElectionWinnerMetricPref=pimBidirDFElectionWinnerMetricPref, pimStaticRPOverrideDynamic=pimStaticRPOverrideDynamic, pimInterfaceTable=pimInterfaceTable, pimAnycastRPSetRowStatus=pimAnycastRPSetRowStatus, pimSGSrcAddress=pimSGSrcAddress, pimInvalidRegisterMsgsRcvd=pimInvalidRegisterMsgsRcvd, pimInterfaceJoinPruneHoldtime=pimInterfaceJoinPruneHoldtime, pimSGRPFRouteMetric=pimSGRPFRouteMetric, pimStarGIIfIndex=pimStarGIIfIndex, pimBidirDFElectionWinnerMetric=pimBidirDFElectionWinnerMetric, pimInvalidJoinPrune=pimInvalidJoinPrune, pimGroupMappingRPAddress=pimGroupMappingRPAddress, pimSGUpstreamPruneState=pimSGUpstreamPruneState, pimAnycastRPSetRouterAddress=pimAnycastRPSetRouterAddress, pimNeighborDRPriority=pimNeighborDRPriority, pimNeighborIfIndex=pimNeighborIfIndex, pimNeighborLossNotificationPeriod=pimNeighborLossNotificationPeriod, pimInvalidRegisterAddressType=pimInvalidRegisterAddressType, pimStarGIAssertWinnerMetric=pimStarGIAssertWinnerMetric, pimGroupMappingAddressType=pimGroupMappingAddressType, pimNeighborPropagationDelay=pimNeighborPropagationDelay, pimNeighborOverrideInterval=pimNeighborOverrideInterval, pimStaticRPGrpPrefixLength=pimStaticRPGrpPrefixLength, pimStarGUpstreamNeighborType=pimStarGUpstreamNeighborType, pimNeighborBidirCapable=pimNeighborBidirCapable, pimRegisterSuppressionTime=pimRegisterSuppressionTime, pimNeighborGenerationIDPresent=pimNeighborGenerationIDPresent, pimInterfaceJoinPruneInterval=pimInterfaceJoinPruneInterval, pimSGIAssertWinnerMetricPref=pimSGIAssertWinnerMetricPref, pimBidirDFElectionWinnerAddress=pimBidirDFElectionWinnerAddress, pimStarGRPFRouteProtocol=pimStarGRPFRouteProtocol, pimNeighborLanPruneDelayPresent=pimNeighborLanPruneDelayPresent, pimNotifications=pimNotifications, pimSGRPFRouteAddress=pimSGRPFRouteAddress, pimInterfaceEffectPropagDelay=pimInterfaceEffectPropagDelay, pimStaticRPAddressType=pimStaticRPAddressType, pimSGIAssertWinnerAddressType=pimSGIAssertWinnerAddressType, pimStaticRPPrecedenceGroup=pimStaticRPPrecedenceGroup, pimStdMIB=pimStdMIB, pimStarGUpstreamJoinState=pimStarGUpstreamJoinState, pimSGUpstreamJoinState=pimSGUpstreamJoinState, pimSGRptIUpTime=pimSGRptIUpTime, pimStarGRPFIfIndex=pimStarGRPFIfIndex, pimSGRptIEntry=pimSGRptIEntry, pimSGRptEntries=pimSGRptEntries, pimNeighborAddressType=pimNeighborAddressType, pimStarGIJoinExpiryTimer=pimStarGIJoinExpiryTimer, pimInvalidRegisterOrigin=pimInvalidRegisterOrigin, pimInterfaceElectionWinCount=pimInterfaceElectionWinCount, pimSGRptUpstreamOverrideTimer=pimSGRptUpstreamOverrideTimer, pimNeighborDRPriorityPresent=pimNeighborDRPriorityPresent, pimBidirDFElectionState=pimBidirDFElectionState, pimSsmGroup=pimSsmGroup, pimInterfaceIPVersion=pimInterfaceIPVersion, pimNeighborLossCount=pimNeighborLossCount, pimSGIEntries=pimSGIEntries, pimBidirDFElectionEntry=pimBidirDFElectionEntry, pimStaticRPRowStatus=pimStaticRPRowStatus, pimGroupMappingOrigin=pimGroupMappingOrigin, pimStarGAddressType=pimStarGAddressType, pimGroupMappingPrecedence=pimGroupMappingPrecedence, pimStarGIAssertWinnerAddressType=pimStarGIAssertWinnerAddressType, pimSGIAssertState=pimSGIAssertState, pimInvalidRegister=pimInvalidRegister, pimInterfaceDFElectionRobustness=pimInterfaceDFElectionRobustness, pimAnycastRPSetAddressType=pimAnycastRPSetAddressType, pimSGRPRegisterPMBRAddress=pimSGRPRegisterPMBRAddress, pimSGRptIEntries=pimSGRptIEntries, pimNeighborSRCapable=pimNeighborSRCapable, pimStarGEntries=pimStarGEntries, pimSGRptUpTime=pimSGRptUpTime, pimStarGRPFRouteMetric=pimStarGRPFRouteMetric, pimLastAssertGroupAddressType=pimLastAssertGroupAddressType, pimStaticRPPrecedence=pimStaticRPPrecedence, pimStarGIAssertWinnerMetricPref=pimStarGIAssertWinnerMetricPref, pimGroupMappingGrpAddress=pimGroupMappingGrpAddress, pimInvalidRegisterNotificationPeriod=pimInvalidRegisterNotificationPeriod, pimSGIJoinExpiryTimer=pimSGIJoinExpiryTimer, pimStarGRPIsLocal=pimStarGRPIsLocal, pimAnycastRPSetEntry=pimAnycastRPSetEntry, pimRPMappingChange=pimRPMappingChange, pimNeighborUpTime=pimNeighborUpTime, pimNbrSecAddressTable=pimNbrSecAddressTable, pimSGRptITable=pimSGRptITable, pimBidirDFElectionTable=pimBidirDFElectionTable, pimNetMgmtNotificationObjects=pimNetMgmtNotificationObjects, pimInterfaceTrigHelloInterval=pimInterfaceTrigHelloInterval, pimStarGUpstreamJoinTimer=pimStarGUpstreamJoinTimer, PimGroupMappingOriginType=PimGroupMappingOriginType, pimSGRptUpstreamPruneState=pimSGRptUpstreamPruneState, PYSNMP_MODULE_ID=pimStdMIB, pimRPMappingNotificationPeriod=pimRPMappingNotificationPeriod, pimInterfaceDRPriorityEnabled=pimInterfaceDRPriorityEnabled, pimStaticRPRPAddress=pimStaticRPRPAddress, pimSGDRRegisterState=pimSGDRRegisterState, pimSGRptSrcAddress=pimSGRptSrcAddress, pimDiagnosticsGroup=pimDiagnosticsGroup, pimInterfaceSuppressionEnabled=pimInterfaceSuppressionEnabled, pimStarGRPAddressType=pimStarGRPAddressType, pimSGRptIPruneExpiryTimer=pimSGRptIPruneExpiryTimer, pimStaticRPGrpAddress=pimStaticRPGrpAddress, pimGroupMappingTable=pimGroupMappingTable, pimRefreshInterval=pimRefreshInterval, pimSGIIfIndex=pimSGIIfIndex)
mibBuilder.exportSymbols('PIM-STD-MIB', pimSGUpstreamNeighbor=pimSGUpstreamNeighbor)