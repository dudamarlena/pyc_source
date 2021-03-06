# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/AGENTX-MIB.py
# Compiled at: 2016-02-13 18:04:18
(ObjectIdentifier, Integer, OctetString) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'Integer', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ConstraintsUnion, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ValueRangeConstraint', 'ValueSizeConstraint', 'ConstraintsUnion', 'ConstraintsIntersection')
(SnmpAdminString,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'SnmpAdminString')
(ObjectGroup, NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'ObjectGroup', 'NotificationGroup', 'ModuleCompliance')
(IpAddress, Bits, Unsigned32, Counter32, NotificationType, MibIdentifier, Gauge32, ModuleIdentity, TimeTicks, Counter64, MibScalar, MibTable, MibTableRow, MibTableColumn, iso, Integer32, ObjectIdentity, mib_2) = mibBuilder.importSymbols('SNMPv2-SMI', 'IpAddress', 'Bits', 'Unsigned32', 'Counter32', 'NotificationType', 'MibIdentifier', 'Gauge32', 'ModuleIdentity', 'TimeTicks', 'Counter64', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'iso', 'Integer32', 'ObjectIdentity', 'mib-2')
(TextualConvention, TimeStamp, TruthValue, TDomain, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'TimeStamp', 'TruthValue', 'TDomain', 'DisplayString')
agentxMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 74)).setRevisions(('2000-01-10 00:00', ))
if mibBuilder.loadTexts:
    agentxMIB.setLastUpdated('200001100000Z')
if mibBuilder.loadTexts:
    agentxMIB.setOrganization('AgentX Working Group')
if mibBuilder.loadTexts:
    agentxMIB.setContactInfo('WG-email:   agentx@dorothy.bmc.com\n               Subscribe:  agentx-request@dorothy.bmc.com\n               WG-email Archive:  ftp://ftp.peer.com/pub/agentx/archives\n               FTP repository:  ftp://ftp.peer.com/pub/agentx\n               http://www.ietf.org/html.charters/agentx-charter.html\n\n               Chair:      Bob Natale\n                           ACE*COMM Corporation\n               Email:      bnatale@acecomm.com\n\n               WG editor:  Mark Ellison\n                           Ellison Software Consulting, Inc.\n               Email:      ellison@world.std.com\n\n               Co-author:  Lauren Heintz\n                           Cisco Systems,\n               EMail:      lheintz@cisco.com\n\n               Co-author:  Smitha Gudur\n                           Independent Consultant\n               Email:      sgudur@hotmail.com\n\n              ')
if mibBuilder.loadTexts:
    agentxMIB.setDescription('This is the MIB module for the SNMP Agent Extensibility\n     Protocol (AgentX).  This MIB module will be implemented by\n     the master agent.\n    ')

class AgentxTAddress(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 255)


