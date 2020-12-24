# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc2634.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedval
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1.type import useful
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5280
MAX = float('inf')
ContentType = rfc5652.ContentType
IssuerAndSerialNumber = rfc5652.IssuerAndSerialNumber
SubjectKeyIdentifier = rfc5652.SubjectKeyIdentifier
PolicyInformation = rfc5280.PolicyInformation
GeneralNames = rfc5280.GeneralNames
CertificateSerialNumber = rfc5280.CertificateSerialNumber
id_aa_signingCertificate = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.12')

class Hash(univ.OctetString):
    __module__ = __name__


class IssuerSerial(univ.Sequence):
    __module__ = __name__


IssuerSerial.componentType = namedtype.NamedTypes(namedtype.NamedType('issuer', GeneralNames()), namedtype.NamedType('serialNumber', CertificateSerialNumber()))

class ESSCertID(univ.Sequence):
    __module__ = __name__


ESSCertID.componentType = namedtype.NamedTypes(namedtype.NamedType('certHash', Hash()), namedtype.OptionalNamedType('issuerSerial', IssuerSerial()))

class SigningCertificate(univ.Sequence):
    __module__ = __name__


SigningCertificate.componentType = namedtype.NamedTypes(namedtype.NamedType('certs', univ.SequenceOf(componentType=ESSCertID())), namedtype.OptionalNamedType('policies', univ.SequenceOf(componentType=PolicyInformation())))
id_aa_mlExpandHistory = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.3')
ub_ml_expansion_history = univ.Integer(64)

class EntityIdentifier(univ.Choice):
    __module__ = __name__


EntityIdentifier.componentType = namedtype.NamedTypes(namedtype.NamedType('issuerAndSerialNumber', IssuerAndSerialNumber()), namedtype.NamedType('subjectKeyIdentifier', SubjectKeyIdentifier()))

class MLReceiptPolicy(univ.Choice):
    __module__ = __name__


MLReceiptPolicy.componentType = namedtype.NamedTypes(namedtype.NamedType('none', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('insteadOf', univ.SequenceOf(componentType=GeneralNames()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX)).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('inAdditionTo', univ.SequenceOf(componentType=GeneralNames()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, MAX)).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))

class MLData(univ.Sequence):
    __module__ = __name__


MLData.componentType = namedtype.NamedTypes(namedtype.NamedType('mailListIdentifier', EntityIdentifier()), namedtype.NamedType('expansionTime', useful.GeneralizedTime()), namedtype.OptionalNamedType('mlReceiptPolicy', MLReceiptPolicy()))

class MLExpansionHistory(univ.SequenceOf):
    __module__ = __name__


MLExpansionHistory.componentType = MLData()
MLExpansionHistory.sizeSpec = constraint.ValueSizeConstraint(1, ub_ml_expansion_history)
id_aa_securityLabel = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.2')
ub_privacy_mark_length = univ.Integer(128)
ub_security_categories = univ.Integer(64)
ub_integer_options = univ.Integer(256)

class ESSPrivacyMark(univ.Choice):
    __module__ = __name__


ESSPrivacyMark.componentType = namedtype.NamedTypes(namedtype.NamedType('pString', char.PrintableString().subtype(subtypeSpec=constraint.ValueSizeConstraint(1, ub_privacy_mark_length))), namedtype.NamedType('utf8String', char.UTF8String().subtype(subtypeSpec=constraint.ValueSizeConstraint(1, MAX))))

class SecurityClassification(univ.Integer):
    __module__ = __name__


SecurityClassification.subtypeSpec = constraint.ValueRangeConstraint(0, ub_integer_options)
SecurityClassification.namedValues = namedval.NamedValues(('unmarked', 0), ('unclassified',
                                                                            1), ('restricted',
                                                                                 2), ('confidential',
                                                                                      3), ('secret',
                                                                                           4), ('top-secret',
                                                                                                5))

class SecurityPolicyIdentifier(univ.ObjectIdentifier):
    __module__ = __name__


class SecurityCategory(univ.Sequence):
    __module__ = __name__


