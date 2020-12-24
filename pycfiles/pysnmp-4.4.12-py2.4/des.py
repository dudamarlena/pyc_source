# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc3414/priv/des.py
# Compiled at: 2019-08-18 17:24:05
import random
from pysnmp.proto.secmod.rfc3414.priv import base
from pysnmp.proto.secmod.rfc3414.auth import hmacmd5, hmacsha
from pysnmp.proto.secmod.rfc3414 import localkey
from pysnmp.proto.secmod.rfc7860.auth import hmacsha2
from pysnmp.proto import errind, error
from pyasn1.type import univ
from sys import version_info
try:
    from Cryptodome.Cipher import DES
except ImportError:
    DES = None

try:
    from hashlib import md5, sha1
except ImportError:
    import md5, sha
    md5 = md5.new
    sha1 = sha.new

random.seed()

class Des(base.AbstractEncryptionService):
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 6, 3, 10, 1, 2, 2)
    keySize = 16
    if version_info < (2, 3):
        _localInt = int(random.random() * 4294967295)
    else:
        _localInt = random.randrange(0, 4294967295)

    def hashPassphrase(self, authProtocol, privKey):
        if authProtocol == hmacmd5.HmacMd5.serviceID:
            hashAlgo = md5
        elif authProtocol == hmacsha.HmacSha.serviceID:
            hashAlgo = sha1
        elif authProtocol in hmacsha2.HmacSha2.hashAlgorithms:
            hashAlgo = hmacsha2.HmacSha2.hashAlgorithms[authProtocol]
        else:
            raise error.ProtocolError('Unknown auth protocol %s' % (authProtocol,))
        return localkey.hashPassphrase(privKey, hashAlgo)

    def localizeKey(self, authProtocol, privKey, snmpEngineID):
        if authProtocol == hmacmd5.HmacMd5.serviceID:
            hashAlgo = md5
        elif authProtocol == hmacsha.HmacSha.serviceID:
            hashAlgo = sha1
        elif authProtocol in hmacsha2.HmacSha2.hashAlgorithms:
            hashAlgo = hmacsha2.HmacSha2.hashAlgorithms[authProtocol]
        else:
            raise error.ProtocolError('Unknown auth protocol %s' % (authProtocol,))
        localPrivKey = localkey.localizeKey(privKey, snmpEngineID, hashAlgo)
        return localPrivKey[:self.keySize]

    def __getEncryptionKey(self, privKey, snmpEngineBoots):
        desKey = privKey[:8]
        preIV = privKey[8:16]
        securityEngineBoots = int(snmpEngineBoots)
        salt = [
         securityEngineBoots >> 24 & 255, securityEngineBoots >> 16 & 255, securityEngineBoots >> 8 & 255, securityEngineBoots & 255, self._localInt >> 24 & 255, self._localInt >> 16 & 255, self._localInt >> 8 & 255, self._localInt & 255]
        if self._localInt == 4294967295:
            self._localInt = 0
        else:
            self._localInt += 1
        return (desKey.asOctets(), univ.OctetString(salt).asOctets(),
         univ.OctetString(map(lambda x, y: x ^ y, salt, preIV.asNumbers())).asOctets())

    @staticmethod
    def __getDecryptionKey(privKey, salt):
        return (privKey[:8].asOctets(),
         univ.OctetString(map(lambda x, y: x ^ y, salt.asNumbers(), privKey[8:16].asNumbers())).asOctets())

    def encryptData(self, encryptKey, privParameters, dataToEncrypt):
        if DES is None:
            raise error.StatusInformation(errorIndication=errind.encryptionError)
        (snmpEngineBoots, snmpEngineTime, salt) = privParameters
        (desKey, salt, iv) = self.__getEncryptionKey(encryptKey, snmpEngineBoots)
        privParameters = univ.OctetString(salt)
        desObj = DES.new(desKey, DES.MODE_CBC, iv)
        plaintext = dataToEncrypt + univ.OctetString((0, ) * (8 - len(dataToEncrypt) % 8)).asOctets()
        ciphertext = desObj.encrypt(plaintext)
        return (
         univ.OctetString(ciphertext), privParameters)

    def decryptData(self, decryptKey, privParameters, encryptedData):
        if DES is None:
            raise error.StatusInformation(errorIndication=errind.decryptionError)
        (snmpEngineBoots, snmpEngineTime, salt) = privParameters
        if len(salt) != 8:
            raise error.StatusInformation(errorIndication=errind.decryptionError)
        (desKey, iv) = self.__getDecryptionKey(decryptKey, salt)
        if len(encryptedData) % 8 != 0:
            raise error.StatusInformation(errorIndication=errind.decryptionError)
        desObj = DES.new(desKey, DES.MODE_CBC, iv)
        return desObj.decrypt(encryptedData.asOctets())