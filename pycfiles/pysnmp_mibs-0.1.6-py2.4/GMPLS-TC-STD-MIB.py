# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/GMPLS-TC-STD-MIB.py
# Compiled at: 2016-02-13 18:13:51
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueRangeConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection')
(mplsStdMIB,) = mibBuilder.importSymbols('MPLS-TC-STD-MIB', 'mplsStdMIB')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Bits, Integer32, Unsigned32, Counter32, Gauge32, iso, MibIdentifier, ModuleIdentity, TimeTicks, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, NotificationType, IpAddress, Counter64) = mibBuilder.importSymbols('SNMPv2-SMI', 'Bits', 'Integer32', 'Unsigned32', 'Counter32', 'Gauge32', 'iso', 'MibIdentifier', 'ModuleIdentity', 'TimeTicks', 'ObjectIdentity', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'NotificationType', 'IpAddress', 'Counter64')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
gmplsTCStdMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 10, 166, 12)).setRevisions(('2007-02-28 00:00', ))
if mibBuilder.loadTexts:
    gmplsTCStdMIB.setLastUpdated('200702280000Z')
if mibBuilder.loadTexts:
    gmplsTCStdMIB.setOrganization('IETF Common Control and Measurement Plane (CCAMP) Working Group')
if mibBuilder.loadTexts:
    gmplsTCStdMIB.setContactInfo('       Thomas D. Nadeau\n               Cisco Systems, Inc.\n        Email: tnadeau@cisco.com\n\n               Adrian Farrel\n               Old Dog Consulting\n        Email: adrian@olddog.co.uk\n\n        Comments about this document should be emailed directly to the\n        CCAMP working group mailing list at ccamp@ops.ietf.org')
if mibBuilder.loadTexts:
    gmplsTCStdMIB.setDescription('Copyright (C) The IETF Trust (2007).  This version of\n        this MIB module is part of RFC 4801; see the RFC itself for\n        full legal notices.\n\n        This MIB module defines TEXTUAL-CONVENTIONs for concepts used in\n        Generalized Multiprotocol Label Switching (GMPLS) networks.')

class GmplsFreeformLabelTC(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(0, 64)


class GmplsLabelTypeTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5, 6))
    namedValues = NamedValues(('gmplsMplsLabel', 1), ('gmplsPortWavelengthLabel', 2), ('gmplsFreeformGeneralizedLabel',
                                                                                       3), ('gmplsSonetLabel',
                                                                                            4), ('gmplsSdhLabel',
                                                                                                 5), ('gmplsWavebandLabel',
                                                                                                      6))


class GmplsSegmentDirectionTC(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2))
    namedValues = NamedValues(('forward', 1), ('reverse', 2))


mibBuilder.exportSymbols('GMPLS-TC-STD-MIB', gmplsTCStdMIB=gmplsTCStdMIB, PYSNMP_MODULE_ID=gmplsTCStdMIB, GmplsSegmentDirectionTC=GmplsSegmentDirectionTC, GmplsLabelTypeTC=GmplsLabelTypeTC, GmplsFreeformLabelTC=GmplsFreeformLabelTC)