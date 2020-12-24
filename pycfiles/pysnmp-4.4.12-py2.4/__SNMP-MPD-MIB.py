# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/instances/__SNMP-MPD-MIB.py
# Compiled at: 2019-08-18 17:24:05
(MibScalarInstance,) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')
(snmpUnknownSecurityModels, snmpInvalidMsgs, snmpUnknownPDUHandlers) = mibBuilder.importSymbols('SNMP-MPD-MIB', 'snmpUnknownSecurityModels', 'snmpInvalidMsgs', 'snmpUnknownPDUHandlers')
__snmpUnknownSecurityModels = MibScalarInstance(snmpUnknownSecurityModels.name, (0, ), snmpUnknownSecurityModels.syntax.clone(0))
__snmpInvalidMsgs = MibScalarInstance(snmpInvalidMsgs.name, (0, ), snmpInvalidMsgs.syntax.clone(0))
__snmpUnknownPDUHandlers = MibScalarInstance(snmpUnknownPDUHandlers.name, (0, ), snmpUnknownPDUHandlers.syntax.clone(0))
mibBuilder.exportSymbols('__SNMP-MPD-MIB', snmpUnknownSecurityModels=__snmpUnknownSecurityModels, snmpInvalidMsgs=__snmpInvalidMsgs, snmpUnknownPDUHandlers=__snmpUnknownPDUHandlers)