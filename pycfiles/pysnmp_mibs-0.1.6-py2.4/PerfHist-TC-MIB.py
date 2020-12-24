# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/PerfHist-TC-MIB.py
# Compiled at: 2016-02-13 18:04:05
(ObjectIdentifier, OctetString, Integer) = mibBuilder.importSymbols('ASN1', 'ObjectIdentifier', 'OctetString', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueRangeConstraint, SingleValueConstraint, ConstraintsUnion, ValueSizeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueRangeConstraint', 'SingleValueConstraint', 'ConstraintsUnion', 'ValueSizeConstraint', 'ConstraintsIntersection')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(Counter64, mib_2, NotificationType, ObjectIdentity, iso, Integer32, MibIdentifier, Gauge32, MibScalar, MibTable, MibTableRow, MibTableColumn, IpAddress, ModuleIdentity, Counter32, Unsigned32, TimeTicks, Bits) = mibBuilder.importSymbols('SNMPv2-SMI', 'Counter64', 'mib-2', 'NotificationType', 'ObjectIdentity', 'iso', 'Integer32', 'MibIdentifier', 'Gauge32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'IpAddress', 'ModuleIdentity', 'Counter32', 'Unsigned32', 'TimeTicks', 'Bits')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
perfHistTCMIB = ModuleIdentity((1, 3, 6, 1, 2, 1, 58))
if mibBuilder.loadTexts:
    perfHistTCMIB.setLastUpdated('9811071100Z')
if mibBuilder.loadTexts:
    perfHistTCMIB.setOrganization('IETF AToMMIB and TrunkMIB WGs')
if mibBuilder.loadTexts:
    perfHistTCMIB.setContactInfo('Kaj Tesink\n              Postal:  Bellcore\n                       331 Newman Springs Road\n                       Red Bank, NJ 07701\n                       USA\n              Tel:     +1 732 758 5254\n              Fax:     +1 732 758 2269\n              E-mail:  kaj@bellcore.com')
if mibBuilder.loadTexts:
    perfHistTCMIB.setDescription('This MIB Module provides Textual Conventions\n             to be used by systems supporting 15 minute\n             based performance history counts.')

class PerfCurrentCount(Gauge32, TextualConvention):
    __module__ = __name__


class PerfIntervalCount(Gauge32, TextualConvention):
    __module__ = __name__


class PerfTotalCount(Gauge32, TextualConvention):
    __module__ = __name__


mibBuilder.exportSymbols('PerfHist-TC-MIB', perfHistTCMIB=perfHistTCMIB, PYSNMP_MODULE_ID=perfHistTCMIB, PerfIntervalCount=PerfIntervalCount, PerfCurrentCount=PerfCurrentCount, PerfTotalCount=PerfTotalCount)