# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/NOTIFICATION-LOG-MIB.py
# Compiled at: 2016-02-13 18:22:51
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsIntersection, ConstraintsUnion, ValueRangeConstraint, ValueSizeConstraint, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsIntersection', 'ConstraintsUnion', 'ValueRangeConstraint', 'ValueSizeConstraint', 'SingleValueConstraint')
(SnmpEngineID, SnmpAdminString) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpEngineID', 'SnmpAdminString')
(ObjectGroup, ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'ModuleCompliance', 'NotificationGroup')
(Integer32, mib_2, MibIdentifier, Gauge32, IpAddress, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn, Bits, Counter64, NotificationType, ModuleIdentity, Opaque, Unsigned32, Counter32, iso, ObjectIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'Integer32', 'mib-2', 'MibIdentifier', 'Gauge32', 'IpAddress', 'TimeTicks', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Bits', 'Counter64', 'NotificationType', 'ModuleIdentity', 'Opaque', 'Unsigned32', 'Counter32', 'iso', 'ObjectIdentity')
(TAddress, DisplayString, RowStatus, TDomain, DateAndTime, StorageType, TextualConvention, TimeStamp) = mibBuilder.importSymbols('SNMPv2-TC', 'TAddress', 'DisplayString', 'RowStatus', 'TDomain', 'DateAndTime', 'StorageType', 'TextualConvention', 'TimeStamp')
notificationLogMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 92)).setRevisions(('2000-11-27 00:00', ))
if mibBuilder.loadTexts:
    notificationLogMIB.setLastUpdated('200011270000Z')
if mibBuilder.loadTexts:
    notificationLogMIB.setOrganization('IETF Distributed Management Working Group')
if mibBuilder.loadTexts:
    notificationLogMIB.setContactInfo('Ramanathan Kavasseri\n                    Cisco Systems, Inc.\n                    170 West Tasman Drive,\n                    San Jose CA 95134-1706.\n                    Phone: +1 408 527 2446\n                    Email: ramk@cisco.com')
if mibBuilder.loadTexts:
    notificationLogMIB.setDescription('The MIB module for logging SNMP Notifications, that is, Traps\n                    and Informs.')
notificationLogMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1))
nlmConfig = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1, 1))
nlmStats = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1, 2))
nlmLog = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 1, 3))
nlmConfigGlobalEntryLimit = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 1, 1), Unsigned32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    nlmConfigGlobalEntryLimit.setDescription('The maximum number of notification entries that may be held\n                in nlmLogTable for all nlmLogNames added together.  A particular\n                setting does not guarantee that much data can be held.\n\n                If an application changes the limit while there are\n                Notifications in the log, the oldest Notifications MUST be\n                discarded to bring the log down to the new limit - thus the\n                value of nlmConfigGlobalEntryLimit MUST take precedence over\n                the values of nlmConfigGlobalAgeOut and nlmConfigLogEntryLimit,\n                even if the Notification being discarded has been present for\n                fewer minutes than the value of nlmConfigGlobalAgeOut, or if\n                the named log has fewer entries than that specified in\n                nlmConfigLogEntryLimit.\n\n                A value of 0 means no limit.\n\n                Please be aware that contention between multiple managers\n                trying to set this object to different values MAY affect the\n                reliability and completeness of data seen by each manager.\n                The default value is 0.')
nlmConfigGlobalAgeOut = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 1, 2), Unsigned32()).setUnits('minutes').setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    nlmConfigGlobalAgeOut.setDescription('The number of minutes a Notification SHOULD be kept in a log\n                before it is automatically removed.\n\n                If an application changes the value of nlmConfigGlobalAgeOut,\n                Notifications older than the new time MAY be discarded to meet the\n                new time.\n\n                A value of 0 means no age out.\n\n                Please be aware that contention between multiple managers\n                trying to set this object to different values MAY affect the\n                reliability and completeness of data seen by each manager.\n                The default value is 1440(24 hours).')
nlmConfigLogTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 1, 3))
if mibBuilder.loadTexts:
    nlmConfigLogTable.setDescription('A table of logging control entries.')
nlmConfigLogEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1)).setIndexNames((0,
                                                                                   'NOTIFICATION-LOG-MIB',
                                                                                   'nlmLogName'))
if mibBuilder.loadTexts:
    nlmConfigLogEntry.setDescription("A logging control entry.  Depending on the entry's storage type\n                entries may be supplied by the system or created and deleted by\n                applications using nlmConfigLogEntryStatus.")
nlmLogName = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32)))
if mibBuilder.loadTexts:
    nlmLogName.setDescription('The name of the log.\n\n                An implementation may allow multiple named logs, up to some\n                implementation-specific limit (which may be none).  A\n                zero-length log name is reserved for creation and deletion by\n                the managed system, and MUST be used as the default log name by\n                systems that do not support named logs.')
nlmConfigLogFilterName = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32)).clone(hexValue='')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    nlmConfigLogFilterName.setDescription('A value of snmpNotifyFilterProfileName as used as an index\n                into the snmpNotifyFilterTable in the SNMP Notification MIB,\n                specifying the locally or remotely originated Notifications\n                to be filtered out and not logged in this log.\n\n                A zero-length value or a name that does not identify an\n                existing entry in snmpNotifyFilterTable indicate no\n                Notifications are to be logged in this log.')
nlmConfigLogEntryLimit = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 3), Unsigned32()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    nlmConfigLogEntryLimit.setDescription('The maximum number of notification entries that can be held in\n                nlmLogTable for this named log.  A particular setting does not\n                guarantee that that much data can be held.\n                \n                If an application changes the limit while there are\n                Notifications in the log, the oldest Notifications are discarded\n                to bring the log down to the new limit.\n                A value of 0 indicates no limit.\n                \n                Please be aware that contention between multiple managers\n                trying to set this object to different values MAY affect the\n                reliability and completeness of data seen by each manager.')
nlmConfigLogAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled',
                                                                                                                                                                                              1), ('disabled',
                                                                                                                                                                                                   2))).clone('enabled')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    nlmConfigLogAdminStatus.setDescription("Control to enable or disable the log without otherwise\n                disturbing the log's entry.\n                \n                Please be aware that contention between multiple managers\n                trying to set this object to different values MAY affect the\n                reliability and completeness of data seen by each manager.")
nlmConfigLogOperStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('disabled',
                                                                                                                                                                                                1), ('operational',
                                                                                                                                                                                                     2), ('noFilter',
                                                                                                                                                                                                          3)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmConfigLogOperStatus.setDescription('The operational status of this log:\n                \n                  disabled  administratively disabled\n                \n                  operational    administratively enabled and working\n                \n                  noFilter  administratively enabled but either\n                            nlmConfigLogFilterName is zero length\n                            or does not name an existing entry in\n                            snmpNotifyFilterTable')
nlmConfigLogStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 6), StorageType()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    nlmConfigLogStorageType.setDescription('The storage type of this conceptual row.')
nlmConfigLogEntryStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 1, 3, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    nlmConfigLogEntryStatus.setDescription("Control for creating and deleting entries.  Entries may be\n                modified while active.\n                \n                For non-null-named logs, the managed system records the security\n                credentials from the request that sets nlmConfigLogStatus\n                to 'active' and uses that identity to apply access control to\n                the objects in the Notification to decide if that Notification\n                may be logged.")
nlmStatsGlobalNotificationsLogged = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 2, 1), Counter32()).setUnits('notifications').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmStatsGlobalNotificationsLogged.setDescription('The number of Notifications put into the nlmLogTable.  This\n                counts a Notification once for each log entry, so a Notification\n                put into multiple logs is counted multiple times.')
nlmStatsGlobalNotificationsBumped = MibScalar((1, 3, 6, 1, 2, 1, 92, 1, 2, 2), Counter32()).setUnits('notifications').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmStatsGlobalNotificationsBumped.setDescription('The number of log entries discarded to make room for a new entry\n                due to lack of resources or the value of nlmConfigGlobalEntryLimit\n                or nlmConfigLogEntryLimit.  This does not include entries discarded\n                due to the value of nlmConfigGlobalAgeOut.')
nlmStatsLogTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 2, 3))
if mibBuilder.loadTexts:
    nlmStatsLogTable.setDescription('A table of Notification log statistics entries.')
nlmStatsLogEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 2, 3, 1))
nlmConfigLogEntry.registerAugmentions(('NOTIFICATION-LOG-MIB', 'nlmStatsLogEntry'))
nlmStatsLogEntry.setIndexNames(*nlmConfigLogEntry.getIndexNames())
if mibBuilder.loadTexts:
    nlmStatsLogEntry.setDescription('A Notification log statistics entry.')
nlmStatsLogNotificationsLogged = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 2, 3, 1,
                                                 1), Counter32()).setUnits('notifications').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmStatsLogNotificationsLogged.setDescription('The number of Notifications put in this named log.')
nlmStatsLogNotificationsBumped = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 2, 3, 1,
                                                 2), Counter32()).setUnits('notifications').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmStatsLogNotificationsBumped.setDescription('The number of log entries discarded from this named log to make\n                room for a new entry due to lack of resources or the value of\n                nlmConfigGlobalEntryLimit or nlmConfigLogEntryLimit.  This does not\n                include entries discarded due to the value of\n                nlmConfigGlobalAgeOut.')
nlmLogTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 3, 1))
if mibBuilder.loadTexts:
    nlmLogTable.setDescription('A table of Notification log entries.\n                \n                It is an implementation-specific matter whether entries in this\n                table are preserved across initializations of the management\n                system.  In general one would expect that they are not.\n                \n                Note that keeping entries across initializations of the\n                management system leads to some confusion with counters and\n                TimeStamps, since both of those are based on sysUpTime, which\n                resets on management initialization.  In this situation,\n                counters apply only after the reset and nlmLogTime for entries\n                made before the reset MUST be set to 0.')
nlmLogEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1)).setIndexNames((0, 'NOTIFICATION-LOG-MIB',
                                                                             'nlmLogName'), (0,
                                                                                             'NOTIFICATION-LOG-MIB',
                                                                                             'nlmLogIndex'))
if mibBuilder.loadTexts:
    nlmLogEntry.setDescription('A Notification log entry.\n                \n                Entries appear in this table when Notifications occur and pass\n                filtering by nlmConfigLogFilterName and access control.  They are\n                removed to make way for new entries due to lack of resources or\n                the values of nlmConfigGlobalEntryLimit, nlmConfigGlobalAgeOut, or\n                nlmConfigLogEntryLimit.\n                \n                If adding an entry would exceed nlmConfigGlobalEntryLimit or system\n                resources in general, the oldest entry in any log SHOULD be removed\n                to make room for the new one.\n                \n                If adding an entry would exceed nlmConfigLogEntryLimit the oldest\n                entry in that log SHOULD be removed to make room for the new one.\n                \n                Before the managed system puts a locally-generated Notification\n                into a non-null-named log it assures that the creator of the log\n                has access to the information in the Notification.  If not it\n                does not log that Notification in that log.')
nlmLogIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    nlmLogIndex.setDescription('A monotonically increasing integer for the sole purpose of\n                indexing entries within the named log.  When it reaches the\n                maximum value, an extremely unlikely event, the agent wraps the\n                value back to 1.')
nlmLogTime = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 2), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogTime.setDescription('The value of sysUpTime when the entry was placed in the log. If\n                the entry occurred before the most recent management system\n                initialization this object value MUST be set to zero.')
nlmLogDateAndTime = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 3), DateAndTime()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogDateAndTime.setDescription('The local date and time when the entry was logged, instantiated\n                only by systems that have date and time capability.')
nlmLogEngineID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 4), SnmpEngineID()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogEngineID.setDescription('The identification of the SNMP engine at which the Notification\n                originated.\n                \n                If the log can contain Notifications from only one engine\n                or the Trap is in SNMPv1 format, this object is a zero-length\n                string.')
nlmLogEngineTAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 5), TAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogEngineTAddress.setDescription('The transport service address of the SNMP engine from which the\n                Notification was received, formatted according to the corresponding\n                value of nlmLogEngineTDomain. This is used to identify the source\n                of an SNMPv1 trap, since an nlmLogEngineId cannot be extracted\n                from the SNMPv1 trap pdu.\n                \n                This object MUST always be instantiated, even if the log\n                can contain Notifications from only one engine.\n                \n                Please be aware that the nlmLogEngineTAddress may not uniquely\n                identify the SNMP engine from which the Notification was received.\n                For example, if an SNMP engine uses DHCP or NAT to obtain\n                ip addresses, the address it uses may be shared with other\n                network devices, and hence will not uniquely identify the\n                SNMP engine.')
nlmLogEngineTDomain = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 6), TDomain()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogEngineTDomain.setDescription('Indicates the kind of transport service by which a Notification\n                was received from an SNMP engine. nlmLogEngineTAddress contains\n                the transport service address of the SNMP engine from which\n                this Notification was received.\n                \n                Possible values for this object are presently found in the\n                Transport Mappings for SNMPv2 document (RFC 1906 [8]).')
nlmLogContextEngineID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 7), SnmpEngineID()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogContextEngineID.setDescription('If the Notification was received in a protocol which has a\n                contextEngineID element like SNMPv3, this object has that value.\n                Otherwise its value is a zero-length string.')
nlmLogContextName = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 8), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogContextName.setDescription('The name of the SNMP MIB context from which the Notification came.\n                For SNMPv1 Traps this is the community string from the Trap.')
nlmLogNotificationID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 1, 1, 9), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogNotificationID.setDescription('The NOTIFICATION-TYPE object identifier of the Notification that\n                occurred.')
nlmLogVariableTable = MibTable((1, 3, 6, 1, 2, 1, 92, 1, 3, 2))
if mibBuilder.loadTexts:
    nlmLogVariableTable.setDescription('A table of variables to go with Notification log entries.')
nlmLogVariableEntry = MibTableRow((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1)).setIndexNames((0,
                                                                                     'NOTIFICATION-LOG-MIB',
                                                                                     'nlmLogName'), (0,
                                                                                                     'NOTIFICATION-LOG-MIB',
                                                                                                     'nlmLogIndex'), (0,
                                                                                                                      'NOTIFICATION-LOG-MIB',
                                                                                                                      'nlmLogVariableIndex'))
if mibBuilder.loadTexts:
    nlmLogVariableEntry.setDescription('A Notification log entry variable.\n                \n                Entries appear in this table when there are variables in\n                the varbind list of a Notification in nlmLogTable.')
nlmLogVariableIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    nlmLogVariableIndex.setDescription('A monotonically increasing integer, starting at 1 for a given\n                nlmLogIndex, for indexing variables within the logged\n                Notification.')
nlmLogVariableID = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 2), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableID.setDescription("The variable's object identifier.")
nlmLogVariableValueType = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9))).clone(namedValues=NamedValues(('counter32',
                                                                                                                                                                                                                   1), ('unsigned32',
                                                                                                                                                                                                                        2), ('timeTicks',
                                                                                                                                                                                                                             3), ('integer32',
                                                                                                                                                                                                                                  4), ('ipAddress',
                                                                                                                                                                                                                                       5), ('octetString',
                                                                                                                                                                                                                                            6), ('objectId',
                                                                                                                                                                                                                                                 7), ('counter64',
                                                                                                                                                                                                                                                      8), ('opaque',
                                                                                                                                                                                                                                                           9)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableValueType.setDescription('The type of the value.  One and only one of the value\n                objects that follow must be instantiated, based on this type.')
nlmLogVariableCounter32Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 4), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableCounter32Val.setDescription("The value when nlmLogVariableType is 'counter32'.")
nlmLogVariableUnsigned32Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 5), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableUnsigned32Val.setDescription("The value when nlmLogVariableType is 'unsigned32'.")
nlmLogVariableTimeTicksVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 6), TimeTicks()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableTimeTicksVal.setDescription("The value when nlmLogVariableType is 'timeTicks'.")
nlmLogVariableInteger32Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 7), Integer32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableInteger32Val.setDescription("The value when nlmLogVariableType is 'integer32'.")
nlmLogVariableOctetStringVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 8), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableOctetStringVal.setDescription("The value when nlmLogVariableType is 'octetString'.")
nlmLogVariableIpAddressVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 9), IpAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableIpAddressVal.setDescription("The value when nlmLogVariableType is 'ipAddress'.\n                Although this seems to be unfriendly for IPv6, we\n                have to recognize that there are a number of older\n                MIBs that do contain an IPv4 format address, known\n                as IpAddress.\n                \n                IPv6 addresses are represented using TAddress or\n                InetAddress, and so the underlying datatype is\n                OCTET STRING, and their value would be stored in\n                the nlmLogVariableOctetStringVal column.")
nlmLogVariableOidVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 10), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableOidVal.setDescription("The value when nlmLogVariableType is 'objectId'.")
nlmLogVariableCounter64Val = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 11), Counter64()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableCounter64Val.setDescription("The value when nlmLogVariableType is 'counter64'.")
nlmLogVariableOpaqueVal = MibTableColumn((1, 3, 6, 1, 2, 1, 92, 1, 3, 2, 1, 12), Opaque()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    nlmLogVariableOpaqueVal.setDescription("The value when nlmLogVariableType is 'opaque'.")
notificationLogMIBConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 3))
notificationLogMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 3, 1))
notificationLogMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 92, 3, 2))
notificationLogMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 92, 3, 1, 1)).setObjects(*(('NOTIFICATION-LOG-MIB', 'notificationLogConfigGroup'), ('NOTIFICATION-LOG-MIB', 'notificationLogStatsGroup'), ('NOTIFICATION-LOG-MIB', 'notificationLogLogGroup')))
if mibBuilder.loadTexts:
    notificationLogMIBCompliance.setDescription('The compliance statement for entities which implement\n                the Notification Log MIB.')
notificationLogConfigGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 1)).setObjects(*(('NOTIFICATION-LOG-MIB', 'nlmConfigGlobalEntryLimit'), ('NOTIFICATION-LOG-MIB', 'nlmConfigGlobalAgeOut'), ('NOTIFICATION-LOG-MIB', 'nlmConfigLogFilterName'), ('NOTIFICATION-LOG-MIB', 'nlmConfigLogEntryLimit'), ('NOTIFICATION-LOG-MIB', 'nlmConfigLogAdminStatus'), ('NOTIFICATION-LOG-MIB', 'nlmConfigLogOperStatus'), ('NOTIFICATION-LOG-MIB', 'nlmConfigLogStorageType'), ('NOTIFICATION-LOG-MIB', 'nlmConfigLogEntryStatus')))
if mibBuilder.loadTexts:
    notificationLogConfigGroup.setDescription('Notification log configuration management.')
notificationLogStatsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 2)).setObjects(*(('NOTIFICATION-LOG-MIB', 'nlmStatsGlobalNotificationsLogged'), ('NOTIFICATION-LOG-MIB', 'nlmStatsGlobalNotificationsBumped'), ('NOTIFICATION-LOG-MIB', 'nlmStatsLogNotificationsLogged'), ('NOTIFICATION-LOG-MIB', 'nlmStatsLogNotificationsBumped')))
if mibBuilder.loadTexts:
    notificationLogStatsGroup.setDescription('Notification log statistics.')
notificationLogLogGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 3)).setObjects(*(('NOTIFICATION-LOG-MIB', 'nlmLogTime'), ('NOTIFICATION-LOG-MIB', 'nlmLogEngineID'), ('NOTIFICATION-LOG-MIB', 'nlmLogEngineTAddress'), ('NOTIFICATION-LOG-MIB', 'nlmLogEngineTDomain'), ('NOTIFICATION-LOG-MIB', 'nlmLogContextEngineID'), ('NOTIFICATION-LOG-MIB', 'nlmLogContextName'), ('NOTIFICATION-LOG-MIB', 'nlmLogNotificationID'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableID'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableValueType'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableCounter32Val'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableUnsigned32Val'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableTimeTicksVal'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableInteger32Val'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableOctetStringVal'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableIpAddressVal'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableOidVal'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableCounter64Val'), ('NOTIFICATION-LOG-MIB', 'nlmLogVariableOpaqueVal')))
if mibBuilder.loadTexts:
    notificationLogLogGroup.setDescription('Notification log data.')
notificationLogDateGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 92, 3, 2, 4)).setObjects(*(('NOTIFICATION-LOG-MIB', 'nlmLogDateAndTime'), ))
if mibBuilder.loadTexts:
    notificationLogDateGroup.setDescription('Conditionally mandatory notification log data.\n                This group is mandatory on systems that keep wall\n                clock date and time and should not be implemented\n                on systems that do not have a wall clock date.')
mibBuilder.exportSymbols('NOTIFICATION-LOG-MIB', nlmStats=nlmStats, notificationLogStatsGroup=notificationLogStatsGroup, notificationLogDateGroup=notificationLogDateGroup, nlmLogVariableOpaqueVal=nlmLogVariableOpaqueVal, nlmStatsLogNotificationsBumped=nlmStatsLogNotificationsBumped, nlmConfigLogTable=nlmConfigLogTable, nlmStatsLogEntry=nlmStatsLogEntry, nlmStatsGlobalNotificationsBumped=nlmStatsGlobalNotificationsBumped, nlmLogEngineTDomain=nlmLogEngineTDomain, nlmLogVariableID=nlmLogVariableID, notificationLogMIBCompliances=notificationLogMIBCompliances, nlmLogVariableEntry=nlmLogVariableEntry, notificationLogLogGroup=notificationLogLogGroup, nlmConfigGlobalEntryLimit=nlmConfigGlobalEntryLimit, nlmLogVariableTimeTicksVal=nlmLogVariableTimeTicksVal, nlmConfigLogAdminStatus=nlmConfigLogAdminStatus, nlmLogVariableCounter64Val=nlmLogVariableCounter64Val, nlmConfigLogEntry=nlmConfigLogEntry, nlmLogTable=nlmLogTable, nlmLogEngineID=nlmLogEngineID, nlmLogVariableOctetStringVal=nlmLogVariableOctetStringVal, nlmLog=nlmLog, PYSNMP_MODULE_ID=notificationLogMIB, nlmLogContextEngineID=nlmLogContextEngineID, nlmConfigLogFilterName=nlmConfigLogFilterName, nlmConfigLogStorageType=nlmConfigLogStorageType, nlmLogIndex=nlmLogIndex, nlmStatsLogTable=nlmStatsLogTable, notificationLogMIB=notificationLogMIB, nlmLogEntry=nlmLogEntry, nlmConfigLogOperStatus=nlmConfigLogOperStatus, notificationLogMIBObjects=notificationLogMIBObjects, nlmLogTime=nlmLogTime, nlmLogVariableOidVal=nlmLogVariableOidVal, notificationLogMIBCompliance=notificationLogMIBCompliance, nlmStatsLogNotificationsLogged=nlmStatsLogNotificationsLogged, nlmConfigLogEntryStatus=nlmConfigLogEntryStatus, nlmLogContextName=nlmLogContextName, nlmLogVariableTable=nlmLogVariableTable, nlmLogVariableCounter32Val=nlmLogVariableCounter32Val, nlmLogVariableIndex=nlmLogVariableIndex, notificationLogMIBGroups=notificationLogMIBGroups, notificationLogConfigGroup=notificationLogConfigGroup, nlmLogVariableInteger32Val=nlmLogVariableInteger32Val, nlmLogVariableValueType=nlmLogVariableValueType, nlmLogNotificationID=nlmLogNotificationID, nlmConfigLogEntryLimit=nlmConfigLogEntryLimit, nlmConfig=nlmConfig, nlmLogVariableIpAddressVal=nlmLogVariableIpAddressVal, nlmLogVariableUnsigned32Val=nlmLogVariableUnsigned32Val, notificationLogMIBConformance=notificationLogMIBConformance, nlmConfigGlobalAgeOut=nlmConfigGlobalAgeOut, nlmStatsGlobalNotificationsLogged=nlmStatsGlobalNotificationsLogged, nlmLogEngineTAddress=nlmLogEngineTAddress, nlmLogName=nlmLogName, nlmLogDateAndTime=nlmLogDateAndTime)