# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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