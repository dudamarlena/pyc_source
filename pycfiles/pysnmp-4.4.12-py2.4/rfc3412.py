# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/rfc3412.py
# Compiled at: 2019-08-18 17:24:05
import sys
from pyasn1.compat.octets import null
from pyasn1.error import PyAsn1Error
from pysnmp.smi import builder, instrum
from pysnmp.proto import errind, error, cache
from pysnmp.proto.api import verdec
from pysnmp.error import PySnmpError
from pysnmp import nextid, debug

class MsgAndPduDispatcher(object):
    """SNMP engine PDU & message dispatcher. Exchanges SNMP PDU's with
       applications and serialized messages with transport level.
    """
    __module__ = __name__

    def __init__(self, mibInstrumController=None):
        if mibInstrumController is None:
            self.mibInstrumController = instrum.MibInstrumController(builder.MibBuilder())
        else:
            self.mibInstrumController = mibInstrumController
        self.mibInstrumController.mibBuilder.loadModules('SNMPv2-MIB', 'SNMP-MPD-MIB', 'SNMP-COMMUNITY-MIB', 'SNMP-TARGET-MIB', 'SNMP-USER-BASED-SM-MIB')
        self.__cache = cache.Cache()
        self.__appsRegistration = {}
        self.__sendPduHandle = nextid.Integer(16777215)
        self.__transportInfo = {}
        return

    def getTransportInfo(self, stateReference):
        if stateReference in self.__transportInfo:
            return self.__transportInfo[stateReference]
        else:
            raise error.ProtocolError('No data for stateReference %s' % stateReference)

    def registerContextEngineId(self, contextEngineId, pduTypes, processPdu):
        """Register application with dispatcher"""
        for pduType in pduTypes:
            k = (
             contextEngineId, pduType)
            if k in self.__appsRegistration:
                raise error.ProtocolError('Duplicate registration %r/%s' % (contextEngineId, pduType))
            self.__appsRegistration[k] = processPdu

        debug.logger & debug.flagDsp and debug.logger('registerContextEngineId: contextEngineId %r pduTypes %s' % (contextEngineId, pduTypes))

    def unregisterContextEngineId(self, contextEngineId, pduTypes):
        """Unregister application with dispatcher"""
        if contextEngineId is None:
            (contextEngineId,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMP-FRAMEWORK-MIB', 'snmpEngineID')
        for pduType in pduTypes:
            k = (
             contextEngineId, pduType)
            if k in self.__appsRegistration:
                del self.__appsRegistration[k]

        debug.logger & debug.flagDsp and debug.logger('unregisterContextEngineId: contextEngineId %r pduTypes %s' % (contextEngineId, pduTypes))
        return

    def getRegisteredApp(self, contextEngineId, pduType):
        k = (
         contextEngineId, pduType)
        if k in self.__appsRegistration:
            return self.__appsRegistration[k]
        k = (
         null, pduType)
        if k in self.__appsRegistration:
            return self.__appsRegistration[k]

    def sendPdu(self, snmpEngine, transportDomain, transportAddress, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, expectResponse, timeout=0, cbFun=None, cbCtx=None):
        """PDU dispatcher -- prepare and serialize a request or notification"""
        k = int(messageProcessingModel)
        if k in snmpEngine.messageProcessingSubsystems:
            mpHandler = snmpEngine.messageProcessingSubsystems[k]
        else:
            raise error.StatusInformation(errorIndication=errind.unsupportedMsgProcessingModel)
        debug.logger & debug.flagDsp and debug.logger('sendPdu: securityName %s, PDU\n%s' % (securityName, PDU.prettyPrint()))
        sendPduHandle = self.__sendPduHandle()
        if expectResponse:
            self.__cache.add(sendPduHandle, messageProcessingModel=messageProcessingModel, sendPduHandle=sendPduHandle, timeout=timeout + snmpEngine.transportDispatcher.getTimerTicks(), cbFun=cbFun, cbCtx=cbCtx)
            debug.logger & debug.flagDsp and debug.logger('sendPdu: current time %d ticks, one tick is %s seconds' % (snmpEngine.transportDispatcher.getTimerTicks(), snmpEngine.transportDispatcher.getTimerResolution()))
        debug.logger & debug.flagDsp and debug.logger('sendPdu: new sendPduHandle %s, timeout %s ticks, cbFun %s' % (sendPduHandle, timeout, cbFun))
        origTransportDomain = transportDomain
        origTransportAddress = transportAddress
        try:
            (transportDomain, transportAddress, outgoingMessage) = mpHandler.prepareOutgoingMessage(snmpEngine, origTransportDomain, origTransportAddress, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, expectResponse, sendPduHandle)
            debug.logger & debug.flagDsp and debug.logger('sendPdu: MP succeeded')
        except PySnmpError:
            if expectResponse:
                self.__cache.pop(sendPduHandle)
                self.releaseStateInformation(snmpEngine, sendPduHandle, messageProcessingModel)
            raise

        if snmpEngine.transportDispatcher is None:
            if expectResponse:
                self.__cache.pop(sendPduHandle)
            raise error.PySnmpError('Transport dispatcher not set')
        snmpEngine.observer.storeExecutionContext(snmpEngine, 'rfc3412.sendPdu', dict(transportDomain=transportDomain, transportAddress=transportAddress, outgoingMessage=outgoingMessage, messageProcessingModel=messageProcessingModel, securityModel=securityModel, securityName=securityName, securityLevel=securityLevel, contextEngineId=contextEngineId, contextName=contextName, pdu=PDU))
        try:
            snmpEngine.transportDispatcher.sendMessage(outgoingMessage, transportDomain, transportAddress)
        except PySnmpError:
            if expectResponse:
                self.__cache.pop(sendPduHandle)
            raise

        snmpEngine.observer.clearExecutionContext(snmpEngine, 'rfc3412.sendPdu')
        if expectResponse:
            self.__cache.update(sendPduHandle, transportDomain=origTransportDomain, transportAddress=origTransportAddress, securityModel=securityModel, securityName=securityName, securityLevel=securityLevel, contextEngineId=contextEngineId, contextName=contextName, pduVersion=pduVersion, PDU=PDU)
        return sendPduHandle

    def returnResponsePdu(self, snmpEngine, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, maxSizeResponseScopedPDU, stateReference, statusInformation):
        k = int(messageProcessingModel)
        if k in snmpEngine.messageProcessingSubsystems:
            mpHandler = snmpEngine.messageProcessingSubsystems[k]
        else:
            raise error.StatusInformation(errorIndication=errind.unsupportedMsgProcessingModel)
        debug.logger & debug.flagDsp and debug.logger('returnResponsePdu: PDU %s' % (PDU and PDU.prettyPrint() or '<empty>',))
        try:
            (transportDomain, transportAddress, outgoingMessage) = mpHandler.prepareResponseMessage(snmpEngine, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, maxSizeResponseScopedPDU, stateReference, statusInformation)
            debug.logger & debug.flagDsp and debug.logger('returnResponsePdu: MP suceeded')
        except error.StatusInformation:
            raise

        (snmpEngineMaxMessageSize,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMP-FRAMEWORK-MIB', 'snmpEngineMaxMessageSize')
        if snmpEngineMaxMessageSize.syntax and len(outgoingMessage) > snmpEngineMaxMessageSize.syntax:
            (snmpSilentDrops,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'snmpSilentDrops')
            snmpSilentDrops.syntax += 1
            raise error.StatusInformation(errorIndication=errind.tooBig)
        snmpEngine.observer.storeExecutionContext(snmpEngine, 'rfc3412.returnResponsePdu', dict(transportDomain=transportDomain, transportAddress=transportAddress, outgoingMessage=outgoingMessage, messageProcessingModel=messageProcessingModel, securityModel=securityModel, securityName=securityName, securityLevel=securityLevel, contextEngineId=contextEngineId, contextName=contextName, pdu=PDU))
        snmpEngine.transportDispatcher.sendMessage(outgoingMessage, transportDomain, transportAddress)
        snmpEngine.observer.clearExecutionContext(snmpEngine, 'rfc3412.returnResponsePdu')

    def receiveMessage(self, snmpEngine, transportDomain, transportAddress, wholeMsg):
        """Message dispatcher -- de-serialize message into PDU"""
        (snmpInPkts,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'snmpInPkts')
        snmpInPkts.syntax += 1
        try:
            restOfWholeMsg = null
            msgVersion = verdec.decodeMessageVersion(wholeMsg)
        except error.ProtocolError:
            (snmpInASNParseErrs,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'snmpInASNParseErrs')
            snmpInASNParseErrs.syntax += 1
            return null

        debug.logger & debug.flagDsp and debug.logger('receiveMessage: msgVersion %s, msg decoded' % msgVersion)
        messageProcessingModel = msgVersion
        try:
            mpHandler = snmpEngine.messageProcessingSubsystems[int(messageProcessingModel)]
        except KeyError:
            (snmpInBadVersions,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'snmpInBadVersions')
            snmpInBadVersions.syntax += 1
            return restOfWholeMsg

        try:
            (messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, pduType, sendPduHandle, maxSizeResponseScopedPDU, statusInformation, stateReference) = mpHandler.prepareDataElements(snmpEngine, transportDomain, transportAddress, wholeMsg)
            debug.logger & debug.flagDsp and debug.logger('receiveMessage: MP succeded')
        except error.StatusInformation:
            statusInformation = sys.exc_info()[1]
            if 'sendPduHandle' in statusInformation:
                debug.logger & debug.flagDsp and debug.logger('receiveMessage: MP failed, statusInformation %s, forcing a retry' % statusInformation)
                self.__expireRequest(statusInformation['sendPduHandle'], self.__cache.pop(statusInformation['sendPduHandle']), snmpEngine, statusInformation)
            return restOfWholeMsg
        except PyAsn1Error:
            debug.logger & debug.flagMP and debug.logger('receiveMessage: %s' % (sys.exc_info()[1],))
            (snmpInASNParseErrs,) = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'snmpInASNParseErrs')
            snmpInASNParseErrs.syntax += 1
            return restOfWholeMsg

        debug.logger & debug.flagDsp and debug.logger('receiveMessage: PDU %s' % PDU.prettyPrint())
        if sendPduHandle is None:
            debug.logger & debug.flagDsp and debug.logger('receiveMessage: pduType %s' % pduType)
            processPdu = self.getRegisteredApp(contextEngineId, pduType)
            if processPdu is None:
                (snmpUnknownPDUHandlers,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMP-MPD-MIB', 'snmpUnknownPDUHandlers')
                snmpUnknownPDUHandlers.syntax += 1
                statusInformation = {'errorIndication': errind.unknownPDUHandler, 'oid': snmpUnknownPDUHandlers.name, 'val': snmpUnknownPDUHandlers.syntax}
                debug.logger & debug.flagDsp and debug.logger('receiveMessage: unhandled PDU type')
                try:
                    (destTransportDomain, destTransportAddress, outgoingMessage) = mpHandler.prepareResponseMessage(snmpEngine, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, maxSizeResponseScopedPDU, stateReference, statusInformation)
                    snmpEngine.transportDispatcher.sendMessage(outgoingMessage, destTransportDomain, destTransportAddress)
                except PySnmpError:
                    debug.logger & debug.flagDsp and debug.logger('receiveMessage: report failed, statusInformation %s' % sys.exc_info()[1])
                else:
                    debug.logger & debug.flagDsp and debug.logger('receiveMessage: reporting succeeded')

                return restOfWholeMsg
            else:
                snmpEngine.observer.storeExecutionContext(snmpEngine, 'rfc3412.receiveMessage:request', dict(transportDomain=transportDomain, transportAddress=transportAddress, wholeMsg=wholeMsg, messageProcessingModel=messageProcessingModel, securityModel=securityModel, securityName=securityName, securityLevel=securityLevel, contextEngineId=contextEngineId, contextName=contextName, pdu=PDU))
                if stateReference is not None:
                    self.__transportInfo[stateReference] = (
                     transportDomain, transportAddress)
                processPdu(snmpEngine, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, maxSizeResponseScopedPDU, stateReference)
                snmpEngine.observer.clearExecutionContext(snmpEngine, 'rfc3412.receiveMessage:request')
                if stateReference is not None:
                    del self.__transportInfo[stateReference]
                debug.logger & debug.flagDsp and debug.logger('receiveMessage: processPdu succeeded')
                return restOfWholeMsg
        else:
            cachedParams = self.__cache.pop(sendPduHandle)
            if cachedParams is None:
                (snmpUnknownPDUHandlers,) = self.mibInstrumController.mibBuilder.importSymbols('__SNMP-MPD-MIB', 'snmpUnknownPDUHandlers')
                snmpUnknownPDUHandlers.syntax += 1
                return restOfWholeMsg
            debug.logger & debug.flagDsp and debug.logger('receiveMessage: cache read by sendPduHandle %s' % sendPduHandle)
            snmpEngine.observer.storeExecutionContext(snmpEngine, 'rfc3412.receiveMessage:response', dict(transportDomain=transportDomain, transportAddress=transportAddress, wholeMsg=wholeMsg, messageProcessingModel=messageProcessingModel, securityModel=securityModel, securityName=securityName, securityLevel=securityLevel, contextEngineId=contextEngineId, contextName=contextName, pdu=PDU))
            processResponsePdu = cachedParams['cbFun']
            processResponsePdu(snmpEngine, messageProcessingModel, securityModel, securityName, securityLevel, contextEngineId, contextName, pduVersion, PDU, statusInformation, cachedParams['sendPduHandle'], cachedParams['cbCtx'])
            snmpEngine.observer.clearExecutionContext(snmpEngine, 'rfc3412.receiveMessage:response')
            debug.logger & debug.flagDsp and debug.logger('receiveMessage: processResponsePdu succeeded')
            return restOfWholeMsg
        return

    def releaseStateInformation(self, snmpEngine, sendPduHandle, messageProcessingModel):
        k = int(messageProcessingModel)
        if k in snmpEngine.messageProcessingSubsystems:
            mpHandler = snmpEngine.messageProcessingSubsystems[k]
            mpHandler.releaseStateInformation(sendPduHandle)
        self.__cache.pop(sendPduHandle)

    def __expireRequest(self, cacheKey, cachedParams, snmpEngine, statusInformation=None):
        timeNow = snmpEngine.transportDispatcher.getTimerTicks()
        timeoutAt = cachedParams['timeout']
        if statusInformation is None and timeNow < timeoutAt:
            return
        processResponsePdu = cachedParams['cbFun']
        debug.logger & debug.flagDsp and debug.logger('__expireRequest: req cachedParams %s' % cachedParams)
        if not statusInformation:
            statusInformation = error.StatusInformation(errorIndication=errind.requestTimedOut)
        self.releaseStateInformation(snmpEngine, cachedParams['sendPduHandle'], cachedParams['messageProcessingModel'])
        processResponsePdu(snmpEngine, None, None, None, None, None, None, None, None, statusInformation, cachedParams['sendPduHandle'], cachedParams['cbCtx'])
        return True

    def receiveTimerTick(self, snmpEngine, timeNow):
        self.__cache.expire(self.__expireRequest, snmpEngine)