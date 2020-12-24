# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8419.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ
from pyasn1_modules import rfc5280

class ShakeOutputLen(univ.Integer):
    __module__ = __name__


id_Ed25519 = univ.ObjectIdentifier('1.3.101.112')
sigAlg_Ed25519 = rfc5280.AlgorithmIdentifier()
sigAlg_Ed25519['algorithm'] = id_Ed25519
id_Ed448 = univ.ObjectIdentifier('1.3.101.113')
sigAlg_Ed448 = rfc5280.AlgorithmIdentifier()
sigAlg_Ed448['algorithm'] = id_Ed448
hashAlgs = univ.ObjectIdentifier('2.16.840.1.101.3.4.2')
id_sha512 = hashAlgs + (3, )
hashAlg_SHA_512 = rfc5280.AlgorithmIdentifier()
hashAlg_SHA_512['algorithm'] = id_sha512
id_shake256 = hashAlgs + (12, )
hashAlg_SHAKE256 = rfc5280.AlgorithmIdentifier()
hashAlg_SHAKE256['algorithm'] = id_shake256
id_shake256_len = hashAlgs + (18, )
hashAlg_SHAKE256_LEN = rfc5280.AlgorithmIdentifier()
hashAlg_SHAKE256_LEN['algorithm'] = id_shake256_len
hashAlg_SHAKE256_LEN['parameters'] = ShakeOutputLen()
_algorithmIdentifierMapUpdate = {id_shake256_len: ShakeOutputLen()}
rfc5280.algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)