# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/IPSEC-SPD-MIB.py
# Compiled at: 2016-02-13 18:18:27
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, SingleValueConstraint, ConstraintsIntersection, ConstraintsUnion, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'SingleValueConstraint', 'ConstraintsIntersection', 'ConstraintsUnion', 'ValueSizeConstraint')
(IfDirection, diffServMIBMultiFieldClfrGroup, diffServMultiFieldClfrNextFree) = mibBuilder.importSymbols('DIFFSERV-MIB', 'IfDirection', 'diffServMIBMultiFieldClfrGroup', 'diffServMultiFieldClfrNextFree')
(InterfaceIndex,) = mibBuilder.importSymbols('IF-MIB', 'InterfaceIndex')
(InetAddress, InetAddressType) = mibBuilder.importSymbols('INET-ADDRESS-MIB', 'InetAddress', 'InetAddressType')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(ModuleCompliance, NotificationGroup, ObjectGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup', 'ObjectGroup')
(Bits, Counter64, TimeTicks, iso, ModuleIdentity, mib_2, NotificationType, MibScalar, MibTable, MibTableRow, MibTableColumn, Gauge32, ObjectIdentity, Integer32, MibIdentifier, Counter32, Unsigned32, IpAddress) = mibBuilder.importSymbols('SNMPv2-SMI', 'Bits', 'Counter64', 'TimeTicks', 'iso', 'ModuleIdentity', 'mib-2', 'NotificationType', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Gauge32', 'ObjectIdentity', 'Integer32', 'MibIdentifier', 'Counter32', 'Unsigned32', 'IpAddress')
(StorageType, TruthValue, TimeStamp, RowStatus, VariablePointer, DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'StorageType', 'TruthValue', 'TimeStamp', 'RowStatus', 'VariablePointer', 'DisplayString', 'TextualConvention')
spdMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 153)).setRevisions(('2007-02-07 00:00',))
if mibBuilder.loadTexts:
    spdMIB.setLastUpdated('200702070000Z')
if mibBuilder.loadTexts:
    spdMIB.setOrganization('IETF IP Security Policy Working Group')
if mibBuilder.loadTexts:
    spdMIB.setContactInfo('Michael Baer\n                  P.O. Box 72682\n                  Davis, CA 95617\n                  Phone: +1 530 902 3131\n                  Email: baerm@tislabs.com\n\n                  Ricky Charlet\n                  Email: rcharlet@alumni.calpoly.edu\n\n                  Wes Hardaker\n                  Sparta, Inc.\n                  P.O. Box 382\n                  Davis, CA  95617\n                  Phone: +1 530 792 1913\n                  Email: hardaker@tislabs.com\n\n                  Robert Story\n                  Revelstone Software\n                  PO Box 1812\n\n\n\n                  Tucker, GA 30085\n                  Phone: +1 770 617 3722\n                  Email: rstory@ipsp.revelstone.com\n\n                  Cliff Wang\n                  ARO\n                  4300 S. Miami Blvd.\n                  Durham, NC 27703\n                  E-Mail: cliffwangmail@yahoo.com')
if mibBuilder.loadTexts:
    spdMIB.setDescription('This MIB module defines configuration objects for managing\n      IPsec Security Policies.  In general, this MIB can be\n      implemented anywhere IPsec security services exist (e.g.,\n      bump-in-the-wire, host, gateway, firewall, router, etc.).\n\n      Copyright (C) The IETF Trust (2007).  This version of\n      this MIB module is part of RFC 4807; see the RFC itself for\n      full legal notices.')
spdConfigObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 1))
spdNotificationObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 2))
spdConformanceObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 3))
spdActions = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 4))

class SpdBooleanOperator(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('or', 1), ('and', 2))


class SpdAdminStatus(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('enabled', 1), ('disabled', 2))


class SpdIPPacketLogging(Integer32, TextualConvention):
    __module__ = __name__
    displayHint = 'd'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(-1, 65535)


class SpdTimePeriod(OctetString, TextualConvention):
    __module__ = __name__
    displayHint = '31t'
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 31)


spdLocalConfigObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 1, 1))
spdIngressPolicyGroupName = MibScalar((1, 3, 6, 1, 2, 1, 153, 1, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    spdIngressPolicyGroupName.setDescription("This object indicates the global system policy group that\n        is to be applied on ingress packets (i.e., arriving at an\n        interface from a network) when a given endpoint does not\n        contain a policy definition in the spdEndpointToGroupTable.\n        Its value can be used as an index into the\n        spdGroupContentsTable to retrieve a list of policies.  A\n        zero length string indicates that no system-wide policy exists\n        and the default policy of 'drop' SHOULD be executed for\n        ingress packets until one is imposed by either this object\n        or by the endpoint processing a given packet.\n\n        This object MUST be persistent")
spdEgressPolicyGroupName = MibScalar((1, 3, 6, 1, 2, 1, 153, 1, 1, 2), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    spdEgressPolicyGroupName.setDescription("This object indicates the policy group containing the\n         global system policy that is to be applied on egress\n         packets (i.e., packets leaving an interface and entering a\n         network) when a given endpoint does not contain a policy\n         definition in the spdEndpointToGroupTable.  Its value can\n         be used as an index into the spdGroupContentsTable to\n         retrieve a list of policies.  A zero length string\n         indicates that no system-wide policy exists and the default\n         policy of 'drop' SHOULD be executed for egress packets\n         until one is imposed by either this object or by the\n         endpoint processing a given packet.\n\n         This object MUST be persistent")
spdEndpointToGroupTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 2))
if mibBuilder.loadTexts:
    spdEndpointToGroupTable.setDescription('This table maps policies (groupings) onto an endpoint\n         (interface).  A policy group assigned to an endpoint is then\n         used to control access to the network traffic passing\n         through that endpoint.\n\n\n\n\n         If an endpoint has been configured with a policy group and\n         no rule within that policy group matches that packet, the\n         default action in this case SHALL be to drop the packet.\n\n         If no policy group has been assigned to an endpoint, then\n         the policy group specified by spdIngressPolicyGroupName MUST\n         be used on traffic inbound from the network through that\n         endpoint, and the policy group specified by\n         spdEgressPolicyGroupName MUST be used for traffic outbound\n         to the network through that endpoint.')
spdEndpointToGroupEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 2, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdEndGroupDirection'), (0, 'IPSEC-SPD-MIB', 'spdEndGroupInterface'))
if mibBuilder.loadTexts:
    spdEndpointToGroupEntry.setDescription('A mapping assigning a policy group to an endpoint.')
spdEndGroupDirection = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 2, 1, 1), IfDirection())
if mibBuilder.loadTexts:
    spdEndGroupDirection.setDescription('This object indicates which direction of packets crossing\n         the interface are associated with which spdEndGroupName\n         object.  Ingress packets, or packets into the device match\n         when this value is inbound(1).  Egress packets or packets\n         out of the device match when this value is outbound(2).')
spdEndGroupInterface = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 2, 1, 2), InterfaceIndex())
if mibBuilder.loadTexts:
    spdEndGroupInterface.setDescription("This value matches the IF-MIB's ifTable's ifIndex column\n         and indicates the interface associated with a given\n         endpoint.  This object can be used to uniquely identify an\n         endpoint that a set of policy groups are applied to.")
spdEndGroupName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 2, 1, 3), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdEndGroupName.setDescription('The policy group name to apply at this endpoint.  The\n         value of the spdEndGroupName object is then used as an\n         index into the spdGroupContentsTable to come up with a list\n         of rules that MUST be applied at this endpoint.')
spdEndGroupLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 2, 1, 4), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdEndGroupLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdEndGroupStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 2, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdEndGroupStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a storage\n         type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdEndGroupRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 2, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdEndGroupRowStatus.setDescription("This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         This object is considered 'notReady' and MUST NOT be set to\n         active until one or more active rows exist within the\n         spdGroupContentsTable for the group referenced by the\n         spdEndGroupName object.")
spdGroupContentsTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 3))
if mibBuilder.loadTexts:
    spdGroupContentsTable.setDescription("This table contains a list of rules and/or subgroups\n         contained within a given policy group.  For a given value\n         of spdGroupContName, the set of rows sharing that value\n         forms a 'group'.  The rows in a group MUST be processed\n         according to the value of the spdGroupContPriority object\n         in each row.  The processing MUST be executed starting with\n         the lowest value of spdGroupContPriority and in ascending\n         order thereafter.\n\n         If an action is executed as the result of the processing of\n         a row in a group, the processing of further rows in that\n         group MUST stop.  Iterating to the next policy group row by\n         finding the next largest spdGroupContPriority object SHALL\n         only be done if no actions were run while processing the\n         current row for a given packet.")
spdGroupContentsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 3, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdGroupContName'), (0, 'IPSEC-SPD-MIB', 'spdGroupContPriority'))
if mibBuilder.loadTexts:
    spdGroupContentsEntry.setDescription('Defines a given sub-component within a policy group.  A\n         sub-component is either a rule or another group as\n         indicated by spdGroupContComponentType and referenced by\n         spdGroupContComponentName.')
spdGroupContName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    spdGroupContName.setDescription("The administrative name of the group associated with this\n        row.  A 'group' is formed by all the rows in this table that\n        have the same value of this object.")
spdGroupContPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)))
if mibBuilder.loadTexts:
    spdGroupContPriority.setDescription('The priority (sequence number) of the sub-component in\n         a group that this row represents.  This value indicates\n         the order that each row of this table MUST be processed\n         from low to high.  For example, a row with a priority of 0\n         is processed before a row with a priority of 1, a 1 before\n         a 2, etc.')
spdGroupContFilter = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 3), VariablePointer().clone((1, 3, 6, 1, 2, 1, 153, 1, 7, 1, 0))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdGroupContFilter.setDescription('spdGroupContFilter points to a filter that is evaluated\n         to determine whether the spdGroupContComponentName within\n         this row is exercised.  Managers can use this object to\n         classify groups of rules, or subgroups, together in order to\n         achieve a greater degree of control and optimization over\n         the execution order of the items within the group.  If the\n\n\n\n         filter evaluates to false, the rule or subgroup will be\n         skipped and the next rule or subgroup will be evaluated\n         instead.  This value can be used to indicate a scalar or\n         row in a table.  When indicating a row in a table, this\n         value MUST point to the first column instance in that row.\n\n         An example usage of this object would be to limit a\n         group of rules to executing only when the IP packet\n         being processed is designated to be processed by IKE.\n         This effectively creates a group of IKE-specific rules.\n\n         The following tables and scalars can be pointed to by this\n         column.  All but diffServMultiFieldClfrTable are defined in\n         this MIB:\n\n                diffServMultiFieldClfrTable\n                spdIpOffsetFilterTable\n                spdTimeFilterTable\n                spdCompoundFilterTable\n                spdTrueFilter\n                spdIpsoHeaderFilterTable\n\n         Implementations MAY choose to provide support for other\n         filter tables or scalars.\n\n         If this column is set to a VariablePointer value, which\n         references a non-existent row in an otherwise supported\n         table, the inconsistentName exception MUST be returned.  If\n         the table or scalar pointed to by the VariablePointer is\n         not supported at all, then an inconsistentValue exception\n         MUST be returned.\n\n         If, during packet processing, a row in this table is applied\n         to a packet and the value of this column in that row\n         references a non-existent or non-supported object, the\n         packet MUST be dropped.')
spdGroupContComponentType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('group', 1), ('rule', 2))).clone('rule')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdGroupContComponentType.setDescription('Indicates whether the spdGroupContComponentName object\n         is the name of another group defined within the\n         spdGroupContentsTable or is the name of a rule defined\n\n\n\n         within the spdRuleDefinitionTable.')
spdGroupContComponentName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 5), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdGroupContComponentName.setDescription('The name of the policy rule or subgroup contained within\n         this row, as indicated by the spdGroupContComponentType\n         object.')
spdGroupContLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 6), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdGroupContLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem,\n         this object SHOULD have a zero value.')
spdGroupContStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 7), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdGroupContStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a storage\n         type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdGroupContRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 3, 1, 8), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdGroupContRowStatus.setDescription("This object indicates the conceptual status of this row.\n\n\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         This object MUST NOT be set to active until the row to\n         which the spdGroupContComponentName points to exists and is\n         active.\n\n         If active, this object MUST remain active unless one of the\n         following two conditions are met:\n\n         I.  No active row in spdEndpointToGroupTable exists that\n             references this row's group (i.e., indicate this row's\n             spdGroupContName).\n\n         II. Or at least one other active row in this table has a\n             matching spdGroupContName.\n\n         If neither condition is met, an attempt to set this row to\n         something other than active MUST result in an\n         inconsistentValue error.")
spdRuleDefinitionTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 4))
if mibBuilder.loadTexts:
    spdRuleDefinitionTable.setDescription('This table defines a rule by associating a filter\n         or a set of filters to an action to be executed.')
spdRuleDefinitionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 4, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdRuleDefName'))
if mibBuilder.loadTexts:
    spdRuleDefinitionEntry.setDescription('A row defining a particular rule definition.  A rule\n         definition binds a filter pointer to an action pointer.')
spdRuleDefName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    spdRuleDefName.setDescription('spdRuleDefName is the administratively assigned name of\n         the rule referred to by the spdGroupContComponentName\n         object.')
spdRuleDefDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 2), SnmpAdminString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdRuleDefDescription.setDescription('A user defined string.  This field MAY be used for\n         administrative tracking purposes.')
spdRuleDefFilter = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 3), VariablePointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdRuleDefFilter.setDescription('spdRuleDefFilter points to a filter that is used to\n         evaluate whether the action associated with this row is\n         executed or not.  The action will only execute if the\n         filter referenced by this object evaluates to TRUE after\n         first applying any negation required by the\n         spdRuleDefFilterNegated object.\n\n         The following tables and scalars can be pointed to by this\n         column.  All but diffServMultiFieldClfrTable are defined in\n         this MIB.  Implementations MAY choose to provide support\n         for other filter tables or scalars as well:\n\n                diffServMultiFieldClfrTable\n\n\n\n                spdIpOffsetFilterTable\n                spdTimeFilterTable\n                spdCompoundFilterTable\n                spdTrueFilter\n\n         If this column is set to a VariablePointer value, which\n         references a non-existent row in an otherwise supported\n         table, the inconsistentName exception MUST be returned.  If\n         the table or scalar pointed to by the VariablePointer is\n         not supported at all, then an inconsistentValue exception\n         MUST be returned.\n\n         If, during packet processing, this column has a value that\n         references a non-existent or non-supported object, the\n         packet MUST be dropped.')
spdRuleDefFilterNegated = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 4), TruthValue().clone('false')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdRuleDefFilterNegated.setDescription('spdRuleDefFilterNegated specifies whether or not the results of\n         the filter referenced by the spdRuleDefFilter object is\n         negated.')
spdRuleDefAction = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 5), VariablePointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdRuleDefAction.setDescription('This column points to the action to be taken.  It MAY,\n         but is not limited to, point to a row in one of the\n         following tables:\n\n            spdCompoundActionTable\n            ipsaSaPreconfiguredActionTable\n            ipiaIkeActionTable\n            ipiaIpsecActionTable\n\n         It MAY also point to one of the scalar objects beneath\n         spdStaticActions.\n\n         If this object is set to a pointer to a row in an\n         unsupported (or unknown) table, an inconsistentValue\n\n\n\n         error MUST be returned.\n\n         If this object is set to point to a non-existent row in an\n         otherwise supported table, an inconsistentName error MUST\n         be returned.\n\n         If, during packet processing, this column has a value that\n         references a non-existent or non-supported object, the\n         packet MUST be dropped.')
spdRuleDefAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 6), SpdAdminStatus().clone('enabled')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdRuleDefAdminStatus.setDescription("Indicates whether the current rule definition is considered\n         active.  If the value is enabled, the rule MUST be evaluated\n         when processing packets.  If the value is disabled, the\n         packet processing MUST continue as if this rule's filter\n         had effectively failed.")
spdRuleDefLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 7), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdRuleDefLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdRuleDefStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 8), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdRuleDefStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a\n         storage type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n\n\n\n         to be writable.')
spdRuleDefRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 4, 1, 9), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdRuleDefRowStatus.setDescription('This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         This object MUST NOT be set to active until the containing\n         conditions, filters, and actions have been defined.  Once\n         active, it MUST remain active until no active\n         policyGroupContents entries are referencing it.  A failed\n         attempt to do so MUST return an inconsistentValue error.')
spdCompoundFilterTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 5))
if mibBuilder.loadTexts:
    spdCompoundFilterTable.setDescription('A table defining compound filters and their associated\n         parameters.  A row in this table can be pointed to by a\n         spdRuleDefFilter object.')
spdCompoundFilterEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 5, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdCompFiltName'))
if mibBuilder.loadTexts:
    spdCompoundFilterEntry.setDescription('An entry in the spdCompoundFilterTable.  Each entry in this\n         table represents a compound filter.  A filter defined by\n         this table is considered to have a TRUE return value if and\n         only if:\n\n         spdCompFiltLogicType is AND and all of the sub-filters\n         associated with it, as defined in the spdSubfiltersTable,\n         are all true themselves (after applying any required\n\n\n\n         negation, as defined by the ficFilterIsNegated object).\n\n         spdCompFiltLogicType is OR and at least one of the\n         sub-filters associated with it, as defined in the\n         spdSubfiltersTable, is true itself (after applying any\n         required negation, as defined by the ficFilterIsNegated\n         object.')
spdCompFiltName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 5, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    spdCompFiltName.setDescription('A user definable string.  This value is used as an index\n         into this table.')
spdCompFiltDescription = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 5, 1, 2), SnmpAdminString()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdCompFiltDescription.setDescription('A user definable string.  This field MAY be used for\n         your administrative tracking purposes.')
spdCompFiltLogicType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 5, 1, 3), SpdBooleanOperator().clone('and')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdCompFiltLogicType.setDescription('Indicates whether the sub-component filters of this\n         compound filter are functionally ANDed or ORed together.')
spdCompFiltLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 5, 1, 4), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdCompFiltLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdCompFiltStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 5, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdCompFiltStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a\n         storage type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdCompFiltRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 5, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdCompFiltRowStatus.setDescription('This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         Once active, it MUST NOT have its value changed if any\n         active rows in the spdRuleDefinitionTable are currently\n         pointing at this row.')
spdSubfiltersTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 6))
if mibBuilder.loadTexts:
    spdSubfiltersTable.setDescription('This table defines a list of filters contained within a\n         given compound filter defined in the\n         spdCompoundFilterTable.')
spdSubfiltersEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 6, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdCompFiltName'), (0, 'IPSEC-SPD-MIB', 'spdSubFiltPriority'))
if mibBuilder.loadTexts:
    spdSubfiltersEntry.setDescription('An entry in the spdSubfiltersTable.  There is an entry in\n         this table for each sub-filter of all compound filters\n         present in the spdCompoundFilterTable.')
spdSubFiltPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 6, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)))
if mibBuilder.loadTexts:
    spdSubFiltPriority.setDescription('The priority of a given filter within a compound filter.\n         The order of execution is from lowest to highest priority\n         value (i.e., priority 0 before priority 1, 1 before 2,\n         etc.).  Implementations MAY choose to follow this ordering,\n         as set by the manager that created the rows.  This can allow\n         a manager to intelligently construct filter lists such that\n         faster filters are evaluated first.')
spdSubFiltSubfilter = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 6, 1, 2), VariablePointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdSubFiltSubfilter.setDescription('The OID of the contained filter.  The value of this\n         object is a VariablePointer that references the filter to\n         be included in this compound filter.\n\n         The following tables and scalars can be pointed to by this\n         column.  All but diffServMultiFieldClfrTable are defined in\n         this MIB.  Implementations MAY choose to provide support\n         for other filter tables or scalars as well:\n\n                diffServMultiFieldClfrTable\n                spdIpsoHeaderFilterTable\n                spdIpOffsetFilterTable\n                spdTimeFilterTable\n                spdCompoundFilterTable\n                spdTrueFilter\n\n         If this column is set to a VariablePointer value that\n         references a non-existent row in an otherwise supported\n         table, the inconsistentName exception MUST be returned.  If\n         the table or scalar pointed to by the VariablePointer is\n         not supported at all, then an inconsistentValue exception\n         MUST be returned.\n\n         If, during packet processing, this column has a value that\n         references a non-existent or non-supported object, the\n         packet MUST be dropped.')
spdSubFiltSubfilterIsNegated = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 6, 1, 3), TruthValue().clone('false')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdSubFiltSubfilterIsNegated.setDescription('Indicates whether or not the result of applying this sub-filter\n         is negated.')
spdSubFiltLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 6, 1, 4), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdSubFiltLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n\n\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdSubFiltStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 6, 1, 5), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdSubFiltStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a\n         storage type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdSubFiltRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 6, 1, 6), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdSubFiltRowStatus.setDescription('This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         This object cannot be made active until a filter\n         referenced by the spdSubFiltSubfilter object is both\n         defined and active.  An attempt to do so MUST result in\n         an inconsistentValue error.\n\n         If active, this object MUST remain active unless one of the\n         following two conditions are met:\n\n         I.  No active row in the SpdCompoundFilterTable exists\n             that has a matching spdCompFiltName.\n\n         II. Or, at least one other active row in this table has a\n             matching spdCompFiltName.\n\n         If neither condition is met, an attempt to set this row to\n         something other than active MUST result in an\n         inconsistentValue error.')
spdStaticFilters = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 1, 7))
spdTrueFilter = MibScalar((1, 3, 6, 1, 2, 1, 153, 1, 7, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdTrueFilter.setDescription('This scalar indicates a (automatic) true result for\n             a filter.  That is, this is a filter that is always\n             true; it is useful for adding as a default filter for a\n             default action or a set of actions.')
spdTrueFilterInstance = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 1, 7, 1, 0))
spdIpOffsetFilterTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 8))
if mibBuilder.loadTexts:
    spdIpOffsetFilterTable.setDescription('This table contains a list of filter definitions to be\n         used within the spdRuleDefinitionTable or the\n         spdSubfiltersTable.\n\n         This type of filter is used to compare an administrator\n         specified octet string to the octets at a particular\n         location in a packet.')
spdIpOffsetFilterEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 8, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdIpOffFiltName'))
if mibBuilder.loadTexts:
    spdIpOffsetFilterEntry.setDescription('A definition of a particular filter.')
spdIpOffFiltName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 8, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    spdIpOffFiltName.setDescription('The administrative name for this filter.')
spdIpOffFiltOffset = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 8, 1, 2), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpOffFiltOffset.setDescription("This is the byte offset from the front of the entire IP\n         packet where the value or arithmetic comparison is done.  A\n         value of '0' indicates the first byte of the packet header.\n         If this value is greater than the length of the packet, the\n         filter represented by this row should be considered to\n         fail.")
spdIpOffFiltType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 8, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))).clone(namedValues=NamedValues(('equal', 1), ('notEqual', 2), ('arithmeticLess', 3), ('arithmeticGreaterOrEqual', 4), ('arithmeticGreater', 5), ('arithmeticLessOrEqual', 6)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpOffFiltType.setDescription("This defines the various tests that are used when\n         evaluating a given filter.\n\n         The various tests definable in this table are as follows:\n\n         equal:\n           - Tests if the OCTET STRING, 'spdIpOffFiltValue', matches\n\n\n\n             a value in the packet starting at the given offset in\n             the packet and comparing the entire OCTET STRING of\n             'spdIpOffFiltValue'.  Any values compared this way are\n             assumed to be unsigned integer values in network byte\n             order of the same length as 'spdIpOffFiltValue'.\n\n         notEqual:\n           - Tests if the OCTET STRING, 'spdIpOffFiltValue', does\n             not match a value in the packet starting at the given\n             offset in the packet and comparing to the entire OCTET\n             STRING of 'spdIpOffFiltValue'.  Any values compared\n             this way are assumed to be unsigned integer values in\n             network byte order of the same length as\n             'spdIpOffFiltValue'.\n\n         arithmeticLess:\n           - Tests if the OCTET STRING, 'spdIpOffFiltValue', is\n             arithmetically less than ('<') the value starting at\n             the given offset within the packet.  The value in the\n             packet is assumed to be an unsigned integer in network\n             byte order of the same length as 'spdIpOffFiltValue'.\n\n         arithmeticGreaterOrEqual:\n           - Tests if the OCTET STRING, 'spdIpOffFiltValue', is\n             arithmetically greater than or equal to ('>=') the\n             value starting at the given offset within the packet.\n             The value in the packet is assumed to be an unsigned\n             integer in network byte order of the same length as\n             'spdIpOffFiltValue'.\n\n         arithmeticGreater:\n           - Tests if the OCTET STRING, 'spdIpOffFiltValue', is\n             arithmetically greater than ('>') the value starting at\n             the given offset within the packet.  The value in the\n             packet is assumed to be an unsigned integer in network\n             byte order of the same length as 'spdIpOffFiltValue'.\n\n         arithmeticLessOrEqual:\n           - Tests if the OCTET STRING, 'spdIpOffFiltValue', is\n             arithmetically less than or equal to ('<=') the value\n             starting at the given offset within the packet.  The\n             value in the packet is assumed to be an unsigned\n             integer in network byte order of the same length as\n             'spdIpOffFiltValue'.")
spdIpOffFiltValue = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 8, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(1, 1024))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpOffFiltValue.setDescription('spdIpOffFiltValue is used for match comparisons of a\n         packet at spdIpOffFiltOffset.')
spdIpOffFiltLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 8, 1, 5), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdIpOffFiltLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdIpOffFiltStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 8, 1, 6), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpOffFiltStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a\n         storage type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdIpOffFiltRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 8, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpOffFiltRowStatus.setDescription('This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         If active, this object MUST remain active if it is\n\n\n\n         referenced by an active row in another table.  An attempt\n         to set it to anything other than active while it is\n         referenced by an active row in another table MUST result in\n         an inconsistentValue error.')
spdTimeFilterTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 9))
if mibBuilder.loadTexts:
    spdTimeFilterTable.setDescription('Defines a table of filters that can be used to\n         effectively enable or disable policies based on a valid\n         time range.')
spdTimeFilterEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 9, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdTimeFiltName'))
if mibBuilder.loadTexts:
    spdTimeFilterEntry.setDescription("A row describing a given time frame for which a policy\n         is filtered on to activate or deactivate the rule.\n\n         If all the column objects in a row are true for the current\n         time, the row evaluates as 'true'.  More explicitly, the\n         time matching column objects in a row MUST be logically\n         ANDed together to form the boolean true/false for the row.")
spdTimeFiltName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    spdTimeFiltName.setDescription('An administratively assigned name for this filter.')
spdTimeFiltPeriod = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 2), SpdTimePeriod().clone('THISANDPRIOR/THISANDFUTURE')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdTimeFiltPeriod.setDescription("The valid time period for this filter.  This column is\n         considered 'true' if the current time is within the range of\n         this object.")
spdTimeFiltMonthOfYearMask = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 3), Bits().clone(namedValues=NamedValues(('january', 0), ('february', 1), ('march', 2), ('april', 3), ('may', 4), ('june', 5), ('july', 6), ('august', 7), ('september', 8), ('october', 9), ('november', 10), ('december', 11))).clone(namedValues=NamedValues(('january', 0), ('february', 1), ('march', 2), ('april', 3), ('may', 4), ('june', 5), ('july', 6), ('august', 7), ('september', 8), ('october', 9), ('november', 10), ('december', 11)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdTimeFiltMonthOfYearMask.setDescription("A bit mask that indicates acceptable months of the year.\n         This column evaluates to 'true' if the current month's bit\n         is set.")
spdTimeFiltDayOfMonthMask = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 4), OctetString().subtype(subtypeSpec=ValueSizeConstraint(8, 8)).setFixedLength(8).clone(hexValue='fffffffffffffffe')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdTimeFiltDayOfMonthMask.setDescription("Defines which days of the month the current time is\n         valid for.  It is a sequence of 64 BITS, where each BIT\n         represents a corresponding day of the month in forward or\n         reverse order.  Starting from the left-most bit, the first\n         31 bits identify the day of the month, counting from the\n         beginning of the month.  The following 31 bits (bits 32-62)\n         indicate the day of the month, counting from the end of the\n\n\n\n         month.  For months with fewer than 31 days, the bits that\n         correspond to the non-existent days of that month are\n         ignored (e.g., for non-leap year Februarys, bits 29-31 and\n         60-62 are ignored).\n\n         This column evaluates to 'true' if the current day of the\n         month's bit is set.\n\n         For example, a value of 0X'80 00 00 01 00 00 00 00'\n         indicates that this column evaluates to true on the first\n         and last days of the month.\n\n         The last two bits in the string MUST be zero.")
spdTimeFiltDayOfWeekMask = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 5), Bits().clone(namedValues=NamedValues(('sunday', 0), ('monday', 1), ('tuesday', 2), ('wednesday', 3), ('thursday', 4), ('friday', 5), ('saturday', 6))).clone(namedValues=NamedValues(('monday', 1), ('tuesday', 2), ('wednesday', 3), ('thursday', 4), ('friday', 5), ('saturday', 6), ('sunday', 0)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdTimeFiltDayOfWeekMask.setDescription("A bit mask that defines which days of the week that the current\n         time is valid for.  This column evaluates to 'true' if the\n         current day of the week's bit is set.")
spdTimeFiltTimeOfDayMask = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 6), SpdTimePeriod().clone('00000000T000000/00000000T240000')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdTimeFiltTimeOfDayMask.setDescription("Indicates the start and end time of the day for which this\n         filter evaluates to true.  The date portions of the\n         spdTimePeriod TC are ignored for purposes of evaluating this\n         mask, and only the time-specific portions are used.\n\n         This column evaluates to 'true' if the current time of day\n         is within the range of the start and end times of the day\n         indicated by this object.")
spdTimeFiltLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 7), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdTimeFiltLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdTimeFiltStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 8), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdTimeFiltStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a storage\n         type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdTimeFiltRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 9, 1, 9), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdTimeFiltRowStatus.setDescription('This object indicates the conceptual status of this\n         row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         If active, this object MUST remain active if it is\n         referenced by an active row in another table.  An attempt\n         to set it to anything other than active while it is\n         referenced by an active row in another table MUST result in\n         an inconsistentValue error.')
spdIpsoHeaderFilterTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 10))
if mibBuilder.loadTexts:
    spdIpsoHeaderFilterTable.setDescription('This table contains a list of IPSO header filter\n         definitions to be used within the spdRuleDefinitionTable or\n         the spdSubfiltersTable.  IPSO headers and their values are\n         described in RFC 1108.')
spdIpsoHeaderFilterEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 10, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdIpsoHeadFiltName'))
if mibBuilder.loadTexts:
    spdIpsoHeaderFilterEntry.setDescription('A definition of a particular filter.')
spdIpsoHeadFiltName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 10, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    spdIpsoHeadFiltName.setDescription('The administrative name for this filter.')
spdIpsoHeadFiltType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 10, 1, 2), Bits().clone(namedValues=NamedValues(('classificationLevel', 0), ('protectionAuthority', 1)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpsoHeadFiltType.setDescription('This object indicates which of the IPSO header field a\n         packet is filtered on for this row.  If this object is set\n         to classification(0), the spdIpsoHeadFiltClassification\n\n\n\n         object indicates how the packet is filtered.  If this object\n         is set to protectionAuthority(1), the\n         spdIpsoHeadFiltProtectionAuth object indicates how the\n         packet is filtered.')
spdIpsoHeadFiltClassification = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 10, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(61, 90, 150, 171))).clone(namedValues=NamedValues(('topSecret', 61), ('secret', 90), ('confidential', 150), ('unclassified', 171)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpsoHeadFiltClassification.setDescription("This object indicates the IPSO classification header field\n         value that the packet MUST have for this row to evaluate to\n         'true'.\n\n         The values of these enumerations are defined by RFC 1108.")
spdIpsoHeadFiltProtectionAuth = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 10, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4))).clone(namedValues=NamedValues(('genser', 0), ('siopesi', 1), ('sci', 2), ('nsa', 3), ('doe', 4)))).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpsoHeadFiltProtectionAuth.setDescription("This object indicates the IPSO protection authority header\n         field value that the packet MUST have for this row to\n         evaluate to 'true'.\n\n         The values of these enumerations are defined by RFC 1108.\n         Hence the reason the SMIv2 convention of not using 0 in\n         enumerated lists is violated here.")
spdIpsoHeadFiltLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 10, 1, 5), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdIpsoHeadFiltLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdIpsoHeadFiltStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 10, 1, 6), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpsoHeadFiltStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a storage\n         type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdIpsoHeadFiltRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 10, 1, 7), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdIpsoHeadFiltRowStatus.setDescription('This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         However, this object MUST NOT be set to active if the\n         requirements of the spdIpsoHeadFiltType object are not met.\n         Specifically, if the spdIpsoHeadFiltType bit for\n         classification(0) is set, the spdIpsoHeadFiltClassification\n         column MUST have a valid value for the row status to be set\n         to active.  If the spdIpsoHeadFiltType bit for\n         protectionAuthority(1) is set, the\n         spdIpsoHeadFiltProtectionAuth column MUST have a valid\n         value for the row status to be set to active.\n\n         If active, this object MUST remain active if it is\n         referenced by an active row in another table.  An attempt\n         to set it to anything other than active while it is\n         referenced by an active row in another table MUST result in\n         an inconsistentValue error.')
spdCompoundActionTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 11))
if mibBuilder.loadTexts:
    spdCompoundActionTable.setDescription('Table used to allow multiple actions to be associated\n         with a rule.  It uses the spdSubactionsTable to do this.\n         The rows from spdSubactionsTable that are partially indexed\n         by spdCompActName form the set of compound actions to be\n         performed.  The spdCompActExecutionStrategy column in this\n         table indicates how those actions are processed.')
spdCompoundActionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 11, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdCompActName'))
if mibBuilder.loadTexts:
    spdCompoundActionEntry.setDescription('A row in the spdCompoundActionTable.')
spdCompActName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 11, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32)))
if mibBuilder.loadTexts:
    spdCompActName.setDescription('This is an administratively assigned name of this\n         compound action.')
spdCompActExecutionStrategy = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 11, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2, 3))).clone(namedValues=NamedValues(('doAll', 1), ('doUntilSuccess', 2), ('doUntilFailure', 3))).clone('doUntilSuccess')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdCompActExecutionStrategy.setDescription('This object indicates how the sub-actions are executed\n         based on the success of the actions as they finish\n         executing.\n\n\n\n         doAll           - run each sub-action regardless of the\n                           exit status of the previous action.\n                           This parent action is always\n                           considered to have acted successfully.\n\n         doUntilSuccess  - run each sub-action until one succeeds,\n                           at which point stop processing the\n                           sub-actions within this parent\n                           compound action.  If one of the\n                           sub-actions did execute successfully,\n                           this parent action is also considered\n                           to have executed successfully.\n\n         doUntilFailure  - run each sub-action until one fails,\n                           at which point stop processing the\n                           sub-actions within this compound\n                           action.  If any sub-action fails, the\n                           result of this parent action is\n                           considered to have failed.')
spdCompActLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 11, 1, 3), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdCompActLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdCompActStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 11, 1, 4), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdCompActStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a storage\n         type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdCompActRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 11, 1, 5), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdCompActRowStatus.setDescription('This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         Once a row in the spdCompoundActionTable has been made\n         active, this object MUST NOT be set to destroy without\n         first destroying all the contained rows listed in the\n         spdSubactionsTable.')
spdSubactionsTable = MibTable((1, 3, 6, 1, 2, 1, 153, 1, 12))
if mibBuilder.loadTexts:
    spdSubactionsTable.setDescription('This table contains a list of the sub-actions within a\n         given compound action.  Compound actions executing these\n         actions MUST execute them in series based on the\n         spdSubActPriority value, with the lowest value executing\n         first.')
spdSubactionsEntry = MibTableRow((1, 3, 6, 1, 2, 1, 153, 1, 12, 1)).setIndexNames((0, 'IPSEC-SPD-MIB', 'spdCompActName'), (0, 'IPSEC-SPD-MIB', 'spdSubActPriority'))
if mibBuilder.loadTexts:
    spdSubactionsEntry.setDescription('A row containing a reference to a given compound-action\n         sub-action.')
spdSubActPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 12, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 65535)))
if mibBuilder.loadTexts:
    spdSubActPriority.setDescription('The priority of a given sub-action within a compound\n         action.  The order in which sub-actions MUST be executed\n         are based on the value from this column, with the lowest\n         numeric value executing first (i.e., priority 0 before\n         priority 1, 1 before 2, etc.).')
spdSubActSubActionName = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 12, 1, 2), VariablePointer()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdSubActSubActionName.setDescription('This column points to the action to be taken.  It MAY,\n         but is not limited to, point to a row in one of the\n         following tables:\n\n            spdCompoundActionTable         - Allowing recursion\n            ipsaSaPreconfiguredActionTable\n            ipiaIkeActionTable\n            ipiaIpsecActionTable\n\n         It MAY also point to one of the scalar objects beneath\n         spdStaticActions.\n\n         If this object is set to a pointer to a row in an\n         unsupported (or unknown) table, an inconsistentValue\n         error MUST be returned.\n\n         If this object is set to point to a non-existent row in\n         an otherwise supported table, an inconsistentName error\n         MUST be returned.\n\n         If, during packet processing, this column has a value that\n         references a non-existent or non-supported object, the\n         packet MUST be dropped.')
spdSubActLastChanged = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 12, 1, 3), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdSubActLastChanged.setDescription('The value of sysUpTime when this row was last modified\n         or created either through SNMP SETs or by some other\n         external means.\n\n         If this row has not been modified since the last\n         re-initialization of the network management subsystem, this\n         object SHOULD have a zero value.')
spdSubActStorageType = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 12, 1, 4), StorageType().clone('nonVolatile')).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdSubActStorageType.setDescription('The storage type for this row.  Rows in this table that\n         were created through an external process MAY have a storage\n         type of readOnly or permanent.\n\n         For a storage type of permanent, none of the columns have\n         to be writable.')
spdSubActRowStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 153, 1, 12, 1, 5), RowStatus()).setMaxAccess('readcreate')
if mibBuilder.loadTexts:
    spdSubActRowStatus.setDescription('This object indicates the conceptual status of this row.\n\n         The value of this object has no effect on whether other\n         objects in this conceptual row can be modified.\n\n         If active, this object MUST remain active unless one of the\n         following two conditions are met.  An attempt to set it to\n         anything other than active while the following conditions\n         are not met MUST result in an inconsistentValue error.  The\n         two conditions are:\n\n         I.  No active row in the spdCompoundActionTable exists\n             which has a matching spdCompActName.\n\n         II. Or, at least one other active row in this table has a\n             matching spdCompActName.')
spdStaticActions = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 1, 13))
spdDropAction = MibScalar((1, 3, 6, 1, 2, 1, 153, 1, 13, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdDropAction.setDescription('This scalar indicates that a packet MUST be dropped\n         and SHOULD NOT have action/packet logging.')
spdDropActionLog = MibScalar((1, 3, 6, 1, 2, 1, 153, 1, 13, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdDropActionLog.setDescription('This scalar indicates that a packet MUST be dropped\n         and SHOULD have action/packet logging.')
spdAcceptAction = MibScalar((1, 3, 6, 1, 2, 1, 153, 1, 13, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdAcceptAction.setDescription('This Scalar indicates that a packet MUST be accepted\n         (pass-through) and SHOULD NOT have action/packet logging.')
spdAcceptActionLog = MibScalar((1, 3, 6, 1, 2, 1, 153, 1, 13, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 1))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    spdAcceptActionLog.setDescription('This scalar indicates that a packet MUST be accepted\n         (pass-through) and SHOULD have action/packet logging.')
spdNotificationVariables = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 2, 1))
spdNotifications = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 2, 0))
spdActionExecuted = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 1), VariablePointer()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdActionExecuted.setDescription('Points to the action instance that was executed that\n         resulted in the notification being sent.')
spdIPEndpointAddType = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 2), InetAddressType()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdIPEndpointAddType.setDescription('Contains the address type for the interface that the\n         notification triggering packet is passing through.')
spdIPEndpointAddress = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 3), InetAddress()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdIPEndpointAddress.setDescription('Contains the interface address for the interface that the\n         notification triggering packet is passing through.\n\n         The format of this object is specified by the\n         spdIPEndpointAddType object.')
spdIPSourceType = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 4), InetAddressType()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdIPSourceType.setDescription('Contains the source address type of the packet that\n\n\n\n         triggered the notification.')
spdIPSourceAddress = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 5), InetAddress()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdIPSourceAddress.setDescription('Contains the source address of the packet that\n         triggered the notification.\n\n         The format of this object is specified by the\n         spdIPSourceType object.')
spdIPDestinationType = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 6), InetAddressType()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdIPDestinationType.setDescription('Contains the destination address type of the packet\n         that triggered the notification.')
spdIPDestinationAddress = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 7), InetAddress()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdIPDestinationAddress.setDescription('Contains the destination address of the packet that\n         triggered the notification.\n\n         The format of this object is specified by the\n         spdIPDestinationType object.')
spdPacketDirection = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 8), IfDirection()).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdPacketDirection.setDescription('Indicates if the packet that triggered the action in\n         questions was ingress (inbound) or egress (outbound).')
spdPacketPart = MibScalar((1, 3, 6, 1, 2, 1, 153, 2, 1, 9), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 65535))).setMaxAccess('accessiblefornotify')
if mibBuilder.loadTexts:
    spdPacketPart.setDescription("spdPacketPart is the front part of the full IP packet that\n         triggered this notification.  The initial size limit is\n         determined by the smaller of the size, indicated by:\n\n         I.  The value of the object with the TC syntax\n             'SpdIPPacketLogging' that indicated the packet SHOULD be\n             logged and\n\n         II. The size of the triggering packet.\n\n         The final limit is determined by the SNMP packet size when\n         sending the notification.  The maximum size that can be\n         included will be the smaller of the initial size, given the\n         above, and the length that will fit in a single SNMP\n         notification packet after the rest of the notification's\n         objects and any other necessary packet data (headers encoding,\n         etc.) have been included in the packet.")
