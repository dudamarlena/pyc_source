# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8494.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import tag
from pyasn1.type import univ
id_mmhs_CDT = univ.ObjectIdentifier('1.3.26.0.4406.0.4.2')

class AlgorithmID_ShortForm(univ.Integer):
    __module__ = __name__


AlgorithmID_ShortForm.namedValues = namedval.NamedValues(('zlibCompress', 0))

class ContentType_ShortForm(univ.Integer):
    __module__ = __name__


ContentType_ShortForm.namedValues = namedval.NamedValues(('unidentified', 0), ('external',
                                                                               1), ('p1',
                                                                                    2), ('p3',
                                                                                         3), ('p7',
                                                                                              4), ('mule',
                                                                                                   25))

class CompressedContentInfo(univ.Sequence):
    __module__ = __name__


CompressedContentInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('unnamed', univ.Choice(componentType=namedtype.NamedTypes(namedtype.NamedType('contentType-ShortForm', ContentType_ShortForm().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('contentType-OID', univ.ObjectIdentifier().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)))))), namedtype.NamedType('compressedContent', univ.OctetString().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))))

class CompressionAlgorithmIdentifier(univ.Choice):
    __module__ = __name__


CompressionAlgorithmIdentifier.componentType = namedtype.NamedTypes(namedtype.NamedType('algorithmID-ShortForm', AlgorithmID_ShortForm().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('algorithmID-OID', univ.ObjectIdentifier().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class CompressedData(univ.Sequence):
    __module__ = __name__


CompressedData.componentType = namedtype.NamedTypes(namedtype.NamedType('compressionAlgorithm', CompressionAlgorithmIdentifier()), namedtype.NamedType('compressedContentInfo', CompressedContentInfo()))