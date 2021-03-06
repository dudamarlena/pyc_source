# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/HPR-IP-MIB.py
# Compiled at: 2016-02-13 18:15:28
(SnaControlPointName,) = mibBuilder.importSymbols('APPN-MIB', 'SnaControlPointName')
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, ConstraintsIntersection, ValueSizeConstraint, SingleValueConstraint, ValueRangeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'ConstraintsIntersection', 'ValueSizeConstraint', 'SingleValueConstraint', 'ValueRangeConstraint')
(hprObjects, hprGroups, hprCompliances) = mibBuilder.importSymbols('HPR-MIB', 'hprObjects', 'hprGroups', 'hprCompliances')
(NotificationGroup, ObjectGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ObjectGroup', 'ModuleCompliance')
(Counter64, TimeTicks, NotificationType, Bits, Counter32, ObjectIdentity, Integer32, Gauge32, MibIdentifier, ModuleIdentity, IpAddress, iso, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32) = mibBuilder.importSymbols('SNMPv2-SMI', 'Counter64', 'TimeTicks', 'NotificationType', 'Bits', 'Counter32', 'ObjectIdentity', 'Integer32', 'Gauge32', 'MibIdentifier', 'ModuleIdentity', 'IpAddress', 'iso', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Unsigned32')
(RowStatus, TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'RowStatus', 'TextualConvention', 'DisplayString')
hprIp = ModuleIdentity((1, 3, 6, 1, 2, 1, 34, 6, 1, 5)).setRevisions(('1998-09-24 00:00', ))
if mibBuilder.loadTexts:
    hprIp.setLastUpdated('9809240000Z')
if mibBuilder.loadTexts:
    hprIp.setOrganization('IETF SNA NAU MIB WG / AIW APPN MIBs SIG')
if mibBuilder.loadTexts:
    hprIp.setContactInfo('\n               Bob Clouston\n               Cisco Systems\n               7025 Kit Creek Road\n               P.O. Box 14987\n               Research Triangle Park, NC 27709, USA\n               Tel:    1 919 472 2333\n               E-mail: clouston@cisco.com\n\n               Bob Moore\n               IBM Corporation\n               4205 S. Miami Boulevard\n               BRQA/501\n               P.O. Box 12195\n               Research Triangle Park, NC 27709, USA\n               Tel:    1 919 254 4436\n               E-mail: remoore@us.ibm.com\n       ')
if mibBuilder.loadTexts:
    hprIp.setDescription('The MIB module for HPR over IP.  This module contains two\n       groups:\n\n        -  the HPR over IP Monitoring Group provides a count of the UDP\n           packets sent by a link station for each APPN traffic type.\n\n        -  the HPR over IP Configuration Group provides for reading and\n           setting the mappings between APPN traffic types and TOS\n           Precedence settings in the IP header.  These mappings are\n           configured at the APPN port level, and are inherited by the\n           APPN connection networks and link stations associated with an\n           APPN port.  A port-level mapping can, however, be overridden\n           for a particular connection network or link station.')

class AppnTrafficType(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))
    namedValues = NamedValues(('low', 1), ('medium', 2), ('high', 3), ('network', 4), ('llcAndFnRoutedNlp',
                                                                                       5))


class AppnTOSPrecedence(DisplayString, TextualConvention):
    __module__ = __name__
    subtypeSpec = DisplayString.subtypeSpec + ValueSizeConstraint(3, 3)
    fixedLength = 3


hprIpActiveLsTable = MibTable((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 1))
if mibBuilder.loadTexts:
    hprIpActiveLsTable.setDescription('The HPR/IP active link station table.  This table provides\n          counts of the number of UDP packets sent for each APPN\n          traffic type.')
hprIpActiveLsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 1, 1)).setIndexNames((0,
                                                                                       'HPR-IP-MIB',
                                                                                       'hprIpActiveLsLsName'), (0,
                                                                                                                'HPR-IP-MIB',
                                                                                                                'hprIpActiveLsAppnTrafficType'))
