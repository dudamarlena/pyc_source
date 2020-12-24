# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8410.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ
from pyasn1_modules import rfc3565
from pyasn1_modules import rfc4055
from pyasn1_modules import rfc5280

class SignatureAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


class KeyEncryptionAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


class CurvePrivateKey(univ.OctetString):
    __module__ = __name__


id_X25519 = univ.ObjectIdentifier('1.3.101.110')
id_X448 = univ.ObjectIdentifier('1.3.101.111')
id_Ed25519 = univ.ObjectIdentifier('1.3.101.112')
id_Ed448 = univ.ObjectIdentifier('1.3.101.113')
id_sha512 = rfc4055.id_sha512
id_aes128_wrap = rfc3565.id_aes128_wrap
id_aes256_wrap = rfc3565.id_aes256_wrap