# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/SFLOW-MIB.py
# Compiled at: 2016-02-13 18:27:54
(ObjectIdentifier, OctetString, Integer) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'OctetString', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, SingleValueConstraint, ConstraintsIntersection, ValueSizeConstraint, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'SingleValueConstraint', 'ConstraintsIntersection', 'ValueSizeConstraint', 'ValueRangeConstraint')
(InetAddressType, InetAddress) = mibBuilder.importSymbols('INET-ADDRESS-MIB', 'InetAddressType', 'InetAddress')
(OwnerString,) = mibBuilder.importSymbols('RMON-MIB', 'OwnerString')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(NotificationGroup, ModuleCompliance, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance', 'ObjectGroup')
(NotificationType, Counter32, enterprises, TimeTicks, ModuleIdentity, Gauge32, Integer32, Counter64, ObjectIdentity, MibIdentifier, Unsigned32, iso, MibScalar, MibTable, MibTableRow, MibTableColumn, Bits, IpAddress) = mibBuilder.importSymbols('SNMPv2-SMI', 'NotificationType', 'Counter32', 'enterprises', 'TimeTicks', 'ModuleIdentity', 'Gauge32', 'Integer32', 'Counter64', 'ObjectIdentity', 'MibIdentifier', 'Unsigned32', 'iso', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Bits', 'IpAddress')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
sFlowMIB = ModuleIdentity((1, 3, 6, 1, 4, 1, 14706, 1)).setRevisions(('2003-10-18 00:00',
                                                                      '2003-09-24 00:00',
                                                                      '2003-04-08 00:00',
                                                                      '2002-09-17 00:00',
                                                                      '2001-07-31 00:00',
                                                                      '2001-05-01 00:00'))
if mibBuilder.loadTexts:
    sFlowMIB.setLastUpdated('200309240000Z')
if mibBuilder.loadTexts:
    sFlowMIB.setOrganization('sFlow.org')
if mibBuilder.loadTexts:
    sFlowMIB.setContactInfo('Peter Phaal\n                sFlow.org\n                http://www.sflow.org/\n\n                Tel:  +1-415-283-3260\n                Email: peter.phaal@sflow.org')
if mibBuilder.loadTexts:
    sFlowMIB.setDescription('The MIB module for managing the generation and transportation\n                 of sFlow data records.')
sFlowAgent = MibIdentifier((1, 3, 6, 1, 4, 1, 14706, 1, 1))

class SFlowDataSource(ObjectIdentifier, TextualConvention):
    __module__ = __name__


class SFlowInstance(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(1, 65535)


class SFlowReceiver(Integer32, TextualConvention):
    __module__ = __name__


sFlowVersion = MibScalar((1, 3, 6, 1, 4, 1, 14706, 1, 1, 1), SnmpAdminString().clone('1.3;;')).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sFlowVersion.setDescription("Uniquely identifies the version and implementation of this MIB.\n                 The version string must have the following structure:\n                    <MIB Version>;<Organization>;<Software Revision>\n                 where:\n                    <MIB Version>  must be '1.3', the version of this MIB.\n                    <Organization> the name of the organization responsible\n                                     for the agent implementation.\n                    <Revision>     the specific software build of this agent.\n\n                 As an example, the string '1.3;InMon Corp.;2.1.1' indicates\n                 that this agent implements version '1.2' of the SFLOW MIB, that\n                 it was developed by 'InMon Corp.' and that the software build\n                 is '2.1.1'.\n\n                 The MIB Version will change with each revision of the SFLOW\n                 MIB.\n\n                 Management entities must check the MIB Version and not attempt\n                 to manage agents with MIB Versions greater than that for which\n                 they were designed.\n\n                 Note: The sFlow Datagram Format has an independent version\n                       number which may change independently from <MIB Version>.\n                       <MIB Version> applies to the structure and semantics of\n                       the SFLOW MIB only.")
sFlowAgentAddressType = MibScalar((1, 3, 6, 1, 4, 1, 14706, 1, 1, 2), InetAddressType()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sFlowAgentAddressType.setDescription('The address type of the address associated with this agent.\n                 Only ipv4 and ipv6 types are supported.')
sFlowAgentAddress = MibScalar((1, 3, 6, 1, 4, 1, 14706, 1, 1, 3), InetAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    sFlowAgentAddress.setDescription('The IP address associated with this agent. In the case of a\n                 multi-homed agent, this should be the loopback address of the\n                 agent. The sFlowAgent address must provide SNMP connectivity\n                 to the agent. The address should be an invariant that does not\n                 change as interfaces are reconfigured, enabled, disabled,\n                 added or removed. A manager should be able to use the \n                 sFlowAgentAddress as a unique key that will identify this\n                 agent over extended periods of time so that a history can\n                 be maintained.')
sFlowRcvrTable = MibTable((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4))
if mibBuilder.loadTexts:
    sFlowRcvrTable.setDescription('A table of the receivers of sFlow information.')
sFlowRcvrEntry = MibTableRow((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1)).setIndexNames((0,
                                                                                   'SFLOW-MIB',
                                                                                   'sFlowRcvrIndex'))
if mibBuilder.loadTexts:
    sFlowRcvrEntry.setDescription('Attributes of an sFlow Receiver.')
sFlowRcvrIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 65535)))
if mibBuilder.loadTexts:
    sFlowRcvrIndex.setDescription('Index into sFlowReceiverTable.')
sFlowRcvrOwner = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1, 2), OwnerString()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowRcvrOwner.setDescription('The entity making use of this sFlowRcvrTable entry. The empty\n                 string indicates that the entry is currently unclaimed.\n                 An entity wishing to claim an sFlowRcvrTable entry must ensure\n                 that the entry is unclaimed before trying to claim it.\n                 The entry is claimed by setting the owner string. The entry\n                 must be claimed before any changes can be made to other sampler\n                 objects.\n\n                 In order to avoid a race condition, the entity taking control\n                 of the sampler must set both the owner and a value for\n                 sFlowRcvrTimeout in the same SNMP set request.\n\n                 When a management entity is finished using the sampler,\n                 it should set the value of sFlowRcvrOwner back to unclaimed. \n                 The agent must restore all other entities this row to their\n                 default values when the owner is set to unclaimed. It must\n                 also free all other resources associated with this \n                 sFlowRcvrTable entry.\n\n                 This mechanism provides no enforcement and relies on the\n                 cooperation of management entities in order to ensure that\n                 competition for a receiver entry is fairly resolved.')
sFlowRcvrTimeout = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1, 3), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowRcvrTimeout.setDescription('The time (in seconds) remaining before the sampler is released\n                 and stops sampling. When set, the owner establishes control\n                 for the specified period. When read, the remaining time in the\n                 interval is returned.\n\n                 A management entity wanting to maintain control of the sampler\n                 is responsible for setting a new value before the old one\n                 expires.\n\n                 When the interval expires, the agent is responsible for \n                 restoring all other entities in this row to their default \n                 values. It must also free all other resources associated with\n                 this sFlowRcvrTable entry.')
sFlowRcvrMaximumDatagramSize = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1,
                                               4), Integer32().clone(1400)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowRcvrMaximumDatagramSize.setDescription('The maximum number of data bytes that can be sent in a single\n                  sample datagram. The manager should set this value to avoid\n                  fragmentation of the sFlow datagrams.')
