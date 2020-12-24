# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8418.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ
from pyasn1_modules import rfc5280

class KeyEncryptionAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


class KeyWrapAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


dhSinglePass_stdDH_sha256kdf_scheme = univ.ObjectIdentifier('1.3.133.16.840.63.0.11.1')
dhSinglePass_stdDH_sha384kdf_scheme = univ.ObjectIdentifier('1.3.133.16.840.63.0.11.2')
dhSinglePass_stdDH_sha512kdf_scheme = univ.ObjectIdentifier('1.3.133.16.840.63.0.11.3')
dhSinglePass_stdDH_hkdf_sha256_scheme = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.19')
dhSinglePass_stdDH_hkdf_sha384_scheme = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.20')
dhSinglePass_stdDH_hkdf_sha512_scheme = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.21')