# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc3414/priv/nopriv.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto.secmod.rfc3414.priv import base
from pysnmp.proto import errind, error

class NoPriv(base.AbstractEncryptionService):
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 6, 3, 10, 1, 2, 1)

    def hashPassphrase(self, authProtocol, privKey):
        pass

    def localizeKey(self, authProtocol, privKey, snmpEngineID):
        pass

    def encryptData(self, encryptKey, privParameters, dataToEncrypt):
        raise error.StatusInformation(errorIndication=errind.noEncryption)

    def decryptData(self, decryptKey, privParameters, encryptedData):
        raise error.StatusInformation(errorIndication=errind.noEncryption)