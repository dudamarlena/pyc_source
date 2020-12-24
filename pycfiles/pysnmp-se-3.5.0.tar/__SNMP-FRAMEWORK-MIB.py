# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/instances/__SNMP-FRAMEWORK-MIB.py
# Compiled at: 2019-08-18 17:24:05
import time
(MibScalarInstance,) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')
(snmpEngineID, snmpEngineBoots, snmpEngineTime, snmpEngineMaxMessageSize) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'snmpEngineID', 'snmpEngineBoots', 'snmpEngineTime', 'snmpEngineMaxMessageSize')
__snmpEngineID = MibScalarInstance(snmpEngineID.name, (0, ), snmpEngineID.syntax)
__snmpEngineBoots = MibScalarInstance(snmpEngineBoots.name, (0, ), snmpEngineBoots.syntax.clone(1))
__snmpEngineTime = MibScalarInstance(snmpEngineTime.name, (0, ), snmpEngineTime.syntax.clone(int(time.time())))
__snmpEngineMaxMessageSize = MibScalarInstance(snmpEngineMaxMessageSize.name, (0, ), snmpEngineMaxMessageSize.syntax.clone(4096))
mibBuilder.exportSymbols('__SNMP-FRAMEWORK-MIB', snmpEngineID=__snmpEngineID, snmpEngineBoots=__snmpEngineBoots, snmpEngineTime=__snmpEngineTime, snmpEngineMaxMessageSize=__snmpEngineMaxMessageSize)