agentxObjects = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 1))
agentxGeneral = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 1, 1))
agentxConnection = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 1, 2))
agentxSession = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 1, 3))
agentxRegistration = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 1, 4))
agentxDefaultTimeout = MibScalar((1, 3, 6, 1, 2, 1, 74, 1, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255)).clone(5)).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxDefaultTimeout.setDescription('The default length of time, in seconds, that the master\n      agent should allow to elapse after dispatching a message\n      to a session before it regards the subagent as not\n      responding.  This is a system-wide value that may\n      override the timeout value associated with a particular\n      session (agentxSessionTimeout) or a particular registered\n      MIB region (agentxRegTimeout).  If the associated value of\n      agentxSessionTimeout and agentxRegTimeout are zero, or\n      impractical in accordance with implementation-specific\n      procedure of the master agent, the value represented by\n      this object will be the effective timeout value for the\n      master agent to await a response to a dispatch from a\n      given subagent.\n     ')
agentxMasterAgentXVer = MibScalar((1, 3, 6, 1, 2, 1, 74, 1, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxMasterAgentXVer.setDescription('The AgentX protocol version supported by this master agent.\n      The current protocol version is 1.  Note that the master agent\n      must also allow interaction with earlier version subagents.\n     ')
agentxConnTableLastChange = MibScalar((1, 3, 6, 1, 2, 1, 74, 1, 2, 1), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxConnTableLastChange.setDescription('The value of sysUpTime when the last row creation or deletion\n      occurred in the agentxConnectionTable.\n     ')
agentxConnectionTable = MibTable((1, 3, 6, 1, 2, 1, 74, 1, 2, 2))
if mibBuilder.loadTexts:
    agentxConnectionTable.setDescription('The agentxConnectionTable tracks all current AgentX transport\n      connections.  There may be zero, one, or more AgentX sessions\n      carried on a given AgentX connection.\n     ')
agentxConnectionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 74, 1, 2, 2, 1)).setIndexNames((0,
                                                                                       'AGENTX-MIB',
                                                                                       'agentxConnIndex'))
if mibBuilder.loadTexts:
    agentxConnectionEntry.setDescription('An agentxConnectionEntry contains information describing a\n      single AgentX transport connection.  A connection may be\n      used to support zero or more AgentX sessions.  An entry is\n      created when a new transport connection is established,\n      and is destroyed when the transport connection is terminated.\n     ')
agentxConnIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 2, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    agentxConnIndex.setDescription('agentxConnIndex contains the value that uniquely identifies\n      an open transport connection used by this master agent\n      to provide AgentX service.  Values of this index should\n      not be re-used.  The value assigned to a given transport\n      connection is constant for the lifetime of that connection.\n     ')
agentxConnOpenTime = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 2, 2, 1, 2), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxConnOpenTime.setDescription('The value of sysUpTime when this connection was established\n      and, therefore, its value when this entry was added to the table.\n     ')
agentxConnTransportDomain = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 2, 2, 1, 3), TDomain()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxConnTransportDomain.setDescription('The transport protocol in use for this connection to the\n      subagent.\n     ')
agentxConnTransportAddress = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 2, 2, 1, 4), AgentxTAddress()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxConnTransportAddress.setDescription('The transport address of the remote (subagent) end of this\n      connection to the master agent.  This object may be zero-length\n      for unix-domain sockets (and possibly other types of transport\n      addresses) since the subagent need not bind a filename to its\n      local socket.\n     ')
agentxSessionTableLastChange = MibScalar((1, 3, 6, 1, 2, 1, 74, 1, 3, 1), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxSessionTableLastChange.setDescription('The value of sysUpTime when the last row creation or deletion\n      occurred in the agentxSessionTable.\n     ')
agentxSessionTable = MibTable((1, 3, 6, 1, 2, 1, 74, 1, 3, 2))
if mibBuilder.loadTexts:
    agentxSessionTable.setDescription('A table of AgentX subagent sessions currently in effect.\n     ')
agentxSessionEntry = MibTableRow((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1)).setIndexNames((0,
                                                                                    'AGENTX-MIB',
                                                                                    'agentxConnIndex'), (0,
                                                                                                         'AGENTX-MIB',
                                                                                                         'agentxSessionIndex'))
if mibBuilder.loadTexts:
    agentxSessionEntry.setDescription('Information about a single open session between the AgentX\n      master agent and a subagent is contained in this entry.  An\n      entry is created when a new session is successfully established\n      and is destroyed either when the subagent transport connection\n      has terminated or when the subagent session is closed.\n     ')
agentxSessionIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(0, 4294967295)))
if mibBuilder.loadTexts:
    agentxSessionIndex.setDescription("A unique index for the subagent session.  It is the same as\n      h.sessionID defined in the agentx header.  Note that if\n      a subagent's session with the master agent is closed for\n      any reason its index should not be re-used.\n      A value of zero(0) is specifically allowed in order\n      to be compatible with the definition of h.sessionId.\n     ")
agentxSessionObjectID = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1, 2), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxSessionObjectID.setDescription("This is taken from the o.id field of the agentx-Open-PDU.\n      This attribute will report a value of '0.0' for subagents\n      not supporting the notion of an AgentX session object\n      identifier.\n     ")
agentxSessionDescr = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1, 3), SnmpAdminString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxSessionDescr.setDescription('A textual description of the session.  This is analogous to\n      sysDescr defined in the SNMPv2-MIB in RFC 1907 [19] and is\n      taken from the o.descr field of the agentx-Open-PDU.\n      This attribute will report a zero-length string value for\n      subagents not supporting the notion of a session description.\n     ')
agentxSessionAdminStatus = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(1, 2))).clone(namedValues=NamedValues(('up',
                                                                                                                                                                                               1), ('down',
                                                                                                                                                                                                    2)))).setMaxAccess('readwrite')
if mibBuilder.loadTexts:
    agentxSessionAdminStatus.setDescription("The administrative (desired) status of the session.  Setting\n      the value to 'down(2)' closes the subagent session (with c.reason\n      set to 'reasonByManager').\n     ")