sFlowRcvrAddressType = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1, 5), InetAddressType().clone('ipv4')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowRcvrAddressType.setDescription('The type of sFlowRcvrCollectorAddress.')
sFlowRcvrAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1, 6), InetAddress().clone(hexValue='00000000')).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowRcvrAddress.setDescription('The IP address of the sFlow collector.\n                 If set to 0.0.0.0 not sFlow datagrams will be sent.')
sFlowRcvrPort = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1, 7), Integer32().clone(6343)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowRcvrPort.setDescription('The destination port for sFlow datagrams.')
sFlowRcvrDatagramVersion = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 4, 1, 8), Integer32().clone(5)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowRcvrDatagramVersion.setDescription('The version of sFlow datagrams that should be sent.\n\n                 When set to a value not support by the agent, the agent should\n                 adjust the value to the highest supported value less than the\n                 requested value, or return an SNMP bad value error if no \n                 such value exists.')
sFlowFsTable = MibTable((1, 3, 6, 1, 4, 1, 14706, 1, 1, 5))
if mibBuilder.loadTexts:
    sFlowFsTable.setDescription('A table of the flow samplers within a device.')
sFlowFsEntry = MibTableRow((1, 3, 6, 1, 4, 1, 14706, 1, 1, 5, 1)).setIndexNames((0,
                                                                                 'SFLOW-MIB',
                                                                                 'sFlowFsDataSource'), (0,
                                                                                                        'SFLOW-MIB',
                                                                                                        'sFlowFsInstance'))
