# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc7860/auth/hmacsha2.py
# Compiled at: 2019-08-18 17:24:05
import sys, hmac
try:
    from hashlib import sha224, sha256, sha384, sha512
except ImportError:

    class NotAvailable(object):
        __module__ = __name__

        def __call__(self, *args, **kwargs):
            raise errind.authenticationError


    sha224 = sha256 = sha384 = sha512 = NotAvailable()

from pyasn1.type import univ
from pysnmp.proto.secmod.rfc3414.auth import base
from pysnmp.proto.secmod.rfc3414 import localkey
from pysnmp.proto import errind, error

class HmacSha2(base.AbstractAuthenticationService):
    __module__ = __name__
    sha224ServiceID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 4)
    sha256ServiceID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 5)
    sha384ServiceID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 6)
    sha512ServiceID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 7)
    keyLengths = {sha224ServiceID: 28, sha256ServiceID: 32, sha384ServiceID: 48, sha512ServiceID: 64}
    digestLengths = {sha224ServiceID: 16, sha256ServiceID: 24, sha384ServiceID: 32, sha512ServiceID: 48}
    hashAlgorithms = {sha224ServiceID: sha224, sha256ServiceID: sha256, sha384ServiceID: sha384, sha512ServiceID: sha512}
    __ipad = [
     54] * 64
    __opad = [92] * 64

    def __init__(self, oid):
        if oid not in self.hashAlgorithms:
            raise error.ProtocolError('No SHA-2 authentication algorithm %s available' % (oid,))
        self.__hashAlgo = self.hashAlgorithms[oid]
        self.__digestLength = self.digestLengths[oid]
        self.__placeHolder = univ.OctetString((0, ) * self.__digestLength).asOctets()

    def hashPassphrase(self, authKey):
        return localkey.hashPassphrase(authKey, self.__hashAlgo)

    def localizeKey(self, authKey, snmpEngineID):
        return localkey.localizeKey(authKey, snmpEngineID, self.__hashAlgo)

    @property
    def digestLength(self):
        return self.__digestLength

    def authenticateOutgoingMsg(self, authKey, wholeMsg):
        location = wholeMsg.find(self.__placeHolder)
        if location == -1:
            raise error.ProtocolError("Can't locate digest placeholder")
        wholeHead = wholeMsg[:location]
        wholeTail = wholeMsg[location + self.__digestLength:]
        try:
            mac = hmac.new(authKey.asOctets(), wholeMsg, self.__hashAlgo)
        except errind.ErrorIndication:
            raise error.StatusInformation(errorIndication=sys.exc_info()[1])

        mac = mac.digest()[:self.__digestLength]
        return wholeHead + mac + wholeTail

    def authenticateIncomingMsg(self, authKey, authParameters, wholeMsg):
        if len(authParameters) != self.__digestLength:
            raise error.StatusInformation(errorIndication=errind.authenticationError)
        location = wholeMsg.find(authParameters.asOctets())
        if location == -1:
            raise error.ProtocolError("Can't locate digest in wholeMsg")
        wholeHead = wholeMsg[:location]
        wholeTail = wholeMsg[location + self.__digestLength:]
        authenticatedWholeMsg = wholeHead + self.__placeHolder + wholeTail
        try:
            mac = hmac.new(authKey.asOctets(), authenticatedWholeMsg, self.__hashAlgo)
        except errind.ErrorIndication:
            raise error.StatusInformation(errorIndication=sys.exc_info()[1])

        mac = mac.digest()[:self.__digestLength]
        if mac != authParameters:
            raise error.StatusInformation(errorIndication=errind.authenticationFailure)
        return authenticatedWholeMsg