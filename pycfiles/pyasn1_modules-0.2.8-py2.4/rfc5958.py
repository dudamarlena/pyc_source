# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5958.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ, constraint, namedtype, namedval, tag
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
MAX = float('inf')

class KeyEncryptionAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


class PrivateKeyAlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


class EncryptedData(univ.OctetString):
    __module__ = __name__


class EncryptedPrivateKeyInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('encryptionAlgorithm', KeyEncryptionAlgorithmIdentifier()), namedtype.NamedType('encryptedData', EncryptedData()))


class Version(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('v1', 0), ('v2', 1))


class PrivateKey(univ.OctetString):
    __module__ = __name__


class Attributes(univ.SetOf):
    __module__ = __name__
    componentType = rfc5652.Attribute()


class PublicKey(univ.BitString):
    __module__ = __name__


class OneAsymmetricKey(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('privateKeyAlgorithm', PrivateKeyAlgorithmIdentifier()), namedtype.NamedType('privateKey', PrivateKey()), namedtype.OptionalNamedType('attributes', Attributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.OptionalNamedType('publicKey', PublicKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))


class PrivateKeyInfo(OneAsymmetricKey):
    __module__ = __name__


id_ct_KP_aKeyPackage = univ.ObjectIdentifier('2.16.840.1.101.2.1.2.78.5')

class AsymmetricKeyPackage(univ.SequenceOf):
    __module__ = __name__


AsymmetricKeyPackage.componentType = OneAsymmetricKey()
AsymmetricKeyPackage.sizeSpec = constraint.ValueSizeConstraint(1, MAX)
_cmsContentTypesMapUpdate = {id_ct_KP_aKeyPackage: AsymmetricKeyPackage()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)