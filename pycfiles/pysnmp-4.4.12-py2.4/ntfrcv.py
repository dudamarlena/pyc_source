# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/entity/rfc3413/ntfrcv.py
# Compiled at: 2019-08-18 17:24:05
import sys
from pyasn1.compat.octets import null
from pysnmp.proto import rfc3411, error
from pysnmp.proto.api import v1, v2c
from pysnmp.proto.proxy import rfc2576
from pysnmp import debug

class NotificationReceiver(object):
    __module__ = __name__
    pduTypes = (v1.TrapPDU.tagSet, v2c.SNMPv2TrapPDU.tagSet, v2c.InformRequestPDU.tagSet)

    def __init__(self, snmpEngine, cbFun, cbCtx=None):
        snmpEngine.msgAndPduDsp.registerContextEngineId(null, self.pduTypes, self.processPdu)
        self.__snmpTrapCommunity = ''
        self.__cbFunVer = 0
        self.__cbFun = cbFun
        self.__cbCtx = cbCtx

        def storeSnmpTrapCommunity(snmpEngine, execpoint, variables, cbCtx):
            self.__snmpTrapCommunity = variables.get('communityName', '')

        snmpEngine.observer.registerObserver(storeSnmpTrapCommunity, 'rfc2576.processIncomingMsg')

    def close(self, snmpEngine):
        snmpEngine.msgAndPduDsp.unregisterContextEngineId(null, self.pduTypes)
        self.__cbFun = self.__cbCtx = None
        return

    def processPdu(self, snmpEngine, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, maxSizeResponseScopedPDU, stateReference):
        if messageProcessingModel == 0:
            origPdu = PDU
            PDU = rfc2576.v1ToV2(PDU, snmpTrapCommunity=self.__snmpTrapCommunity)
        else:
            origPdu = None
        errorStatus = 'noError'
        errorIndex = 0
        varBinds = v2c.apiPDU.getVarBinds(PDU)
        debug.logger & debug.flagApp and debug.logger('processPdu: stateReference %s, varBinds %s' % (stateReference, varBinds))
        if PDU.tagSet in rfc3411.confirmedClassPDUs:
            rspPDU = v2c.apiPDU.getResponse(PDU)
            v2c.apiPDU.setErrorStatus(rspPDU, errorStatus)
            v2c.apiPDU.setErrorIndex(rspPDU, errorIndex)
            v2c.apiPDU.setVarBinds(rspPDU, varBinds)
            debug.logger & debug.flagApp and debug.logger('processPdu: stateReference %s, confirm PDU %s' % (stateReference, rspPDU.prettyPrint()))
            if messageProcessingModel == 0:
                rspPDU = rfc2576.v2ToV1(rspPDU, origPdu)
            statusInformation = {}
            try:
                snmpEngine.msgAndPduDsp.returnResponsePdu(snmpEngine, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, rspPDU, maxSizeResponseScopedPDU, stateReference, statusInformation)
            except error.StatusInformation:
                debug.logger & debug.flagApp and debug.logger('processPdu: stateReference %s, statusInformation %s' % (stateReference, sys.exc_info()[1]))
                (snmpSilentDrops,) = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'snmpSilentDrops')
                snmpSilentDrops.syntax += 1

        elif PDU.tagSet in rfc3411.unconfirmedClassPDUs:
            pass
        else:
            raise error.ProtocolError('Unexpected PDU class %s' % PDU.tagSet)
        debug.logger & debug.flagApp and debug.logger('processPdu: stateReference %s, user cbFun %s, cbCtx %s, varBinds %s' % (stateReference, self.__cbFun, self.__cbCtx, varBinds))
        if self.__cbFunVer:
            self.__cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, self.__cbCtx)
        else:
            try:
                self.__cbFun(snmpEngine, contextEngineId, contextName, varBinds, self.__cbCtx)
            except TypeError:
                self.__cbFunVer = 1
                self.__cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, self.__cbCtx)

        return