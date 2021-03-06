# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/APPN-DLUR-MIB.py
# Compiled at: 2016-02-13 18:05:25
(SnaControlPointName,) = mibBuilder.importSymbols('APPN-MIB', 'SnaControlPointName')
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ConstraintsUnion, SingleValueConstraint, ValueSizeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection')
(snanauMIB,) = mibBuilder.importSymbols('SNA-NAU-MIB', 'snanauMIB')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(Gauge32, Unsigned32, TimeTicks, Bits, Counter32, Counter64, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, iso, NotificationType, ObjectIdentity, Integer32, MibIdentifier, ModuleIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'Unsigned32', 'TimeTicks', 'Bits', 'Counter32', 'Counter64', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'IpAddress', 'iso', 'NotificationType', 'ObjectIdentity', 'Integer32', 'MibIdentifier', 'ModuleIdentity')
(TruthValue, DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'TruthValue', 'DisplayString', 'TextualConvention')
dlurMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 34, 5))
if mibBuilder.loadTexts:
    dlurMIB.setLastUpdated('9705101500Z')
if mibBuilder.loadTexts:
    dlurMIB.setOrganization('IETF SNA NAU MIB WG / AIW APPN/HPR MIBs SIG')
if mibBuilder.loadTexts:
    dlurMIB.setContactInfo('\n                        Bob Clouston\n                        Cisco Systems\n                        7025 Kit Creek Road\n                        P.O. Box 14987\n                        Research Triangle Park, NC 27709, USA\n                        Tel:    1 919 472 2333\n                        E-mail: clouston@cisco.com\n\n                        Bob Moore\n                        IBM Corporation\n                        800 Park Offices Drive\n                        RHJA/664\n                        P.O. Box 12195\n                        Research Triangle Park, NC 27709, USA\n                        Tel:    1 919 254 4436\n                        E-mail: remoore@ralvm6.vnet.ibm.com\n                ')
if mibBuilder.loadTexts:
    dlurMIB.setDescription('This is the MIB module for objects used to manage\n                network devices with DLUR capabilities.  This MIB\n                contains information that is useful for managing an APPN\n                product that implements a DLUR (Dependent Logical Unit\n                Requester).  The DLUR product has a client/server\n                relationship with an APPN product that implements a DLUS\n                (Dependent Logical Unit Server).')
dlurObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 1))
dlurNodeInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 1, 1))
dlurNodeCapabilities = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1))
dlurNodeCpName = MibScalar((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1, 1), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurNodeCpName.setDescription('Administratively assigned network name for the APPN node where\n          this DLUR implementation resides.  If this object has the same\n          value as the appnNodeCpName object in the APPN MIB, then the\n          two objects are referring to the same APPN node.')
dlurReleaseLevel = MibScalar((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(2, 2)).setFixedLength(2)).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurReleaseLevel.setDescription("The DLUR release level of this implementation.  This is the\n          value that is encoded in the DLUR/DLUS Capabilites (CV 51).\n          To insure consistent display, this one-byte value is encoded\n          here as two displayable characters that are equivalent to a\n          hexadecimal display.  For example, if the one-byte value as\n          encoded in CV51 is X'01', this object will contain the\n          displayable string '01'.")
dlurAnsSupport = MibScalar((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('continueOrStop',
                                                                                                                                                                                1), ('stopOnly',
                                                                                                                                                                                     2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurAnsSupport.setDescription("Automatic Network Shutdown (ANS) capability of this node.\n\n              -  'continueOrStop' indicates that the DLUR implementation\n                 supports either ANS value (continue or stop) as\n                 specified by the DLUS on ACTPU for each PU.\n\n              -  'stopOnly' indicates that the DLUR implementation only\n                 supports the ANS value of stop.\n\n           ANS = continue means that the DLUR node will keep LU-LU\n           sessions active even if SSCP-PU and SSCP-LU control sessions\n           are interrupted.\n\n           ANS = stop means that LU-LU sessions will be interrupted when\n           the SSCP-PU and SSCP-LU sessions are interrupted.")
dlurMultiSubnetSupport = MibScalar((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1, 4), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurMultiSubnetSupport.setDescription('Indication of whether this DLUR implementation can support\n          CPSVRMGR sessions that cross NetId boundaries.')
dlurDefaultDefPrimDlusName = MibScalar((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1, 5), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurDefaultDefPrimDlusName.setDescription('The SNA name of the defined default primary DLUS for all of\n          the PUs served by this DLUR.  This can be overridden for a\n          particular PU by a defined primary DLUS for that PU,\n          represented by the dlurPuDefPrimDlusName object.')
dlurNetworkNameForwardingSupport = MibScalar((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1, 6), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurNetworkNameForwardingSupport.setDescription('Indication of whether this DLUR implementation supports\n          forwarding of Network Name control vectors on ACTPUs and\n          ACTLUs to DLUR-served PUs and their associated LUs.\n\n          This object corresponds to byte 9. bit 3 of cv51.')
dlurNondisDlusDlurSessDeactSup = MibScalar((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 1, 7), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurNondisDlusDlurSessDeactSup.setDescription("Indication of whether this DLUR implementation supports\n          nondisruptive deactivation of its DLUR-DLUS sessions.\n          Upon receiving from a DLUS an UNBIND for the CPSVRMGR pipe\n          with sense data X'08A0 000B', a DLUR that supports this\n          option immediately begins attempting to activate a CPSVRMGR\n          pipe with a DLUS other than the one that sent the UNBIND.\n\n          This object corresponds to byte 9. bit 4 of cv51.")
dlurDefaultDefBackupDlusTable = MibTable((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 2))
if mibBuilder.loadTexts:
    dlurDefaultDefBackupDlusTable.setDescription('This table contains an ordered list of defined backup DLUSs\n          for all of the PUs served by this DLUR.  These can be\n          overridden for a particular PU by a list of defined backup\n          DLUSs for that PU, represented by the\n          dlurPuDefBackupDlusNameTable.  Entries in this table are\n          ordered from most preferred default backup DLUS to least\n          preferred.')
dlurDefaultDefBackupDlusEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 2, 1)).setIndexNames((0,
                                                                                                  'APPN-DLUR-MIB',
                                                                                                  'dlurDefaultDefBackupDlusIndex'))
if mibBuilder.loadTexts:
    dlurDefaultDefBackupDlusEntry.setDescription('This table is indexed by an integer-valued index, which\n          orders the entries from most preferred default backup DLUS\n          to least preferred.')
dlurDefaultDefBackupDlusIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 2, 1,
                                                1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    dlurDefaultDefBackupDlusIndex.setDescription('Index for this table.  The index values start at 1,\n          which identifies the most preferred default backup DLUS.')
dlurDefaultDefBackupDlusName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 1, 2, 1,
                                               2), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurDefaultDefBackupDlusName.setDescription('Fully qualified name of a default backup DLUS for PUs served\n          by this DLUR.')
dlurPuInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 1, 2))
dlurPuTable = MibTable((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1))
if mibBuilder.loadTexts:
    dlurPuTable.setDescription('Information about the PUs supported by this DLUR.')
dlurPuEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1)).setIndexNames((0,
                                                                                'APPN-DLUR-MIB',
                                                                                'dlurPuName'))
if mibBuilder.loadTexts:
    dlurPuEntry.setDescription('Entry in a table of PU information, indexed by PU name.')
dlurPuName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 17)))
if mibBuilder.loadTexts:
    dlurPuName.setDescription('Locally administered name of the PU.')
