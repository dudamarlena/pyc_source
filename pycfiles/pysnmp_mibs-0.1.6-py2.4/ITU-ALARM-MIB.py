# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/ITU-ALARM-MIB.py
# Compiled at: 2016-02-13 18:19:29
(alarmListName, alarmActiveIndex, alarmActiveDateAndTime, alarmModelIndex) = mibBuilder.importSymbols('ALARM-MIB', 'alarmListName', 'alarmActiveIndex', 'alarmActiveDateAndTime', 'alarmModelIndex')
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ConstraintsUnion, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ConstraintsUnion', 'ValueRangeConstraint')
(IANAItuProbableCause, IANAItuEventType) = mibBuilder.importSymbols('IANA-ITU-ALARM-TC-MIB', 'IANAItuProbableCause', 'IANAItuEventType')
(ItuPerceivedSeverity, ItuTrendIndication) = mibBuilder.importSymbols('ITU-ALARM-TC-MIB', 'ItuPerceivedSeverity', 'ItuTrendIndication')
(ZeroBasedCounter32,) = mibBuilder.importSymbols('RMON2-MIB', 'ZeroBasedCounter32')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(ObjectGroup, NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'NotificationGroup', 'ModuleCompliance')
(MibScalar, MibTable, MibTableRow, MibTableColumn, ObjectIdentity, Gauge32, Counter64, IpAddress, NotificationType, Unsigned32, ModuleIdentity, MibIdentifier, Bits, mib_2, TimeTicks, iso, Integer32, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'ObjectIdentity', 'Gauge32', 'Counter64', 'IpAddress', 'NotificationType', 'Unsigned32', 'ModuleIdentity', 'MibIdentifier', 'Bits', 'mib-2', 'TimeTicks', 'iso', 'Integer32', 'Counter32')
(AutonomousType, TextualConvention, RowPointer, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'AutonomousType', 'TextualConvention', 'RowPointer', 'DisplayString')
ituAlarmMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 121)).setRevisions(('2004-09-09 00:00', ))
if mibBuilder.loadTexts:
    ituAlarmMIB.setLastUpdated('200409090000Z')
if mibBuilder.loadTexts:
    ituAlarmMIB.setOrganization('IETF Distributed Management Working Group')
if mibBuilder.loadTexts:
    ituAlarmMIB.setContactInfo('WG EMail: disman@ietf.org\n           Subscribe: disman-request@ietf.org\n           http://www.ietf.org/html.charters/disman-charter.html\n\n           Chair:     Randy Presuhn\n                      randy_presuhn@mindspring.com\n\n           Editors:   Sharon Chisholm\n                      Nortel Networks\n                      PO Box 3511 Station C\n                      Ottawa, Ont.  K1Y 4H7\n                      Canada\n                      schishol@nortelnetworks.com\n\n                      Dan Romascanu\n                      Avaya\n                      Atidim Technology Park, Bldg. #3\n                      Tel Aviv, 61131\n\n                      Israel\n                      Tel: +972-3-645-8414\n                      Email: dromasca@avaya.com')
if mibBuilder.loadTexts:
    ituAlarmMIB.setDescription('The MIB module describes ITU Alarm information\n              as defined in ITU Recommendation M.3100 [M.3100],\n              X.733 [X.733] and X.736 [X.736].\n\n              Copyright (C) The Internet Society (2004).  The\n              initial version of this MIB module was published\n              in RFC 3877.  For full legal notices see the RFC\n              itself.  Supplementary information may be available on:\n              http://www.ietf.org/copyrights/ianamib.html')
ituAlarmObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 121, 1))
ituAlarmModel = MibIdentifier((1, 3, 6, 1, 2, 1, 121, 1, 1))
ituAlarmActive = MibIdentifier((1, 3, 6, 1, 2, 1, 121, 1, 2))
ituAlarmTable = MibTable((1, 3, 6, 1, 2, 1, 121, 1, 1, 1))
if mibBuilder.loadTexts:
    ituAlarmTable.setDescription('A table of ITU Alarm information for possible alarms\n       on the system.')
