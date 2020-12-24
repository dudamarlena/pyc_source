# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/TRIP-TC-MIB.py
# Compiled at: 2016-02-13 18:32:10
(Integer, ObjectIdentifier, OctetString) = mibBuilder.importSymbols('ASN1', 'Integer', 'ObjectIdentifier', 'OctetString')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ConstraintsUnion, ConstraintsIntersection, ValueRangeConstraint, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ConstraintsUnion', 'ConstraintsIntersection', 'ValueRangeConstraint', 'ValueSizeConstraint')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(Unsigned32, Counter64, Counter32, MibIdentifier, ModuleIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, NotificationType, Bits, iso, TimeTicks, Integer32, ObjectIdentity, Gauge32, mib_2) = mibBuilder.importSymbols('SNMPv2-SMI', 'Unsigned32', 'Counter64', 'Counter32', 'MibIdentifier', 'ModuleIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'IpAddress', 'NotificationType', 'Bits', 'iso', 'TimeTicks', 'Integer32', 'ObjectIdentity', 'Gauge32', 'mib-2')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
tripTC = ModuleIdentity((1, 3, 6, 1, 2, 1, 115)).setRevisions(('2004-09-02 00:00', ))
if mibBuilder.loadTexts:
    tripTC.setLastUpdated('200409020000Z')
if mibBuilder.loadTexts:
    tripTC.setOrganization('IETF IPTel Working Group.\n        Mailing list: iptel@lists.bell-labs.com')
if mibBuilder.loadTexts:
    tripTC.setContactInfo('Co-editor  David Zinman\n        postal:    265 Ridley Blvd.\n                   Toronto ON, M5M 4N8\n                   Canada\n        email:     dzinman@rogers.com\n        phone:     +1 416 433 4298\n\n        Co-editor: David Walker\n                   Sedna Wireless Inc.\n        postal:    495 March Road, Suite 500\n                   Ottawa, ON K2K 3G1\n                   Canada\n        email:     david.walker@sedna-wireless.com\n        phone:     +1 613 878 8142\n\n        Co-editor   Jianping Jiang\n                    Syndesis Limited\n        postal:     30 Fulton Way\n                    Richmond Hill, ON L4B 1J5\n                    Canada\n\n        email:      jjiang@syndesis.com\n        phone:      +1 905 886-7818 x2515\n        ')
if mibBuilder.loadTexts:
    tripTC.setDescription('Initial version of TRIP (Telephony Routing Over IP)\n        MIB Textual Conventions module used by other\n\n        TRIP-related MIB Modules.\n\n        Copyright (C) The Internet Society (2004). This version of\n        this MIB module is part of RFC 3872, see the RFC itself\n        for full legal notices.')

class TripItad(Unsigned32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(0, 4294967295)


class TripId(Unsigned32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(0, 4294967295)


class TripAddressFamily(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 255))
    namedValues = NamedValues(('decimal', 1), ('pentadecimal', 2), ('e164', 3), ('other',
                                                                                 255))


class TripAppProtocol(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 255))
    namedValues = NamedValues(('sip', 1), ('q931', 2), ('ras', 3), ('annexG', 4), ('other',
                                                                                   255))


class TripCommunityId(Unsigned32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Unsigned32.subtypeSpec + ValueRangeConstraint(0, 4294967295)


class TripProtocolVersion(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(1, 255)


class TripSendReceiveMode(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3))
    namedValues = NamedValues(('sendReceive', 1), ('sendOnly', 2), ('receiveOnly',
                                                                    3))


mibBuilder.exportSymbols('TRIP-TC-MIB', TripAppProtocol=TripAppProtocol, TripAddressFamily=TripAddressFamily, TripSendReceiveMode=TripSendReceiveMode, PYSNMP_MODULE_ID=tripTC, TripItad=TripItad, TripCommunityId=TripCommunityId, TripId=TripId, TripProtocolVersion=TripProtocolVersion, tripTC=tripTC)