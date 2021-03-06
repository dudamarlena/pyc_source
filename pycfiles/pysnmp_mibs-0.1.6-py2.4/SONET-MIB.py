# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/SONET-MIB.py
# Compiled at: 2016-02-13 18:12:12
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsUnion, ValueSizeConstraint, ConstraintsIntersection, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueSizeConstraint', 'ConstraintsIntersection', 'ValueRangeConstraint')
(ifIndex,) = mibBuilder.importSymbols('IF-MIB', 'ifIndex')
(PerfCurrentCount, PerfIntervalCount) = mibBuilder.importSymbols('PerfHist-TC-MIB', 'PerfCurrentCount', 'PerfIntervalCount')
(ObjectGroup, ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'ModuleCompliance', 'NotificationGroup')
(Integer32, ModuleIdentity, Gauge32, Unsigned32, Bits, NotificationType, iso, transmission, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64, MibIdentifier, IpAddress, Counter32, ObjectIdentity, TimeTicks) = mibBuilder.importSymbols('SNMPv2-SMI', 'Integer32', 'ModuleIdentity', 'Gauge32', 'Unsigned32', 'Bits', 'NotificationType', 'iso', 'transmission', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64', 'MibIdentifier', 'IpAddress', 'Counter32', 'ObjectIdentity', 'TimeTicks')
(TruthValue, TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TruthValue', 'TextualConvention', 'DisplayString')
sonetMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 39)).setRevisions(('2003-08-11 00:00',
                                                                    '1998-10-19 00:00',
                                                                    '1994-01-03 00:00'))
if mibBuilder.loadTexts:
    sonetMIB.setLastUpdated('200308110000Z')
if mibBuilder.loadTexts:
    sonetMIB.setOrganization('IETF AToM MIB Working Group')
if mibBuilder.loadTexts:
    sonetMIB.setContactInfo('WG charter:\n            http://www.ietf.org/html.charters/atommib-charter.html\n\n          Mailing Lists:\n            General Discussion: atommib@research.telcordia.com\n            To Subscribe: atommib-request@research.telcordia.com\n\n          Kaj Tesink\n          Telcordia Technologies\n          Tel: (732) 758-5254\n          Fax: (732) 758-2269\n          E-mail: kaj@research.telcordia.com.')
if mibBuilder.loadTexts:
    sonetMIB.setDescription('The MIB module to describe SONET/SDH interface objects.\n\n          Copyright (C) The Internet Society (2003).  This version\n          of this MIB module is part of RFC 3592;  see the RFC\n          itself for full legal notices.')
sonetObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 1))
sonetObjectsPath = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 2))
sonetObjectsVT = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 3))
sonetMedium = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 1, 1))
sonetSection = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 1, 2))
sonetLine = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 1, 3))
sonetFarEndLine = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 1, 4))
sonetPath = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 2, 1))
sonetFarEndPath = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 2, 2))
sonetVT = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 3, 1))
sonetFarEndVT = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 3, 2))
sonetMediumTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1))
if mibBuilder.loadTexts:
    sonetMediumTable.setDescription('The SONET/SDH Medium table.')
sonetMediumEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1)).setIndexNames((0,
                                                                                      'IF-MIB',
                                                                                      'ifIndex'))
if mibBuilder.loadTexts:
    sonetMediumEntry.setDescription('An entry in the SONET/SDH Medium table.')
sonetMediumType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('sonet',
                                                                                                                                                                                          1), ('sdh',
                                                                                                                                                                                               2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetMediumType.setDescription('This variable identifies whether a SONET\n          or a SDH signal is used across this interface.')
sonetMediumTimeElapsed = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 900))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetMediumTimeElapsed.setDescription("The number of seconds, including partial seconds,\n          that have elapsed since the beginning of the current\n          measurement period. If, for some reason, such as an\n          adjustment in the system's time-of-day clock, the\n          current interval exceeds the maximum value, the\n          agent will return the maximum value.")
sonetMediumValidIntervals = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetMediumValidIntervals.setDescription('The number of previous 15-minute intervals\n          for which data was collected.\n          A SONET/SDH interface must be capable\n          of supporting at least n intervals.\n          The minimum value of n is 4.\n          The default of n is 32.\n          The maximum value of n is 96.\n          The value will be <n> unless the measurement was\n          (re-)started within the last (<n>*15) minutes, in which\n          case the value will be the number of complete 15\n          minute intervals for which the agent has at least\n          some data. In certain cases (e.g., in the case\n          where the agent is a proxy) it is possible that some\n          intervals are unavailable.  In this case, this\n          interval is the maximum interval number for\n          which data is available. ')
sonetMediumLineCoding = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('sonetMediumOther',
                                                                                                                                                                                                         1), ('sonetMediumB3ZS',
                                                                                                                                                                                                              2), ('sonetMediumCMI',
                                                                                                                                                                                                                   3), ('sonetMediumNRZ',
                                                                                                                                                                                                                        4), ('sonetMediumRZ',
                                                                                                                                                                                                                             5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetMediumLineCoding.setDescription('This variable describes the line coding for\n          this interface. The B3ZS and CMI are used for\n          electrical SONET/SDH signals (STS-1 and STS-3).\n          The Non-Return to Zero (NRZ) and the Return\n          to Zero are used for optical SONET/SDH signals.')
sonetMediumLineType = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('sonetOther',
                                                                                                                                                                                                          1), ('sonetShortSingleMode',
                                                                                                                                                                                                               2), ('sonetLongSingleMode',
                                                                                                                                                                                                                    3), ('sonetMultiMode',
                                                                                                                                                                                                                         4), ('sonetCoax',
                                                                                                                                                                                                                              5), ('sonetUTP',
                                                                                                                                                                                                                                   6)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetMediumLineType.setDescription('This variable describes the line type for\n          this interface. The line types are\n          Short and Long Range\n          Single Mode fiber or Multi-Mode fiber interfaces,\n          and coax and UTP for electrical interfaces.  The\n          value sonetOther should be used when the Line Type is\n          not one of the listed values.')
sonetMediumCircuitIdentifier = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1,
                                               6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 255))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetMediumCircuitIdentifier.setDescription("This variable contains the transmission\n          vendor's circuit identifier, for the\n          purpose of facilitating troubleshooting.\n          Note that the circuit identifier, if available,\n          is also represented by ifPhysAddress.")
sonetMediumInvalidIntervals = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1,
                                              7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 96))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetMediumInvalidIntervals.setDescription('The number of intervals in the range from\n           0 to sonetMediumValidIntervals for which no\n           data is available. This object will typically\n           be zero except in cases where the data for some\n           intervals are not available (e.g., in proxy\n           situations).')
