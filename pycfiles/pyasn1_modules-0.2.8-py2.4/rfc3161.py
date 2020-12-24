# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3161.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1.type import useful
from pyasn1_modules import rfc4210
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
Extensions = rfc5280.Extensions
AlgorithmIdentifier = rfc5280.AlgorithmIdentifier
GeneralName = rfc5280.GeneralName
ContentInfo = rfc5652.ContentInfo
PKIFreeText = rfc4210.PKIFreeText
id_ct_TSTInfo = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.4')

class Accuracy(univ.Sequence):
    __module__ = __name__


Accuracy.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('seconds', univ.Integer()), namedtype.OptionalNamedType('millis', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, 999)).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('micros', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, 999)).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class MessageImprint(univ.Sequence):
    __module__ = __name__


MessageImprint.componentType = namedtype.NamedTypes(namedtype.NamedType('hashAlgorithm', AlgorithmIdentifier()), namedtype.NamedType('hashedMessage', univ.OctetString()))

class PKIFailureInfo(univ.BitString):
    __module__ = __name__


PKIFailureInfo.namedValues = namedval.NamedValues(('badAlg', 0), ('badRequest', 2), ('badDataFormat',
                                                                                     5), ('timeNotAvailable',
                                                                                          14), ('unacceptedPolicy',
                                                                                                15), ('unacceptedExtension',
                                                                                                      16), ('addInfoNotAvailable',
                                                                                                            17), ('systemFailure',
                                                                                                                  25))

class PKIStatus(univ.Integer):
    __module__ = __name__


PKIStatus.namedValues = namedval.NamedValues(('granted', 0), ('grantedWithMods', 1), ('rejection',
                                                                                      2), ('waiting',
                                                                                           3), ('revocationWarning',
                                                                                                4), ('revocationNotification',
                                                                                                     5))

class PKIStatusInfo(univ.Sequence):
    __module__ = __name__


PKIStatusInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('status', PKIStatus()), namedtype.OptionalNamedType('statusString', PKIFreeText()), namedtype.OptionalNamedType('failInfo', PKIFailureInfo()))

class TSAPolicyId(univ.ObjectIdentifier):
    __module__ = __name__


class TSTInfo(univ.Sequence):
    __module__ = __name__


TSTInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('v1',
                                                                                                                           1)))), namedtype.NamedType('policy', TSAPolicyId()), namedtype.NamedType('messageImprint', MessageImprint()), namedtype.NamedType('serialNumber', univ.Integer()), namedtype.NamedType('genTime', useful.GeneralizedTime()), namedtype.OptionalNamedType('accuracy', Accuracy()), namedtype.DefaultedNamedType('ordering', univ.Boolean().subtype(value=0)), namedtype.OptionalNamedType('nonce', univ.Integer()), namedtype.OptionalNamedType('tsa', GeneralName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('extensions', Extensions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class TimeStampReq(univ.Sequence):
    __module__ = __name__


TimeStampReq.componentType = namedtype.NamedTypes(namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('v1',
                                                                                                                                1)))), namedtype.NamedType('messageImprint', MessageImprint()), namedtype.OptionalNamedType('reqPolicy', TSAPolicyId()), namedtype.OptionalNamedType('nonce', univ.Integer()), namedtype.DefaultedNamedType('certReq', univ.Boolean().subtype(value=0)), namedtype.OptionalNamedType('extensions', Extensions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))))

class TimeStampToken(ContentInfo):
    __module__ = __name__


class TimeStampResp(univ.Sequence):
    __module__ = __name__


TimeStampResp.componentType = namedtype.NamedTypes(namedtype.NamedType('status', PKIStatusInfo()), namedtype.OptionalNamedType('timeStampToken', TimeStampToken()))