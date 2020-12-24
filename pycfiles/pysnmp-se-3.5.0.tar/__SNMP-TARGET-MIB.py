# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/instances/__SNMP-TARGET-MIB.py
# Compiled at: 2019-08-18 17:24:05
(MibScalarInstance,) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')
(snmpTargetSpinLock, snmpUnavailableContexts, snmpUnknownContexts) = mibBuilder.importSymbols('SNMP-TARGET-MIB', 'snmpTargetSpinLock', 'snmpUnavailableContexts', 'snmpUnknownContexts')
__snmpTargetSpinLock = MibScalarInstance(snmpTargetSpinLock.name, (0, ), snmpTargetSpinLock.syntax.clone(0))
__snmpUnavailableContexts = MibScalarInstance(snmpUnavailableContexts.name, (0, ), snmpUnavailableContexts.syntax.clone(0))
__snmpUnknownContexts = MibScalarInstance(snmpUnknownContexts.name, (0, ), snmpUnknownContexts.syntax.clone(0))
mibBuilder.exportSymbols('__SNMP-TARGET-MIB', snmpTargetSpinLock=__snmpTargetSpinLock, snmpUnavailableContexts=__snmpUnavailableContexts, snmpUnknownContexts=__snmpUnknownContexts)