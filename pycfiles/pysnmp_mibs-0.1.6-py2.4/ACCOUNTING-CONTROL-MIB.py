# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/ACCOUNTING-CONTROL-MIB.py
# Compiled at: 2016-02-13 18:03:47
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, ValueSizeConstraint, ConstraintsUnion, ConstraintsIntersection, SingleValueConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'ValueSizeConstraint', 'ConstraintsUnion', 'ConstraintsIntersection', 'SingleValueConstraint')
(ifIndex,) = mibBuilder.importSymbols('IF-MIB', 'ifIndex')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, Integer32, NotificationType, MibIdentifier, Bits, Unsigned32, ObjectIdentity, ModuleIdentity, TimeTicks, Counter64, IpAddress, iso, Counter32, mib_2) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Integer32', 'NotificationType', 'MibIdentifier', 'Bits', 'Unsigned32', 'ObjectIdentity', 'ModuleIdentity', 'TimeTicks', 'Counter64', 'IpAddress', 'iso', 'Counter32', 'mib-2')
(TruthValue, TextualConvention, DisplayString, TestAndIncr, RowStatus) = mibBuilder.importSymbols('SNMPv2-TC', 'TruthValue', 'TextualConvention', 'DisplayString', 'TestAndIncr', 'RowStatus')
accountingControlMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 60))
if mibBuilder.loadTexts:
    accountingControlMIB.setLastUpdated('9809281000Z')
if mibBuilder.loadTexts:
    accountingControlMIB.setOrganization('IETF AToM MIB Working Group')
if mibBuilder.loadTexts:
    accountingControlMIB.setContactInfo('Keith McCloghrie\n                  Cisco Systems, Inc.\n                  170 West Tasman Drive,\n                  San Jose CA 95134-1706.\n                  Phone: +1 408 526 5260\n                  Email: kzm@cisco.com')
if mibBuilder.loadTexts:
    accountingControlMIB.setDescription('The MIB module for managing the collection and storage of\n            accounting information for connections in a connection-\n            oriented network such as ATM.')
acctngMIBObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 1))
acctngSelectionControl = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 1, 1))
acctngFileControl = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 1, 2))
acctngInterfaceControl = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 1, 3))
acctngTrapControl = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 1, 4))

class DataCollectionSubtree(ObjectIdentifier, TextualConvention):
    __module__ = __name__


class DataCollectionList(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 8)


class FileIndex(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(1, 65535)


acctngSelectionTable = MibTable((1, 3, 6, 1, 2, 1, 60, 1, 1, 1))
if mibBuilder.loadTexts:
    acctngSelectionTable.setDescription("A list of accounting information selection entries.\n\n            Note that additions, modifications and deletions of entries\n            in this table can occur at any time, but such changes only\n            take effect on the next occasion when collection begins into\n            a new file.  Thus, between modification and the next 'swap',\n            the content of this table does not reflect the current\n            selection.")
acctngSelectionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 60, 1, 1, 1, 1)).setIndexNames((0, 'ACCOUNTING-CONTROL-MIB', 'acctngSelectionIndex'))
if mibBuilder.loadTexts:
    acctngSelectionEntry.setDescription('An entry identifying an (subtree, list) tuple used to\n            select a set of accounting information which is to be\n            collected.')
acctngSelectionIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 1, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    acctngSelectionIndex.setDescription("An arbitrary integer value which uniquely identifies a\n            tuple stored in this table.  This value is required to be\n            the permanent 'handle' for an entry in this table for as\n            long as that entry exists, including across restarts and\n            power outages.")
acctngSelectionSubtree = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 1, 1, 1, 2), DataCollectionSubtree()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngSelectionSubtree.setDescription('The combination of acctngSelectionSubtree and\n            acctngSelectionList specifies one (subtree, list) tuple\n            which is to be collected.')
acctngSelectionList = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 1, 1, 1, 3), DataCollectionList()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngSelectionList.setDescription('The combination of acctngSelectionSubtree and\n            acctngSelectionList specifies one (subtree, list) tuple\n            which is to be collected.')
acctngSelectionFile = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 1, 1, 1, 4), FileIndex()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngSelectionFile.setDescription('An indication of the file into which the accounting\n            information identified by this entry is to be stored.  If\n            there is no conceptual row in the acctngFileTable for which\n            the value of acctngFileIndex has the same value as this\n            object, then the information selected by this entry is not\n            collected.')
acctngSelectionType = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 1, 1, 1, 5), Bits().clone(namedValues=NamedValues(('svcIncoming', 0), ('svcOutgoing', 1), ('svpIncoming', 2), ('svpOutgoing', 3), ('pvc', 4), ('pvp', 5), ('spvcOriginator', 6), ('spvcTarget', 7), ('spvpOriginator', 8), ('spvpTarget', 9))).clone(namedValues=NamedValues(('svcIncoming', 0), ('svcOutgoing', 1), ('svpIncoming', 2), ('svpOutgoing', 3)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngSelectionType.setDescription('Indicates the types of connections for which the\n            information selected by this entry are to be collected.')
acctngSelectionRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 1, 1, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngSelectionRowStatus.setDescription("The status of this conceptual row.  An agent may refuse to\n            create new conceptual rows and/or modify existing conceptual\n            rows, if such creation/modification would cause multiple\n            rows to have the same values of acctngSelectionSubtree and\n            acctngSelectionList.\n\n            A conceptual row can not have the status of 'active' until\n            values have been assigned to the acctngSelectionSubtree,\n            acctngSelectionList and acctngSelectionFile columnar objects\n            within that row.\n\n            An agent must not refuse to change the values of the\n            acctngSelectionSubtree, acctngSelectionList and\n            acctngSelectionFile columnar objects within a conceptual row\n            even while that row's status is 'active'.  Similarly, an\n            agent must not refuse to destroy an existing conceptual row\n            while the file referenced by that row's instance of\n            acctngSelectionFile is in active use, i.e., while the\n            corresponding instance of acctngFileRowStatus has the value\n            'active'.  However, such changes only take effect upon the\n            next occasion when collection begins into a new (version of\n            the) file.")
acctngFileTable = MibTable((1, 3, 6, 1, 2, 1, 60, 1, 2, 1))
if mibBuilder.loadTexts:
    acctngFileTable.setDescription('A list of files into which accounting information is to be\n            stored.')
acctngFileEntry = MibTableRow((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1)).setIndexNames((0, 'ACCOUNTING-CONTROL-MIB', 'acctngFileIndex'))
if mibBuilder.loadTexts:
    acctngFileEntry.setDescription('An entry identifying a file into which accounting\n            information is to be collected.')
acctngFileIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 1), FileIndex())
if mibBuilder.loadTexts:
    acctngFileIndex.setDescription("A unique value identifying a file into which accounting\n            data is to be stored.  This value is required to be the\n            permanent 'handle' for an entry in this table for as long as\n            that entry exists, including across restarts and power\n            outages.")
