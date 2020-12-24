# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3709.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc6170
MAX = float('inf')

class HashAlgAndValue(univ.Sequence):
    __module__ = __name__


HashAlgAndValue.componentType = namedtype.NamedTypes(namedtype.NamedType('hashAlg', rfc5280.AlgorithmIdentifier()), namedtype.NamedType('hashValue', univ.OctetString()))

class LogotypeDetails(univ.Sequence):
    __module__ = __name__


LogotypeDetails.componentType = namedtype.NamedTypes(namedtype.NamedType('mediaType', char.IA5String()), namedtype.NamedType('logotypeHash', univ.SequenceOf(componentType=HashAlgAndValue()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))), namedtype.NamedType('logotypeURI', univ.SequenceOf(componentType=char.IA5String()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))))

class LogotypeAudioInfo(univ.Sequence):
    __module__ = __name__


LogotypeAudioInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('fileSize', univ.Integer()), namedtype.NamedType('playTime', univ.Integer()), namedtype.NamedType('channels', univ.Integer()), namedtype.OptionalNamedType('sampleRate', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))), namedtype.OptionalNamedType('language', char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))))

class LogotypeAudio(univ.Sequence):
    __module__ = __name__


LogotypeAudio.componentType = namedtype.NamedTypes(namedtype.NamedType('audioDetails', LogotypeDetails()), namedtype.OptionalNamedType('audioInfo', LogotypeAudioInfo()))

class LogotypeImageType(univ.Integer):
    __module__ = __name__


LogotypeImageType.namedValues = namedval.NamedValues(('grayScale', 0), ('color', 1))

class LogotypeImageResolution(univ.Choice):
    __module__ = __name__


LogotypeImageResolution.componentType = namedtype.NamedTypes(namedtype.NamedType('numBits', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('tableSize', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))

class LogotypeImageInfo(univ.Sequence):
    __module__ = __name__


LogotypeImageInfo.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('type', LogotypeImageType().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='color')), namedtype.NamedType('fileSize', univ.Integer()), namedtype.NamedType('xSize', univ.Integer()), namedtype.NamedType('ySize', univ.Integer()), namedtype.OptionalNamedType('resolution', LogotypeImageResolution()), namedtype.OptionalNamedType('language', char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))))

class LogotypeImage(univ.Sequence):
    __module__ = __name__


LogotypeImage.componentType = namedtype.NamedTypes(namedtype.NamedType('imageDetails', LogotypeDetails()), namedtype.OptionalNamedType('imageInfo', LogotypeImageInfo()))

class LogotypeData(univ.Sequence):
    __module__ = __name__


LogotypeData.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('image', univ.SequenceOf(componentType=LogotypeImage())), namedtype.OptionalNamedType('audio', univ.SequenceOf(componentType=LogotypeAudio()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class LogotypeReference(univ.Sequence):
    __module__ = __name__


LogotypeReference.componentType = namedtype.NamedTypes(namedtype.NamedType('refStructHash', univ.SequenceOf(componentType=HashAlgAndValue()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))), namedtype.NamedType('refStructURI', univ.SequenceOf(componentType=char.IA5String()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX))))

class LogotypeInfo(univ.Choice):
    __module__ = __name__


LogotypeInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('direct', LogotypeData().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('indirect', LogotypeReference().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))
id_logo_background = univ.ObjectIdentifier('1.3.6.1.5.5.7.20.2')
id_logo_loyalty = univ.ObjectIdentifier('1.3.6.1.5.5.7.20.1')
id_logo_certImage = rfc6170.id_logo_certImage

class OtherLogotypeInfo(univ.Sequence):
    __module__ = __name__


OtherLogotypeInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('logotypeType', univ.ObjectIdentifier()), namedtype.NamedType('info', LogotypeInfo()))
id_pe_logotype = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.12')

class LogotypeExtn(univ.Sequence):
    __module__ = __name__


LogotypeExtn.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('communityLogos', univ.SequenceOf(componentType=LogotypeInfo()).subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('issuerLogo', LogotypeInfo().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), namedtype.OptionalNamedType('subjectLogo', LogotypeInfo().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))), namedtype.OptionalNamedType('otherLogos', univ.SequenceOf(componentType=OtherLogotypeInfo()).subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))))
_certificateExtensionsMapUpdate = {id_pe_logotype: LogotypeExtn()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)