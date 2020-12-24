# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8017.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import univ
from pyasn1_modules import rfc2437
from pyasn1_modules import rfc3447
from pyasn1_modules import rfc4055
from pyasn1_modules import rfc5280
MAX = float('inf')
AlgorithmIdentifier = rfc5280.AlgorithmIdentifier

class DigestAlgorithm(AlgorithmIdentifier):
    __module__ = __name__


class HashAlgorithm(AlgorithmIdentifier):
    __module__ = __name__


class MaskGenAlgorithm(AlgorithmIdentifier):
    __module__ = __name__


class PSourceAlgorithm(AlgorithmIdentifier):
    __module__ = __name__


hashAlgs = univ.ObjectIdentifier('2.16.840.1.101.3.4.2')
id_sha256 = rfc4055.id_sha256
id_sha384 = rfc4055.id_sha384
id_sha512 = rfc4055.id_sha512
id_sha224 = rfc4055.id_sha224
id_sha512_224 = hashAlgs + (5,)
id_sha512_256 = hashAlgs + (6,)
pkcs_1 = univ.ObjectIdentifier('1.2.840.113549.1.1')
rsaEncryption = rfc2437.rsaEncryption
id_RSAES_OAEP = rfc2437.id_RSAES_OAEP
id_pSpecified = rfc2437.id_pSpecified
id_RSASSA_PSS = rfc4055.id_RSASSA_PSS
md2WithRSAEncryption = rfc2437.md2WithRSAEncryption
md5WithRSAEncryption = rfc2437.md5WithRSAEncryption
sha1WithRSAEncryption = rfc2437.sha1WithRSAEncryption
sha224WithRSAEncryption = rfc4055.sha224WithRSAEncryption
sha256WithRSAEncryption = rfc4055.sha256WithRSAEncryption
sha384WithRSAEncryption = rfc4055.sha384WithRSAEncryption
sha512WithRSAEncryption = rfc4055.sha512WithRSAEncryption
sha512_224WithRSAEncryption = pkcs_1 + (15,)
sha512_256WithRSAEncryption = pkcs_1 + (16,)
id_sha1 = rfc2437.id_sha1
id_md2 = univ.ObjectIdentifier('1.2.840.113549.2.2')
id_md5 = univ.ObjectIdentifier('1.2.840.113549.2.5')
id_mgf1 = rfc2437.id_mgf1
sha1 = rfc4055.sha1Identifier
SHA1Parameters = univ.Null('')
mgf1SHA1 = rfc4055.mgf1SHA1Identifier

class EncodingParameters(univ.OctetString):
    __module__ = __name__
    subtypeSpec = constraint.ValueSizeConstraint(0, MAX)


pSpecifiedEmpty = rfc4055.pSpecifiedEmptyIdentifier
emptyString = EncodingParameters(value='')

class Version(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('two-prime', 0), ('multi', 1))


class TrailerField(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('trailerFieldBC', 1))


RSAPublicKey = rfc2437.RSAPublicKey
OtherPrimeInfo = rfc3447.OtherPrimeInfo
OtherPrimeInfos = rfc3447.OtherPrimeInfos
RSAPrivateKey = rfc3447.RSAPrivateKey
RSAES_OAEP_params = rfc4055.RSAES_OAEP_params
rSAES_OAEP_Default_Identifier = rfc4055.rSAES_OAEP_Default_Identifier
RSASSA_PSS_params = rfc4055.RSASSA_PSS_params
rSASSA_PSS_Default_Identifier = rfc4055.rSASSA_PSS_Default_Identifier

class DigestInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('digestAlgorithm', DigestAlgorithm()), namedtype.NamedType('digest', univ.OctetString()))


_algorithmIdentifierMapUpdate = {id_sha1: univ.Null(), id_sha224: univ.Null(), id_sha256: univ.Null(), id_sha384: univ.Null(), id_sha512: univ.Null(), id_sha512_224: univ.Null(), id_sha512_256: univ.Null(), id_mgf1: AlgorithmIdentifier(), id_pSpecified: univ.OctetString(), id_RSAES_OAEP: RSAES_OAEP_params(), id_RSASSA_PSS: RSASSA_PSS_params(), md2WithRSAEncryption: univ.Null(), md5WithRSAEncryption: univ.Null(), sha1WithRSAEncryption: univ.Null(), sha224WithRSAEncryption: univ.Null(), sha256WithRSAEncryption: univ.Null(), sha384WithRSAEncryption: univ.Null(), sha512WithRSAEncryption: univ.Null(), sha512_224WithRSAEncryption: univ.Null(), sha512_256WithRSAEncryption: univ.Null()}
rfc5280.algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)