if mibBuilder.loadTexts:
    sFlowFsEntry.setDescription('Attributes of a flow sampler.')
sFlowFsDataSource = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 5, 1, 1), SFlowDataSource())
if mibBuilder.loadTexts:
    sFlowFsDataSource.setDescription('sFlowDataSource for this flow sampler.')
sFlowFsInstance = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 5, 1, 2), SFlowInstance())
if mibBuilder.loadTexts:
    sFlowFsInstance.setDescription('The sFlow instance for this flow sampler.')
sFlowFsReceiver = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 5, 1, 3), SFlowReceiver()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowFsReceiver.setDescription('The SFlowReceiver for this flow sampler.')
sFlowFsPacketSamplingRate = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 5, 1, 4), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowFsPacketSamplingRate.setDescription('The statistical sampling rate for packet sampling from this\n                 source. \n\n                 Set to N to sample 1/Nth of the packets in the monitored flows.\n                 An agent should choose its own algorithm to introduce variance\n                 into the sampling so that exactly every Nth packet is not\n                 counted. A sampling rate of 1 counts all packets. A sampling\n                 rate of 0 disables sampling.\n                 \n                 The agent is permitted to have minimum and maximum allowable\n                 values for the sampling rate. A minimum rate lets the agent\n                 designer set an upper bound on the overhead associated with\n                 sampling, and a maximum rate may be the result of hardware\n                 restrictions (such as counter size). In addition not all values\n                 between the maximum and minimum may be realizable as the \n                 sampling rate (again because of implementation considerations).\n\n                 When the sampling rate is set the agent is free to adjust the\n                 value so that it lies between the maximum and minimum values\n                 and has the closest achievable value.\n\n                 When read, the agent must return the actual sampling rate it\n                 will be using (after the adjustments previously described). The\n                 sampling algorithm must converge so that over time the number\n                 of packets sampled approaches 1/Nth of the total number of\n                 packets in the monitored flows.')
sFlowFsMaximumHeaderSize = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 5, 1, 5), Integer32().clone(128)).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowFsMaximumHeaderSize.setDescription('The maximum number of bytes that should be copied from a\n                 sampled packet. The agent may have an internal maximum and\n                 minimum permissible sizes. If an attempt is made to set this \n                 value outside the permissible range then the agent should \n                 adjust the value to the closest permissible value.')
sFlowCpTable = MibTable((1, 3, 6, 1, 4, 1, 14706, 1, 1, 6))
if mibBuilder.loadTexts:
    sFlowCpTable.setDescription('A table of the counter pollers within a device.')
sFlowCpEntry = MibTableRow((1, 3, 6, 1, 4, 1, 14706, 1, 1, 6, 1)).setIndexNames((0,
                                                                                 'SFLOW-MIB',
                                                                                 'sFlowCpDataSource'), (0,
                                                                                                        'SFLOW-MIB',
                                                                                                        'sFlowCpInstance'))
if mibBuilder.loadTexts:
    sFlowCpEntry.setDescription('Attributes of a counter poller.')
sFlowCpDataSource = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 6, 1, 1), SFlowDataSource())
if mibBuilder.loadTexts:
    sFlowCpDataSource.setDescription('Identifies the source of the data for the counter poller.')
sFlowCpInstance = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 6, 1, 2), SFlowInstance())
if mibBuilder.loadTexts:
    sFlowCpInstance.setDescription('The sFlowInstance for this counter poller.')
