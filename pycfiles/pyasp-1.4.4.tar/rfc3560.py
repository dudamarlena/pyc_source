# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3560.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1_modules import rfc4055
id_sha1 = rfc4055.id_sha1
id_sha256 = rfc4055.id_sha256
id_sha384 = rfc4055.id_sha384
id_sha512 = rfc4055.id_sha512
id_mgf1 = rfc4055.id_mgf1
rsaEncryption = rfc4055.rsaEncryption
id_RSAES_OAEP = rfc4055.id_RSAES_OAEP
id_pSpecified = rfc4055.id_pSpecified
sha1Identifier = rfc4055.sha1Identifier
sha256Identifier = rfc4055.sha256Identifier
sha384Identifier = rfc4055.sha384Identifier
sha512Identifier = rfc4055.sha512Identifier
mgf1SHA1Identifier = rfc4055.mgf1SHA1Identifier
mgf1SHA256Identifier = rfc4055.mgf1SHA256Identifier
mgf1SHA384Identifier = rfc4055.mgf1SHA384Identifier
mgf1SHA512Identifier = rfc4055.mgf1SHA512Identifier
pSpecifiedEmptyIdentifier = rfc4055.pSpecifiedEmptyIdentifier

class RSAES_OAEP_params(rfc4055.RSAES_OAEP_params):
    __module__ = __name__


rSAES_OAEP_Default_Params = RSAES_OAEP_params()
rSAES_OAEP_Default_Identifier = rfc4055.rSAES_OAEP_Default_Identifier
rSAES_OAEP_SHA256_Params = rfc4055.rSAES_OAEP_SHA256_Params
rSAES_OAEP_SHA256_Identifier = rfc4055.rSAES_OAEP_SHA256_Identifier
rSAES_OAEP_SHA384_Params = rfc4055.rSAES_OAEP_SHA384_Params
rSAES_OAEP_SHA384_Identifier = rfc4055.rSAES_OAEP_SHA384_Identifier
rSAES_OAEP_SHA512_Params = rfc4055.rSAES_OAEP_SHA512_Params
rSAES_OAEP_SHA512_Identifier = rfc4055.rSAES_OAEP_SHA512_Identifier