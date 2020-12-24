# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/rfc3414/localkey.py
# Compiled at: 2019-08-18 17:24:05
try:
    from hashlib import md5, sha1
except ImportError:
    import md5, sha
    md5 = md5.new
    sha1 = sha.new

from pyasn1.type import univ

def hashPassphrase(passphrase, hashFunc):
    passphrase = univ.OctetString(passphrase).asOctets()
    hasher = hashFunc()
    ringBuffer = passphrase * (64 // len(passphrase) + 1)
    ringBufferLen = len(ringBuffer)
    count = 0
    mark = 0
    while count < 16384:
        e = mark + 64
        if e < ringBufferLen:
            hasher.update(ringBuffer[mark:e])
            mark = e
        else:
            hasher.update(ringBuffer[mark:ringBufferLen] + ringBuffer[0:e - ringBufferLen])
            mark = e - ringBufferLen
        count += 1

    digest = hasher.digest()
    return univ.OctetString(digest)


def passwordToKey(passphrase, snmpEngineId, hashFunc):
    return localizeKey(hashPassphrase(passphrase, hashFunc), snmpEngineId, hashFunc)


def localizeKey(passKey, snmpEngineId, hashFunc):
    passKey = univ.OctetString(passKey).asOctets()
    digest = hashFunc(passKey + snmpEngineId.asOctets() + passKey).digest()
    return univ.OctetString(digest)


def hashPassphraseMD5(passphrase):
    return hashPassphrase(passphrase, md5)


def hashPassphraseSHA(passphrase):
    return hashPassphrase(passphrase, sha1)


def passwordToKeyMD5(passphrase, snmpEngineId):
    return localizeKey(hashPassphraseMD5(passphrase), snmpEngineId, md5)


def passwordToKeySHA(passphrase, snmpEngineId):
    return localizeKey(hashPassphraseMD5(passphrase), snmpEngineId, sha1)


def localizeKeyMD5(passKey, snmpEngineId):
    return localizeKey(passKey, snmpEngineId, md5)


def localizeKeySHA(passKey, snmpEngineId):
    return localizeKey(passKey, snmpEngineId, sha1)