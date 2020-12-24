# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/RFC1158-MIB.py
# Compiled at: 2019-08-18 17:24:05
(Integer32, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, iso, Gauge32, MibIdentifier, Bits, Counter32) = mibBuilder.importSymbols('SNMPv2-SMI', 'Integer32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'TimeTicks', 'iso', 'Gauge32', 'MibIdentifier', 'Bits', 'Counter32')
snmpInBadTypes = MibScalar((1, 3, 6, 1, 2, 1, 11, 7), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpInBadTypes.setStatus('mandatory')
snmpOutReadOnlys = MibScalar((1, 3, 6, 1, 2, 1, 11, 23), Counter32()).setMaxAccess('readonly')
if mibBuilder.loadTexts:
    snmpOutReadOnlys.setStatus('mandatory')
mibBuilder.exportSymbols('RFC1158-MIB', snmpOutReadOnlys=snmpOutReadOnlys, snmpInBadTypes=snmpInBadTypes)