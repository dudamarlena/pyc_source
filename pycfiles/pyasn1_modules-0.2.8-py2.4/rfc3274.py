# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3274.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652

class CompressionAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


id_ct_compressedData = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.9')

class CompressedData(univ.Sequence):
    __module__ = __name__


CompressedData.componentType = namedtype.NamedTypes(namedtype.NamedType('version', rfc5652.CMSVersion()), namedtype.NamedType('compressionAlgorithm', CompressionAlgorithmIdentifier()), namedtype.NamedType('encapContentInfo', rfc5652.EncapsulatedContentInfo()))
id_alg_zlibCompress = univ.ObjectIdentifier('1.2.840.113549.1.9.16.3.8')
cpa_zlibCompress = rfc5280.AlgorithmIdentifier()
cpa_zlibCompress['algorithm'] = id_alg_zlibCompress
_cmsContentTypesMapUpdate = {id_ct_compressedData: CompressedData()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)