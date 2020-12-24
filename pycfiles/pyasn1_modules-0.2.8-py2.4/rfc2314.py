# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc2314.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1_modules.rfc2459 import *

class Attributes(univ.SetOf):
    __module__ = __name__
    componentType = Attribute()


class Version(univ.Integer):
    __module__ = __name__


class CertificationRequestInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('subject', Name()), namedtype.NamedType('subjectPublicKeyInfo', SubjectPublicKeyInfo()), namedtype.NamedType('attributes', Attributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))))


class Signature(univ.BitString):
    __module__ = __name__


class SignatureAlgorithmIdentifier(AlgorithmIdentifier):
    __module__ = __name__


class CertificationRequest(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('certificationRequestInfo', CertificationRequestInfo()), namedtype.NamedType('signatureAlgorithm', SignatureAlgorithmIdentifier()), namedtype.NamedType('signature', Signature()))