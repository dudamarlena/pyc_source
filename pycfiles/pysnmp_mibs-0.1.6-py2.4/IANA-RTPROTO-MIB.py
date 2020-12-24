# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/IANA-RTPROTO-MIB.py
# Compiled at: 2016-02-13 18:16:07
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsIntersection, ValueRangeConstraint, SingleValueConstraint, ValueSizeConstraint, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsIntersection', 'ValueRangeConstraint', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsUnion')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(mib_2, Gauge32, Integer32, IpAddress, Counter32, NotificationType, iso, Unsigned32, TimeTicks, ObjectIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, ModuleIdentity, Counter64, Bits) = mibBuilder.importSymbols('SNMPv2-SMI', 'mib-2', 'Gauge32', 'Integer32', 'IpAddress', 'Counter32', 'NotificationType', 'iso', 'Unsigned32', 'TimeTicks', 'ObjectIdentity', 'MibIdentifier', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'ModuleIdentity', 'Counter64', 'Bits')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
ianaRtProtoMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 84)).setRevisions(('2000-09-26 00:00', ))
if mibBuilder.loadTexts:
    ianaRtProtoMIB.setLastUpdated('200009260000Z')
if mibBuilder.loadTexts:
    ianaRtProtoMIB.setOrganization('IANA')
if mibBuilder.loadTexts:
    ianaRtProtoMIB.setContactInfo(' Internet Assigned Numbers Authority\n              Internet Corporation for Assigned Names and Numbers\n              4676 Admiralty Way, Suite 330\n              Marina del Rey, CA 90292-6601\n\n              Phone: +1 310 823 9358\n              EMail: iana@iana.org')
if mibBuilder.loadTexts:
    ianaRtProtoMIB.setDescription('This MIB module defines the IANAipRouteProtocol and\n            IANAipMRouteProtocol textual conventions for use in MIBs\n            which need to identify unicast or multicast routing\n            mechanisms.\n\n            Any additions or changes to the contents of this MIB module\n            require either publication of an RFC, or Designated Expert\n            Review as defined in RFC 2434, Guidelines for Writing an\n            IANA Considerations Section in RFCs.  The Designated Expert \n            will be selected by the IESG Area Director(s) of the Routing\n            Area.')

class IANAipRouteProtocol(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17))
    namedValues = NamedValues(('other', 1), ('local', 2), ('netmgmt', 3), ('icmp',
                                                                           4), ('egp',
                                                                                5), ('ggp',
                                                                                     6), ('hello',
                                                                                          7), ('rip',
                                                                                               8), ('isIs',
                                                                                                    9), ('esIs',
                                                                                                         10), ('ciscoIgrp',
                                                                                                               11), ('bbnSpfIgp',
                                                                                                                     12), ('ospf',
                                                                                                                           13), ('bgp',
                                                                                                                                 14), ('idpr',
                                                                                                                                       15), ('ciscoEigrp',
                                                                                                                                             16), ('dvmrp',
                                                                                                                                                   17))


class IANAipMRouteProtocol(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12))
    namedValues = NamedValues(('other', 1), ('local', 2), ('netmgmt', 3), ('dvmrp',
                                                                           4), ('mospf',
                                                                                5), ('pimSparseDense',
                                                                                     6), ('cbt',
                                                                                          7), ('pimSparseMode',
                                                                                               8), ('pimDenseMode',
                                                                                                    9), ('igmpOnly',
                                                                                                         10), ('bgmp',
                                                                                                               11), ('msdp',
                                                                                                                     12))


mibBuilder.exportSymbols('IANA-RTPROTO-MIB', IANAipMRouteProtocol=IANAipMRouteProtocol, PYSNMP_MODULE_ID=ianaRtProtoMIB, ianaRtProtoMIB=ianaRtProtoMIB, IANAipRouteProtocol=IANAipRouteProtocol)