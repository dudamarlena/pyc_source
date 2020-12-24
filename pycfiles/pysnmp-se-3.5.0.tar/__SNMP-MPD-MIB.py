# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/instances/__SNMP-MPD-MIB.py
# Compiled at: 2019-08-18 17:24:05
(MibScalarInstance,) = mibBuilder.importSymbols('SNMPv2-SMI', 'MibScalarInstance')
(snmpUnknownSecurityModels, snmpInvalidMsgs, snmpUnknownPDUHandlers) = mibBuilder.importSymbols('SNMP-MPD-MIB', 'snmpUnknownSecurityModels', 'snmpInvalidMsgs', 'snmpUnknownPDUHandlers')
__snmpUnknownSecurityModels = MibScalarInstance(snmpUnknownSecurityModels.name, (0, ), snmpUnknownSecurityModels.syntax.clone(0))
__snmpInvalidMsgs = MibScalarInstance(snmpInvalidMsgs.name, (0, ), snmpInvalidMsgs.syntax.clone(0))
__snmpUnknownPDUHandlers = MibScalarInstance(snmpUnknownPDUHandlers.name, (0, ), snmpUnknownPDUHandlers.syntax.clone(0))
mibBuilder.exportSymbols('__SNMP-MPD-MIB', snmpUnknownSecurityModels=__snmpUnknownSecurityModels, snmpInvalidMsgs=__snmpInvalidMsgs, snmpUnknownPDUHandlers=__snmpUnknownPDUHandlers)