# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7296.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5280

class CertificateOrCRL(univ.Choice):
    __module__ = __name__


CertificateOrCRL.componentType = namedtype.NamedTypes(namedtype.NamedType('cert', rfc5280.Certificate().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('crl', rfc5280.CertificateList().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class CertificateBundle(univ.SequenceOf):
    __module__ = __name__


CertificateBundle.componentType = CertificateOrCRL()