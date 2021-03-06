# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/IANA-MALLOC-MIB.py
# Compiled at: 2016-02-13 18:15:58
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, Counter64, iso, Counter32, MibIdentifier, NotificationType, Integer32, ObjectIdentity, Bits, ModuleIdentity, TimeTicks, mib_2, IpAddress) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Unsigned32', 'Counter64', 'iso', 'Counter32', 'MibIdentifier', 'NotificationType', 'Integer32', 'ObjectIdentity', 'Bits', 'ModuleIdentity', 'TimeTicks', 'mib-2', 'IpAddress')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
ianaMallocMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 102)).setRevisions(('2003-01-27 12:00', ))
if mibBuilder.loadTexts:
    ianaMallocMIB.setLastUpdated('200301271200Z')
if mibBuilder.loadTexts:
    ianaMallocMIB.setOrganization('IANA')
if mibBuilder.loadTexts:
    ianaMallocMIB.setContactInfo(' Internet Assigned Numbers Authority\n              Internet Corporation for Assigned Names and Numbers\n              4676 Admiralty Way, Suite 330\n              Marina del Rey, CA 90292-6601\n\n              Phone: +1 310 823 9358\n              EMail: iana@iana.org')
if mibBuilder.loadTexts:
    ianaMallocMIB.setDescription('This MIB module defines the IANAscopeSource and\n            IANAmallocRangeSource textual conventions for use in MIBs\n            which need to identify ways of learning multicast scope and\n            range information.\n\n            Any additions or changes to the contents of this MIB module\n            require either publication of an RFC, or Designated Expert\n            Review as defined in the Guidelines for Writing IANA\n            Considerations Section document.  The Designated Expert will\n            be selected by the IESG Area Director(s) of the Transport\n            Area.')

class IANAscopeSource(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3, 4, 5))
    namedValues = NamedValues(('other', 1), ('manual', 2), ('local', 3), ('mzap', 4), ('madcap',
                                                                                       5))


class IANAmallocRangeSource(Integer32, TextualConvention):
    __module__ = __name__
    subtypeSpec = Integer32.subtypeSpec + ConstraintsUnion(SingleValueConstraint(1, 2, 3))
    namedValues = NamedValues(('other', 1), ('manual', 2), ('local', 3))


mibBuilder.exportSymbols('IANA-MALLOC-MIB', IANAmallocRangeSource=IANAmallocRangeSource, PYSNMP_MODULE_ID=ianaMallocMIB, ianaMallocMIB=ianaMallocMIB, IANAscopeSource=IANAscopeSource)