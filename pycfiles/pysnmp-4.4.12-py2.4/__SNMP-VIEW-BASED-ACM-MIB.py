# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/instances/__SNMP-VIEW-BASED-ACM-MIB.py
# Compiled at: 2019-08-18 17:24:05
(MibScalarInstance,) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')
(vacmViewSpinLock,) = mibBuilder.importSymbols('SNMP-VIEW-BASED-ACM-MIB', 'vacmViewSpinLock')
__vacmViewSpinLock = MibScalarInstance(vacmViewSpinLock.name, (0, ), vacmViewSpinLock.syntax)
mibBuilder.exportSymbols('__SNMP-VIEW-BASED-ACM-MIB', vacmViewSpinLock=__vacmViewSpinLock)