if mibBuilder.loadTexts:
    hprIpActiveLsEntry.setDescription('Entry of the HPR/IP link station table.')
hprIpActiveLsLsName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 1, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10)))
if mibBuilder.loadTexts:
    hprIpActiveLsLsName.setDescription('Administratively assigned name for the link station.  If this\n          object has the same value as the appnLsName in the APPN MIB,\n          then the two objects are referring to the same APPN link\n          station.')
hprIpActiveLsAppnTrafficType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 1, 1,
                                               2), AppnTrafficType())
if mibBuilder.loadTexts:
    hprIpActiveLsAppnTrafficType.setDescription('APPN traffic type being sent through the link station.')
hprIpActiveLsUdpPackets = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 1, 1, 3), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    hprIpActiveLsUdpPackets.setDescription('The count of outgoing UDP packets carrying this type of APPN\n          traffic.  A discontinuity in the counter is indicated by the\n          appnLsCounterDisconTime object in the APPN MIB.')
hprIpAppnPortTable = MibTable((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 2))
if mibBuilder.loadTexts:
    hprIpAppnPortTable.setDescription('The HPR/IP APPN port table.  This table supports reading and\n          setting the mapping between APPN traffic types and TOS\n          Precedence settings for all the link stations at this APPN\n          port.  This mapping can be overridden for an individual link\n          station or an individual connection network via, respectively,\n          the hprIpLsTOSPrecedence and the hprIpCnTOSPrecedence objects.')
hprIpAppnPortEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 2, 1)).setIndexNames((0,
                                                                                       'HPR-IP-MIB',
                                                                                       'hprIpAppnPortName'), (0,
                                                                                                              'HPR-IP-MIB',
                                                                                                              'hprIpAppnPortAppnTrafficType'))
if mibBuilder.loadTexts:
    hprIpAppnPortEntry.setDescription('Entry of the HPR/IP APPN port table.  Entries exist for\n          every APPN port defined to support HPR over IP.')
hprIpAppnPortName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 2, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10)))
if mibBuilder.loadTexts:
    hprIpAppnPortName.setDescription('Administratively assigned name for this APPN port.  If this\n          object has the same value as the appnPortName in the APPN MIB,\n          then the two objects are referring to the same APPN port.')
hprIpAppnPortAppnTrafficType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 2, 1,
                                               2), AppnTrafficType())
if mibBuilder.loadTexts:
    hprIpAppnPortAppnTrafficType.setDescription('APPN traffic type sent through the port.')
hprIpAppnPortTOSPrecedence = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 2, 1, 3), AppnTOSPrecedence()).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    hprIpAppnPortTOSPrecedence.setDescription('A setting for the three TOS Precedence bits in the IP Type of\n          Service field for this APPN traffic type.\n\n          When this value is changed via a Set operation, the new setting\n          for the TOS Precedence bits takes effect immediately, rather\n          than waiting for some event such as reinitialization of the\n          port or of the APPN node itself.')
hprIpLsTable = MibTable((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 3))
if mibBuilder.loadTexts:
    hprIpLsTable.setDescription('The HPR/IP link station table.  Values for TOS Precedence at\n          the link station level override those at the level of the\n          containing port.  If there is no entry in this table for a\n          given link station, then that link station inherits its TOS\n          Precedence values from its port.')
hprIpLsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 3, 1)).setIndexNames((0,
                                                                                 'HPR-IP-MIB',
                                                                                 'hprIpLsLsName'), (0,
                                                                                                    'HPR-IP-MIB',
                                                                                                    'hprIpLsAppnTrafficType'))
if mibBuilder.loadTexts:
    hprIpLsEntry.setDescription('Entry of the HPR/IP link station table.')
