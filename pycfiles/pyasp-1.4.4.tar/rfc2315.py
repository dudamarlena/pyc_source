# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc2315.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1_modules.rfc2459 import *

class Attribute(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('type', AttributeType()), namedtype.NamedType('values', univ.SetOf(componentType=AttributeValue())))


class AttributeValueAssertion(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('attributeType', AttributeType()), namedtype.NamedType('attributeValue', AttributeValue(), openType=opentype.OpenType('type', certificateAttributesMap)))


pkcs_7 = univ.ObjectIdentifier('1.2.840.113549.1.7')
data = univ.ObjectIdentifier('1.2.840.113549.1.7.1')
signedData = univ.ObjectIdentifier('1.2.840.113549.1.7.2')
envelopedData = univ.ObjectIdentifier('1.2.840.113549.1.7.3')
signedAndEnvelopedData = univ.ObjectIdentifier('1.2.840.113549.1.7.4')
digestedData = univ.ObjectIdentifier('1.2.840.113549.1.7.5')
encryptedData = univ.ObjectIdentifier('1.2.840.113549.1.7.6')

class ContentType(univ.ObjectIdentifier):
    __module__ = __name__


class ContentEncryptionAlgorithmIdentifier(AlgorithmIdentifier):
    __module__ = __name__


class EncryptedContent(univ.OctetString):
    __module__ = __name__


contentTypeMap = {}

class EncryptedContentInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('contentType', ContentType()), namedtype.NamedType('contentEncryptionAlgorithm', ContentEncryptionAlgorithmIdentifier()), namedtype.OptionalNamedType('encryptedContent', EncryptedContent().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0)), openType=opentype.OpenType('contentType', contentTypeMap)))


class Version(univ.Integer):
    __module__ = __name__


class EncryptedData(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('encryptedContentInfo', EncryptedContentInfo()))


class DigestAlgorithmIdentifier(AlgorithmIdentifier):
    __module__ = __name__


class DigestAlgorithmIdentifiers(univ.SetOf):
    __module__ = __name__
    componentType = DigestAlgorithmIdentifier()


class Digest(univ.OctetString):
    __module__ = __name__


class ContentInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('contentType', ContentType()), namedtype.OptionalNamedType('content', univ.Any().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0)), openType=opentype.OpenType('contentType', contentTypeMap)))


class DigestedData(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('digestAlgorithm', DigestAlgorithmIdentifier()), namedtype.NamedType('contentInfo', ContentInfo()), namedtype.NamedType('digest', Digest()))


class IssuerAndSerialNumber(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('issuer', Name()), namedtype.NamedType('serialNumber', CertificateSerialNumber()))


class KeyEncryptionAlgorithmIdentifier(AlgorithmIdentifier):
    __module__ = __name__


class EncryptedKey(univ.OctetString):
    __module__ = __name__


class RecipientInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('issuerAndSerialNumber', IssuerAndSerialNumber()), namedtype.NamedType('keyEncryptionAlgorithm', KeyEncryptionAlgorithmIdentifier()), namedtype.NamedType('encryptedKey', EncryptedKey()))


class RecipientInfos(univ.SetOf):
    __module__ = __name__
    componentType = RecipientInfo()


class Attributes(univ.SetOf):
    __module__ = __name__
    componentType = Attribute()


class ExtendedCertificateInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('certificate', Certificate()), namedtype.NamedType('attributes', Attributes()))


class SignatureAlgorithmIdentifier(AlgorithmIdentifier):
    __module__ = __name__


class Signature(univ.BitString):
    __module__ = __name__


class ExtendedCertificate(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('extendedCertificateInfo', ExtendedCertificateInfo()), namedtype.NamedType('signatureAlgorithm', SignatureAlgorithmIdentifier()), namedtype.NamedType('signature', Signature()))


class ExtendedCertificateOrCertificate(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('certificate', Certificate()), namedtype.NamedType('extendedCertificate', ExtendedCertificate().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))))


class ExtendedCertificatesAndCertificates(univ.SetOf):
    __module__ = __name__
    componentType = ExtendedCertificateOrCertificate()


class SerialNumber(univ.Integer):
    __module__ = __name__


class CRLEntry(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('userCertificate', SerialNumber()), namedtype.NamedType('revocationDate', useful.UTCTime()))


class TBSCertificateRevocationList(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('signature', AlgorithmIdentifier()), namedtype.NamedType('issuer', Name()), namedtype.NamedType('lastUpdate', useful.UTCTime()), namedtype.NamedType('nextUpdate', useful.UTCTime()), namedtype.OptionalNamedType('revokedCertificates', univ.SequenceOf(componentType=CRLEntry())))


class CertificateRevocationList(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('tbsCertificateRevocationList', TBSCertificateRevocationList()), namedtype.NamedType('signatureAlgorithm', AlgorithmIdentifier()), namedtype.NamedType('signature', univ.BitString()))


class CertificateRevocationLists(univ.SetOf):
    __module__ = __name__
    componentType = CertificateRevocationList()


class DigestEncryptionAlgorithmIdentifier(AlgorithmIdentifier):
    __module__ = __name__


class EncryptedDigest(univ.OctetString):
    __module__ = __name__


class SignerInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('issuerAndSerialNumber', IssuerAndSerialNumber()), namedtype.NamedType('digestAlgorithm', DigestAlgorithmIdentifier()), namedtype.OptionalNamedType('authenticatedAttributes', Attributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('digestEncryptionAlgorithm', DigestEncryptionAlgorithmIdentifier()), namedtype.NamedType('encryptedDigest', EncryptedDigest()), namedtype.OptionalNamedType('unauthenticatedAttributes', Attributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))


class SignerInfos(univ.SetOf):
    __module__ = __name__
    componentType = SignerInfo()


class SignedAndEnvelopedData(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('recipientInfos', RecipientInfos()), namedtype.NamedType('digestAlgorithms', DigestAlgorithmIdentifiers()), namedtype.NamedType('encryptedContentInfo', EncryptedContentInfo()), namedtype.OptionalNamedType('certificates', ExtendedCertificatesAndCertificates().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.OptionalNamedType('crls', CertificateRevocationLists().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), namedtype.NamedType('signerInfos', SignerInfos()))


class EnvelopedData(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.NamedType('recipientInfos', RecipientInfos()), namedtype.NamedType('encryptedContentInfo', EncryptedContentInfo()))


class DigestInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('digestAlgorithm', DigestAlgorithmIdentifier()), namedtype.NamedType('digest', Digest()))


class SignedData(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', Version()), namedtype.OptionalNamedType('digestAlgorithms', DigestAlgorithmIdentifiers()), namedtype.NamedType('contentInfo', ContentInfo()), namedtype.OptionalNamedType('certificates', ExtendedCertificatesAndCertificates().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.OptionalNamedType('crls', CertificateRevocationLists().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), namedtype.OptionalNamedType('signerInfos', SignerInfos()))


class Data(univ.OctetString):
    __module__ = __name__


_contentTypeMapUpdate = {data: Data(), signedData: SignedData(), envelopedData: EnvelopedData(), signedAndEnvelopedData: SignedAndEnvelopedData(), digestedData: DigestedData(), encryptedData: EncryptedData()}
contentTypeMap.update(_contentTypeMapUpdate)