# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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