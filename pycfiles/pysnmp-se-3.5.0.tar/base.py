# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc3414/priv/base.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto import error

class AbstractEncryptionService(object):
    __module__ = __name__
    serviceID = None
    keySize = 0

    def hashPassphrase(self, authProtocol, privKey):
        raise error.ProtocolError('no encryption')

    def localizeKey(self, authProtocol, privKey, snmpEngineID):
        raise error.ProtocolError('no encryption')

    def encryptData(self, encryptKey, privParameters, dataToEncrypt):
        raise error.ProtocolError('no encryption')

    def decryptData(self, decryptKey, privParameters, encryptedData):
        raise error.ProtocolError('no encryption')