acctngFileName = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 2), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileName.setDescription("The name of the file into which accounting data is to be\n            stored.  If files are named using suffixes, then the name of\n            the current file is the concatenation of acctngFileName and\n            acctngFileNameSuffix.\n\n            An agent will respond with an error (e.g., 'wrongValue') to\n            a management set operation which attempts to modify the\n            value of this object to the same value as already held by\n            another instance of acctngFileName.  An agent will also\n            respond with an error (e.g., 'wrongValue') if the new value\n            is invalid for use as a file name on the local file system\n            (e.g., many file systems do not support white space embedded\n            in file names).\n\n            The value of this object can not be modified while the\n            corresponding instance of acctngFileRowStatus is 'active'.")
acctngFileNameSuffix = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 3), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(0, 8))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    acctngFileNameSuffix.setDescription('The suffix, if any, of the name of a file into which\n            accounting data is currently being stored.  If suffixes are\n            not used, then the value of this object is the zero-length\n            string.  Note that if a separator, such as a period, is used\n            in appending the suffix to the file name, then that\n            separator appears as the first character of this value.')
acctngFileDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 4), DisplayString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileDescription.setDescription('The textual description of the accounting data which will\n            be stored (on the next occasion) when header information is\n            stored in the file.  The value of this object may be\n            modified at any time.')
acctngFileCommand = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4))).clone(namedValues=NamedValues(('idle', 1), ('cmdInProgress', 2), ('swapToNewFile', 3), ('collectNow', 4))).clone('idle')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileCommand.setDescription("A control object for the collection of accounting data.\n            When read the value is either 'idle' or 'cmdInProgress'.\n            Writing a value is only allowed when the current value is\n            'idle'.  When a value is successfully written, the value\n            changes to 'cmdInProgress' until completion of the action,\n            at which time the value reverts to 'idle'.  Actions are\n            invoked by writing the following values:\n\n               'swapToNewFile' - the collection of data into the current\n                      file is terminated, and collection continues into\n                      a new (version of the) file.\n\n               'collectNow' - the agent creates and stores a connection\n                      record into the current file for each active\n                      connection having a type matching\n                      acctngSelectionType and an age greater than\n                      acctngFileMinAge.")
acctngFileMaximumSize = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(100, 2147483647)).clone(5000000)).setUnits('bytes').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileMaximumSize.setDescription("The maximum size of the file (including header\n            information).  When the file of collected data reaches this\n            size, either the agent automatically swaps to a new version\n            (i.e., a new value acctngFileNameSuffix) of the file, or new\n            records are discarded.  Since a file must contain an\n            integral number of connection records, the actual maximum\n            size of the file may be just less OR Just greater than the\n            value of this object.\n\n            The value of this object can not be modified while the\n            corresponding instance of acctngFileRowStatus is 'active'.\n            The largest value of the maximum file size in some agents\n            will be less than 2147483647 bytes.")
acctngFileCurrentSize = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 2147483647))).setUnits('bytes').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    acctngFileCurrentSize.setDescription('The current size of the file into which data is currently\n            being collected, including header information.')
acctngFileFormat = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('other', 1), ('ber', 2))).clone('ber')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileFormat.setDescription("An indication of the format in which the accounting data is\n            to be stored in the file.  If the value is modified, the new\n            value takes effect after the next 'swap' to a new file.  The\n            value ber(2) indicates the standard format.")
acctngFileCollectMode = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 9), Bits().clone(namedValues=NamedValues(('onRelease', 0), ('periodically', 1))).clone(namedValues=NamedValues(('onRelease', 0)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileCollectMode.setDescription("An indication of when accounting data is to be written into\n            this file.  Note that in addition to the occasions indicated\n            by the value of this object, an agent always writes\n            information on appropriate connections to the file when the\n            corresponding instance of acctngFileCommand is set to\n            'collectNow'.\n\n              - 'onRelease' - whenever a connection (or possibly,\n                      connection attempt) is terminated, either through\n                      a Release message or through management removal,\n                      information on that connection is written.\n\n              - 'periodically' - information on appropriate connections\n                      is written on the expiry of a periodic timer,\n\n            This value may be modified at any time.")
acctngFileCollectFailedAttempts = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 10), Bits().clone(namedValues=NamedValues(('soft', 0), ('regular', 1))).clone(namedValues=NamedValues(('soft', 0), ('regular', 1)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileCollectFailedAttempts.setDescription("An indication of whether connection data is to be collected\n            for failed connection attempts when the value of the\n            corresponding instance of acctngFileCollectMode includes\n            'onRelease'.  The individual values have the following\n            meaning:\n\n              'soft' - indicates that connection data is to be collected\n            for failed Soft PVCs/PVPs which originate or terminate at\n            the relevant interface.\n\n              'regular' - indicates that connection data is to be\n            collected for failed SVCs, including Soft PVCs/PVPs not\n            originating or terminating at the relevant interface.\n\n            This value may be modified at any time.")
acctngFileInterval = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 11), Integer32().subtype(subtypeSpec=ValueRangeConstraint(60, 86400)).clone(3600)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileInterval.setDescription("The number of seconds between the periodic collections of\n            accounting data when the value of the corresponding instance\n            of acctngFileCollectMode includes 'periodically'.  Some\n            agents may impose restrictions on the range of this\n            interval.  This value may be modified at any time.")
acctngFileMinAge = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 12), Integer32().subtype(subtypeSpec=ValueRangeConstraint(60, 86400)).clone(3600)).setUnits('seconds').setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileMinAge.setDescription("The minimum age of a connection, as used to determine the\n            set of connections for which data is to be collected at the\n            periodic intervals and/or when acctngFileCommand is set to\n            'collectNow'.  The age of a connection is the elapsed time\n            since it was last installed.\n\n            When the periodic interval expires for a file or when\n            acctngFileCommand is set to 'collectNow', accounting data is\n            collected and stored in the file for each connection having\n            a type matching acctngSelectionType and whose age at that\n            time is greater than the value of acctngFileMinAge\n            associated with the file.  This value may be modified at any\n            time.")
acctngFileRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 2, 1, 1, 13), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    acctngFileRowStatus.setDescription("The status of this conceptual row.\n\n            This object can not be set to 'active' until a value has\n            been assigned to the corresponding instance of\n            acctngFileName.  Collection of data into the file does not\n            begin until this object has the value 'active' and one or\n            more (active) instances of acctngSelectionFile refer to it.\n            If this value is modified after a collection has begun,\n            collection into this file terminates and a new (or new\n            version of the) file is immediately made ready for future\n            collection (as if acctngFileCommand had been set to\n            'swapToNewFile'), but collection into the new (or new\n            version of the) file does not begin until the value is\n            subsequently set back to active.")
acctngAdminStatus = MibScalar((1, 3, 6, 1, 2, 1, 60, 1, 3, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled', 1), ('disabled', 2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    acctngAdminStatus.setDescription("A control object to indicate the administratively desired\n            state of the collection of accounting records across all\n            interfaces.\n\n            Modifying the value of acctngAdminStatus to 'disabled' does\n            not remove or change the current configuration as\n            represented by the active rows in the acctngSelectionTable,\n            acctngFileTable and acctngInterfaceTable tables.")
acctngOperStatus = MibScalar((1, 3, 6, 1, 2, 1, 60, 1, 3, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('enabled', 1), ('disabled', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    acctngOperStatus.setDescription("A status object to indicate the operational state of the\n            collection of accounting records across all interfaces.\n\n            When the value of acctngAdminStatus is modified to be\n            'enabled', the value of this object will change to 'enabled'\n            providing it is possible to begin collecting accounting\n            records.\n\n            When the value of acctngAdminStatus is modified to be\n            'disabled', the value of this object will change to\n            'disabled' as soon as the collection of accounting records\n            has terminated.")
acctngProtection = MibScalar((1, 3, 6, 1, 2, 1, 60, 1, 3, 3), TestAndIncr()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    acctngProtection.setDescription("A control object to protect against duplication of control\n            commands.  Over some transport/network protocols, it is\n            possible for SNMP messages to get duplicated.  Such\n            duplication, if it occurred at just the wrong time could\n            cause serious disruption to the collection and retrieval of\n            accounting data, e.g., if a SNMP message setting\n            acctngFileCommand to 'swapToNewFile' were to be duplicated,\n            a whole file of accounting data could be lost.\n\n            To protect against such duplication, a management\n            application should retrieve the value of this object, and\n            include in the Set operation needing protection, a variable\n            binding which sets this object to the retrieved value.")
acctngAgentMode = MibScalar((1, 3, 6, 1, 2, 1, 60, 1, 3, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('swapOnCommand', 1), ('swapOnFull', 2)))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    acctngAgentMode.setDescription("An indication of the behaviour mode of the agent when a\n            file becomes full:\n\n               'swapOnCommand' - the agent does not automatically swap\n                      to a new file; rather, it discards newly collected\n                      data until a management application subsequently\n                      instructs it to swap to a new file.\n\n               'swapOnFull' - the agent terminates collection into the\n                      current file as and when that file becomes full.")
acctngInterfaceTable = MibTable((1, 3, 6, 1, 2, 1, 60, 1, 3, 5))
if mibBuilder.loadTexts:
    acctngInterfaceTable.setDescription('A table controlling the collection of accounting data on\n            specific interfaces of the switch.')
acctngInterfaceEntry = MibTableRow((1, 3, 6, 1, 2, 1, 60, 1, 3, 5, 1)).setIndexNames((0, 'IF-MIB', 'ifIndex'))
if mibBuilder.loadTexts:
    acctngInterfaceEntry.setDescription('An entry which controls whether accounting data is to be\n            collected on an interface.  The types of interfaces which\n            are represented in this table is implementation-specific.')
acctngInterfaceEnable = MibTableColumn((1, 3, 6, 1, 2, 1, 60, 1, 3, 5, 1, 1), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    acctngInterfaceEnable.setDescription('Indicates whether the collection of accounting data is\n            enabled on this interface.')
acctngControlTrapThreshold = MibScalar((1, 3, 6, 1, 2, 1, 60, 1, 4, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 99))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    acctngControlTrapThreshold.setDescription("A percentage of the maximum file size at which a 'nearly-\n            full' trap is generated.  The value of 0 indicates that no\n            'nearly-full' trap is to be generated.")
acctngControlTrapEnable = MibScalar((1, 3, 6, 1, 2, 1, 60, 1, 4, 2), TruthValue()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    acctngControlTrapEnable.setDescription('An indication of whether the acctngFileNearlyFull and\n            acctngFileFull traps are enabled.')
acctngNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 2))
acctngNotifyPrefix = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 2, 0))
acctngFileNearlyFull = NotificationType((1, 3, 6, 1, 2, 1, 60, 2, 0, 1)).setObjects(*(('ACCOUNTING-CONTROL-MIB', 'acctngFileName'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileMaximumSize'), ('ACCOUNTING-CONTROL-MIB', 'acctngControlTrapThreshold'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileNameSuffix')))
if mibBuilder.loadTexts:
    acctngFileNearlyFull.setDescription('An indication that the size of the file into which\n            accounting information is currently being collected has\n            exceeded the threshold percentage of its maximum file size.\n            This notification is generated only at the time of the\n            transition from not-exceeding to exceeding.')
acctngFileFull = NotificationType((1, 3, 6, 1, 2, 1, 60, 2, 0, 2)).setObjects(*(('ACCOUNTING-CONTROL-MIB', 'acctngFileName'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileMaximumSize'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileNameSuffix')))
if mibBuilder.loadTexts:
    acctngFileFull.setDescription("An indication that the size of the file into which\n            accounting information is currently being collected has\n            transistioned to its maximum file size.  This notification\n            is generated (for all values of acctngAgentMode) at the time\n            of the transition from not-full to full.  If acctngAgentMode\n            has the value 'swapOnCommand', it is also generated\n            periodically thereafter until such time as collection of\n            data is no longer inhibited by the file full condition.")
acctngConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 3))
acctngGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 3, 1))
acctngCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 60, 3, 2))
acctngCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 60, 3, 2, 1)).setObjects(*(('ACCOUNTING-CONTROL-MIB', 'acctngBasicGroup'), ('ACCOUNTING-CONTROL-MIB', 'acctngNotificationsGroup')))
if mibBuilder.loadTexts:
    acctngCompliance.setDescription('The compliance statement for switches which implement the\n            Accounting Control MIB.')
acctngBasicGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 60, 3, 1, 1)).setObjects(*(('ACCOUNTING-CONTROL-MIB', 'acctngSelectionSubtree'), ('ACCOUNTING-CONTROL-MIB', 'acctngSelectionList'), ('ACCOUNTING-CONTROL-MIB', 'acctngSelectionFile'), ('ACCOUNTING-CONTROL-MIB', 'acctngSelectionType'), ('ACCOUNTING-CONTROL-MIB', 'acctngSelectionRowStatus'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileName'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileNameSuffix'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileDescription'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileCommand'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileMaximumSize'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileCurrentSize'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileRowStatus'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileFormat'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileCollectMode'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileCollectFailedAttempts'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileInterval'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileMinAge'), ('ACCOUNTING-CONTROL-MIB', 'acctngAdminStatus'), ('ACCOUNTING-CONTROL-MIB', 'acctngOperStatus'), ('ACCOUNTING-CONTROL-MIB', 'acctngProtection'), ('ACCOUNTING-CONTROL-MIB', 'acctngAgentMode'), ('ACCOUNTING-CONTROL-MIB', 'acctngInterfaceEnable'), ('ACCOUNTING-CONTROL-MIB', 'acctngControlTrapThreshold'), ('ACCOUNTING-CONTROL-MIB', 'acctngControlTrapEnable')))
if mibBuilder.loadTexts:
    acctngBasicGroup.setDescription('A collection of objects providing control of the basic\n            collection of accounting data for connection-oriented\n            networks.')
acctngNotificationsGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 60, 3, 1, 2)).setObjects(*(('ACCOUNTING-CONTROL-MIB', 'acctngFileNearlyFull'), ('ACCOUNTING-CONTROL-MIB', 'acctngFileFull')))
if mibBuilder.loadTexts:
    acctngNotificationsGroup.setDescription('The notifications of events relating to controlling the\n            collection of accounting data.')
mibBuilder.exportSymbols('ACCOUNTING-CONTROL-MIB', DataCollectionSubtree=DataCollectionSubtree, acctngInterfaceTable=acctngInterfaceTable, acctngSelectionTable=acctngSelectionTable, acctngMIBObjects=acctngMIBObjects, acctngInterfaceControl=acctngInterfaceControl, acctngSelectionType=acctngSelectionType, acctngFileCurrentSize=acctngFileCurrentSize, acctngNotificationsGroup=acctngNotificationsGroup, acctngFileMinAge=acctngFileMinAge, acctngFileName=acctngFileName, acctngSelectionControl=acctngSelectionControl, acctngSelectionEntry=acctngSelectionEntry, accountingControlMIB=accountingControlMIB, acctngFileRowStatus=acctngFileRowStatus, acctngNotifyPrefix=acctngNotifyPrefix, acctngOperStatus=acctngOperStatus, acctngFileCommand=acctngFileCommand, acctngAdminStatus=acctngAdminStatus, acctngInterfaceEnable=acctngInterfaceEnable, acctngSelectionIndex=acctngSelectionIndex, acctngFileTable=acctngFileTable, acctngFileEntry=acctngFileEntry, acctngFileCollectMode=acctngFileCollectMode, acctngFileInterval=acctngFileInterval, acctngSelectionFile=acctngSelectionFile, acctngNotifications=acctngNotifications, acctngFileFormat=acctngFileFormat, PYSNMP_MODULE_ID=accountingControlMIB, FileIndex=FileIndex, acctngFileMaximumSize=acctngFileMaximumSize, acctngFileControl=acctngFileControl, acctngFileFull=acctngFileFull, acctngControlTrapEnable=acctngControlTrapEnable, acctngGroups=acctngGroups, acctngFileDescription=acctngFileDescription, acctngFileNearlyFull=acctngFileNearlyFull, acctngInterfaceEntry=acctngInterfaceEntry, acctngProtection=acctngProtection, acctngSelectionList=acctngSelectionList, acctngFileNameSuffix=acctngFileNameSuffix, acctngFileCollectFailedAttempts=acctngFileCollectFailedAttempts, acctngControlTrapThreshold=acctngControlTrapThreshold, acctngCompliances=acctngCompliances, acctngAgentMode=acctngAgentMode, acctngTrapControl=acctngTrapControl, DataCollectionList=DataCollectionList, acctngSelectionRowStatus=acctngSelectionRowStatus, acctngCompliance=acctngCompliance, acctngBasicGroup=acctngBasicGroup, acctngSelectionSubtree=acctngSelectionSubtree, acctngFileIndex=acctngFileIndex, acctngConformance=acctngConformance)