# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/PTOPO-MIB.py
# Compiled at: 2016-02-13 18:24:59
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ConstraintsUnion, ValueSizeConstraint, ConstraintsIntersection, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ConstraintsUnion', 'ValueSizeConstraint', 'ConstraintsIntersection', 'SingleValueConstraint')
(PhysicalIndex,) = mibBuilder.importSymbols('ENTITY-MIB', 'PhysicalIndex')
(AddressFamilyNumbers,) = mibBuilder.importSymbols('IANA-ADDRESS-FAMILY-NUMBERS-MIB', 'AddressFamilyNumbers')
(TimeFilter,) = mibBuilder.importSymbols('RMON2-MIB', 'TimeFilter')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(Integer32, IpAddress, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter32, NotificationType, iso, TimeTicks, Unsigned32, mib_2, Gauge32, ObjectIdentity, Bits, MibIdentifier, ModuleIdentity, Counter64) = mibBuilder.importSymbols('SNMPv2-SMI', 'Integer32', 'IpAddress', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter32', 'NotificationType', 'iso', 'TimeTicks', 'Unsigned32', 'mib-2', 'Gauge32', 'ObjectIdentity', 'Bits', 'MibIdentifier', 'ModuleIdentity', 'Counter64')
(TruthValue, TimeStamp, DisplayString, RowStatus, AutonomousType, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'TruthValue', 'TimeStamp', 'DisplayString', 'RowStatus', 'AutonomousType', 'TextualConvention')
ptopoMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 79)).setRevisions(('2000-09-21 00:00', ))
if mibBuilder.loadTexts:
    ptopoMIB.setLastUpdated('200009210000Z')
if mibBuilder.loadTexts:
    ptopoMIB.setOrganization('IETF; PTOPOMIB Working Group')
if mibBuilder.loadTexts:
    ptopoMIB.setContactInfo('PTOPOMIB WG Discussion:\n        ptopo@3com.com\n        Subscription:\n        majordomo@3com.com\n          msg body: [un]subscribe ptopomib\n\n        Andy Bierman\n        Cisco Systems Inc.\n        170 West Tasman Drive\n        San Jose, CA 95134\n        408-527-3711\n        abierman@cisco.com\n\n        Kendall S. Jones\n        Nortel Networks\n        4401 Great America Parkway\n        Santa Clara, CA 95054\n        408-495-7356\n        kejones@nortelnetworks.com')
if mibBuilder.loadTexts:
    ptopoMIB.setDescription('The MIB module for physical topology information.')
ptopoMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 1))
ptopoData = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 1, 1))
ptopoGeneral = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 1, 2))
ptopoConfig = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 1, 3))

class PtopoGenAddr(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 20)


class PtopoChassisIdType(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))
    namedValues = NamedValues(('chasIdEntPhysicalAlias', 1), ('chasIdIfAlias', 2), ('chasIdPortEntPhysicalAlias',
                                                                                    3), ('chasIdMacAddress',
                                                                                         4), ('chasIdPtopoGenAddr',
                                                                                              5))


class PtopoChassisId(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(1, 32)


class PtopoPortIdType(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))
    namedValues = NamedValues(('portIdIfAlias', 1), ('portIdEntPhysicalAlias', 2), ('portIdMacAddr',
                                                                                    3), ('portIdPtopoGenAddr',
                                                                                         4))


class PtopoPortId(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(1, 32)


class PtopoAddrSeenState(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))
    namedValues = NamedValues(('notUsed', 1), ('unknown', 2), ('oneAddr', 3), ('multiAddr',
                                                                               4))


ptopoConnTable = MibTable((1, 3, 6, 1, 2, 1, 79, 1, 1, 1))
if mibBuilder.loadTexts:
    ptopoConnTable.setDescription('This table contains one or more rows per physical network\n            connection known to this agent.  The agent may wish to\n            ensure that only one ptopoConnEntry is present for each\n            local port, or it may choose to maintain multiple\n            ptopoConnEntries for the same local port.\n\n            Entries based on lower numbered identifier types are\n            preferred over higher numbered identifier types, i.e., lower\n            values of the ptopoConnRemoteChassisType and\n            ptopoConnRemotePortType objects.')
ptopoConnEntry = MibTableRow((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1)).setIndexNames((0,
                                                                                'PTOPO-MIB',
                                                                                'ptopoConnTimeMark'), (0,
                                                                                                       'PTOPO-MIB',
                                                                                                       'ptopoConnLocalChassis'), (0,
                                                                                                                                  'PTOPO-MIB',
                                                                                                                                  'ptopoConnLocalPort'), (0,
                                                                                                                                                          'PTOPO-MIB',
                                                                                                                                                          'ptopoConnIndex'))
