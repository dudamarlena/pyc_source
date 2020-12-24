# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6486.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import useful
from pyasn1.type import univ
from pyasn1_modules import rfc5652
MAX = float('inf')
id_smime = univ.ObjectIdentifier('1.2.840.113549.1.9.16')
id_ct = id_smime + (1, )
id_ct_rpkiManifest = id_ct + (26, )

class FileAndHash(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('file', char.IA5String()), namedtype.NamedType('hash', univ.BitString()))


class Manifest(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', univ.Integer().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value=0)), namedtype.NamedType('manifestNumber', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, MAX))), namedtype.NamedType('thisUpdate', useful.GeneralizedTime()), namedtype.NamedType('nextUpdate', useful.GeneralizedTime()), namedtype.NamedType('fileHashAlg', univ.ObjectIdentifier()), namedtype.NamedType('fileList', univ.SequenceOf(componentType=FileAndHash()).subtype(subtypeSpec=constraint.ValueSizeConstraint(0, MAX))))


_cmsContentTypesMapUpdate = {id_ct_rpkiManifest: Manifest()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)