agentxSessionOpenTime = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1, 5), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxSessionOpenTime.setDescription('The value of sysUpTime when this session was opened and,\n      therefore, its value when this entry was added to the table.\n     ')
agentxSessionAgentXVer = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1, 6), Integer32().subtype(subtypeSpec=ValueRangeConstraint(1, 255))).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxSessionAgentXVer.setDescription('The version of the AgentX protocol supported by the\n      session.  This must be less than or equal to the value of\n      agentxMasterAgentXVer.\n     ')
agentxSessionTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 3, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxSessionTimeout.setDescription("The length of time, in seconds, that a master agent should\n      allow to elapse after dispatching a message to this session\n      before it regards the subagent as not responding.  This value\n      is taken from the o.timeout field of the agentx-Open-PDU.\n      This is a session-specific value that may be overridden by\n      values associated with the specific registered MIB regions\n      (see agentxRegTimeout). A value of zero(0) indicates that\n      the master agent's default timeout value should be used\n      (see agentxDefaultTimeout).\n     ")
agentxRegistrationTableLastChange = MibScalar((1, 3, 6, 1, 2, 1, 74, 1, 4, 1), TimeStamp()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegistrationTableLastChange.setDescription('The value of sysUpTime when the last row creation or deletion\n      occurred in the agentxRegistrationTable.\n     ')
agentxRegistrationTable = MibTable((1, 3, 6, 1, 2, 1, 74, 1, 4, 2))
if mibBuilder.loadTexts:
    agentxRegistrationTable.setDescription('A table of registered regions.\n     ')
agentxRegistrationEntry = MibTableRow((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1)).setIndexNames((0,
                                                                                         'AGENTX-MIB',
                                                                                         'agentxConnIndex'), (0,
                                                                                                              'AGENTX-MIB',
                                                                                                              'agentxSessionIndex'), (0,
                                                                                                                                      'AGENTX-MIB',
                                                                                                                                      'agentxRegIndex'))
if mibBuilder.loadTexts:
    agentxRegistrationEntry.setDescription('Contains information for a single registered region.  An\n      entry is created when a session  successfully registers a\n      region and is destroyed for any of three reasons: this region\n      is unregistered by the session, the session is closed,\n      or the subagent connection is closed.\n     ')
agentxRegIndex = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 1), Unsigned32().subtype(subtypeSpec=ValueRangeConstraint(1, 4294967295)))
if mibBuilder.loadTexts:
    agentxRegIndex.setDescription('agentxRegIndex uniquely identifies a registration entry.\n      This value is constant for the lifetime of an entry.\n     ')
agentxRegContext = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 2), OctetString()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegContext.setDescription('The context in which the session supports the objects in this\n      region.  A zero-length context indicates the default context.\n     ')
agentxRegStart = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 3), ObjectIdentifier()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegStart.setDescription('The starting OBJECT IDENTIFIER of this registration entry.  The\n      session identified by agentxSessionIndex implements objects\n      starting at this value (inclusive).  Note that this value could\n      identify an object type, an object instance, or a partial object\n      instance.\n     ')
agentxRegRangeSubId = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 4), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegRangeSubId.setDescription("agentxRegRangeSubId is used to specify the range.  This is\n      taken from r.region_subid in the registration PDU.  If the value\n      of this object is zero, no range is specified.  If it is non-zero,\n      it identifies the `nth' sub-identifier in r.region for which\n      this entry's agentxRegUpperBound value is substituted in the\n      OID for purposes of defining the region's upper bound.\n     ")
agentxRegUpperBound = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 5), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegUpperBound.setDescription('agentxRegUpperBound represents the upper-bound sub-identifier in\n     a registration.  This is taken from the r.upper_bound in the\n     registration PDU.  If agentxRegRangeSubid (r.region_subid) is\n     zero, this value is also zero and is not used to define an upper\n     bound for this registration.\n    ')
agentxRegPriority = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 6), Unsigned32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegPriority.setDescription('The registration priority.  Lower values have higher priority.\n      This value is taken from r.priority in the register PDU.\n      Sessions should use the value of 127 for r.priority if a\n      default value is desired.\n     ')
agentxRegTimeout = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 255))).setUnits('seconds').setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegTimeout.setDescription('The timeout value, in seconds, for responses to\n      requests associated with this registered MIB region.\n      A value of zero(0) indicates the default value (indicated\n      by by agentxSessionTimeout or agentxDefaultTimeout) is to\n      be used.  This value is taken from the r.timeout field of\n      the agentx-Register-PDU.\n     ')
agentxRegInstance = MibTableColumn((1, 3, 6, 1, 2, 1, 74, 1, 4, 2, 1, 8), TruthValue()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    agentxRegInstance.setDescription("The value of agentxRegInstance is `true' for\n      registrations for which the INSTANCE_REGISTRATION\n      was set, and is `false' for all other registrations.\n     ")
agentxConformance = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 2))
agentxMIBGroups = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 2, 1))
agentxMIBCompliances = MibIdentifier((1, 3, 6, 1, 2, 1, 74, 2, 2))
agentxMIBCompliance = ModuleCompliance((1, 3, 6, 1, 2, 1, 74, 2, 2, 1)).setObjects(*(('AGENTX-MIB', 'agentxMIBGroup'), ))
if mibBuilder.loadTexts:
    agentxMIBCompliance.setDescription('The compliance statement for SNMP entities that implement the\n      AgentX protocol.  Note that a compliant agent can implement all\n      objects in this MIB module as read-only.\n     ')