sonetMediumLoopbackConfig = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 1, 1, 8), Bits().clone(namedValues=NamedValues(('sonetNoLoop',
                                                                                                                            0), ('sonetFacilityLoop',
                                                                                                                                 1), ('sonetTerminalLoop',
                                                                                                                                      2), ('sonetOtherLoop',
                                                                                                                                           3)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetMediumLoopbackConfig.setDescription('The current loopback state of the SONET/SDH interface.  The\n           values mean:\n\n             sonetNoLoop\n                Not in the loopback state. A device that is not\n                capable of performing a loopback on this interface\n                shall always return this value.\n\n             sonetFacilityLoop\n                The received signal at this interface is looped back\n                out through the corresponding transmitter in the return\n                direction.\n\n             sonetTerminalLoop\n                The signal that is about to be transmitted is connected\n                to the associated incoming receiver.\n\n             sonetOtherLoop\n                Loopbacks that are not defined here.')
sonetSESthresholdSet = MibScalar((1, 3, 6, 1, 2, 1, 10, 39, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('other',
                                                                                                                                                                                             1), ('bellcore1991',
                                                                                                                                                                                                  2), ('ansi1993',
                                                                                                                                                                                                       3), ('itu1995',
                                                                                                                                                                                                            4), ('ansi1997',
                                                                                                                                                                                                                 5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetSESthresholdSet.setDescription('An enumerated integer indicating which\n          recognized set of SES thresholds that\n          the agent uses for determining severely\n          errored seconds and unavailable time.\n\n          other(1)\n            None of the following.\n\n          bellcore1991(2)\n            Bellcore TR-NWT-000253, 1991 [TR253], or\n            ANSI T1M1.3/93-005R2, 1993 [T1M1.3].\n            See also Appendix B.\n\n          ansi1993(3)\n            ANSI T1.231, 1993 [T1.231a], or\n            Bellcore GR-253-CORE, Issue 2, 1995 [GR253]\n\n          itu1995(4)\n            ITU Recommendation G.826, 1995 [G.826]\n\n          ansi1997(5)\n            ANSI T1.231, 1997 [T1.231b]\n\n          If a manager changes the value of this\n          object then the SES statistics collected\n          prior to this change must be invalidated.')
sonetSectionCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 1))
if mibBuilder.loadTexts:
    sonetSectionCurrentTable.setDescription('The SONET/SDH Section Current table.')
sonetSectionCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 1, 1)).setIndexNames((0,
                                                                                              'IF-MIB',
                                                                                              'ifIndex'))
if mibBuilder.loadTexts:
    sonetSectionCurrentEntry.setDescription('An entry in the SONET/SDH Section Current table.')
sonetSectionCurrentStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 6))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionCurrentStatus.setDescription('This variable indicates the\n          status of the interface.\n          The sonetSectionCurrentStatus\n          is a bit map represented\n          as a sum, therefore,\n          it can represent multiple defects\n          simultaneously.\n          The sonetSectionNoDefect should be\n          set if and only if\n          no other flag is set.\n\n          The various bit positions are:\n                1   sonetSectionNoDefect\n                2   sonetSectionLOS\n                4   sonetSectionLOF')
sonetSectionCurrentESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 1, 1, 2), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionCurrentESs.setDescription('The counter associated with the number of Errored\n          Seconds encountered by a SONET/SDH\n          Section in the current 15 minute interval.')
sonetSectionCurrentSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 1, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionCurrentSESs.setDescription('The counter associated with the number of\n          Severely Errored Seconds\n          encountered by a SONET/SDH Section in the current 15\n          minute interval.')
sonetSectionCurrentSEFSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 1, 1, 4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionCurrentSEFSs.setDescription('The counter associated with the number of\n          Severely Errored Framing Seconds\n          encountered by a SONET/SDH Section in the current\n          15 minute interval.')
sonetSectionCurrentCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 1, 1, 5), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionCurrentCVs.setDescription('The counter associated with the number of Coding\n          Violations encountered by a\n          SONET/SDH Section in the current 15 minute interval.')
sonetSectionIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2))
if mibBuilder.loadTexts:
    sonetSectionIntervalTable.setDescription('The SONET/SDH Section Interval table.')
sonetSectionIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2, 1)).setIndexNames((0,
                                                                                               'IF-MIB',
                                                                                               'ifIndex'), (0,
                                                                                                            'SONET-MIB',
                                                                                                            'sonetSectionIntervalNumber'))
if mibBuilder.loadTexts:
    sonetSectionIntervalEntry.setDescription('An entry in the SONET/SDH Section Interval table.')
sonetSectionIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2, 1,
                                             1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96)))
if mibBuilder.loadTexts:
    sonetSectionIntervalNumber.setDescription('A number between 1 and 96, which identifies the\n         interval for which the set of statistics is available.\n         The interval identified by 1 is the most recently\n         completed 15 minute interval,\n         and the interval identified\n         by N is the interval immediately preceding the\n         one identified\n         by N-1.')
sonetSectionIntervalESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2, 1, 2), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionIntervalESs.setDescription('The counter associated with the number of\n          Errored Seconds encountered\n          by a SONET/SDH Section in a\n          particular 15-minute interval\n          in the past 24 hours.')
sonetSectionIntervalSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2, 1, 3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionIntervalSESs.setDescription('The counter associated with the number of\n          Severely Errored Seconds\n          encountered by a SONET/SDH Section in a\n          particular 15-minute interval\n          in the past 24 hours.')
sonetSectionIntervalSEFSs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2, 1, 4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionIntervalSEFSs.setDescription('The counter associated with the number of\n          Severely Errored Framing Seconds\n          encountered by a SONET/SDH Section in a\n          particular 15-minute interval\n          in the past 24 hours.')
sonetSectionIntervalCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2, 1, 5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionIntervalCVs.setDescription('The counter associated with the number of Coding\n          Violations encountered by a\n          SONET/SDH Section in a particular 15-minute interval\n          in the past 24 hours.')
sonetSectionIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 2, 2,
                                                1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetSectionIntervalValidData.setDescription('This variable indicates if the data for this\n           interval is valid.')
sonetLineCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 1))
if mibBuilder.loadTexts:
    sonetLineCurrentTable.setDescription('The SONET/SDH Line Current table.')
sonetLineCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 1, 1)).setIndexNames((0,
                                                                                           'IF-MIB',
                                                                                           'ifIndex'))
if mibBuilder.loadTexts:
    sonetLineCurrentEntry.setDescription('An entry in the SONET/SDH Line Current table.')
sonetLineCurrentStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 6))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineCurrentStatus.setDescription('This variable indicates the\n          status of the interface.\n          The sonetLineCurrentStatus\n          is a bit map represented\n          as a sum, therefore,\n          it can represent multiple defects\n          simultaneously.\n          The sonetLineNoDefect should be\n          set if and only if\n          no other flag is set.\n\n          The various bit positions are:\n           1   sonetLineNoDefect\n           2   sonetLineAIS\n           4   sonetLineRDI')
sonetLineCurrentESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 1, 1, 2), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineCurrentESs.setDescription('The counter associated with the number of Errored\n        Seconds encountered by a SONET/SDH\n        Line in the current 15 minute interval.')
sonetLineCurrentSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 1, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineCurrentSESs.setDescription('The counter associated with the number of\n        Severely Errored Seconds\n        encountered by a SONET/SDH Line in the current 15\n        minute\n        interval.')
sonetLineCurrentCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 1, 1, 4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineCurrentCVs.setDescription('The counter associated with the number of Coding\n        Violations encountered by a\n        SONET/SDH Line in the current 15 minute interval.')
sonetLineCurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 1, 1, 5), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineCurrentUASs.setDescription('The counter associated with the number of\n        Unavailable Seconds\n        encountered by a SONET/SDH Line in the current 15\n        minute\n        interval.')
sonetLineIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2))
if mibBuilder.loadTexts:
    sonetLineIntervalTable.setDescription('The SONET/SDH Line Interval table.')
sonetLineIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2, 1)).setIndexNames((0,
                                                                                            'IF-MIB',
                                                                                            'ifIndex'), (0,
                                                                                                         'SONET-MIB',
                                                                                                         'sonetLineIntervalNumber'))
if mibBuilder.loadTexts:
    sonetLineIntervalEntry.setDescription('An entry in the SONET/SDH Line Interval table.')
sonetLineIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96)))
if mibBuilder.loadTexts:
    sonetLineIntervalNumber.setDescription('A number between 1 and 96, which identifies the\n           interval for which the set of statistics is available.\n           The interval identified by 1 is the most recently\n           completed 15 minute interval,\n           and the interval identified\n           by N is the interval immediately preceding the\n           one identified\n           by N-1.')
sonetLineIntervalESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2, 1, 2), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineIntervalESs.setDescription('The counter associated with the number of\n          Errored Seconds encountered\n          by a SONET/SDH Line in a\n          particular 15-minute interval\n          in the past 24 hours.')
sonetLineIntervalSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2, 1, 3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineIntervalSESs.setDescription('The counter associated with the number of\n          Severely Errored Seconds\n          encountered by a SONET/SDH Line in a\n          particular 15-minute interval\n          in the past 24 hours.')
sonetLineIntervalCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2, 1, 4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineIntervalCVs.setDescription('The counter associated with the number of Coding\n         Violations encountered by a\n         SONET/SDH Line in a\n         particular 15-minute interval\n         in the past 24 hours.')
sonetLineIntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2, 1, 5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineIntervalUASs.setDescription('The counter associated with the\n         number of Unavailable Seconds\n         encountered by a SONET/SDH Line in\n         a particular 15-minute interval\n         in the past 24 hours.')
sonetLineIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 3, 2, 1,
                                             6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetLineIntervalValidData.setDescription('This variable indicates if the data for this\n           interval is valid.')
sonetFarEndLineCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 1))
if mibBuilder.loadTexts:
    sonetFarEndLineCurrentTable.setDescription('The SONET/SDH Far End Line Current table.')
sonetFarEndLineCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 1, 1)).setIndexNames((0,
                                                                                                 'IF-MIB',
                                                                                                 'ifIndex'))
if mibBuilder.loadTexts:
    sonetFarEndLineCurrentEntry.setDescription('An entry in the SONET/SDH Far End Line Current table.')
sonetFarEndLineCurrentESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 1, 1, 1), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineCurrentESs.setDescription('The counter associated with the number of Far\n          End Errored Seconds encountered by a SONET/SDH\n          interface in the current 15 minute interval.')
sonetFarEndLineCurrentSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 1, 1,
                                             2), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineCurrentSESs.setDescription('The counter associated with the number of\n          Far End Severely Errored Seconds\n          encountered by a SONET/SDH Medium/Section/Line\n          interface in the current 15 minute\n          interval.')
sonetFarEndLineCurrentCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 1, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineCurrentCVs.setDescription('The counter associated with the number of\n          Far End Coding Violations reported via\n          the far end block error count\n          encountered by a\n          SONET/SDH Medium/Section/Line\n          interface in the current 15 minute interval.')
sonetFarEndLineCurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 1, 1,
                                             4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineCurrentUASs.setDescription('The counter associated with the number of\n          Far End Unavailable Seconds\n          encountered by a\n          SONET/SDH Medium/Section/Line\n          interface in the current 15 minute interval.')
sonetFarEndLineIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 2))
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalTable.setDescription('The SONET/SDH Far End Line Interval table.')
sonetFarEndLineIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 2, 1)).setIndexNames((0,
                                                                                                  'IF-MIB',
                                                                                                  'ifIndex'), (0,
                                                                                                               'SONET-MIB',
                                                                                                               'sonetFarEndLineIntervalNumber'))
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalEntry.setDescription('An entry in the SONET/SDH Far\n        End Line Interval table.')
sonetFarEndLineIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 2,
                                                1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96)))
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalNumber.setDescription('A number between 1 and 96, which identifies the\n            interval for which the set of statistics is available.\n            The interval identified by 1 is the most recently\n            completed 15 minute interval,\n            and the interval identified\n            by N is the interval immediately preceding the\n            one identified\n            by N-1.')
sonetFarEndLineIntervalESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 2, 1,
                                             2), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalESs.setDescription('The counter associated with the number of\n           Far End Errored Seconds encountered\n           by a SONET/SDH Line\n           interface in a particular 15-minute interval\n           in the past 24 hours.')
sonetFarEndLineIntervalSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 2, 1,
                                              3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalSESs.setDescription('The counter associated with the number of\n           Far End Severely Errored Seconds\n           encountered by a SONET/SDH Line\n           interface in a particular 15-minute interval\n           in the past 24 hours.')
sonetFarEndLineIntervalCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 2, 1,
                                             4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalCVs.setDescription('The counter associated with the number of\n            Far End Coding Violations reported via\n            the far end block error count\n            encountered by a\n            SONET/SDH Line\n            interface in a particular 15-minute interval\n            in the past 24 hours.')
sonetFarEndLineIntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4, 2, 1,
                                              5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalUASs.setDescription('The counter associated with the number of\n          Far End Unavailable Seconds\n          encountered by a\n          SONET/SDH Line\n          interface in a particular 15-minute interval\n          in the past 24 hours.')
sonetFarEndLineIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 1, 4,
                                                   2, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndLineIntervalValidData.setDescription('This variable indicates if the data for this\n           interval is valid.')
sonetPathCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1))
if mibBuilder.loadTexts:
    sonetPathCurrentTable.setDescription('The SONET/SDH Path Current table.')
sonetPathCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1, 1)).setIndexNames((0,
                                                                                           'IF-MIB',
                                                                                           'ifIndex'))
if mibBuilder.loadTexts:
    sonetPathCurrentEntry.setDescription('An entry in the SONET/SDH Path Current table.')
sonetPathCurrentWidth = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7))).clone(namedValues=NamedValues(('sts1',
                                                                                                                                                                                                               1), ('sts3cSTM1',
                                                                                                                                                                                                                    2), ('sts12cSTM4',
                                                                                                                                                                                                                         3), ('sts24c',
                                                                                                                                                                                                                              4), ('sts48cSTM16',
                                                                                                                                                                                                                                   5), ('sts192cSTM64',
                                                                                                                                                                                                                                        6), ('sts768cSTM256',
                                                                                                                                                                                                                                             7)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetPathCurrentWidth.setDescription('A value that indicates the type of the SONET/SDH\n        Path.  For SONET, the assigned types are\n        the STS-Nc SPEs, where N = 1, 3, 12, 24, 48, 192 and 768.\n        STS-1 is equal to 51.84 Mbps.  For SDH, the assigned\n        types are the STM-Nc VCs, where N = 1, 4, 16, 64 and 256.')
sonetPathCurrentStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 62))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathCurrentStatus.setDescription('This variable indicates the\n         status of the interface.\n         The sonetPathCurrentStatus\n         is a bit map represented\n         as a sum, therefore,\n         it can represent multiple defects\n         simultaneously.\n         The sonetPathNoDefect should be\n         set if and only if\n         no other flag is set.\n\n         The various bit positions are:\n            1   sonetPathNoDefect\n            2   sonetPathSTSLOP\n            4   sonetPathSTSAIS\n            8   sonetPathSTSRDI\n           16   sonetPathUnequipped\n           32   sonetPathSignalLabelMismatch')
sonetPathCurrentESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathCurrentESs.setDescription('The counter associated with the number of Errored\n        Seconds encountered by a SONET/SDH\n        Path in the current 15 minute interval.')
sonetPathCurrentSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1, 1, 4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathCurrentSESs.setDescription('The counter associated with the number of\n        Severely Errored Seconds\n        encountered by a SONET/SDH Path in the current 15\n        minute\n        interval.')
sonetPathCurrentCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1, 1, 5), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathCurrentCVs.setDescription('The counter associated with the number of Coding\n        Violations encountered by a\n        SONET/SDH Path in the current 15 minute interval.')
sonetPathCurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 1, 1, 6), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathCurrentUASs.setDescription('The counter associated with the number of\n        Unavailable Seconds\n        encountered by a Path in the current\n        15 minute interval.')
sonetPathIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2))
if mibBuilder.loadTexts:
    sonetPathIntervalTable.setDescription('The SONET/SDH Path Interval table.')
sonetPathIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2, 1)).setIndexNames((0,
                                                                                            'IF-MIB',
                                                                                            'ifIndex'), (0,
                                                                                                         'SONET-MIB',
                                                                                                         'sonetPathIntervalNumber'))
if mibBuilder.loadTexts:
    sonetPathIntervalEntry.setDescription('An entry in the SONET/SDH Path Interval table.')
sonetPathIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96)))
if mibBuilder.loadTexts:
    sonetPathIntervalNumber.setDescription('A number between 1 and 96, which identifies the\n          interval for which the set of statistics is available.\n          The interval identified by 1 is the most recently\n          completed 15 minute interval,\n          and the interval identified\n          by N is the interval immediately preceding the\n          one identified\n          by N-1.')
sonetPathIntervalESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2, 1, 2), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathIntervalESs.setDescription('The counter associated with the number of\n        Errored Seconds encountered\n        by a SONET/SDH Path in a\n        particular 15-minute interval\n        in the past 24 hours.')
sonetPathIntervalSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2, 1, 3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathIntervalSESs.setDescription('The counter associated with the number of\n        Severely Errored Seconds\n        encountered by a SONET/SDH Path in\n        a particular 15-minute interval\n        in the past 24 hours.')
sonetPathIntervalCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2, 1, 4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathIntervalCVs.setDescription('The counter associated with the number of Coding\n        Violations encountered by a\n        SONET/SDH Path in a particular 15-minute interval\n        in the past 24 hours.')
sonetPathIntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2, 1, 5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathIntervalUASs.setDescription('The counter associated with the number of\n        Unavailable Seconds\n        encountered by a Path in a\n        particular 15-minute interval\n        in the past 24 hours.')
sonetPathIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 1, 2, 1,
                                             6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetPathIntervalValidData.setDescription('This variable indicates if the data for this\n           interval is valid.')
sonetFarEndPathCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 1))
if mibBuilder.loadTexts:
    sonetFarEndPathCurrentTable.setDescription('The SONET/SDH Far End Path Current table.')
sonetFarEndPathCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 1, 1)).setIndexNames((0,
                                                                                                 'IF-MIB',
                                                                                                 'ifIndex'))
if mibBuilder.loadTexts:
    sonetFarEndPathCurrentEntry.setDescription('An entry in the SONET/SDH Far End Path Current table.')
sonetFarEndPathCurrentESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 1, 1, 1), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathCurrentESs.setDescription('The counter associated with the number of Far\n            End Errored Seconds encountered by a SONET/SDH\n            interface in the current 15 minute interval.')
sonetFarEndPathCurrentSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 1, 1,
                                             2), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathCurrentSESs.setDescription('The counter associated with the number of\n            Far End Severely Errored Seconds\n            encountered by a SONET/SDH Path\n            interface in the current 15 minute\n            interval.')
sonetFarEndPathCurrentCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 1, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathCurrentCVs.setDescription('The counter associated with the number of\n            Far End Coding Violations reported via\n            the far end block error count\n            encountered by a\n            SONET/SDH Path interface in\n            the current 15 minute interval.')
sonetFarEndPathCurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 1, 1,
                                             4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathCurrentUASs.setDescription('The counter associated with the number of\n          Far End Unavailable Seconds\n          encountered by a\n          SONET/SDH Path interface in\n          the current 15 minute interval.')
sonetFarEndPathIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 2))
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalTable.setDescription('The SONET/SDH Far End Path Interval table.')
sonetFarEndPathIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 2, 1)).setIndexNames((0,
                                                                                                  'IF-MIB',
                                                                                                  'ifIndex'), (0,
                                                                                                               'SONET-MIB',
                                                                                                               'sonetFarEndPathIntervalNumber'))
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalEntry.setDescription('An entry in the SONET/SDH Far\n          End Path Interval table.')
sonetFarEndPathIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 2,
                                                1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96)))
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalNumber.setDescription('A number between 1 and 96, which identifies the\n           interval for which the set of statistics is available.\n           The interval identified by 1 is the most recently\n           completed 15 minute interval,\n           and the interval identified\n           by N is the interval immediately preceding the\n           one identified\n           by N-1.')
sonetFarEndPathIntervalESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 2, 1,
                                             2), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalESs.setDescription('The counter associated with the number of\n           Far End Errored Seconds encountered\n           by a SONET/SDH Path interface in a\n           particular 15-minute interval\n           in the past 24 hours.')
sonetFarEndPathIntervalSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 2, 1,
                                              3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalSESs.setDescription('The counter associated with the number of\n           Far End Severely Errored Seconds\n           encountered by a SONET/SDH Path interface\n           in a particular 15-minute interval\n           in the past 24 hours.')
sonetFarEndPathIntervalCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 2, 1,
                                             4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalCVs.setDescription('The counter associated with the number of\n            Far End Coding Violations reported via\n            the far end block error count\n            encountered by a\n            SONET/SDH Path interface\n            in a particular 15-minute interval\n            in the past 24 hours.')
sonetFarEndPathIntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2, 2, 1,
                                              5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalUASs.setDescription('The counter associated with the number of\n          Far End Unavailable Seconds\n          encountered by a\n          SONET/SDH Path interface in\n          a particular 15-minute interval\n          in the past 24 hours.')
sonetFarEndPathIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 2, 2,
                                                   2, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndPathIntervalValidData.setDescription('This variable indicates if the data for this\n           interval is valid.')
sonetVTCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1))
if mibBuilder.loadTexts:
    sonetVTCurrentTable.setDescription('The SONET/SDH VT Current table.')
sonetVTCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1, 1)).setIndexNames((0,
                                                                                         'IF-MIB',
                                                                                         'ifIndex'))
if mibBuilder.loadTexts:
    sonetVTCurrentEntry.setDescription('An entry in the SONET/SDH VT Current table.')
sonetVTCurrentWidth = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))).clone(namedValues=NamedValues(('vtWidth15VC11',
                                                                                                                                                                                                       1), ('vtWidth2VC12',
                                                                                                                                                                                                            2), ('vtWidth3',
                                                                                                                                                                                                                 3), ('vtWidth6VC2',
                                                                                                                                                                                                                      4), ('vtWidth6c',
                                                                                                                                                                                                                           5)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sonetVTCurrentWidth.setDescription('A value that indicates the type of the SONET\n        VT and SDH VC.  Assigned widths are\n        VT1.5/VC11, VT2/VC12, VT3, VT6/VC2, and VT6c.')
sonetVTCurrentStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 126))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTCurrentStatus.setDescription('This variable indicates the\n         status of the interface.\n         The sonetVTCurrentStatus\n         is a bit map represented\n         as a sum, therefore,\n         it can represent multiple defects\n         and failures\n         simultaneously.\n         The sonetVTNoDefect should be\n         set if and only if\n         no other flag is set.\n\n         The various bit positions are:\n            1   sonetVTNoDefect\n            2   sonetVTLOP\n            4   sonetVTPathAIS\n            8   sonetVTPathRDI\n           16   sonetVTPathRFI\n           32   sonetVTUnequipped\n           64   sonetVTSignalLabelMismatch')
sonetVTCurrentESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTCurrentESs.setDescription('The counter associated with the number of Errored\n        Seconds encountered by a SONET/SDH\n        VT in the current 15 minute interval.')
sonetVTCurrentSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1, 1, 4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTCurrentSESs.setDescription('The counter associated with the number of\n        Severely Errored Seconds\n        encountered by a SONET/SDH VT in the current 15 minute\n        interval.')
sonetVTCurrentCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1, 1, 5), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTCurrentCVs.setDescription('The counter associated with the number of Coding\n        Violations encountered by a\n        SONET/SDH VT in the current 15 minute interval.')
sonetVTCurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 1, 1, 6), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTCurrentUASs.setDescription('The counter associated with the number of\n        Unavailable Seconds\n        encountered by a VT in the current\n        15 minute interval.')
sonetVTIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2))
if mibBuilder.loadTexts:
    sonetVTIntervalTable.setDescription('The SONET/SDH VT Interval table.')
sonetVTIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2, 1)).setIndexNames((0,
                                                                                          'IF-MIB',
                                                                                          'ifIndex'), (0,
                                                                                                       'SONET-MIB',
                                                                                                       'sonetVTIntervalNumber'))
if mibBuilder.loadTexts:
    sonetVTIntervalEntry.setDescription('An entry in the SONET/SDH VT Interval table.')
sonetVTIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96)))
if mibBuilder.loadTexts:
    sonetVTIntervalNumber.setDescription('A number between 1 and 96, which identifies the\n         interval for which the set of statistics is available.\n         The interval identified by 1 is the most recently\n         completed 15 minute interval,\n         and the interval identified\n         by N is the interval immediately preceding the\n         one identified\n         by N-1.')
sonetVTIntervalESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2, 1, 2), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTIntervalESs.setDescription('The counter associated with the number of\n        Errored Seconds encountered\n        by a SONET/SDH VT in a particular 15-minute interval\n        in the past 24 hours.')
sonetVTIntervalSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2, 1, 3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTIntervalSESs.setDescription('The counter associated with the number of\n        Severely Errored Seconds\n        encountered by a SONET/SDH VT\n        in a particular 15-minute interval\n        in the past 24 hours.')
sonetVTIntervalCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2, 1, 4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTIntervalCVs.setDescription('The counter associated with the number of Coding\n        Violations encountered by a\n        SONET/SDH VT in a particular 15-minute interval\n        in the past 24 hours.')
sonetVTIntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2, 1, 5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTIntervalUASs.setDescription('The counter associated with the number of\n        Unavailable Seconds\n        encountered by a VT in a particular 15-minute interval\n        in the past 24 hours.')
sonetVTIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 1, 2, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetVTIntervalValidData.setDescription('This variable indicates if the data for this\n           interval is valid.')
sonetFarEndVTCurrentTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 1))
if mibBuilder.loadTexts:
    sonetFarEndVTCurrentTable.setDescription('The SONET/SDH Far End VT Current table.')
sonetFarEndVTCurrentEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 1, 1)).setIndexNames((0,
                                                                                               'IF-MIB',
                                                                                               'ifIndex'))
if mibBuilder.loadTexts:
    sonetFarEndVTCurrentEntry.setDescription('An entry in the SONET/SDH Far End VT Current table.')
sonetFarEndVTCurrentESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 1, 1, 1), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTCurrentESs.setDescription('The counter associated with the number of Far\n           End Errored Seconds encountered by a SONET/SDH\n           interface in the current 15 minute interval.')
sonetFarEndVTCurrentSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 1, 1, 2), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTCurrentSESs.setDescription('The counter associated with the number of\n           Far End Severely Errored Seconds\n           encountered by a SONET/SDH VT interface\n           in the current 15 minute\n           interval.')
sonetFarEndVTCurrentCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 1, 1, 3), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTCurrentCVs.setDescription('The counter associated with the number of\n           Far End Coding Violations reported via\n           the far end block error count\n           encountered by a\n           SONET/SDH VT interface\n           in the current 15 minute interval.')
sonetFarEndVTCurrentUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 1, 1, 4), PerfCurrentCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTCurrentUASs.setDescription('The counter associated with the number of\n         Far End Unavailable Seconds\n         encountered by a\n         SONET/SDH VT interface\n         in the current 15 minute interval.')
sonetFarEndVTIntervalTable = MibTable((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2))
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalTable.setDescription('The SONET/SDH Far End VT Interval table.')
sonetFarEndVTIntervalEntry = MibTableRow((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2, 1)).setIndexNames((0,
                                                                                                'IF-MIB',
                                                                                                'ifIndex'), (0,
                                                                                                             'SONET-MIB',
                                                                                                             'sonetFarEndVTIntervalNumber'))
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalEntry.setDescription('An entry in the SONET/SDH Far\n         End VT Interval table.')
sonetFarEndVTIntervalNumber = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2, 1,
                                              1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 96)))
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalNumber.setDescription('A number between 1 and 96, which identifies the\n          interval for which the set of statistics is available.\n          The interval identified by 1 is the most recently\n          completed 15 minute interval,\n          and the interval identified\n          by N is the interval immediately preceding the\n          one identified\n          by N-1.')
sonetFarEndVTIntervalESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2, 1, 2), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalESs.setDescription('The counter associated with the number of\n             Far End Errored Seconds encountered\n             by a SONET/SDH VT interface\n             in a particular 15-minute interval\n             in the past 24 hours.')
sonetFarEndVTIntervalSESs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2, 1, 3), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalSESs.setDescription('The counter associated with the number of\n             Far End Severely Errored Seconds\n             encountered by a SONET/SDH VT interface\n             in a particular 15-minute interval\n             in the past 24 hours.')
sonetFarEndVTIntervalCVs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2, 1, 4), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalCVs.setDescription('The counter associated with the number of\n            Far End Coding Violations reported via\n            the far end block error count\n            encountered by a\n            SONET/SDH VT interface in a\n            particular 15-minute interval\n            in the past 24 hours.')
sonetFarEndVTIntervalUASs = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2, 1, 5), PerfIntervalCount()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalUASs.setDescription('The counter associated with the number of\n          Far End Unavailable Seconds\n          encountered by a\n          SONET/SDH VT interface in a\n          particular 15-minute interval\n          in the past 24 hours.')
sonetFarEndVTIntervalValidData = MibTableColumn((1, 3, 6, 1, 2, 1, 10, 39, 3, 2, 2,
                                                 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sonetFarEndVTIntervalValidData.setDescription('This variable indicates if the data for this\n           interval is valid.')
sonetConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 4))
sonetGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 4, 1))
sonetCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 10, 39, 4, 2))
sonetCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 39, 4, 2, 1)).setObjects(*(('SONET-MIB', 'sonetMediumStuff'), ('SONET-MIB', 'sonetSectionStuff'), ('SONET-MIB', 'sonetLineStuff'), ('SONET-MIB', 'sonetFarEndLineStuff'), ('SONET-MIB', 'sonetPathStuff'), ('SONET-MIB', 'sonetFarEndPathStuff'), ('SONET-MIB', 'sonetVTStuff'), ('SONET-MIB', 'sonetFarEndVTStuff')))
if mibBuilder.loadTexts:
    sonetCompliance.setDescription('The compliance statement for SONET/SDH interfaces.')
sonetCompliance2 = ModuleCompliance((1, 3, 6, 1, 2, 1, 10, 39, 4, 2, 2)).setObjects(*(('SONET-MIB', 'sonetMediumStuff2'), ('SONET-MIB', 'sonetSectionStuff2')))
if mibBuilder.loadTexts:
    sonetCompliance2.setDescription('The compliance statement for SONET/SDH interfaces.')
sonetMediumStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 1)).setObjects(*(('SONET-MIB', 'sonetMediumType'), ('SONET-MIB', 'sonetMediumTimeElapsed'), ('SONET-MIB', 'sonetMediumValidIntervals'), ('SONET-MIB', 'sonetMediumLineCoding'), ('SONET-MIB', 'sonetMediumLineType'), ('SONET-MIB', 'sonetMediumCircuitIdentifier')))
if mibBuilder.loadTexts:
    sonetMediumStuff.setDescription('A collection of objects providing configuration\n               information applicable to all SONET/SDH interfaces.')
sonetSectionStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 2)).setObjects(*(('SONET-MIB', 'sonetSectionCurrentStatus'), ('SONET-MIB', 'sonetSectionCurrentESs'), ('SONET-MIB', 'sonetSectionCurrentSESs'), ('SONET-MIB', 'sonetSectionCurrentSEFSs'), ('SONET-MIB', 'sonetSectionCurrentCVs'), ('SONET-MIB', 'sonetSectionIntervalESs'), ('SONET-MIB', 'sonetSectionIntervalSESs'), ('SONET-MIB', 'sonetSectionIntervalSEFSs'), ('SONET-MIB', 'sonetSectionIntervalCVs')))
if mibBuilder.loadTexts:
    sonetSectionStuff.setDescription('A collection of objects providing information\n               specific to SONET/SDH Section interfaces.')
sonetLineStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 3)).setObjects(*(('SONET-MIB', 'sonetLineCurrentStatus'), ('SONET-MIB', 'sonetLineCurrentESs'), ('SONET-MIB', 'sonetLineCurrentSESs'), ('SONET-MIB', 'sonetLineCurrentCVs'), ('SONET-MIB', 'sonetLineCurrentUASs'), ('SONET-MIB', 'sonetLineIntervalESs'), ('SONET-MIB', 'sonetLineIntervalSESs'), ('SONET-MIB', 'sonetLineIntervalCVs'), ('SONET-MIB', 'sonetLineIntervalUASs')))
if mibBuilder.loadTexts:
    sonetLineStuff.setDescription('A collection of objects providing information\n               specific to SONET/SDH Line interfaces.')
sonetFarEndLineStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 4)).setObjects(*(('SONET-MIB', 'sonetFarEndLineCurrentESs'), ('SONET-MIB', 'sonetFarEndLineCurrentSESs'), ('SONET-MIB', 'sonetFarEndLineCurrentCVs'), ('SONET-MIB', 'sonetFarEndLineCurrentUASs'), ('SONET-MIB', 'sonetFarEndLineIntervalESs'), ('SONET-MIB', 'sonetFarEndLineIntervalSESs'), ('SONET-MIB', 'sonetFarEndLineIntervalCVs'), ('SONET-MIB', 'sonetFarEndLineIntervalUASs')))
if mibBuilder.loadTexts:
    sonetFarEndLineStuff.setDescription('A collection of objects providing information\n               specific to SONET/SDH Line interfaces,\n               and maintaining Line Far End information.')
sonetPathStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 5)).setObjects(*(('SONET-MIB', 'sonetPathCurrentWidth'), ('SONET-MIB', 'sonetPathCurrentStatus'), ('SONET-MIB', 'sonetPathCurrentESs'), ('SONET-MIB', 'sonetPathCurrentSESs'), ('SONET-MIB', 'sonetPathCurrentCVs'), ('SONET-MIB', 'sonetPathCurrentUASs'), ('SONET-MIB', 'sonetPathIntervalESs'), ('SONET-MIB', 'sonetPathIntervalSESs'), ('SONET-MIB', 'sonetPathIntervalCVs'), ('SONET-MIB', 'sonetPathIntervalUASs')))
if mibBuilder.loadTexts:
    sonetPathStuff.setDescription('A collection of objects providing information\n               specific to SONET/SDH Path interfaces.')
sonetFarEndPathStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 6)).setObjects(*(('SONET-MIB', 'sonetFarEndPathCurrentESs'), ('SONET-MIB', 'sonetFarEndPathCurrentSESs'), ('SONET-MIB', 'sonetFarEndPathCurrentCVs'), ('SONET-MIB', 'sonetFarEndPathCurrentUASs'), ('SONET-MIB', 'sonetFarEndPathIntervalESs'), ('SONET-MIB', 'sonetFarEndPathIntervalSESs'), ('SONET-MIB', 'sonetFarEndPathIntervalCVs'), ('SONET-MIB', 'sonetFarEndPathIntervalUASs')))
if mibBuilder.loadTexts:
    sonetFarEndPathStuff.setDescription('A collection of objects providing information\n               specific to SONET/SDH Path interfaces,\n               and maintaining Path Far End information.')
sonetVTStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 7)).setObjects(*(('SONET-MIB', 'sonetVTCurrentWidth'), ('SONET-MIB', 'sonetVTCurrentStatus'), ('SONET-MIB', 'sonetVTCurrentESs'), ('SONET-MIB', 'sonetVTCurrentSESs'), ('SONET-MIB', 'sonetVTCurrentCVs'), ('SONET-MIB', 'sonetVTCurrentUASs'), ('SONET-MIB', 'sonetVTIntervalESs'), ('SONET-MIB', 'sonetVTIntervalSESs'), ('SONET-MIB', 'sonetVTIntervalCVs'), ('SONET-MIB', 'sonetVTIntervalUASs')))
if mibBuilder.loadTexts:
    sonetVTStuff.setDescription('A collection of objects providing information\n               specific to SONET/SDH VT interfaces.')
sonetFarEndVTStuff = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 8)).setObjects(*(('SONET-MIB', 'sonetFarEndVTCurrentESs'), ('SONET-MIB', 'sonetFarEndVTCurrentSESs'), ('SONET-MIB', 'sonetFarEndVTCurrentCVs'), ('SONET-MIB', 'sonetFarEndVTCurrentUASs'), ('SONET-MIB', 'sonetFarEndVTIntervalESs'), ('SONET-MIB', 'sonetFarEndVTIntervalSESs'), ('SONET-MIB', 'sonetFarEndVTIntervalCVs'), ('SONET-MIB', 'sonetFarEndVTIntervalUASs')))
if mibBuilder.loadTexts:
    sonetFarEndVTStuff.setDescription('A collection of objects providing information\n               specific to SONET/SDH VT interfaces,\n               and maintaining VT Far End information.')
sonetMediumStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 9)).setObjects(*(('SONET-MIB', 'sonetMediumType'), ('SONET-MIB', 'sonetMediumTimeElapsed'), ('SONET-MIB', 'sonetMediumValidIntervals'), ('SONET-MIB', 'sonetMediumLineCoding'), ('SONET-MIB', 'sonetMediumLineType'), ('SONET-MIB', 'sonetMediumCircuitIdentifier'), ('SONET-MIB', 'sonetMediumInvalidIntervals'), ('SONET-MIB', 'sonetMediumLoopbackConfig'), ('SONET-MIB', 'sonetSESthresholdSet')))
if mibBuilder.loadTexts:
    sonetMediumStuff2.setDescription('A collection of objects providing configuration\n               information applicable to all SONET/SDH interfaces.')
sonetSectionStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 10)).setObjects(*(('SONET-MIB', 'sonetSectionCurrentStatus'), ('SONET-MIB', 'sonetSectionCurrentESs'), ('SONET-MIB', 'sonetSectionCurrentSESs'), ('SONET-MIB', 'sonetSectionCurrentSEFSs'), ('SONET-MIB', 'sonetSectionCurrentCVs'), ('SONET-MIB', 'sonetSectionIntervalESs'), ('SONET-MIB', 'sonetSectionIntervalSESs'), ('SONET-MIB', 'sonetSectionIntervalSEFSs'), ('SONET-MIB', 'sonetSectionIntervalCVs'), ('SONET-MIB', 'sonetSectionIntervalValidData')))
if mibBuilder.loadTexts:
    sonetSectionStuff2.setDescription('A collection of objects providing information\n               specific to SONET/SDH Section interfaces.')
sonetLineStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 11)).setObjects(*(('SONET-MIB', 'sonetLineCurrentStatus'), ('SONET-MIB', 'sonetLineCurrentESs'), ('SONET-MIB', 'sonetLineCurrentSESs'), ('SONET-MIB', 'sonetLineCurrentCVs'), ('SONET-MIB', 'sonetLineCurrentUASs'), ('SONET-MIB', 'sonetLineIntervalESs'), ('SONET-MIB', 'sonetLineIntervalSESs'), ('SONET-MIB', 'sonetLineIntervalCVs'), ('SONET-MIB', 'sonetLineIntervalUASs'), ('SONET-MIB', 'sonetLineIntervalValidData')))
if mibBuilder.loadTexts:
    sonetLineStuff2.setDescription('A collection of objects providing information\n               specific to SONET/SDH Line interfaces.')
sonetPathStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 12)).setObjects(*(('SONET-MIB', 'sonetPathCurrentWidth'), ('SONET-MIB', 'sonetPathCurrentStatus'), ('SONET-MIB', 'sonetPathCurrentESs'), ('SONET-MIB', 'sonetPathCurrentSESs'), ('SONET-MIB', 'sonetPathCurrentCVs'), ('SONET-MIB', 'sonetPathCurrentUASs'), ('SONET-MIB', 'sonetPathIntervalESs'), ('SONET-MIB', 'sonetPathIntervalSESs'), ('SONET-MIB', 'sonetPathIntervalCVs'), ('SONET-MIB', 'sonetPathIntervalUASs'), ('SONET-MIB', 'sonetPathIntervalValidData')))
if mibBuilder.loadTexts:
    sonetPathStuff2.setDescription('A collection of objects providing information\n               specific to SONET/SDH Path interfaces.')
sonetVTStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 13)).setObjects(*(('SONET-MIB', 'sonetVTCurrentWidth'), ('SONET-MIB', 'sonetVTCurrentStatus'), ('SONET-MIB', 'sonetVTCurrentESs'), ('SONET-MIB', 'sonetVTCurrentSESs'), ('SONET-MIB', 'sonetVTCurrentCVs'), ('SONET-MIB', 'sonetVTCurrentUASs'), ('SONET-MIB', 'sonetVTIntervalESs'), ('SONET-MIB', 'sonetVTIntervalSESs'), ('SONET-MIB', 'sonetVTIntervalCVs'), ('SONET-MIB', 'sonetVTIntervalUASs'), ('SONET-MIB', 'sonetVTIntervalValidData')))
if mibBuilder.loadTexts:
    sonetVTStuff2.setDescription('A collection of objects providing information\n               specific to SONET/SDH VT interfaces.')
sonetFarEndLineStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 14)).setObjects(*(('SONET-MIB', 'sonetFarEndLineCurrentESs'), ('SONET-MIB', 'sonetFarEndLineCurrentSESs'), ('SONET-MIB', 'sonetFarEndLineCurrentCVs'), ('SONET-MIB', 'sonetFarEndLineCurrentUASs'), ('SONET-MIB', 'sonetFarEndLineIntervalESs'), ('SONET-MIB', 'sonetFarEndLineIntervalSESs'), ('SONET-MIB', 'sonetFarEndLineIntervalCVs'), ('SONET-MIB', 'sonetFarEndLineIntervalUASs'), ('SONET-MIB', 'sonetFarEndLineIntervalValidData')))
if mibBuilder.loadTexts:
    sonetFarEndLineStuff2.setDescription('A collection of objects providing information\n               specific to SONET/SDH Line interfaces,\n               and maintaining Line Far End information.')
sonetFarEndPathStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 15)).setObjects(*(('SONET-MIB', 'sonetFarEndPathCurrentESs'), ('SONET-MIB', 'sonetFarEndPathCurrentSESs'), ('SONET-MIB', 'sonetFarEndPathCurrentCVs'), ('SONET-MIB', 'sonetFarEndPathCurrentUASs'), ('SONET-MIB', 'sonetFarEndPathIntervalESs'), ('SONET-MIB', 'sonetFarEndPathIntervalSESs'), ('SONET-MIB', 'sonetFarEndPathIntervalCVs'), ('SONET-MIB', 'sonetFarEndPathIntervalUASs'), ('SONET-MIB', 'sonetFarEndPathIntervalValidData')))
if mibBuilder.loadTexts:
    sonetFarEndPathStuff2.setDescription('A collection of objects providing information\n               specific to SONET/SDH Path interfaces,\n               and maintaining Path Far End information.')
sonetFarEndVTStuff2 = ObjectGroup((1, 3, 6, 1, 2, 1, 10, 39, 4, 1, 16)).setObjects(*(('SONET-MIB', 'sonetFarEndVTCurrentESs'), ('SONET-MIB', 'sonetFarEndVTCurrentSESs'), ('SONET-MIB', 'sonetFarEndVTCurrentCVs'), ('SONET-MIB', 'sonetFarEndVTCurrentUASs'), ('SONET-MIB', 'sonetFarEndVTIntervalESs'), ('SONET-MIB', 'sonetFarEndVTIntervalSESs'), ('SONET-MIB', 'sonetFarEndVTIntervalCVs'), ('SONET-MIB', 'sonetFarEndVTIntervalUASs'), ('SONET-MIB', 'sonetFarEndVTIntervalValidData')))
if mibBuilder.loadTexts:
    sonetFarEndVTStuff2.setDescription('A collection of objects providing information\n               specific to SONET/SDH VT interfaces,\n               and maintaining VT Far End information.')