spdActionNotification = NotificationType((1, 3, 6, 1, 2, 1, 153, 2, 0, 1)).setObjects(*(('IPSEC-SPD-MIB', 'spdActionExecuted'), ('IPSEC-SPD-MIB', 'spdIPEndpointAddType'), ('IPSEC-SPD-MIB', 'spdIPEndpointAddress'), ('IPSEC-SPD-MIB', 'spdIPSourceType'), ('IPSEC-SPD-MIB', 'spdIPSourceAddress'), ('IPSEC-SPD-MIB', 'spdIPDestinationType'), ('IPSEC-SPD-MIB', 'spdIPDestinationAddress'), ('IPSEC-SPD-MIB', 'spdPacketDirection')))
if mibBuilder.loadTexts:
    spdActionNotification.setDescription('Notification that an action was executed by a rule.\n         Only actions with logging enabled will result in this\n         notification getting sent.  The object includes the\n         spdActionExecuted object, which will indicate which action\n         was executed within the scope of the rule.  Additionally,\n         the spdIPSourceType, spdIPSourceAddress,\n         spdIPDestinationType, and spdIPDestinationAddress objects\n         are included to indicate the packet source and destination\n         of the packet that triggered the action.  Finally, the\n         spdIPEndpointAddType, spdIPEndpointAddress, and\n         spdPacketDirection objects indicate which interface the\n         executed action was associated with, and if the packet was\n         ingress or egress through the endpoint.\n\n         A spdActionNotification SHOULD be limited to a maximum of\n         one notification sent per minute for any action\n         notifications that do not have any other configuration\n         controlling their send rate.\n\n\n\n         Note that compound actions with multiple executed\n         sub-actions may result in multiple notifications being sent\n         from a single rule execution.')
spdPacketNotification = NotificationType((1, 3, 6, 1, 2, 1, 153, 2, 0, 2)).setObjects(*(('IPSEC-SPD-MIB', 'spdActionExecuted'), ('IPSEC-SPD-MIB', 'spdIPEndpointAddType'), ('IPSEC-SPD-MIB', 'spdIPEndpointAddress'), ('IPSEC-SPD-MIB', 'spdIPSourceType'), ('IPSEC-SPD-MIB', 'spdIPSourceAddress'), ('IPSEC-SPD-MIB', 'spdIPDestinationType'), ('IPSEC-SPD-MIB', 'spdIPDestinationAddress'), ('IPSEC-SPD-MIB', 'spdPacketDirection'), ('IPSEC-SPD-MIB', 'spdPacketPart')))
if mibBuilder.loadTexts:
    spdPacketNotification.setDescription("Notification that a packet passed through a Security\n         Association (SA).  Only SAs created by actions with packet\n         logging enabled will result in this notification getting\n         sent.  The objects sent MUST include the spdActionExecuted,\n         which will indicate which action was executed within the\n         scope of the rule.  Additionally, the spdIPSourceType,\n         spdIPSourceAddress, spdIPDestinationType, and\n         spdIPDestinationAddress objects MUST be included to\n         indicate the packet source and destination of the packet\n         that triggered the action.  The spdIPEndpointAddType,\n         spdIPEndpointAddress, and spdPacketDirection objects are\n         included to indicate which endpoint the packet was\n         associated with.  Finally, spdPacketPart is included to\n         enable sending a variable sized part of the front of the\n         packet with the size dependent on the value of the object of\n         TC syntax 'SpdIPPacketLogging', which indicated that logging\n         should be done.\n\n         A spdPacketNotification SHOULD be limited to a maximum of\n         one notification sent per minute for any action\n         notifications that do not have any other configuration\n         controlling their send rate.\n\n         An action notification SHOULD be limited to a maximum of\n         one notification sent per minute for any action\n         notifications that do not have any other configuration\n         controlling their send rate.")
spdCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 3, 1))
spdGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 153, 3, 2))
spdRuleFilterFullCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 153, 3, 1, 1)).setObjects(*(('IPSEC-SPD-MIB', 'spdEndpointGroup'), ('IPSEC-SPD-MIB', 'spdGroupContentsGroup'), ('IPSEC-SPD-MIB', 'spdRuleDefinitionGroup'), ('IPSEC-SPD-MIB', 'spdStaticFilterGroup'), ('IPSEC-SPD-MIB', 'spdStaticActionGroup'), ('IPSEC-SPD-MIB', 'diffServMIBMultiFieldClfrGroup'), ('IPSEC-SPD-MIB', 'spdIpsecSystemPolicyNameGroup'), ('IPSEC-SPD-MIB', 'spdCompoundFilterGroup'), ('IPSEC-SPD-MIB', 'spdIPOffsetFilterGroup'), ('IPSEC-SPD-MIB', 'spdTimeFilterGroup'), ('IPSEC-SPD-MIB', 'spdIpsoHeaderFilterGroup'), ('IPSEC-SPD-MIB', 'spdCompoundActionGroup')))
if mibBuilder.loadTexts:
    spdRuleFilterFullCompliance.setDescription('The compliance statement for SNMP entities that include\n         an IPsec MIB implementation with Endpoint, Rules, and\n         filters support.\n\n         When this MIB is implemented with support for read-create,\n         then such an implementation can claim full compliance.  Such\n         devices can then be both monitored and configured with this\n         MIB.')
spdLoggingCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 153, 3, 1, 2)).setObjects(*(('IPSEC-SPD-MIB', 'spdActionLoggingObjectGroup'), ('IPSEC-SPD-MIB', 'spdActionNotificationGroup')))
if mibBuilder.loadTexts:
    spdLoggingCompliance.setDescription('The compliance statement for SNMP entities that support\n         sending notifications when actions are invoked.')
spdRuleFilterReadOnlyCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 153, 3, 1, 3)).setObjects(*(('IPSEC-SPD-MIB', 'spdEndpointGroup'), ('IPSEC-SPD-MIB', 'spdGroupContentsGroup'), ('IPSEC-SPD-MIB', 'spdRuleDefinitionGroup'), ('IPSEC-SPD-MIB', 'spdStaticFilterGroup'), ('IPSEC-SPD-MIB', 'spdStaticActionGroup'), ('IPSEC-SPD-MIB', 'diffServMIBMultiFieldClfrGroup'), ('IPSEC-SPD-MIB', 'spdIpsecSystemPolicyNameGroup'), ('IPSEC-SPD-MIB', 'spdCompoundFilterGroup'), ('IPSEC-SPD-MIB', 'spdIPOffsetFilterGroup'), ('IPSEC-SPD-MIB', 'spdTimeFilterGroup'), ('IPSEC-SPD-MIB', 'spdIpsoHeaderFilterGroup'), ('IPSEC-SPD-MIB', 'spdCompoundActionGroup')))
if mibBuilder.loadTexts:
    spdRuleFilterReadOnlyCompliance.setDescription('The compliance statement for SNMP entities that include\n         an IPsec MIB implementation with Endpoint, Rules, and\n         filters support.\n\n         If this MIB is implemented without support for read-create\n         (i.e., in read-only), it is not in full compliance, but it\n         can claim read-only compliance.  Such a device can then be\n         monitored, but cannot be configured with this MIB.')
spdEndpointGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 1)).setObjects(*(('IPSEC-SPD-MIB', 'spdEndGroupName'), ('IPSEC-SPD-MIB', 'spdEndGroupLastChanged'), ('IPSEC-SPD-MIB', 'spdEndGroupStorageType'), ('IPSEC-SPD-MIB', 'spdEndGroupRowStatus')))
if mibBuilder.loadTexts:
    spdEndpointGroup.setDescription('This group is made up of objects from the IPsec Policy\n         Endpoint Table.')
spdGroupContentsGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 2)).setObjects(*(('IPSEC-SPD-MIB', 'spdGroupContComponentType'), ('IPSEC-SPD-MIB', 'spdGroupContFilter'), ('IPSEC-SPD-MIB', 'spdGroupContComponentName'), ('IPSEC-SPD-MIB', 'spdGroupContLastChanged'), ('IPSEC-SPD-MIB', 'spdGroupContStorageType'), ('IPSEC-SPD-MIB', 'spdGroupContRowStatus')))
if mibBuilder.loadTexts:
    spdGroupContentsGroup.setDescription('This group is made up of objects from the IPsec Policy\n         Group Contents Table.')
spdIpsecSystemPolicyNameGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 3)).setObjects(*(('IPSEC-SPD-MIB', 'spdIngressPolicyGroupName'), ('IPSEC-SPD-MIB', 'spdEgressPolicyGroupName')))
if mibBuilder.loadTexts:
    spdIpsecSystemPolicyNameGroup.setDescription('This group is made up of objects represent the System\n         Policy Group Names.')
spdRuleDefinitionGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 4)).setObjects(*(('IPSEC-SPD-MIB', 'spdRuleDefDescription'), ('IPSEC-SPD-MIB', 'spdRuleDefFilter'), ('IPSEC-SPD-MIB', 'spdRuleDefFilterNegated'), ('IPSEC-SPD-MIB', 'spdRuleDefAction'), ('IPSEC-SPD-MIB', 'spdRuleDefAdminStatus'), ('IPSEC-SPD-MIB', 'spdRuleDefLastChanged'), ('IPSEC-SPD-MIB', 'spdRuleDefStorageType'), ('IPSEC-SPD-MIB', 'spdRuleDefRowStatus')))
if mibBuilder.loadTexts:
    spdRuleDefinitionGroup.setDescription('This group is made up of objects from the IPsec Policy Rule\n        Definition Table.')
spdCompoundFilterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 5)).setObjects(*(('IPSEC-SPD-MIB', 'spdCompFiltDescription'), ('IPSEC-SPD-MIB', 'spdCompFiltLogicType'), ('IPSEC-SPD-MIB', 'spdCompFiltLastChanged'), ('IPSEC-SPD-MIB', 'spdCompFiltStorageType'), ('IPSEC-SPD-MIB', 'spdCompFiltRowStatus'), ('IPSEC-SPD-MIB', 'spdSubFiltSubfilter'), ('IPSEC-SPD-MIB', 'spdSubFiltSubfilterIsNegated'), ('IPSEC-SPD-MIB', 'spdSubFiltLastChanged'), ('IPSEC-SPD-MIB', 'spdSubFiltStorageType'), ('IPSEC-SPD-MIB', 'spdSubFiltRowStatus')))
if mibBuilder.loadTexts:
    spdCompoundFilterGroup.setDescription('This group is made up of objects from the IPsec Policy\n         Compound Filter Table and Sub-Filter Table Group.')
spdStaticFilterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 6)).setObjects(*(('IPSEC-SPD-MIB', 'spdTrueFilter'),))
if mibBuilder.loadTexts:
    spdStaticFilterGroup.setDescription('The static filter group.  Currently this is just a true\n          filter.')
spdIPOffsetFilterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 7)).setObjects(*(('IPSEC-SPD-MIB', 'spdIpOffFiltOffset'), ('IPSEC-SPD-MIB', 'spdIpOffFiltType'), ('IPSEC-SPD-MIB', 'spdIpOffFiltValue'), ('IPSEC-SPD-MIB', 'spdIpOffFiltLastChanged'), ('IPSEC-SPD-MIB', 'spdIpOffFiltStorageType'), ('IPSEC-SPD-MIB', 'spdIpOffFiltRowStatus')))
if mibBuilder.loadTexts:
    spdIPOffsetFilterGroup.setDescription('This group is made up of objects from the IPsec Policy IP\n         Offset Filter Table.')
spdTimeFilterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 8)).setObjects(*(('IPSEC-SPD-MIB', 'spdTimeFiltPeriod'), ('IPSEC-SPD-MIB', 'spdTimeFiltMonthOfYearMask'), ('IPSEC-SPD-MIB', 'spdTimeFiltDayOfMonthMask'), ('IPSEC-SPD-MIB', 'spdTimeFiltDayOfWeekMask'), ('IPSEC-SPD-MIB', 'spdTimeFiltTimeOfDayMask'), ('IPSEC-SPD-MIB', 'spdTimeFiltLastChanged'), ('IPSEC-SPD-MIB', 'spdTimeFiltStorageType'), ('IPSEC-SPD-MIB', 'spdTimeFiltRowStatus')))
if mibBuilder.loadTexts:
    spdTimeFilterGroup.setDescription('This group is made up of objects from the IPsec Policy Time\n         Filter Table.')
spdIpsoHeaderFilterGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 9)).setObjects(*(('IPSEC-SPD-MIB', 'spdIpsoHeadFiltType'), ('IPSEC-SPD-MIB', 'spdIpsoHeadFiltClassification'), ('IPSEC-SPD-MIB', 'spdIpsoHeadFiltProtectionAuth'), ('IPSEC-SPD-MIB', 'spdIpsoHeadFiltLastChanged'), ('IPSEC-SPD-MIB', 'spdIpsoHeadFiltStorageType'), ('IPSEC-SPD-MIB', 'spdIpsoHeadFiltRowStatus')))
if mibBuilder.loadTexts:
    spdIpsoHeaderFilterGroup.setDescription('This group is made up of objects from the IPsec Policy IPSO\n         Header Filter Table.')
spdStaticActionGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 10)).setObjects(*(('IPSEC-SPD-MIB', 'spdDropAction'), ('IPSEC-SPD-MIB', 'spdAcceptAction'), ('IPSEC-SPD-MIB', 'spdDropActionLog'), ('IPSEC-SPD-MIB', 'spdAcceptActionLog')))
if mibBuilder.loadTexts:
    spdStaticActionGroup.setDescription('This group is made up of objects from the IPsec Policy\n         Static Actions.')
spdCompoundActionGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 11)).setObjects(*(('IPSEC-SPD-MIB', 'spdCompActExecutionStrategy'), ('IPSEC-SPD-MIB', 'spdCompActLastChanged'), ('IPSEC-SPD-MIB', 'spdCompActStorageType'), ('IPSEC-SPD-MIB', 'spdCompActRowStatus'), ('IPSEC-SPD-MIB', 'spdSubActSubActionName'), ('IPSEC-SPD-MIB', 'spdSubActLastChanged'), ('IPSEC-SPD-MIB', 'spdSubActStorageType'), ('IPSEC-SPD-MIB', 'spdSubActRowStatus')))
if mibBuilder.loadTexts:
    spdCompoundActionGroup.setDescription('The IPsec Policy Compound Action Table and Actions In\n\n\n\n         Compound Action Table Group.')
spdActionLoggingObjectGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 12)).setObjects(*(('IPSEC-SPD-MIB', 'spdActionExecuted'), ('IPSEC-SPD-MIB', 'spdIPEndpointAddType'), ('IPSEC-SPD-MIB', 'spdIPEndpointAddress'), ('IPSEC-SPD-MIB', 'spdIPSourceType'), ('IPSEC-SPD-MIB', 'spdIPSourceAddress'), ('IPSEC-SPD-MIB', 'spdIPDestinationType'), ('IPSEC-SPD-MIB', 'spdIPDestinationAddress'), ('IPSEC-SPD-MIB', 'spdPacketDirection'), ('IPSEC-SPD-MIB', 'spdPacketPart')))
if mibBuilder.loadTexts:
    spdActionLoggingObjectGroup.setDescription('This group is made up of all the Notification objects for\n        this MIB.')
spdActionNotificationGroup = NotificationGroup((1, 3, 6, 1, 2, 1, 153, 3, 2, 13)).setObjects(*(('IPSEC-SPD-MIB', 'spdActionNotification'), ('IPSEC-SPD-MIB', 'spdPacketNotification')))
if mibBuilder.loadTexts:
    spdActionNotificationGroup.setDescription('This group is made up of all the Notifications for this MIB.')
