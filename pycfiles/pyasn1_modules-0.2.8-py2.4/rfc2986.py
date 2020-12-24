# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc2986.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
AttributeType = rfc5280.AttributeType
AttributeValue = rfc5280.AttributeValue
AttributeTypeAndValue = rfc5280.AttributeTypeAndValue
Attribute = rfc5280.Attribute
RelativeDistinguishedName = rfc5280.RelativeDistinguishedName
RDNSequence = rfc5280.RDNSequence
Name = rfc5280.Name
AlgorithmIdentifier = rfc5280.AlgorithmIdentifier
SubjectPublicKeyInfo = rfc5280.SubjectPublicKeyInfo

class Attributes(univ.SetOf):
    __module__ = __name__


Attributes.componentType = Attribute()

class CertificationRequestInfo(univ.Sequence):
    __module__ = __name__


CertificationRequestInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('version', univ.Integer()), namedtype.NamedType('subject', Name()), namedtype.NamedType('subjectPKInfo', SubjectPublicKeyInfo()), namedtype.NamedType('attributes', Attributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))))

class CertificationRequest(univ.Sequence):
    __module__ = __name__


CertificationRequest.componentType = namedtype.NamedTypes(namedtype.NamedType('certificationRequestInfo', CertificationRequestInfo()), namedtype.NamedType('signatureAlgorithm', AlgorithmIdentifier()), namedtype.NamedType('signature', univ.BitString()))