SecurityCategory.componentType = namedtype.NamedTypes(namedtype.NamedType('type', univ.ObjectIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('value', univ.Any().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class SecurityCategories(univ.SetOf):
    __module__ = __name__


SecurityCategories.componentType = SecurityCategory()
SecurityCategories.sizeSpec = constraint.ValueSizeConstraint(1, ub_security_categories)

class ESSSecurityLabel(univ.Set):
    __module__ = __name__


ESSSecurityLabel.componentType = namedtype.NamedTypes(namedtype.NamedType('security-policy-identifier', SecurityPolicyIdentifier()), namedtype.OptionalNamedType('security-classification', SecurityClassification()), namedtype.OptionalNamedType('privacy-mark', ESSPrivacyMark()), namedtype.OptionalNamedType('security-categories', SecurityCategories()))
id_aa_equivalentLabels = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.9')

class EquivalentLabels(univ.SequenceOf):
    __module__ = __name__


EquivalentLabels.componentType = ESSSecurityLabel()
id_aa_contentIdentifier = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.7')

class ContentIdentifier(univ.OctetString):
    __module__ = __name__


id_aa_contentReference = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.10')

class ContentReference(univ.Sequence):
    __module__ = __name__


ContentReference.componentType = namedtype.NamedTypes(namedtype.NamedType('contentType', ContentType()), namedtype.NamedType('signedContentIdentifier', ContentIdentifier()), namedtype.NamedType('originatorSignatureValue', univ.OctetString()))
id_aa_msgSigDigest = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.5')

class MsgSigDigest(univ.OctetString):
    __module__ = __name__


id_aa_contentHint = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.4')

class ContentHints(univ.Sequence):
    __module__ = __name__


ContentHints.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('contentDescription', char.UTF8String().subtype(subtypeSpec=constraint.ValueSizeConstraint(1, MAX))), namedtype.NamedType('contentType', ContentType()))

class AllOrFirstTier(univ.Integer):
    __module__ = __name__


AllOrFirstTier.namedValues = namedval.NamedValues(('allReceipts', 0), ('firstTierRecipients',
                                                                       1))

class ReceiptsFrom(univ.Choice):
    __module__ = __name__


ReceiptsFrom.componentType = namedtype.NamedTypes(namedtype.NamedType('allOrFirstTier', AllOrFirstTier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('receiptList', univ.SequenceOf(componentType=GeneralNames()).subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))
id_aa_receiptRequest = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.1')
ub_receiptsTo = univ.Integer(16)

class ReceiptRequest(univ.Sequence):
    __module__ = __name__


ReceiptRequest.componentType = namedtype.NamedTypes(namedtype.NamedType('signedContentIdentifier', ContentIdentifier()), namedtype.NamedType('receiptsFrom', ReceiptsFrom()), namedtype.NamedType('receiptsTo', univ.SequenceOf(componentType=GeneralNames()).subtype(sizeSpec=constraint.ValueSizeConstraint(1, ub_receiptsTo))))

class ESSVersion(univ.Integer):
    __module__ = __name__


ESSVersion.namedValues = namedval.NamedValues(('v1', 1))
id_ct_receipt = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.1')

class Receipt(univ.Sequence):
    __module__ = __name__


Receipt.componentType = namedtype.NamedTypes(namedtype.NamedType('version', ESSVersion()), namedtype.NamedType('contentType', ContentType()), namedtype.NamedType('signedContentIdentifier', ContentIdentifier()), namedtype.NamedType('originatorSignatureValue', univ.OctetString()))
_cmsAttributesMapUpdate = {id_aa_signingCertificate: SigningCertificate(), id_aa_mlExpandHistory: MLExpansionHistory(), id_aa_securityLabel: ESSSecurityLabel(), id_aa_equivalentLabels: EquivalentLabels(), id_aa_contentIdentifier: ContentIdentifier(), id_aa_contentReference: ContentReference(), id_aa_msgSigDigest: MsgSigDigest(), id_aa_contentHint: ContentHints(), id_aa_receiptRequest: ReceiptRequest()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)
_cmsContentTypesMapUpdate = {id_ct_receipt: Receipt()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)