mibBuilder.exportSymbols('IPSEC-SPD-MIB', spdRuleDefFilter=spdRuleDefFilter, spdEndpointToGroupTable=spdEndpointToGroupTable, spdIpOffFiltValue=spdIpOffFiltValue, spdCompoundFilterTable=spdCompoundFilterTable, spdRuleDefRowStatus=spdRuleDefRowStatus, spdSubFiltRowStatus=spdSubFiltRowStatus, spdStaticActions=spdStaticActions, spdEndGroupInterface=spdEndGroupInterface, spdRuleFilterReadOnlyCompliance=spdRuleFilterReadOnlyCompliance, spdCompoundFilterGroup=spdCompoundFilterGroup, spdEndpointGroup=spdEndpointGroup, spdEgressPolicyGroupName=spdEgressPolicyGroupName, spdGroupContentsTable=spdGroupContentsTable, spdSubFiltSubfilter=spdSubFiltSubfilter, spdIpsoHeadFiltClassification=spdIpsoHeadFiltClassification, spdGroupContStorageType=spdGroupContStorageType, spdCompliances=spdCompliances, spdCompFiltName=spdCompFiltName, spdRuleDefName=spdRuleDefName, spdIPOffsetFilterGroup=spdIPOffsetFilterGroup, spdSubfiltersTable=spdSubfiltersTable, SpdIPPacketLogging=SpdIPPacketLogging, spdTimeFilterEntry=spdTimeFilterEntry, spdTimeFilterTable=spdTimeFilterTable, spdGroupContPriority=spdGroupContPriority, spdTimeFiltStorageType=spdTimeFiltStorageType, spdSubactionsEntry=spdSubactionsEntry, spdActions=spdActions, spdIpsoHeaderFilterGroup=spdIpsoHeaderFilterGroup, spdTimeFiltLastChanged=spdTimeFiltLastChanged, spdRuleDefinitionEntry=spdRuleDefinitionEntry, spdGroupContComponentName=spdGroupContComponentName, spdTimeFiltDayOfMonthMask=spdTimeFiltDayOfMonthMask, spdStaticFilters=spdStaticFilters, spdSubFiltPriority=spdSubFiltPriority, spdRuleDefLastChanged=spdRuleDefLastChanged, spdNotificationVariables=spdNotificationVariables, spdSubFiltSubfilterIsNegated=spdSubFiltSubfilterIsNegated, spdIpsoHeadFiltType=spdIpsoHeadFiltType, PYSNMP_MODULE_ID=spdMIB, spdIpsoHeadFiltName=spdIpsoHeadFiltName, spdRuleDefAction=spdRuleDefAction, spdGroupContComponentType=spdGroupContComponentType, spdActionLoggingObjectGroup=spdActionLoggingObjectGroup, spdIpsoHeaderFilterTable=spdIpsoHeaderFilterTable, spdStaticActionGroup=spdStaticActionGroup, spdIpOffsetFilterEntry=spdIpOffsetFilterEntry, spdEndGroupLastChanged=spdEndGroupLastChanged, spdRuleDefinitionTable=spdRuleDefinitionTable, spdCompFiltLogicType=spdCompFiltLogicType, spdIpOffFiltRowStatus=spdIpOffFiltRowStatus, spdNotificationObjects=spdNotificationObjects, spdRuleDefinitionGroup=spdRuleDefinitionGroup, spdTimeFiltRowStatus=spdTimeFiltRowStatus, spdIpOffFiltOffset=spdIpOffFiltOffset, spdCompFiltDescription=spdCompFiltDescription, spdGroupContentsGroup=spdGroupContentsGroup, spdMIB=spdMIB, spdConformanceObjects=spdConformanceObjects, spdEndGroupDirection=spdEndGroupDirection, spdEndGroupName=spdEndGroupName, spdCompoundFilterEntry=spdCompoundFilterEntry, spdIpsoHeadFiltRowStatus=spdIpsoHeadFiltRowStatus, spdTimeFilterGroup=spdTimeFilterGroup, spdRuleDefAdminStatus=spdRuleDefAdminStatus, spdIpOffFiltLastChanged=spdIpOffFiltLastChanged, spdCompoundActionGroup=spdCompoundActionGroup, spdSubActStorageType=spdSubActStorageType, spdIpOffFiltName=spdIpOffFiltName, spdSubfiltersEntry=spdSubfiltersEntry, SpdBooleanOperator=SpdBooleanOperator, spdEndGroupStorageType=spdEndGroupStorageType, spdIPSourceType=spdIPSourceType, spdCompActLastChanged=spdCompActLastChanged, spdGroupContentsEntry=spdGroupContentsEntry, spdPacketDirection=spdPacketDirection, spdRuleDefStorageType=spdRuleDefStorageType, spdIPDestinationType=spdIPDestinationType, spdActionNotificationGroup=spdActionNotificationGroup, spdTrueFilter=spdTrueFilter, spdSubActRowStatus=spdSubActRowStatus, spdPacketPart=spdPacketPart, spdTimeFiltDayOfWeekMask=spdTimeFiltDayOfWeekMask, spdCompActName=spdCompActName, spdIpOffFiltType=spdIpOffFiltType, spdIpOffFiltStorageType=spdIpOffFiltStorageType, spdRuleDefDescription=spdRuleDefDescription, spdIpOffsetFilterTable=spdIpOffsetFilterTable, spdIPEndpointAddType=spdIPEndpointAddType, spdEndGroupRowStatus=spdEndGroupRowStatus, spdSubActPriority=spdSubActPriority, spdLocalConfigObjects=spdLocalConfigObjects, spdDropActionLog=spdDropActionLog, spdTimeFiltTimeOfDayMask=spdTimeFiltTimeOfDayMask, spdSubActLastChanged=spdSubActLastChanged, spdDropAction=spdDropAction, spdTrueFilterInstance=spdTrueFilterInstance, spdConfigObjects=spdConfigObjects, spdActionNotification=spdActionNotification, spdIpsecSystemPolicyNameGroup=spdIpsecSystemPolicyNameGroup, spdActionExecuted=spdActionExecuted, SpdTimePeriod=SpdTimePeriod, spdCompActRowStatus=spdCompActRowStatus, spdSubactionsTable=spdSubactionsTable, spdNotifications=spdNotifications, spdCompFiltLastChanged=spdCompFiltLastChanged, SpdAdminStatus=SpdAdminStatus, spdGroupContRowStatus=spdGroupContRowStatus, spdIPEndpointAddress=spdIPEndpointAddress, spdEndpointToGroupEntry=spdEndpointToGroupEntry, spdCompoundActionTable=spdCompoundActionTable, spdLoggingCompliance=spdLoggingCompliance, spdIpsoHeadFiltLastChanged=spdIpsoHeadFiltLastChanged, spdGroups=spdGroups, spdIpsoHeadFiltProtectionAuth=spdIpsoHeadFiltProtectionAuth, spdGroupContFilter=spdGroupContFilter, spdIpsoHeadFiltStorageType=spdIpsoHeadFiltStorageType, spdSubActSubActionName=spdSubActSubActionName, spdTimeFiltName=spdTimeFiltName, spdCompActExecutionStrategy=spdCompActExecutionStrategy, spdRuleFilterFullCompliance=spdRuleFilterFullCompliance, spdStaticFilterGroup=spdStaticFilterGroup, spdAcceptAction=spdAcceptAction, spdIPSourceAddress=spdIPSourceAddress, spdTimeFiltPeriod=spdTimeFiltPeriod, spdRuleDefFilterNegated=spdRuleDefFilterNegated, spdAcceptActionLog=spdAcceptActionLog, spdCompActStorageType=spdCompActStorageType, spdPacketNotification=spdPacketNotification, spdGroupContLastChanged=spdGroupContLastChanged, spdSubFiltLastChanged=spdSubFiltLastChanged, spdSubFiltStorageType=spdSubFiltStorageType, spdIPDestinationAddress=spdIPDestinationAddress, spdCompoundActionEntry=spdCompoundActionEntry, spdCompFiltStorageType=spdCompFiltStorageType, spdGroupContName=spdGroupContName, spdIpsoHeaderFilterEntry=spdIpsoHeaderFilterEntry, spdTimeFiltMonthOfYearMask=spdTimeFiltMonthOfYearMask, spdCompFiltRowStatus=spdCompFiltRowStatus, spdIngressPolicyGroupName=spdIngressPolicyGroupName)