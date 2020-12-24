# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/eso/priv/aesbase.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto.secmod.rfc3826.priv import aes
from pysnmp.proto.secmod.rfc3414.auth import hmacmd5, hmacsha
from pysnmp.proto.secmod.rfc7860.auth import hmacsha2
from pysnmp.proto.secmod.rfc3414 import localkey
from pysnmp.proto import error
from math import ceil
try:
    from hashlib import md5, sha1
except ImportError:
    import md5, sha
    md5 = md5.new
    sha1 = sha.new

class AbstractAesBlumenthal(aes.Aes):
    __module__ = __name__
    serviceID = ()
    keySize = 0

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
        for count in range(1, int(ceil(self.keySize * 1.0 / len(localPrivKey)))):
            localPrivKey += localPrivKey.clone(hashAlgo(localPrivKey.asOctets()).digest())

        return localPrivKey[:self.keySize]


class AbstractAesReeder(aes.Aes):
    """AES encryption with non-standard key localization.

    Many vendors (including Cisco) do not use:

    https://tools.itef.org/pdf/draft_bluementhal-aes-usm-04.txt

    for key localization instead, they use the procedure for 3DES key localization
    specified in:

    https://tools.itef.org/pdf/draft_reeder_snmpv3-usm-3desede-00.pdf

    The difference between the two is that the Reeder draft does key extension by repeating
    the steps in the password to key algorithm (hash phrase, then localize with SNMPEngine ID).
    """
    __module__ = __name__
    serviceID = ()
    keySize = 0

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
        while len(localPrivKey) < self.keySize:
            newKey = localkey.hashPassphrase(localPrivKey, hashAlgo)
            localPrivKey += localkey.localizeKey(newKey, snmpEngineID, hashAlgo)

        return localPrivKey[:self.keySize]