ituAlarmEntry = MibTableRow((1, 3, 6, 1, 2, 1, 121, 1, 1, 1, 1)).setIndexNames((0,
                                                                                'ALARM-MIB',
                                                                                'alarmListName'), (0,
                                                                                                   'ALARM-MIB',
                                                                                                   'alarmModelIndex'), (0,
                                                                                                                        'ITU-ALARM-MIB',
                                                                                                                        'ituAlarmPerceivedSeverity'))
if mibBuilder.loadTexts:
    ituAlarmEntry.setDescription('Entries appear in this table whenever an entry is created\n        in the alarmModelTable with a value of alarmModelState in\n        the range from 1 to 6.  Entries disappear from this table\n        whenever the corresponding entries are deleted from the\n        alarmModelTable, including in cases where those entries\n        have been deleted due to local system action.  The value of\n        alarmModelSpecificPointer has no effect on the creation\n        or deletion of entries in this table.  Values of\n        alarmModelState map to values of ituAlarmPerceivedSeverity\n        as follows:\n\n          alarmModelState -> ituAlarmPerceivedSeverity\n                 1        ->         clear (1)\n                 2        ->         indeterminate (2)\n                 3        ->         warning (6)\n                 4        ->         minor (5)\n                 5        ->         major (4)\n                 6        ->         critical (3)\n\n        All other values of alarmModelState MUST NOT appear\n        in this table.\n\n        This table MUST be persistent across system reboots.')
ituAlarmPerceivedSeverity = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 1, 1, 1, 1), ItuPerceivedSeverity())
if mibBuilder.loadTexts:
    ituAlarmPerceivedSeverity.setDescription('ITU perceived severity values.')
ituAlarmEventType = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 1, 1, 1, 2), IANAItuEventType()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    ituAlarmEventType.setDescription('Represents the event type values for the alarms')
ituAlarmProbableCause = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 1, 1, 1, 3), IANAItuProbableCause()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    ituAlarmProbableCause.setDescription('ITU probable cause values.')
ituAlarmAdditionalText = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 1, 1, 1, 4), SnmpAdminString()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    ituAlarmAdditionalText.setDescription('Represents the additional text field for the alarm.')
ituAlarmGenericModel = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 1, 1, 1, 5), RowPointer()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    ituAlarmGenericModel.setDescription('This object points to the corresponding\n    row in the alarmModelTable for this alarm severity.\n\n    This corresponding entry to alarmModelTable could also\n    be derived by performing the reverse of the mapping\n    from alarmModelState to ituAlarmPerceivedSeverity defined\n\n    in the description of ituAlarmEntry to determine the\n    appropriate { alarmListName, alarmModelIndex, alarmModelState }\n    for this { alarmListName, alarmModelIndex,\n    ituAlarmPerceivedSeverity }.')
ituAlarmActiveTable = MibTable((1, 3, 6, 1, 2, 1, 121, 1, 2, 1))
if mibBuilder.loadTexts:
    ituAlarmActiveTable.setDescription('A table of ITU information for active alarms entries.')
ituAlarmActiveEntry = MibTableRow((1, 3, 6, 1, 2, 1, 121, 1, 2, 1, 1)).setIndexNames((0,
                                                                                      'ALARM-MIB',
                                                                                      'alarmListName'), (0,
                                                                                                         'ALARM-MIB',
                                                                                                         'alarmActiveDateAndTime'), (0,
                                                                                                                                     'ALARM-MIB',
                                                                                                                                     'alarmActiveIndex'))
if mibBuilder.loadTexts:
    ituAlarmActiveEntry.setDescription('Entries appear in this table when alarms are active.  They\n       are removed when the alarm is no longer occurring.')
ituAlarmActiveTrendIndication = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 1, 1,
                                                1), ItuTrendIndication()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveTrendIndication.setDescription('Represents the trend indication values for the alarms.')
ituAlarmActiveDetector = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 1, 1, 2), AutonomousType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveDetector.setDescription('Represents the SecurityAlarmDetector object.')
ituAlarmActiveServiceProvider = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 1, 1,
                                                3), AutonomousType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveServiceProvider.setDescription('Represents the ServiceProvider object.')
