# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/VPN-TC-STD-MIB.py
# Compiled at: 2016-02-13 18:20:45
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, SingleValueConstraint, ConstraintsUnion, ConstraintsIntersection, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ConstraintsIntersection', 'ValueSizeConstraint')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(iso, Counter64, IpAddress, Integer32, Bits, NotificationType, ObjectIdentity, Unsigned32, Gauge32, mib_2, MibScalar, MibTable, MibTableRow, MibTableColumn, ModuleIdentity, MibIdentifier, TimeTicks, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'iso', 'Counter64', 'IpAddress', 'Integer32', 'Bits', 'NotificationType', 'ObjectIdentity', 'Unsigned32', 'Gauge32', 'mib-2', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'ModuleIdentity', 'MibIdentifier', 'TimeTicks', 'Counter32')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
vpnTcMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 129)).setRevisions(('2005-11-15 00:00', ))
if mibBuilder.loadTexts:
    vpnTcMIB.setLastUpdated('200511150000Z')
if mibBuilder.loadTexts:
    vpnTcMIB.setOrganization('Layer 3 Virtual Private Networks (L3VPN) Working Group.')
if mibBuilder.loadTexts:
    vpnTcMIB.setContactInfo('Benson Schliesser\n         bensons@savvis.net\n\n         Thomas D. Nadeau\n         tnadeau@cisco.com\n\n         This TC MIB is a product of the PPVPN\n         http://www.ietf.org/html.charters/ppvpn-charter.html\n         and subsequently the L3VPN\n         http://www.ietf.org/html.charters/l3vpn-charter.html\n         working groups.\n\n         Comments and discussion should be directed to\n         l3vpn@ietf.org')
if mibBuilder.loadTexts:
    vpnTcMIB.setDescription('This MIB contains TCs for VPNs.\n\n         Copyright (C) The Internet Society (2005).  This version\n         of this MIB module is part of RFC 4265;  see the RFC\n         itself for full legal notices.')

class VPNId(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ValueSizeConstraint(7, 7)
    fixedLength = 7


class VPNIdOrZero(OctetString, TextualConvention):
    __module__ = __name__
    subtypeSpec = OctetString.subtypeSpec + ConstraintsUnion(ValueSizeConstraint(0, 0), ValueSizeConstraint(7, 7))


mibBuilder.exportSymbols('VPN-TC-STD-MIB', VPNId=VPNId, VPNIdOrZero=VPNIdOrZero, vpnTcMIB=vpnTcMIB, PYSNMP_MODULE_ID=vpnTcMIB)