if mibBuilder.loadTexts:
    ptopoConnEntry.setDescription('Information about a particular physical network connection.\n            Entries may be created and deleted in this table, either\n            manually or by the agent, if a physical topology discovery\n            process is active.')
ptopoConnTimeMark = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 1), TimeFilter())
if mibBuilder.loadTexts:
    ptopoConnTimeMark.setDescription('A TimeFilter for this entry.  See the TimeFilter textual\n            convention in RFC 2021 to see how this works.')
ptopoConnLocalChassis = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 2), PhysicalIndex())
if mibBuilder.loadTexts:
    ptopoConnLocalChassis.setDescription('The entPhysicalIndex value used to identify the chassis\n            component associated with the local connection endpoint.')
ptopoConnLocalPort = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 3), PhysicalIndex())
if mibBuilder.loadTexts:
    ptopoConnLocalPort.setDescription('The entPhysicalIndex value used to identify the port\n            component associated with the local connection endpoint.')
ptopoConnIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)))
if mibBuilder.loadTexts:
    ptopoConnIndex.setDescription('This object represents an arbitrary local integer value\n            used by this agent to identify a particular connection\n            instance, unique only for the indicated local connection\n            endpoint.\n\n            A particular ptopoConnIndex value may be reused in the event\n            an entry is aged out and later re-learned with the same (or\n            different) remote chassis and port identifiers.\n\n            An agent is encouraged to assign monotonically increasing\n            index values to new entries, starting with one, after each\n            reboot.  It is considered unlikely that the ptopoConnIndex\n            will wrap between reboots.')
