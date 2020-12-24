# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/HCNUM-TC.py
# Compiled at: 2016-02-13 18:10:39
(Integer, OctetString, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'Integer', 'OctetString', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ConstraintsUnion, ValueRangeConstraint, ConstraintsIntersection, SingleValueConstraint, ValueSizeConstraint) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ConstraintsUnion', 'ValueRangeConstraint', 'ConstraintsIntersection', 'SingleValueConstraint', 'ValueSizeConstraint')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(Gauge32, Counter64, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, TimeTicks, ModuleIdentity, Unsigned32, IpAddress, iso, NotificationType, Bits, mib_2, ObjectIdentity, Integer32, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'Counter64', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'MibIdentifier', 'TimeTicks', 'ModuleIdentity', 'Unsigned32', 'IpAddress', 'iso', 'NotificationType', 'Bits', 'mib-2', 'ObjectIdentity', 'Integer32', 'Counter32')
(TextualConvention, DisplayString) = mibBuilder.importSymbols('SNMPv2-TC', 'TextualConvention', 'DisplayString')
hcnumTC = ModuleIdentity((1, 3, 6, 1, 2, 1, 78)).setRevisions(('2000-06-08 00:00', ))
if mibBuilder.loadTexts:
    hcnumTC.setLastUpdated('200006080000Z')
if mibBuilder.loadTexts:
    hcnumTC.setOrganization('IETF OPS Area')
if mibBuilder.loadTexts:
    hcnumTC.setContactInfo('        E-mail: mibs@ops.ietf.org\n                    Subscribe: majordomo@psg.com\n                      with msg body: subscribe mibs\n\n                    Andy Bierman\n                    Cisco Systems Inc.\n                    170 West Tasman Drive\n                    San Jose, CA 95134 USA\n                    +1 408-527-3711\n                    abierman@cisco.com\n\n                    Keith McCloghrie\n                    Cisco Systems Inc.\n                    170 West Tasman Drive\n                    San Jose, CA 95134 USA\n                    +1 408-526-5260\n                    kzm@cisco.com\n\n                    Randy Presuhn\n                    BMC Software, Inc.\n                    Office 1-3141\n                    2141 North First Street\n                    San Jose,  California 95131 USA\n                    +1 408 546-1006\n                    rpresuhn@bmc.com')
if mibBuilder.loadTexts:
    hcnumTC.setDescription('A MIB module containing textual conventions\n            for high capacity data types. This module\n            addresses an immediate need for data types not directly\n            supported in the SMIv2. This short-term solution\n            is meant to be deprecated as a long-term solution\n            is deployed.')

class CounterBasedGauge64(Counter64, TextualConvention):
    __module__ = __name__


class ZeroBasedCounter64(Counter64, TextualConvention):
    __module__ = __name__


mibBuilder.exportSymbols('HCNUM-TC', ZeroBasedCounter64=ZeroBasedCounter64, CounterBasedGauge64=CounterBasedGauge64, PYSNMP_MODULE_ID=hcnumTC, hcnumTC=hcnumTC)