sFlowCpReceiver = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 6, 1, 3), SFlowReceiver()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowCpReceiver.setDescription('The SFlowReciever associated with this counter poller.')
sFlowCpInterval = MibTableColumn((1, 3, 6, 1, 4, 1, 14706, 1, 1, 6, 1, 4), Integer32()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    sFlowCpInterval.setDescription('The maximum number of seconds between successive samples of the\n                 counters associated with this data source. A sampling interval \n                 of 0 disables counter sampling.\n\n                 The agent is permitted to have minimum and maximum allowable\n                 values for the counter polling interval. A minimum interval\n                 lets the agent designer set an upper bound on the overhead\n                 associated with polling, and a maximum interval may be the\n                 result of implementation restrictions (such as counter size).\n                 In addition not all values between the maximum and minimum may\n                 be realizable as the sampling interval (again because of\n                 implementation considerations).\n\n                 When the sampling rate is set the agent is free to adjust the\n                 value so that it lies between the maximum and minimum values\n                 and has the closest achievable value.\n\n                 When read, the agent must return the actual sampling interval\n                 it will be using (after the adjustments previously described).\n                 The sampling algorithm must converge so that over time the\n                 number of packets sampled approaches 1/Nth of the total number\n                 of packets in the monitored flows.')
sFlowMIBConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 14706, 1, 2))
sFlowMIBGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 14706, 1, 2, 1))
sFlowMIBCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 14706, 1, 2, 2))
sFlowCompliance = ModuleCompliance((1, 3, 6, 1, 4, 1, 14706, 1, 2, 2, 1)).setObjects(*(('SFLOW-MIB', 'sFlowAgentGroup'), ))
if mibBuilder.loadTexts:
    sFlowCompliance.setDescription('Compliance statements for the sFlow Agent.')
sFlowAgentGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 14706, 1, 2, 1, 1)).setObjects(*(('SFLOW-MIB', 'sFlowVersion'), ('SFLOW-MIB', 'sFlowAgentAddressType'), ('SFLOW-MIB', 'sFlowAgentAddress'), ('SFLOW-MIB', 'sFlowRcvrOwner'), ('SFLOW-MIB', 'sFlowRcvrTimeout'), ('SFLOW-MIB', 'sFlowRcvrMaximumDatagramSize'), ('SFLOW-MIB', 'sFlowRcvrAddressType'), ('SFLOW-MIB', 'sFlowRcvrAddress'), ('SFLOW-MIB', 'sFlowRcvrPort'), ('SFLOW-MIB', 'sFlowRcvrDatagramVersion'), ('SFLOW-MIB', 'sFlowFsReceiver'), ('SFLOW-MIB', 'sFlowFsPacketSamplingRate'), ('SFLOW-MIB', 'sFlowFsMaximumHeaderSize'), ('SFLOW-MIB', 'sFlowCpReceiver'), ('SFLOW-MIB', 'sFlowCpInterval')))
if mibBuilder.loadTexts:
    sFlowAgentGroup.setDescription('A collection of objects for managing the generation and\n                  transportation of sFlow data records.')
mibBuilder.exportSymbols('SFLOW-MIB', sFlowAgent=sFlowAgent, sFlowVersion=sFlowVersion, sFlowMIB=sFlowMIB, SFlowReceiver=SFlowReceiver, sFlowRcvrPort=sFlowRcvrPort, sFlowCpTable=sFlowCpTable, sFlowMIBConformance=sFlowMIBConformance, sFlowRcvrEntry=sFlowRcvrEntry, sFlowFsMaximumHeaderSize=sFlowFsMaximumHeaderSize, sFlowCompliance=sFlowCompliance, sFlowRcvrAddressType=sFlowRcvrAddressType, sFlowAgentAddressType=sFlowAgentAddressType, sFlowRcvrIndex=sFlowRcvrIndex, sFlowRcvrDatagramVersion=sFlowRcvrDatagramVersion, sFlowAgentAddress=sFlowAgentAddress, sFlowCpDataSource=sFlowCpDataSource, SFlowDataSource=SFlowDataSource, sFlowFsTable=sFlowFsTable, sFlowRcvrAddress=sFlowRcvrAddress, sFlowCpReceiver=sFlowCpReceiver, sFlowMIBCompliances=sFlowMIBCompliances, SFlowInstance=SFlowInstance, sFlowRcvrTable=sFlowRcvrTable, sFlowCpEntry=sFlowCpEntry, sFlowCpInterval=sFlowCpInterval, sFlowFsInstance=sFlowFsInstance, sFlowFsPacketSamplingRate=sFlowFsPacketSamplingRate, sFlowAgentGroup=sFlowAgentGroup, sFlowRcvrOwner=sFlowRcvrOwner, sFlowRcvrMaximumDatagramSize=sFlowRcvrMaximumDatagramSize, sFlowFsEntry=sFlowFsEntry, sFlowFsReceiver=sFlowFsReceiver, sFlowFsDataSource=sFlowFsDataSource, PYSNMP_MODULE_ID=sFlowMIB, sFlowMIBGroups=sFlowMIBGroups, sFlowCpInstance=sFlowCpInstance, sFlowRcvrTimeout=sFlowRcvrTimeout)