ptopoConnRemoteChassisType = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 5), PtopoChassisIdType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnRemoteChassisType.setDescription('The type of encoding used to identify the chassis\n            associated with the remote connection endpoint.\n\n            This object may not be modified if the associated\n            ptopoConnRowStatus object has a value of active(1).')
ptopoConnRemoteChassis = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 6), PtopoChassisId()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnRemoteChassis.setDescription('The string value used to identify the chassis component\n            associated with the remote connection endpoint.\n\n            This object may not be modified if the associated\n            ptopoConnRowStatus object has a value of active(1).')
ptopoConnRemotePortType = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 7), PtopoPortIdType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnRemotePortType.setDescription("The type of port identifier encoding used in the associated\n            'ptopoConnRemotePort' object.\n\n            This object may not be modified if the associated\n            ptopoConnRowStatus object has a value of active(1).")
ptopoConnRemotePort = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 8), PtopoPortId()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnRemotePort.setDescription('The string value used to identify the port component\n            associated with the remote connection endpoint.\n            This object may not be modified if the associated\n            ptopoConnRowStatus object has a value of active(1).')
ptopoConnDiscAlgorithm = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 9), AutonomousType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnDiscAlgorithm.setDescription('An indication of the algorithm used to discover the\n            information contained in this conceptual row.\n\n            A value of ptopoDiscoveryLocal indicates this entry was\n            configured by the local agent, without use of a discovery\n            protocol.\n\n            A value of { 0 0 } indicates this entry was created manually\n            by an NMS via the associated RowStatus object. ')
ptopoConnAgentNetAddrType = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 10), AddressFamilyNumbers()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnAgentNetAddrType.setDescription('This network address type of the associated\n            ptopoConnNetAddr object, unless that object contains a zero\n            length string.  In such a case, an NMS application should\n            ignore any returned value for this object.\n\n            This object may not be modified if the associated\n            ptopoConnRowStatus object has a value of active(1).')
ptopoConnAgentNetAddr = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 11), PtopoGenAddr()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnAgentNetAddr.setDescription("This object identifies a network address which may be used\n            to reach an SNMP agent entity containing information for the\n            chassis and port components represented by the associated\n            'ptopoConnRemoteChassis' and 'ptopoConnRemotePort' objects.\n            If no such address is known, then this object shall contain\n            an empty string.\n\n            This object may not be modified if the associated\n            ptopoConnRowStatus object has a value of active(1).")
ptopoConnMultiMacSASeen = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 12), PtopoAddrSeenState()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnMultiMacSASeen.setDescription("This object indicates if multiple unicast source MAC\n            addresses have been detected by the agent from the remote\n            connection endpoint, since the creation of this entry.\n\n            If this entry has an associated ptopoConnRemoteChassisType\n            and/or ptopoConnRemotePortType value other than\n            'portIdMacAddr(3)', then the value 'notUsed(1)' is returned.\n\n            Otherwise, one of the following conditions must be true:\n\n            If the agent has not yet detected any unicast source MAC\n            addresses from the remote port, then the value 'unknown(2)'\n            is returned.\n\n            If the agent has detected exactly one unicast source MAC\n            address from the remote port, then the value 'oneAddr(3)' is\n            returned.\n\n            If the agent has detected more than one unicast source MAC\n            address from the remote port, then the value 'multiAddr(4)'\n            is returned.")
ptopoConnMultiNetSASeen = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 13), PtopoAddrSeenState()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnMultiNetSASeen.setDescription("This object indicates if multiple network layer source\n            addresses have been detected by the agent from the remote\n            connection endpoint, since the creation of this entry.\n\n            If this entry has an associated ptopoConnRemoteChassisType\n            or ptopoConnRemotePortType value other than\n            'portIdGenAddr(4)' then the value 'notUsed(1)' is returned.\n\n            Otherwise, one of the following conditions must be true:\n\n            If the agent has not yet detected any network source\n            addresses of the appropriate type from the remote port, then\n            the value 'unknown(2)' is returned.\n            If the agent has detected exactly one network source address\n            of the appropriate type from the remote port, then the value\n            'oneAddr(3)' is returned.\n\n            If the agent has detected more than one network source\n            address (of the same appropriate type) from the remote port,\n            this the value 'multiAddr(4)' is returned.")
ptopoConnIsStatic = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 14), TruthValue().clone('false')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnIsStatic.setDescription("This object identifies static ptopoConnEntries.  If this\n            object has the value 'true(1)', then this entry is not\n            subject to any age-out mechanisms implemented by the agent.\n\n            If this object has the value 'false(2)', then this entry is\n            subject to all age-out mechanisms implemented by the agent.\n\n            This object may not be modified if the associated\n            ptopoConnRowStatus object has a value of active(1).")
ptopoConnLastVerifyTime = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 15), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnLastVerifyTime.setDescription("If the associated value of ptopoConnIsStatic is equal to\n            'false(2)', then this object contains the value of sysUpTime\n            at the time the conceptual row was last verified by the\n            agent, e.g., via reception of a topology protocol message,\n            pertaining to the associated remote chassis and port.\n\n            If the associated value of ptopoConnIsStatic is equal to\n            'true(1)', then this object shall contain the value of\n            sysUpTime at the time this entry was last activated (i.e.,\n            ptopoConnRowStatus set to 'active(1)').")
ptopoConnRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 79, 1, 1, 1, 1, 16), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    ptopoConnRowStatus.setDescription('The status of this conceptual row.')
ptopoLastChangeTime = MibScalar((1, 3, 6, 1, 2, 1, 79, 1, 2, 1), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoLastChangeTime.setDescription('The value of sysUpTime at the time a conceptual row is\n            created, modified, or deleted in the ptopoConnTable.\n\n            An NMS can use this object to reduce polling of the\n            ptopoData group objects.')
ptopoConnTabInserts = MibScalar((1, 3, 6, 1, 2, 1, 79, 1, 2, 2), Counter32()).setUnits('table entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnTabInserts.setDescription('The number of times an entry has been inserted into the\n            ptopoConnTable.')
ptopoConnTabDeletes = MibScalar((1, 3, 6, 1, 2, 1, 79, 1, 2, 3), Counter32()).setUnits('table entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnTabDeletes.setDescription('The number of times an entry has been deleted from the\n            ptopoConnTable.')
ptopoConnTabDrops = MibScalar((1, 3, 6, 1, 2, 1, 79, 1, 2, 4), Counter32()).setUnits('table entries').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnTabDrops.setDescription('The number of times an entry would have been added to the\n            ptopoConnTable, (e.g., via information learned from a\n            topology protocol), but was not because of insufficient\n            resources.')
ptopoConnTabAgeouts = MibScalar((1, 3, 6, 1, 2, 1, 79, 1, 2, 5), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ptopoConnTabAgeouts.setDescription('The number of times an entry has been deleted from the\n            ptopoConnTable because the information timeliness interval\n            for that entry has expired.')
ptopoConfigTrapInterval = MibScalar((1, 3, 6, 1, 2, 1, 79, 1, 3, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0, 0), ValueRangeConstraint(5, 3600)))).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    ptopoConfigTrapInterval.setDescription("This object controls the transmission of PTOPO\n            notifications.\n\n            If this object has a value of zero, then no\n            ptopoConfigChange notifications will be transmitted by the\n            agent.\n\n            If this object has a non-zero value, then the agent must not\n            generate more than one ptopoConfigChange trap-event in the\n            indicated period, where a 'trap-event' is the transmission\n            of a single notification PDU type to a list of notification\n            destinations.  If additional configuration changes occur\n            within the indicated throttling period, then these trap-\n            events must be suppressed by the agent. An NMS should\n            periodically check the value of ptopoLastChangeTime to\n            detect any missed ptopoConfigChange trap-events, e.g. due to\n            throttling or transmission loss.\n            If notification transmission is enabled, the suggested\n            default throttling period is 60 seconds, but transmission\n            should be disabled by default.\n\n            If the agent is capable of storing non-volatile\n            configuration, then the value of this object must be\n            restored after a re-initialization of the management\n            system.")
ptopoConfigMaxHoldTime = MibScalar((1, 3, 6, 1, 2, 1, 79, 1, 3, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 2147483647)).clone(300)).setUnits('seconds').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    ptopoConfigMaxHoldTime.setDescription("This object specifies the desired time interval for which\n            an agent will maintain dynamic ptopoConnEntries.\n\n            After the specified number of seconds since the last time an\n            entry was verified, in the absence of new verification\n            (e.g., receipt of a topology protocol message), the agent\n            shall remove the entry.  Note that entries may not always be\n            removed immediately, but may possibly be removed at periodic\n            garbage collection intervals.\n            This object only affects dynamic ptopoConnEntries, i.e.  for\n            which ptopoConnIsStatic equals 'false(2)'. Static entries\n            are not aged out.\n\n            Note that dynamic ptopoConnEntries may also be removed by\n            the agent due to the expired timeliness of learned topology\n            information (e.g., timeliness interval for a remote port\n            expires).  The actual age-out interval for a given entry is\n            defined by the following formula:\n\n              age-out-time =\n                min(ptopoConfigMaxHoldTime, <entry-specific hold-time>)\n\n            where <entry-specific hold-time> is determined by the\n            discovery algorithm, and may be different for each entry.")
ptopoMIBNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 2))
ptopoMIBTrapPrefix = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 2, 0))
ptopoConfigChange = NotificationType((1, 3, 6, 1, 2, 1, 79, 2, 0, 1)).setObjects(*(('PTOPO-MIB', 'ptopoConnTabInserts'), ('PTOPO-MIB', 'ptopoConnTabDeletes'), ('PTOPO-MIB', 'ptopoConnTabDrops'), ('PTOPO-MIB', 'ptopoConnTabAgeouts')))
if mibBuilder.loadTexts:
    ptopoConfigChange.setDescription("A ptopoConfigChange notification is sent when the value of\n            ptopoLastChangeTime changes. It can be utilized by an NMS to\n            trigger physical topology table maintenance polls.\n\n            Note that transmission of ptopoConfigChange notifications\n            are throttled by the agent, as specified by the\n            'ptopoConfigTrapInterval' object.")
