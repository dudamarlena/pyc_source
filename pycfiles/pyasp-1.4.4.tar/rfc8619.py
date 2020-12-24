# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8619.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ
from pyasn1_modules import rfc5280
id_alg_hkdf_with_sha256 = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.28')
id_alg_hkdf_with_sha384 = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.29')
id_alg_hkdf_with_sha512 = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.30')
kda_hkdf_with_sha256 = rfc5280.AlgorithmIdentifier()
kda_hkdf_with_sha256['algorithm'] = id_alg_hkdf_with_sha256
kda_hkdf_with_sha384 = rfc5280.AlgorithmIdentifier()
kda_hkdf_with_sha384['algorithm'] = id_alg_hkdf_with_sha384
kda_hkdf_with_sha512 = rfc5280.AlgorithmIdentifier()
kda_hkdf_with_sha512['algorithm'] = id_alg_hkdf_with_sha512