hprIpLsLsName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 3, 1, 1), DisplayString().subtype(subtypeSpec=ValueSizeConstraint(1, 10)))
if mibBuilder.loadTexts:
    hprIpLsLsName.setDescription('Administratively assigned name for the link station.  If this\n          object has the same value as the appnLsName in the APPN MIB,\n          then the two objects are referring to the same APPN link\n          station.')
hprIpLsAppnTrafficType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 3, 1, 2), AppnTrafficType())
if mibBuilder.loadTexts:
    hprIpLsAppnTrafficType.setDescription('APPN traffic type sent through the link station.')
hprIpLsTOSPrecedence = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 3, 1, 3), AppnTOSPrecedence()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hprIpLsTOSPrecedence.setDescription('A setting for the three TOS Precedence bits in the IP Type of\n          Service field for this APPN traffic type.\n\n          When this value is changed via a Set operation, the new setting\n          for the TOS Precedence bits takes effect immediately, rather\n          than waiting for some event such as reinitialization of the\n          port or of the APPN node itself.')
hprIpLsRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 3, 1, 4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hprIpLsRowStatus.setDescription("This object allows entries to be created and deleted in the\n          hprIpLsTable.  As soon as an entry becomes active, the mapping\n          between APPN traffic types and TOS Precedence settings that it\n          specifies becomes effective.\n\n          The value of the other accessible object in this entry,\n          hprIpLsTOSPrecedence, can be changed via a Set operation when\n          this object's value is active(1).\n\n          An entry in this table is deleted by setting this object to\n          destroy(6).  Deleting an entry in this table causes the\n          link station to revert to the default TOS Precedence\n          mapping for its port.")
hprIpCnTable = MibTable((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 4))
if mibBuilder.loadTexts:
    hprIpCnTable.setDescription('The HPR/IP connection network table.  Values for TOS\n          Precedence at the connection network level override those at\n          the level of the containing port.  If there is no entry in\n          this table for a given connection network, then that\n          connection network inherits its TOS Precedence values from\n          its port.\n\n          A node may have connections to a given connection network\n          through multiple ports.  There is no provision in the HPR-IP\n          architecture for variations in TOS Precedence values for\n          a single connection network based on the port through which\n          traffic is flowing to the connection network.  Thus an entry\n          in this table overrides the port-level settings for all the\n          ports through which the node can reach the connection\n          network.')
hprIpCnEntry = MibTableRow((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 4, 1)).setIndexNames((0,
                                                                                 'HPR-IP-MIB',
                                                                                 'hprIpCnVrnName'), (0,
                                                                                                     'HPR-IP-MIB',
                                                                                                     'hprIpCnAppnTrafficType'))
if mibBuilder.loadTexts:
    hprIpCnEntry.setDescription('Entry of the HPR/IP connection network table.')
hprIpCnVrnName = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 4, 1, 1), SnaControlPointName())
if mibBuilder.loadTexts:
    hprIpCnVrnName.setDescription('SNA control point name of the virtual routing node (VRN) that\n          identifies the connection network in the APPN topology\n          database.  If this object has the same value as the appnVrnName\n          in the APPN MIB, then the two objects are referring\n          to the same APPN VRN.')
hprIpCnAppnTrafficType = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 4, 1, 2), AppnTrafficType())
if mibBuilder.loadTexts:
    hprIpCnAppnTrafficType.setDescription('APPN traffic type sent to this connection network.')