ituAlarmActiveServiceUser = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 1, 1, 4), AutonomousType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveServiceUser.setDescription('Represents the ServiceUser object.')
ituAlarmActiveStatsTable = MibTable((1, 3, 6, 1, 2, 1, 121, 1, 2, 2))
if mibBuilder.loadTexts:
    ituAlarmActiveStatsTable.setDescription('This table represents the ITU alarm statistics\n         information.')
ituAlarmActiveStatsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 121, 1, 2, 2, 1)).setIndexNames((0,
                                                                                           'ALARM-MIB',
                                                                                           'alarmListName'))
if mibBuilder.loadTexts:
    ituAlarmActiveStatsEntry.setDescription('Statistics on the current active ITU alarms.')
ituAlarmActiveStatsIndeterminateCurrent = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1,
                                                          2, 2, 1, 1), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsIndeterminateCurrent.setDescription('A count of the current number of active alarms with a\n        ituAlarmPerceivedSeverity of indeterminate.')
ituAlarmActiveStatsCriticalCurrent = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2,
                                                     1, 2), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsCriticalCurrent.setDescription('A count of the current number of active alarms with a\n        ituAlarmPerceivedSeverity of critical.')
ituAlarmActiveStatsMajorCurrent = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2, 1,
                                                  3), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsMajorCurrent.setDescription('A count of the current number of active alarms with a\n\n        ituAlarmPerceivedSeverity of major.')
ituAlarmActiveStatsMinorCurrent = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2, 1,
                                                  4), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsMinorCurrent.setDescription('A count of the current number of active alarms with a\n        ituAlarmPerceivedSeverity of minor.')
ituAlarmActiveStatsWarningCurrent = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2,
                                                    1, 5), Gauge32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsWarningCurrent.setDescription('A count of the current number of active alarms with a\n        ituAlarmPerceivedSeverity of warning.')
ituAlarmActiveStatsIndeterminates = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2,
                                                    1, 6), ZeroBasedCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsIndeterminates.setDescription('A count of the total number of active alarms with a\n        ituAlarmPerceivedSeverity of indeterminate since system\n        restart.')
ituAlarmActiveStatsCriticals = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2, 1, 7), ZeroBasedCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsCriticals.setDescription('A count of the total number of active alarms with a\n        ituAlarmPerceivedSeverity of critical since system restart.')
ituAlarmActiveStatsMajors = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2, 1, 8), ZeroBasedCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsMajors.setDescription('A count of the total number of active alarms with a\n        ituAlarmPerceivedSeverity of major since system restart.')
ituAlarmActiveStatsMinors = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2, 1, 9), ZeroBasedCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsMinors.setDescription('A count of the total number of active alarms with a\n        ituAlarmPerceivedSeverity of minor since system restart.')
ituAlarmActiveStatsWarnings = MibTableColumn((1, 3, 6, 1, 2, 1, 121, 1, 2, 2, 1, 10), ZeroBasedCounter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    ituAlarmActiveStatsWarnings.setDescription('A count of the total number of active alarms with a\n        ituAlarmPerceivedSeverity of warning since system restart.')
ituAlarmConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 121, 2))
ituAlarmCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 121, 2, 1))
ituAlarmCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 121, 2, 1, 1)).setObjects(*(('ITU-ALARM-MIB', 'ituAlarmGroup'), ('ITU-ALARM-MIB', 'ituAlarmServiceUserGroup'), ('ITU-ALARM-MIB', 'ituAlarmSecurityGroup'), ('ITU-ALARM-MIB', 'ituAlarmStatisticsGroup')))
if mibBuilder.loadTexts:
    ituAlarmCompliance.setDescription('The compliance statement for systems supporting\n          the ITU Alarm MIB.')
ituAlarmGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 121, 2, 2))
ituAlarmGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 121, 2, 2, 1)).setObjects(*(('ITU-ALARM-MIB', 'ituAlarmEventType'), ('ITU-ALARM-MIB', 'ituAlarmProbableCause'), ('ITU-ALARM-MIB', 'ituAlarmGenericModel')))
if mibBuilder.loadTexts:
    ituAlarmGroup.setDescription('ITU alarm details list group.')
ituAlarmServiceUserGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 121, 2, 2, 2)).setObjects(*(('ITU-ALARM-MIB', 'ituAlarmAdditionalText'), ('ITU-ALARM-MIB', 'ituAlarmActiveTrendIndication')))
if mibBuilder.loadTexts:
    ituAlarmServiceUserGroup.setDescription('The use of these parameters is a service-user option.')
ituAlarmSecurityGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 121, 2, 2, 3)).setObjects(*(('ITU-ALARM-MIB', 'ituAlarmActiveDetector'), ('ITU-ALARM-MIB', 'ituAlarmActiveServiceProvider'), ('ITU-ALARM-MIB', 'ituAlarmActiveServiceUser')))
if mibBuilder.loadTexts:
    ituAlarmSecurityGroup.setDescription('Security Alarm Reporting Function')
ituAlarmStatisticsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 121, 2, 2, 4)).setObjects(*(('ITU-ALARM-MIB', 'ituAlarmActiveStatsIndeterminateCurrent'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsCriticalCurrent'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsMajorCurrent'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsMinorCurrent'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsWarningCurrent'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsIndeterminates'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsCriticals'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsMajors'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsMinors'), ('ITU-ALARM-MIB', 'ituAlarmActiveStatsWarnings')))
if mibBuilder.loadTexts:
    ituAlarmStatisticsGroup.setDescription('ITU Active Alarm Statistics.')
mibBuilder.exportSymbols('ITU-ALARM-MIB', ituAlarmGroups=ituAlarmGroups, ituAlarmActiveTrendIndication=ituAlarmActiveTrendIndication, ituAlarmActive=ituAlarmActive, ituAlarmActiveStatsCriticals=ituAlarmActiveStatsCriticals, ituAlarmActiveStatsMajors=ituAlarmActiveStatsMajors, ituAlarmPerceivedSeverity=ituAlarmPerceivedSeverity, ituAlarmActiveServiceProvider=ituAlarmActiveServiceProvider, ituAlarmActiveStatsWarnings=ituAlarmActiveStatsWarnings, ituAlarmTable=ituAlarmTable, ituAlarmActiveStatsCriticalCurrent=ituAlarmActiveStatsCriticalCurrent, ituAlarmActiveStatsIndeterminates=ituAlarmActiveStatsIndeterminates, ituAlarmServiceUserGroup=ituAlarmServiceUserGroup, ituAlarmObjects=ituAlarmObjects, ituAlarmActiveEntry=ituAlarmActiveEntry, ituAlarmActiveStatsEntry=ituAlarmActiveStatsEntry, ituAlarmModel=ituAlarmModel, ituAlarmActiveStatsMajorCurrent=ituAlarmActiveStatsMajorCurrent, ituAlarmProbableCause=ituAlarmProbableCause, ituAlarmActiveStatsTable=ituAlarmActiveStatsTable, ituAlarmSecurityGroup=ituAlarmSecurityGroup, ituAlarmActiveStatsMinors=ituAlarmActiveStatsMinors, ituAlarmActiveDetector=ituAlarmActiveDetector, ituAlarmConformance=ituAlarmConformance, ituAlarmActiveStatsWarningCurrent=ituAlarmActiveStatsWarningCurrent, PYSNMP_MODULE_ID=ituAlarmMIB, ituAlarmActiveStatsMinorCurrent=ituAlarmActiveStatsMinorCurrent, ituAlarmActiveStatsIndeterminateCurrent=ituAlarmActiveStatsIndeterminateCurrent, ituAlarmActiveServiceUser=ituAlarmActiveServiceUser, ituAlarmStatisticsGroup=ituAlarmStatisticsGroup, ituAlarmGroup=ituAlarmGroup, ituAlarmCompliances=ituAlarmCompliances, ituAlarmMIB=ituAlarmMIB, ituAlarmAdditionalText=ituAlarmAdditionalText, ituAlarmCompliance=ituAlarmCompliance, ituAlarmActiveTable=ituAlarmActiveTable, ituAlarmGenericModel=ituAlarmGenericModel, ituAlarmEntry=ituAlarmEntry, ituAlarmEventType=ituAlarmEventType)