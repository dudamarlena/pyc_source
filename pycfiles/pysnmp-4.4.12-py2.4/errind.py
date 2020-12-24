# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/errind.py
# Compiled at: 2019-08-18 17:24:05


class ErrorIndication(Exception):
    """SNMPv3 error-indication values"""
    __module__ = __name__

    def __init__(self, descr=None):
        self.__value = self.__descr = self.__class__.__name__[0].lower() + self.__class__.__name__[1:]
        if descr:
            self.__descr = descr

    def __eq__(self, other):
        return self.__value == other

    def __ne__(self, other):
        return self.__value != other

    def __lt__(self, other):
        return self.__value < other

    def __le__(self, other):
        return self.__value <= other

    def __gt__(self, other):
        return self.__value > other

    def __ge__(self, other):
        return self.__value >= other

    def __str__(self):
        return self.__descr


class SerializationError(ErrorIndication):
    __module__ = __name__


serializationError = SerializationError('SNMP message serialization error')

class DeserializationError(ErrorIndication):
    __module__ = __name__


deserializationError = DeserializationError('SNMP message deserialization error')

class ParseError(DeserializationError):
    __module__ = __name__


parseError = ParseError('SNMP message deserialization error')

class UnsupportedMsgProcessingModel(ErrorIndication):
    __module__ = __name__


unsupportedMsgProcessingModel = UnsupportedMsgProcessingModel('Unknown SNMP message processing model ID encountered')

class UnknownPDUHandler(ErrorIndication):
    __module__ = __name__


unknownPDUHandler = UnknownPDUHandler('Unhandled PDU type encountered')

class UnsupportedPDUtype(ErrorIndication):
    __module__ = __name__


unsupportedPDUtype = UnsupportedPDUtype('Unsupported SNMP PDU type encountered')

class RequestTimedOut(ErrorIndication):
    __module__ = __name__


requestTimedOut = RequestTimedOut('No SNMP response received before timeout')

class EmptyResponse(ErrorIndication):
    __module__ = __name__


emptyResponse = EmptyResponse('Empty SNMP response message')

class NonReportable(ErrorIndication):
    __module__ = __name__


nonReportable = NonReportable('Report PDU generation not attempted')

class DataMismatch(ErrorIndication):
    __module__ = __name__


dataMismatch = DataMismatch('SNMP request/response parameters mismatched')

class EngineIDMismatch(ErrorIndication):
    __module__ = __name__


engineIDMismatch = EngineIDMismatch('SNMP engine ID mismatch encountered')

class UnknownEngineID(ErrorIndication):
    __module__ = __name__


unknownEngineID = UnknownEngineID('Unknown SNMP engine ID encountered')

class TooBig(ErrorIndication):
    __module__ = __name__


tooBig = TooBig('SNMP message will be too big')

class LoopTerminated(ErrorIndication):
    __module__ = __name__


loopTerminated = LoopTerminated('Infinite SNMP entities talk terminated')

class InvalidMsg(ErrorIndication):
    __module__ = __name__


invalidMsg = InvalidMsg('Invalid SNMP message header parameters encountered')

class UnknownCommunityName(ErrorIndication):
    __module__ = __name__


unknownCommunityName = UnknownCommunityName('Unknown SNMP community name encountered')

class NoEncryption(ErrorIndication):
    __module__ = __name__


noEncryption = NoEncryption('No encryption services configured')

class EncryptionError(ErrorIndication):
    __module__ = __name__


encryptionError = EncryptionError('Ciphering services not available')

class DecryptionError(ErrorIndication):
    __module__ = __name__


decryptionError = DecryptionError('Ciphering services not available or ciphertext is broken')

class NoAuthentication(ErrorIndication):
    __module__ = __name__


noAuthentication = NoAuthentication('No authentication services configured')

class AuthenticationError(ErrorIndication):
    __module__ = __name__


authenticationError = AuthenticationError('Ciphering services not available or bad parameters')

class AuthenticationFailure(ErrorIndication):
    __module__ = __name__


authenticationFailure = AuthenticationFailure('Authenticator mismatched')

class UnsupportedAuthProtocol(ErrorIndication):
    __module__ = __name__


unsupportedAuthProtocol = UnsupportedAuthProtocol('Authentication protocol is not supprted')

class UnsupportedPrivProtocol(ErrorIndication):
    __module__ = __name__


unsupportedPrivProtocol = UnsupportedPrivProtocol('Privacy protocol is not supprted')

class UnknownSecurityName(ErrorIndication):
    __module__ = __name__


unknownSecurityName = UnknownSecurityName('Unknown SNMP security name encountered')

class UnsupportedSecurityModel(ErrorIndication):
    __module__ = __name__


unsupportedSecurityModel = UnsupportedSecurityModel('Unsupported SNMP security model')

class UnsupportedSecurityLevel(ErrorIndication):
    __module__ = __name__


UnsupportedSecLevel = UnsupportedSecurityLevel
unsupportedSecurityLevel = UnsupportedSecurityLevel('Unsupported SNMP security level')

class NotInTimeWindow(ErrorIndication):
    __module__ = __name__


notInTimeWindow = NotInTimeWindow('SNMP message timing parameters not in windows of trust')

class UnknownUserName(ErrorIndication):
    __module__ = __name__


unknownUserName = UnknownUserName('Unknown USM user')

class WrongDigest(ErrorIndication):
    __module__ = __name__


wrongDigest = WrongDigest('Wrong SNMP PDU digest')

class ReportPduReceived(ErrorIndication):
    __module__ = __name__


reportPduReceived = ReportPduReceived('Remote SNMP engine reported error')

class NoSuchView(ErrorIndication):
    __module__ = __name__


noSuchView = NoSuchView('No such MIB view currently exists')

class NoAccessEntry(ErrorIndication):
    __module__ = __name__


noAccessEntry = NoAccessEntry('Access to MIB node denined')

class NoGroupName(ErrorIndication):
    __module__ = __name__


noGroupName = NoGroupName('No such VACM group configured')

class NoSuchContext(ErrorIndication):
    __module__ = __name__


noSuchContext = NoSuchContext('SNMP context now found')

class NotInView(ErrorIndication):
    __module__ = __name__


notInView = NotInView('Requested OID is out of MIB view')

class AccessAllowed(ErrorIndication):
    __module__ = __name__


accessAllowed = AccessAllowed()

class OtherError(ErrorIndication):
    __module__ = __name__


otherError = OtherError('Unspecified SNMP engine error occurred')

class OidNotIncreasing(ErrorIndication):
    __module__ = __name__


oidNotIncreasing = OidNotIncreasing('OID not increasing')