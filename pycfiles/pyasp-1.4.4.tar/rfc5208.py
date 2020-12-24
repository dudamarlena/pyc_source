# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5208.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1_modules import rfc2251
from pyasn1_modules.rfc2459 import *

class KeyEncryptionAlgorithms(AlgorithmIdentifier):
    __module__ = __name__


class PrivateKeyAlgorithms(AlgorithmIdentifier):
    __module__ = __name__


class EncryptedData(univ.OctetString):
    __module__ = __name__


class EncryptedPrivateKeyInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('encryptionAlgorithm', AlgorithmIdentifier()), namedtype.NamedType('encryptedData', EncryptedData()))


class PrivateKey(univ.OctetString):
    __module__ = __name__


class Attributes(univ.SetOf):
    __module__ = __name__
    componentType = rfc2251.Attribute()


class Version(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('v1', 0), ('v2', 1))


class PrivateKeyInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('privateKeyAlgorithm', AlgorithmIdentifier()), namedtype.NamedType('privateKey', PrivateKey()), namedtype.OptionalNamedType('attributes', Attributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))))