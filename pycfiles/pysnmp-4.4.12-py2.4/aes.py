# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc3826/priv/aes.py
# Compiled at: 2019-08-18 17:24:05
import random
from pyasn1.type import univ
from pysnmp.proto.secmod.rfc3414.priv import base
from pysnmp.proto.secmod.rfc3414.auth import hmacmd5, hmacsha
from pysnmp.proto.secmod.rfc7860.auth import hmacsha2
from pysnmp.proto.secmod.rfc3414 import localkey
from pysnmp.proto import errind, error
try:
    from Cryptodome.Cipher import AES
except ImportError:
    AES = None

try:
    from hashlib import md5, sha1
except ImportError:
    import md5, sha
    md5 = md5.new
    sha1 = sha.new

random.seed()

class Aes(base.AbstractEncryptionService):
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 6, 3, 10, 1, 2, 4)
    keySize = 16
    _localInt = random.randrange(0, 18446744073709551615)

    def __getEncryptionKey(self, privKey, snmpEngineBoots, snmpEngineTime):
        salt = [
         self._localInt >> 56 & 255, self._localInt >> 48 & 255, self._localInt >> 40 & 255, self._localInt >> 32 & 255, self._localInt >> 24 & 255, self._localInt >> 16 & 255, self._localInt >> 8 & 255, self._localInt & 255]
        if self._localInt == 18446744073709551615:
            self._localInt = 0
        else:
            self._localInt += 1
        return self.__getDecryptionKey(privKey, snmpEngineBoots, snmpEngineTime, salt) + (univ.OctetString(salt).asOctets(),)

    def __getDecryptionKey(self, privKey, snmpEngineBoots, snmpEngineTime, salt):
        snmpEngineBoots, snmpEngineTime, salt = int(snmpEngineBoots), int(snmpEngineTime), salt
        iv = [
         snmpEngineBoots >> 24 & 255, snmpEngineBoots >> 16 & 255, snmpEngineBoots >> 8 & 255, snmpEngineBoots & 255, snmpEngineTime >> 24 & 255, snmpEngineTime >> 16 & 255, snmpEngineTime >> 8 & 255, snmpEngineTime & 255] + salt
        return (
         privKey[:self.keySize].asOctets(), univ.OctetString(iv).asOctets())

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

    def encryptData(self, encryptKey, privParameters, dataToEncrypt):
        if AES is None:
            raise error.StatusInformation(errorIndication=errind.encryptionError)
        (snmpEngineBoots, snmpEngineTime, salt) = privParameters
        (aesKey, iv, salt) = self.__getEncryptionKey(encryptKey, snmpEngineBoots, snmpEngineTime)
        aesObj = AES.new(aesKey, AES.MODE_CFB, iv, segment_size=128)
        dataToEncrypt = dataToEncrypt + univ.OctetString((0, ) * (16 - len(dataToEncrypt) % 16)).asOctets()
        ciphertext = aesObj.encrypt(dataToEncrypt)
        return (
         univ.OctetString(ciphertext), univ.OctetString(salt))

    def decryptData(self, decryptKey, privParameters, encryptedData):
        if AES is None:
            raise error.StatusInformation(errorIndication=errind.decryptionError)
        (snmpEngineBoots, snmpEngineTime, salt) = privParameters
        if len(salt) != 8:
            raise error.StatusInformation(errorIndication=errind.decryptionError)
        (aesKey, iv) = self.__getDecryptionKey(decryptKey, snmpEngineBoots, snmpEngineTime, salt)
        aesObj = AES.new(aesKey, AES.MODE_CFB, iv, segment_size=128)
        encryptedData = encryptedData + univ.OctetString((0, ) * (16 - len(encryptedData) % 16)).asOctets()
        return aesObj.decrypt(encryptedData.asOctets())