hprIpCnTOSPrecedence = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 4, 1, 3), AppnTOSPrecedence()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hprIpCnTOSPrecedence.setDescription('A setting for the three TOS Precedence bits in the IP Type of\n          Service field for this APPN traffic type.  This setting applies\n          to all traffic sent to this connection network by this node,\n          regardless of the port through which the traffic is sent.\n\n          When this value is changed via a Set operation, the new setting\n          for the TOS Precedence bits takes effect immediately, rather\n          than waiting for some event such as reinitialization of a\n          port or of the APPN node itself.')
hprIpCnRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 34, 6, 1, 5, 4, 1, 4), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    hprIpCnRowStatus.setDescription("This object allows entries to be created and deleted in the\n          hprIpCnTable.  As soon as an entry becomes active, the mapping\n          between APPN traffic types and TOS Precedence settings that it\n          specifies becomes effective.\n\n          The value of the other accessible object in this entry,\n          hprIpCnTOSPrecedence, can be changed via a Set operation when\n          this object's value is active(1).\n\n          An entry in this table is deleted by setting this object to\n          destroy(6).  Deleting an entry in this table causes the\n          connection network to revert to the default TOS Precedence\n          mapping for each port through which it is accessed.")
hprIpCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 34, 6, 2, 1, 2)).setObjects(*(('HPR-IP-MIB', 'hprIpMonitoringGroup'), ('HPR-IP-MIB', 'hprIpConfigurationGroup')))
if mibBuilder.loadTexts:
    hprIpCompliance.setDescription('Compliance statement for the HPR over IP MIB module.')
hprIpMonitoringGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 6, 2, 2, 5)).setObjects(*(('HPR-IP-MIB', 'hprIpActiveLsUdpPackets'), ))
if mibBuilder.loadTexts:
    hprIpMonitoringGroup.setDescription('An object for counting outgoing HPR/IP traffic for each APPN\n          traffic type.')
hprIpConfigurationGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 34, 6, 2, 2, 6)).setObjects(*(('HPR-IP-MIB', 'hprIpAppnPortTOSPrecedence'), ('HPR-IP-MIB', 'hprIpLsTOSPrecedence'), ('HPR-IP-MIB', 'hprIpLsRowStatus'), ('HPR-IP-MIB', 'hprIpCnTOSPrecedence'), ('HPR-IP-MIB', 'hprIpCnRowStatus')))
if mibBuilder.loadTexts:
    hprIpConfigurationGroup.setDescription('A collection of HPR/IP objects representing the mappings\n          between APPN traffic types and TOS Precedence bits at the APPN\n          port, APPN link station, and APPN connection network levels.')
mibBuilder.exportSymbols('HPR-IP-MIB', hprIpLsTOSPrecedence=hprIpLsTOSPrecedence, hprIpAppnPortTOSPrecedence=hprIpAppnPortTOSPrecedence, hprIpLsRowStatus=hprIpLsRowStatus, hprIpCompliance=hprIpCompliance, hprIpAppnPortName=hprIpAppnPortName, hprIpActiveLsEntry=hprIpActiveLsEntry, hprIpAppnPortTable=hprIpAppnPortTable, hprIpLsTable=hprIpLsTable, hprIpCnAppnTrafficType=hprIpCnAppnTrafficType, hprIpCnVrnName=hprIpCnVrnName, hprIpCnTable=hprIpCnTable, PYSNMP_MODULE_ID=hprIp, hprIpActiveLsLsName=hprIpActiveLsLsName, hprIpCnEntry=hprIpCnEntry, hprIpConfigurationGroup=hprIpConfigurationGroup, hprIpCnRowStatus=hprIpCnRowStatus, AppnTrafficType=AppnTrafficType, hprIpMonitoringGroup=hprIpMonitoringGroup, hprIpActiveLsUdpPackets=hprIpActiveLsUdpPackets, hprIpActiveLsAppnTrafficType=hprIpActiveLsAppnTrafficType, hprIpLsEntry=hprIpLsEntry, hprIpLsAppnTrafficType=hprIpLsAppnTrafficType, hprIpAppnPortAppnTrafficType=hprIpAppnPortAppnTrafficType, hprIpCnTOSPrecedence=hprIpCnTOSPrecedence, hprIpLsLsName=hprIpLsLsName, hprIpAppnPortEntry=hprIpAppnPortEntry, AppnTOSPrecedence=AppnTOSPrecedence, hprIpActiveLsTable=hprIpActiveLsTable, hprIp=hprIp)