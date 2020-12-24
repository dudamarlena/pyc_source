# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc3414/auth/hmacsha.py
# Compiled at: 2019-08-18 17:24:05
try:
    from hashlib import sha1
except ImportError:
    import sha
    sha1 = sha.new

from pyasn1.type import univ
from pysnmp.proto.secmod.rfc3414.auth import base
from pysnmp.proto.secmod.rfc3414 import localkey
from pysnmp.proto import errind, error
_twelveZeros = univ.OctetString((0, ) * 12).asOctets()
_fortyFourZeros = (0, ) * 44

class HmacSha(base.AbstractAuthenticationService):
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 6, 3, 10, 1, 1, 3)
    __ipad = [54] * 64
    __opad = [92] * 64

    def hashPassphrase(self, authKey):
        return localkey.hashPassphraseSHA(authKey)

    def localizeKey(self, authKey, snmpEngineID):
        return localkey.localizeKeySHA(authKey, snmpEngineID)

    @property
    def digestLength(self):
        return 12

    def authenticateOutgoingMsg(self, authKey, wholeMsg):
        l = wholeMsg.find(_twelveZeros)
        if l == -1:
            raise error.ProtocolError('Cant locate digest placeholder')
        wholeHead = wholeMsg[:l]
        wholeTail = wholeMsg[l + 12:]
        extendedAuthKey = authKey.asNumbers() + _fortyFourZeros
        k1 = univ.OctetString(map(lambda x, y: x ^ y, extendedAuthKey, self.__ipad))
        k2 = univ.OctetString(map(lambda x, y: x ^ y, extendedAuthKey, self.__opad))
        d1 = sha1(k1.asOctets() + wholeMsg).digest()
        d2 = sha1(k2.asOctets() + d1).digest()
        mac = d2[:12]
        return wholeHead + mac + wholeTail

    def authenticateIncomingMsg(self, authKey, authParameters, wholeMsg):
        if len(authParameters) != 12:
            raise error.StatusInformation(errorIndication=errind.authenticationError)
        l = wholeMsg.find(authParameters.asOctets())
        if l == -1:
            raise error.ProtocolError('Cant locate digest in wholeMsg')
        wholeHead = wholeMsg[:l]
        wholeTail = wholeMsg[l + 12:]
        authenticatedWholeMsg = wholeHead + _twelveZeros + wholeTail
        extendedAuthKey = authKey.asNumbers() + _fortyFourZeros
        k1 = univ.OctetString(map(lambda x, y: x ^ y, extendedAuthKey, self.__ipad))
        k2 = univ.OctetString(map(lambda x, y: x ^ y, extendedAuthKey, self.__opad))
        d1 = sha1(k1.asOctets() + authenticatedWholeMsg).digest()
        d2 = sha1(k2.asOctets() + d1).digest()
        mac = d2[:12]
        if mac != authParameters:
            raise error.StatusInformation(errorIndication=errind.authenticationFailure)
        return authenticatedWholeMsg