mibBuilder.exportSymbols('SONET-MIB', sonetObjects=sonetObjects, sonetSectionIntervalCVs=sonetSectionIntervalCVs, sonetPathIntervalEntry=sonetPathIntervalEntry, sonetLineIntervalSESs=sonetLineIntervalSESs, sonetLineIntervalUASs=sonetLineIntervalUASs, sonetPathCurrentEntry=sonetPathCurrentEntry, sonetSectionStuff=sonetSectionStuff, sonetLineCurrentUASs=sonetLineCurrentUASs, sonetFarEndLineIntervalUASs=sonetFarEndLineIntervalUASs, sonetPathIntervalTable=sonetPathIntervalTable, sonetLineStuff=sonetLineStuff, sonetPathCurrentSESs=sonetPathCurrentSESs, sonetConformance=sonetConformance, sonetFarEndVTIntervalESs=sonetFarEndVTIntervalESs, sonetLineIntervalCVs=sonetLineIntervalCVs, sonetFarEndPathIntervalUASs=sonetFarEndPathIntervalUASs, sonetPathIntervalSESs=sonetPathIntervalSESs, sonetFarEndPathStuff2=sonetFarEndPathStuff2, sonetFarEndPathCurrentSESs=sonetFarEndPathCurrentSESs, sonetMediumEntry=sonetMediumEntry, sonetFarEndPathIntervalCVs=sonetFarEndPathIntervalCVs, sonetFarEndLineIntervalCVs=sonetFarEndLineIntervalCVs, sonetCompliance=sonetCompliance, sonetLine=sonetLine, sonetVTCurrentWidth=sonetVTCurrentWidth, sonetLineCurrentTable=sonetLineCurrentTable, sonetLineCurrentCVs=sonetLineCurrentCVs, sonetFarEndLineCurrentESs=sonetFarEndLineCurrentESs, sonetSectionIntervalSESs=sonetSectionIntervalSESs, sonetPath=sonetPath, sonetVTIntervalEntry=sonetVTIntervalEntry, sonetPathIntervalUASs=sonetPathIntervalUASs, sonetFarEndVTIntervalTable=sonetFarEndVTIntervalTable, sonetFarEndLineIntervalTable=sonetFarEndLineIntervalTable, sonetObjectsPath=sonetObjectsPath, sonetMediumValidIntervals=sonetMediumValidIntervals, sonetSectionCurrentESs=sonetSectionCurrentESs, sonetVTIntervalSESs=sonetVTIntervalSESs, sonetMediumStuff=sonetMediumStuff, sonetFarEndPathIntervalSESs=sonetFarEndPathIntervalSESs, sonetMediumStuff2=sonetMediumStuff2, sonetPathCurrentUASs=sonetPathCurrentUASs, sonetPathStuff=sonetPathStuff, sonetLineIntervalNumber=sonetLineIntervalNumber, sonetMIB=sonetMIB, sonetFarEndPathCurrentCVs=sonetFarEndPathCurrentCVs, sonetFarEndVTCurrentSESs=sonetFarEndVTCurrentSESs, sonetPathCurrentCVs=sonetPathCurrentCVs, sonetLineIntervalValidData=sonetLineIntervalValidData, sonetPathIntervalCVs=sonetPathIntervalCVs, sonetFarEndPathIntervalTable=sonetFarEndPathIntervalTable, sonetSectionCurrentCVs=sonetSectionCurrentCVs, sonetMedium=sonetMedium, sonetFarEndLineIntervalESs=sonetFarEndLineIntervalESs, sonetFarEndVTStuff=sonetFarEndVTStuff, sonetMediumLineType=sonetMediumLineType, sonetGroups=sonetGroups, sonetLineCurrentEntry=sonetLineCurrentEntry, sonetFarEndVTIntervalSESs=sonetFarEndVTIntervalSESs, sonetSectionCurrentSEFSs=sonetSectionCurrentSEFSs, sonetFarEndLineCurrentTable=sonetFarEndLineCurrentTable, sonetFarEndLineIntervalValidData=sonetFarEndLineIntervalValidData, sonetMediumLineCoding=sonetMediumLineCoding, sonetFarEndLineCurrentUASs=sonetFarEndLineCurrentUASs, sonetCompliances=sonetCompliances, sonetPathIntervalValidData=sonetPathIntervalValidData, sonetFarEndPathCurrentESs=sonetFarEndPathCurrentESs, sonetVTIntervalUASs=sonetVTIntervalUASs, sonetVTCurrentTable=sonetVTCurrentTable, sonetSectionStuff2=sonetSectionStuff2, sonetMediumCircuitIdentifier=sonetMediumCircuitIdentifier, sonetPathIntervalESs=sonetPathIntervalESs, sonetMediumLoopbackConfig=sonetMediumLoopbackConfig, sonetPathCurrentESs=sonetPathCurrentESs, sonetVTIntervalCVs=sonetVTIntervalCVs, sonetSectionIntervalESs=sonetSectionIntervalESs, sonetPathCurrentWidth=sonetPathCurrentWidth, sonetFarEndLine=sonetFarEndLine, sonetSectionIntervalTable=sonetSectionIntervalTable, sonetFarEndVTCurrentTable=sonetFarEndVTCurrentTable, sonetFarEndPathStuff=sonetFarEndPathStuff, sonetLineStuff2=sonetLineStuff2, sonetVTIntervalNumber=sonetVTIntervalNumber, sonetFarEndVTCurrentESs=sonetFarEndVTCurrentESs, sonetFarEndPathCurrentEntry=sonetFarEndPathCurrentEntry, sonetPathStuff2=sonetPathStuff2, sonetSection=sonetSection, sonetFarEndLineStuff2=sonetFarEndLineStuff2, sonetMediumTimeElapsed=sonetMediumTimeElapsed, sonetFarEndVTIntervalEntry=sonetFarEndVTIntervalEntry, sonetMediumTable=sonetMediumTable, sonetFarEndVT=sonetFarEndVT, sonetSectionIntervalValidData=sonetSectionIntervalValidData, sonetVTStuff=sonetVTStuff, sonetLineIntervalEntry=sonetLineIntervalEntry, sonetPathIntervalNumber=sonetPathIntervalNumber, sonetSectionIntervalNumber=sonetSectionIntervalNumber, sonetVTCurrentCVs=sonetVTCurrentCVs, sonetFarEndVTCurrentEntry=sonetFarEndVTCurrentEntry, PYSNMP_MODULE_ID=sonetMIB, sonetFarEndLineCurrentSESs=sonetFarEndLineCurrentSESs, sonetFarEndVTCurrentUASs=sonetFarEndVTCurrentUASs, sonetLineCurrentSESs=sonetLineCurrentSESs, sonetFarEndLineCurrentEntry=sonetFarEndLineCurrentEntry, sonetVTIntervalValidData=sonetVTIntervalValidData, sonetFarEndVTStuff2=sonetFarEndVTStuff2, sonetFarEndVTCurrentCVs=sonetFarEndVTCurrentCVs, sonetFarEndVTIntervalCVs=sonetFarEndVTIntervalCVs, sonetSectionCurrentEntry=sonetSectionCurrentEntry, sonetSectionIntervalSEFSs=sonetSectionIntervalSEFSs, sonetPathCurrentStatus=sonetPathCurrentStatus, sonetLineCurrentStatus=sonetLineCurrentStatus, sonetFarEndLineIntervalSESs=sonetFarEndLineIntervalSESs, sonetFarEndPathCurrentUASs=sonetFarEndPathCurrentUASs, sonetLineIntervalTable=sonetLineIntervalTable, sonetFarEndPathIntervalEntry=sonetFarEndPathIntervalEntry, sonetMediumInvalidIntervals=sonetMediumInvalidIntervals, sonetVT=sonetVT, sonetFarEndPathIntervalESs=sonetFarEndPathIntervalESs, sonetFarEndVTIntervalNumber=sonetFarEndVTIntervalNumber, sonetFarEndPathCurrentTable=sonetFarEndPathCurrentTable, sonetSectionCurrentStatus=sonetSectionCurrentStatus, sonetLineCurrentESs=sonetLineCurrentESs, sonetFarEndLineIntervalNumber=sonetFarEndLineIntervalNumber, sonetVTCurrentStatus=sonetVTCurrentStatus, sonetVTCurrentESs=sonetVTCurrentESs, sonetFarEndVTIntervalValidData=sonetFarEndVTIntervalValidData, sonetSESthresholdSet=sonetSESthresholdSet, sonetVTIntervalTable=sonetVTIntervalTable, sonetSectionIntervalEntry=sonetSectionIntervalEntry, sonetFarEndLineCurrentCVs=sonetFarEndLineCurrentCVs, sonetVTIntervalESs=sonetVTIntervalESs, sonetVTStuff2=sonetVTStuff2, sonetFarEndPathIntervalNumber=sonetFarEndPathIntervalNumber, sonetVTCurrentEntry=sonetVTCurrentEntry, sonetObjectsVT=sonetObjectsVT, sonetCompliance2=sonetCompliance2, sonetFarEndPath=sonetFarEndPath, sonetSectionCurrentSESs=sonetSectionCurrentSESs, sonetVTCurrentUASs=sonetVTCurrentUASs, sonetFarEndLineIntervalEntry=sonetFarEndLineIntervalEntry, sonetVTCurrentSESs=sonetVTCurrentSESs, sonetMediumType=sonetMediumType, sonetSectionCurrentTable=sonetSectionCurrentTable, sonetPathCurrentTable=sonetPathCurrentTable, sonetLineIntervalESs=sonetLineIntervalESs, sonetFarEndVTIntervalUASs=sonetFarEndVTIntervalUASs, sonetFarEndPathIntervalValidData=sonetFarEndPathIntervalValidData, sonetFarEndLineStuff=sonetFarEndLineStuff)