dlurPuSscpSuppliedName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 17))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuSscpSuppliedName.setDescription('The SNA name of the PU.  This value is supplied to a PU by the\n          SSCP that activated it.  If a value has not been supplied, a\n          zero-length string is returned.')
dlurPuStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9))).clone(namedValues=NamedValues(('reset',
                                                                                                                                                                                                           1), ('pendReqActpuRsp',
                                                                                                                                                                                                                2), ('pendActpu',
                                                                                                                                                                                                                     3), ('pendActpuRsp',
                                                                                                                                                                                                                          4), ('active',
                                                                                                                                                                                                                               5), ('pendLinkact',
                                                                                                                                                                                                                                    6), ('pendDactpuRsp',
                                                                                                                                                                                                                                         7), ('pendInop',
                                                                                                                                                                                                                                              8), ('pendInopActpu',
                                                                                                                                                                                                                                                   9)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuStatus.setDescription('Status of the DLUR-supported PU.  The following values are\n          defined:\n\n             reset(1)           -  reset\n             pendReqActpuRsp(2) -  pending a response from the DLUS\n                                   to a Request ACTPU\n             pendActpu(3)       -  pending an ACTPU from the DLUS\n             pendActpuRsp(4)    -  pending an ACTPU response from the PU\n             active(5)          -  active\n             pendLinkact(6)     -  pending activation of the link to a\n                                   downstream PU\n             pendDactpuRsp(7)   -  pending a DACTPU response from the PU\n             pendInop(8)        -  the CPSVRMGR pipe became inoperative\n                                   while the DLUR was pending an ACTPU\n                                   response from the PU\n             pendInopActpu(9)   -  when the DLUR was in the pendInop\n                                   state, a CPSVRMGR pipe became active\n                                   and a new ACTPU was received over it,\n                                   before a response to the previous\n                                   ACTPU was received from the PU.')
dlurPuAnsSupport = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('continue',
                                                                                                                                                                                          1), ('stop',
                                                                                                                                                                                               2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuAnsSupport.setDescription("The Automatic Network Shutdown (ANS) support configured for\n          this PU.  This value (as configured by the network\n          administrator) is sent by DLUS with ACTPU for each PU.\n\n              -  'continue' means that the DLUR node will attempt to keep\n                 LU-LU sessions active even if SSCP-PU and SSCP-LU\n                 control sessions are interrupted.\n\n              -  'stop' means that LU-LU sessions will be interrupted\n                 when the SSCP-PU and SSCP-LU sessions are interrupted.")
dlurPuLocation = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('internal',
                                                                                                                                                                                        1), ('downstream',
                                                                                                                                                                                             2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuLocation.setDescription('Location of the DLUR-support PU:\n              internal(1)   - internal to the APPN node itself (no link)\n              downstream(2) - downstream of the APPN node (connected via\n                              a link).')
dlurPuLsName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 6), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 10))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuLsName.setDescription('Administratively assigned name of the link station through\n          which a downstream PU is connected to this DLUR.  A zero-length\n          string is returned for internal PUs.  If this object has the\n          same value as the appnLsName object in the APPN MIB, then the\n          two are identifying the same link station.')
dlurPuDlusSessnStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('reset',
                                                                                                                                                                                                     1), ('pendingActive',
                                                                                                                                                                                                          2), ('active',
                                                                                                                                                                                                               3), ('pendingInactive',
                                                                                                                                                                                                                    4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuDlusSessnStatus.setDescription("Status of the control session to the DLUS identified in\n          dlurPuActiveDlusName.  This is a combination of the separate\n          states for the contention-winner and contention-loser sessions:\n\n          reset(1)           - none of the cases below\n          pendingActive(2)   - either contention-winner session or\n                               contention-loser session is pending active\n          active(3)          - contention-winner and contention-loser\n                               sessions are both active\n          pendingInactive(4) - either contention-winner session or\n                               contention-loser session is pending\n                               inactive - this test is made AFTER the\n                               'pendingActive' test.\n\n          The following matrix provides a different representation of\n          how the values of this object are related to the individual\n          states of the contention-winner and contention-loser sessions:\n\n               Conwinner\n               | pA | pI | A | X = !(pA | pI | A)\n          C ++++++++++++++++++++++++++++++++++\n          o pA | 2  |  2 | 2 | 2\n          n ++++++++++++++++++++++++++++++++++\n          l pI | 2  |  4 | 4 | 4\n          o ++++++++++++++++++++++++++++++++++\n          s A  | 2  |  4 | 3 | 1\n          e ++++++++++++++++++++++++++++++++++\n          r X  | 2  |  4 | 1 | 1\n            ++++++++++++++++++++++++++++++++++\n          ")
dlurPuActiveDlusName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 8), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 17))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuActiveDlusName.setDescription('The SNA name of the active DLUS for this PU.  If its length\n          is not zero, this name follows the SnaControlPointName textual\n          convention.  A zero-length string indicates that the PU does\n          not currently have an active DLUS.')
dlurPuDefPrimDlusName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 1, 1, 9), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 17))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuDefPrimDlusName.setDescription('The SNA name of the defined primary DLUS for this PU, if one\n          has been defined.  If present, this name follows the\n          SnaControlPointName textual convention.  A zero-length string\n          indicates that no primary DLUS has been defined for this PU, in\n          which case the global default represented by the\n          dlurDefaultDefPrimDlusName object is used.')
dlurPuDefBackupDlusTable = MibTable((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 2))
if mibBuilder.loadTexts:
    dlurPuDefBackupDlusTable.setDescription('This table contains an ordered list of defined backup DLUSs\n          for those PUs served by this DLUR that have their own defined\n          backup DLUSs.  PUs that have no entries in this table use the\n          global default backup DLUSs for the DLUR, represented by the\n          dlurDefaultDefBackupDlusNameTable.  Entries in this table are\n          ordered from most preferred backup DLUS to least preferred for\n          each PU.')
dlurPuDefBackupDlusEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 2, 1)).setIndexNames((0,
                                                                                             'APPN-DLUR-MIB',
                                                                                             'dlurPuDefBackupDlusPuName'), (0,
                                                                                                                            'APPN-DLUR-MIB',
                                                                                                                            'dlurPuDefBackupDlusIndex'))
if mibBuilder.loadTexts:
    dlurPuDefBackupDlusEntry.setDescription('This table is indexed by PU name and by an integer-valued\n          index, which orders the entries from most preferred backup DLUS\n          for the PU to least preferred.')
dlurPuDefBackupDlusPuName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 2, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 17)))
if mibBuilder.loadTexts:
    dlurPuDefBackupDlusPuName.setDescription('Locally administered name of the PU.  If this object has the\n          same value as the dlurPuName object, then the two are\n          identifying the same PU.')
dlurPuDefBackupDlusIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 2, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    dlurPuDefBackupDlusIndex.setDescription('Secondary index for this table.  The index values start at 1,\n          which identifies the most preferred backup DLUS for the PU.')
dlurPuDefBackupDlusName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 2, 2, 1, 3), SnaControlPointName()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurPuDefBackupDlusName.setDescription('Fully qualified name of a backup DLUS for this PU.')
dlurDlusInfo = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 1, 3))
dlurDlusTable = MibTable((1, 3, 6, 1, 2, 1, 34, 5, 1, 3, 1))
if mibBuilder.loadTexts:
    dlurDlusTable.setDescription('Information about DLUS control sessions.')
dlurDlusEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 5, 1, 3, 1, 1)).setIndexNames((0,
                                                                                  'APPN-DLUR-MIB',
                                                                                  'dlurDlusName'))
if mibBuilder.loadTexts:
    dlurDlusEntry.setDescription('This entry is indexed by the name of the DLUS.')
dlurDlusName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 3, 1, 1, 1), SnaControlPointName())
if mibBuilder.loadTexts:
    dlurDlusName.setDescription('The SNA name of a DLUS with which this DLUR currently has a\n          CPSVRMGR pipe established.')
dlurDlusSessnStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 5, 1, 3, 1, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('reset',
                                                                                                                                                                                                   1), ('pendingActive',
                                                                                                                                                                                                        2), ('active',
                                                                                                                                                                                                             3), ('pendingInactive',
                                                                                                                                                                                                                  4)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    dlurDlusSessnStatus.setDescription("Status of the CPSVRMGR pipe between the DLUR and this DLUS.\n          This is a combination of the separate states for the\n          contention-winner and contention-loser sessions:\n\n          reset(1)           - none of the cases below\n          pendingActive(2)   - either contention-winner session or\n                               contention-loser session is pending active\n          active(3)          - contention-winner and contention-loser\n                               sessions are both active\n          pendingInactive(4) - either contention-winner session or\n                               contention-loser session is pending\n                               inactive - this test is made AFTER the\n                               'pendingActive' test.\n\n          The following matrix provides a different representation of\n          how the values of this object are related to the individual\n          states of the contention-winner and contention-loser sessions:\n\n               Conwinner\n               | pA | pI | A | X = !(pA | pI | A)\n          C ++++++++++++++++++++++++++++++++++\n          o pA | 2  |  2 | 2 | 2\n          n ++++++++++++++++++++++++++++++++++\n          l pI | 2  |  4 | 4 | 4\n          o ++++++++++++++++++++++++++++++++++\n          s A  | 2  |  4 | 3 | 1\n          e ++++++++++++++++++++++++++++++++++\n          r X  | 2  |  4 | 1 | 1\n            ++++++++++++++++++++++++++++++++++\n          ")
dlurConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 2))
dlurCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 2, 1))
dlurGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 34, 5, 2, 2))
dlurCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 34, 5, 2, 1, 1)).setObjects(*(('APPN-DLUR-MIB', 'dlurConfGroup'), ))
if mibBuilder.loadTexts:
    dlurCompliance.setDescription('The compliance statement for the SNMPv2 entities which\n          implement the DLUR MIB.')
dlurConfGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 5, 2, 2, 1)).setObjects(*(('APPN-DLUR-MIB', 'dlurNodeCpName'), ('APPN-DLUR-MIB', 'dlurReleaseLevel'), ('APPN-DLUR-MIB', 'dlurAnsSupport'), ('APPN-DLUR-MIB', 'dlurMultiSubnetSupport'), ('APPN-DLUR-MIB', 'dlurNetworkNameForwardingSupport'), ('APPN-DLUR-MIB', 'dlurNondisDlusDlurSessDeactSup'), ('APPN-DLUR-MIB', 'dlurDefaultDefPrimDlusName'), ('APPN-DLUR-MIB', 'dlurDefaultDefBackupDlusName'), ('APPN-DLUR-MIB', 'dlurPuSscpSuppliedName'), ('APPN-DLUR-MIB', 'dlurPuStatus'), ('APPN-DLUR-MIB', 'dlurPuAnsSupport'), ('APPN-DLUR-MIB', 'dlurPuLocation'), ('APPN-DLUR-MIB', 'dlurPuLsName'), ('APPN-DLUR-MIB', 'dlurPuDlusSessnStatus'), ('APPN-DLUR-MIB', 'dlurPuActiveDlusName'), ('APPN-DLUR-MIB', 'dlurPuDefPrimDlusName'), ('APPN-DLUR-MIB', 'dlurPuDefBackupDlusName'), ('APPN-DLUR-MIB', 'dlurDlusSessnStatus')))
if mibBuilder.loadTexts:
    dlurConfGroup.setDescription('A collection of objects providing information on an\n          implementation of APPN DLUR.')
mibBuilder.exportSymbols('APPN-DLUR-MIB', dlurDefaultDefBackupDlusName=dlurDefaultDefBackupDlusName, dlurPuSscpSuppliedName=dlurPuSscpSuppliedName, dlurCompliance=dlurCompliance, dlurPuEntry=dlurPuEntry, dlurNodeCpName=dlurNodeCpName, dlurPuLsName=dlurPuLsName, dlurPuName=dlurPuName, dlurPuAnsSupport=dlurPuAnsSupport, dlurDlusSessnStatus=dlurDlusSessnStatus, dlurAnsSupport=dlurAnsSupport, dlurNodeCapabilities=dlurNodeCapabilities, dlurConformance=dlurConformance, dlurDlusEntry=dlurDlusEntry, dlurPuDlusSessnStatus=dlurPuDlusSessnStatus, dlurNodeInfo=dlurNodeInfo, dlurDefaultDefPrimDlusName=dlurDefaultDefPrimDlusName, dlurPuTable=dlurPuTable, dlurNondisDlusDlurSessDeactSup=dlurNondisDlusDlurSessDeactSup, dlurDlusInfo=dlurDlusInfo, dlurDefaultDefBackupDlusIndex=dlurDefaultDefBackupDlusIndex, dlurPuDefBackupDlusTable=dlurPuDefBackupDlusTable, dlurPuDefBackupDlusEntry=dlurPuDefBackupDlusEntry, dlurDlusTable=dlurDlusTable, dlurPuInfo=dlurPuInfo, dlurPuDefPrimDlusName=dlurPuDefPrimDlusName, dlurCompliances=dlurCompliances, dlurMultiSubnetSupport=dlurMultiSubnetSupport, PYSNMP_MODULE_ID=dlurMIB, dlurReleaseLevel=dlurReleaseLevel, dlurObjects=dlurObjects, dlurPuDefBackupDlusIndex=dlurPuDefBackupDlusIndex, dlurConfGroup=dlurConfGroup, dlurDefaultDefBackupDlusEntry=dlurDefaultDefBackupDlusEntry, dlurPuActiveDlusName=dlurPuActiveDlusName, dlurPuDefBackupDlusPuName=dlurPuDefBackupDlusPuName, dlurDefaultDefBackupDlusTable=dlurDefaultDefBackupDlusTable, dlurNetworkNameForwardingSupport=dlurNetworkNameForwardingSupport, dlurPuStatus=dlurPuStatus, dlurGroups=dlurGroups, dlurPuDefBackupDlusName=dlurPuDefBackupDlusName, dlurDlusName=dlurDlusName, dlurMIB=dlurMIB, dlurPuLocation=dlurPuLocation)