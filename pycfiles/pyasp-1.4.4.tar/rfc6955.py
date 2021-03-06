# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6955.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc3279
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
MessageDigest = rfc5652.MessageDigest
IssuerAndSerialNumber = rfc5652.IssuerAndSerialNumber
id_pkix = rfc5280.id_pkix
Dss_Sig_Value = rfc3279.Dss_Sig_Value
DomainParameters = rfc3279.DomainParameters

class DhSigStatic(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('issuerAndSerial', IssuerAndSerialNumber()), namedtype.NamedType('hashValue', MessageDigest()))


id_dh_sig_hmac_sha1 = id_pkix + (6, 3)
id_dhPop_static_sha1_hmac_sha1 = univ.ObjectIdentifier(id_dh_sig_hmac_sha1)
id_alg_dh_pop = id_pkix + (6, 4)
id_alg_dhPop_sha1 = univ.ObjectIdentifier(id_alg_dh_pop)
id_alg_dhPop_sha224 = id_pkix + (6, 5)
id_alg_dhPop_sha256 = id_pkix + (6, 6)
id_alg_dhPop_sha384 = id_pkix + (6, 7)
id_alg_dhPop_sha512 = id_pkix + (6, 8)
id_alg_dhPop_static_sha224_hmac_sha224 = id_pkix + (6, 15)
id_alg_dhPop_static_sha256_hmac_sha256 = id_pkix + (6, 16)
id_alg_dhPop_static_sha384_hmac_sha384 = id_pkix + (6, 17)
id_alg_dhPop_static_sha512_hmac_sha512 = id_pkix + (6, 18)
id_alg_ecdhPop_static_sha224_hmac_sha224 = id_pkix + (6, 25)
id_alg_ecdhPop_static_sha256_hmac_sha256 = id_pkix + (6, 26)
id_alg_ecdhPop_static_sha384_hmac_sha384 = id_pkix + (6, 27)
id_alg_ecdhPop_static_sha512_hmac_sha512 = id_pkix + (6, 28)
_algorithmIdentifierMapUpdate = {id_alg_dh_pop: DomainParameters(), id_alg_dhPop_sha224: DomainParameters(), id_alg_dhPop_sha256: DomainParameters(), id_alg_dhPop_sha384: DomainParameters(), id_alg_dhPop_sha512: DomainParameters(), id_dh_sig_hmac_sha1: univ.Null(''), id_alg_dhPop_static_sha224_hmac_sha224: univ.Null(''), id_alg_dhPop_static_sha256_hmac_sha256: univ.Null(''), id_alg_dhPop_static_sha384_hmac_sha384: univ.Null(''), id_alg_dhPop_static_sha512_hmac_sha512: univ.Null(''), id_alg_ecdhPop_static_sha224_hmac_sha224: univ.Null(''), id_alg_ecdhPop_static_sha256_hmac_sha256: univ.Null(''), id_alg_ecdhPop_static_sha384_hmac_sha384: univ.Null(''), id_alg_ecdhPop_static_sha512_hmac_sha512: univ.Null('')}
rfc5280.algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)