agentxMIBGroup = ObjectGroup((1, 3, 6, 1, 2, 1, 74, 2, 1, 1)).setObjects(*(('AGENTX-MIB', 'agentxDefaultTimeout'), ('AGENTX-MIB', 'agentxMasterAgentXVer'), ('AGENTX-MIB', 'agentxConnTableLastChange'), ('AGENTX-MIB', 'agentxConnOpenTime'), ('AGENTX-MIB', 'agentxConnTransportDomain'), ('AGENTX-MIB', 'agentxConnTransportAddress'), ('AGENTX-MIB', 'agentxSessionTableLastChange'), ('AGENTX-MIB', 'agentxSessionTimeout'), ('AGENTX-MIB', 'agentxSessionObjectID'), ('AGENTX-MIB', 'agentxSessionDescr'), ('AGENTX-MIB', 'agentxSessionAdminStatus'), ('AGENTX-MIB', 'agentxSessionOpenTime'), ('AGENTX-MIB', 'agentxSessionAgentXVer'), ('AGENTX-MIB', 'agentxRegistrationTableLastChange'), ('AGENTX-MIB', 'agentxRegContext'), ('AGENTX-MIB', 'agentxRegStart'), ('AGENTX-MIB', 'agentxRegRangeSubId'), ('AGENTX-MIB', 'agentxRegUpperBound'), ('AGENTX-MIB', 'agentxRegPriority'), ('AGENTX-MIB', 'agentxRegTimeout'), ('AGENTX-MIB', 'agentxRegInstance')))
if mibBuilder.loadTexts:
    agentxMIBGroup.setDescription('All accessible objects in the AgentX MIB.\n     ')
mibBuilder.exportSymbols('AGENTX-MIB', agentxRegUpperBound=agentxRegUpperBound, agentxRegStart=agentxRegStart, agentxRegistrationTableLastChange=agentxRegistrationTableLastChange, agentxConnOpenTime=agentxConnOpenTime, agentxSessionAdminStatus=agentxSessionAdminStatus, agentxConformance=agentxConformance, agentxMIBGroup=agentxMIBGroup, agentxSessionObjectID=agentxSessionObjectID, agentxConnectionEntry=agentxConnectionEntry, PYSNMP_MODULE_ID=agentxMIB, agentxRegistrationTable=agentxRegistrationTable, agentxConnTransportDomain=agentxConnTransportDomain, agentxRegInstance=agentxRegInstance, agentxRegTimeout=agentxRegTimeout, agentxRegPriority=agentxRegPriority, agentxSessionTableLastChange=agentxSessionTableLastChange, agentxConnectionTable=agentxConnectionTable, agentxRegContext=agentxRegContext, agentxConnTransportAddress=agentxConnTransportAddress, agentxMIBCompliance=agentxMIBCompliance, agentxObjects=agentxObjects, agentxConnIndex=agentxConnIndex, agentxSessionEntry=agentxSessionEntry, agentxMIB=agentxMIB, agentxRegRangeSubId=agentxRegRangeSubId, agentxConnTableLastChange=agentxConnTableLastChange, agentxSessionTimeout=agentxSessionTimeout, agentxMasterAgentXVer=agentxMasterAgentXVer, agentxSessionOpenTime=agentxSessionOpenTime, agentxRegistration=agentxRegistration, agentxSessionDescr=agentxSessionDescr, agentxSessionIndex=agentxSessionIndex, agentxMIBCompliances=agentxMIBCompliances, agentxGeneral=agentxGeneral, agentxSessionAgentXVer=agentxSessionAgentXVer, agentxRegistrationEntry=agentxRegistrationEntry, agentxSessionTable=agentxSessionTable, agentxRegIndex=agentxRegIndex, AgentxTAddress=AgentxTAddress, agentxSession=agentxSession, agentxConnection=agentxConnection, agentxMIBGroups=agentxMIBGroups, agentxDefaultTimeout=agentxDefaultTimeout)