ptopoRegistrationPoints = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 3))
ptopoDiscoveryMechanisms = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 3, 1))
ptopoDiscoveryLocal = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 3, 1, 1))
ptopoConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 4))
ptopoCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 4, 1))
ptopoGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 79, 4, 2))
ptopoCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 79, 4, 1, 1)).setObjects(*(('PTOPO-MIB', 'ptopoDataGroup'), ('PTOPO-MIB', 'ptopoGeneralGroup'), ('PTOPO-MIB', 'ptopoConfigGroup'), ('PTOPO-MIB', 'ptopoNotificationsGroup')))
if mibBuilder.loadTexts:
    ptopoCompliance.setDescription('The compliance statement for SNMP entities which implement\n            the PTOPO MIB.')
ptopoDataGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 79, 4, 2, 1)).setObjects(*(('PTOPO-MIB', 'ptopoConnRemoteChassisType'), ('PTOPO-MIB', 'ptopoConnRemoteChassis'), ('PTOPO-MIB', 'ptopoConnRemotePortType'), ('PTOPO-MIB', 'ptopoConnRemotePort'), ('PTOPO-MIB', 'ptopoConnDiscAlgorithm'), ('PTOPO-MIB', 'ptopoConnAgentNetAddrType'), ('PTOPO-MIB', 'ptopoConnAgentNetAddr'), ('PTOPO-MIB', 'ptopoConnMultiMacSASeen'), ('PTOPO-MIB', 'ptopoConnMultiNetSASeen'), ('PTOPO-MIB', 'ptopoConnIsStatic'), ('PTOPO-MIB', 'ptopoConnLastVerifyTime'), ('PTOPO-MIB', 'ptopoConnRowStatus')))
if mibBuilder.loadTexts:
    ptopoDataGroup.setDescription('The collection of objects which are used to represent\n            physical topology information for which a single agent\n            provides management information.\n\n            This group is mandatory for all implementations of the PTOPO\n            MIB.')
ptopoGeneralGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 79, 4, 2, 2)).setObjects(*(('PTOPO-MIB', 'ptopoLastChangeTime'), ('PTOPO-MIB', 'ptopoConnTabInserts'), ('PTOPO-MIB', 'ptopoConnTabDeletes'), ('PTOPO-MIB', 'ptopoConnTabDrops'), ('PTOPO-MIB', 'ptopoConnTabAgeouts')))
if mibBuilder.loadTexts:
    ptopoGeneralGroup.setDescription('The collection of objects which are used to report the\n            general status of the PTOPO MIB implementation.\n\n            This group is mandatory for all agents which implement the\n            PTOPO MIB.')
ptopoConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 79, 4, 2, 3)).setObjects(*(('PTOPO-MIB', 'ptopoConfigTrapInterval'), ('PTOPO-MIB', 'ptopoConfigMaxHoldTime')))
if mibBuilder.loadTexts:
    ptopoConfigGroup.setDescription('The collection of objects which are used to configure the\n            PTOPO MIB implementation behavior.\n\n            This group is mandatory for agents which implement the PTOPO\n            MIB.')
ptopoNotificationsGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 79, 4, 2, 4)).setObjects(*(('PTOPO-MIB', 'ptopoConfigChange'), ))
if mibBuilder.loadTexts:
    ptopoNotificationsGroup.setDescription('The collection of notifications used to indicate PTOPO MIB\n            data consistency and general status information.\n\n            This group is mandatory for agents which implement the PTOPO\n            MIB.')
mibBuilder.exportSymbols('PTOPO-MIB', PtopoChassisId=PtopoChassisId, ptopoConnMultiNetSASeen=ptopoConnMultiNetSASeen, ptopoGroups=ptopoGroups, ptopoConnRemotePort=ptopoConnRemotePort, ptopoConnLastVerifyTime=ptopoConnLastVerifyTime, ptopoConnTabAgeouts=ptopoConnTabAgeouts, ptopoLastChangeTime=ptopoLastChangeTime, ptopoConformance=ptopoConformance, ptopoConfigGroup=ptopoConfigGroup, PYSNMP_MODULE_ID=ptopoMIB, ptopoConnTimeMark=ptopoConnTimeMark, ptopoConnEntry=ptopoConnEntry, ptopoData=ptopoData, ptopoConnLocalPort=ptopoConnLocalPort, ptopoConnIsStatic=ptopoConnIsStatic, ptopoGeneral=ptopoGeneral, ptopoConfigMaxHoldTime=ptopoConfigMaxHoldTime, ptopoMIB=ptopoMIB, ptopoConfigChange=ptopoConfigChange, PtopoGenAddr=PtopoGenAddr, ptopoDataGroup=ptopoDataGroup, ptopoConnDiscAlgorithm=ptopoConnDiscAlgorithm, ptopoConnIndex=ptopoConnIndex, ptopoConnRemoteChassisType=ptopoConnRemoteChassisType, PtopoChassisIdType=PtopoChassisIdType, PtopoAddrSeenState=PtopoAddrSeenState, ptopoConnAgentNetAddrType=ptopoConnAgentNetAddrType, ptopoMIBNotifications=ptopoMIBNotifications, ptopoMIBObjects=ptopoMIBObjects, ptopoDiscoveryMechanisms=ptopoDiscoveryMechanisms, ptopoRegistrationPoints=ptopoRegistrationPoints, ptopoConnRowStatus=ptopoConnRowStatus, ptopoConnTabDrops=ptopoConnTabDrops, ptopoConfig=ptopoConfig, PtopoPortId=PtopoPortId, ptopoCompliance=ptopoCompliance, ptopoConnTabDeletes=ptopoConnTabDeletes, ptopoConnLocalChassis=ptopoConnLocalChassis, ptopoCompliances=ptopoCompliances, ptopoConnTable=ptopoConnTable, ptopoConnRemoteChassis=ptopoConnRemoteChassis, ptopoNotificationsGroup=ptopoNotificationsGroup, ptopoGeneralGroup=ptopoGeneralGroup, ptopoConfigTrapInterval=ptopoConfigTrapInterval, ptopoMIBTrapPrefix=ptopoMIBTrapPrefix, ptopoConnRemotePortType=ptopoConnRemotePortType, ptopoConnMultiMacSASeen=ptopoConnMultiMacSASeen, ptopoDiscoveryLocal=ptopoDiscoveryLocal, PtopoPortIdType=PtopoPortIdType, ptopoConnAgentNetAddr=ptopoConnAgentNetAddr, ptopoConnTabInserts=ptopoConnTabInserts)