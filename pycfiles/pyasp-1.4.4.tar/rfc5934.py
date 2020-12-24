# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5934.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import univ, char, namedtype, namedval, tag, constraint, useful
from pyasn1_modules import rfc2985
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5914
MAX = float('inf')

def _OID(*components):
    output = []
    for x in tuple(components):
        if isinstance(x, univ.ObjectIdentifier):
            output.extend(list(x))
        else:
            output.append(int(x))

    return univ.ObjectIdentifier(output)


SingleAttribute = rfc2985.SingleAttribute
CertPathControls = rfc5914.CertPathControls
TrustAnchorChoice = rfc5914.TrustAnchorChoice
TrustAnchorTitle = rfc5914.TrustAnchorTitle
AlgorithmIdentifier = rfc5280.AlgorithmIdentifier
AnotherName = rfc5280.AnotherName
Attribute = rfc5280.Attribute
Certificate = rfc5280.Certificate
CertificateSerialNumber = rfc5280.CertificateSerialNumber
Extension = rfc5280.Extension
Extensions = rfc5280.Extensions
KeyIdentifier = rfc5280.KeyIdentifier
Name = rfc5280.Name
SubjectPublicKeyInfo = rfc5280.SubjectPublicKeyInfo
TBSCertificate = rfc5280.TBSCertificate
Validity = rfc5280.Validity
id_tamp = univ.ObjectIdentifier('2.16.840.1.101.2.1.2.77')
id_ct_TAMP_statusQuery = _OID(id_tamp, 1)

class TAMPVersion(univ.Integer):
    __module__ = __name__


TAMPVersion.namedValues = namedval.NamedValues(('v1', 1), ('v2', 2))

class TerseOrVerbose(univ.Enumerated):
    __module__ = __name__


TerseOrVerbose.namedValues = namedval.NamedValues(('terse', 1), ('verbose', 2))

class HardwareSerialEntry(univ.Choice):
    __module__ = __name__


HardwareSerialEntry.componentType = namedtype.NamedTypes(namedtype.NamedType('all', univ.Null()), namedtype.NamedType('single', univ.OctetString()), namedtype.NamedType('block', univ.Sequence(componentType=namedtype.NamedTypes(namedtype.NamedType('low', univ.OctetString()), namedtype.NamedType('high', univ.OctetString())))))

class HardwareModules(univ.Sequence):
    __module__ = __name__


HardwareModules.componentType = namedtype.NamedTypes(namedtype.NamedType('hwType', univ.ObjectIdentifier()), namedtype.NamedType('hwSerialEntries', univ.SequenceOf(componentType=HardwareSerialEntry()).subtype(subtypeSpec=constraint.ValueSizeConstraint(1, MAX))))

class HardwareModuleIdentifierList(univ.SequenceOf):
    __module__ = __name__


HardwareModuleIdentifierList.componentType = HardwareModules()
HardwareModuleIdentifierList.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)

class Community(univ.ObjectIdentifier):
    __module__ = __name__


class CommunityIdentifierList(univ.SequenceOf):
    __module__ = __name__


CommunityIdentifierList.componentType = Community()
CommunityIdentifierList.subtypeSpec = constraint.ValueSizeConstraint(0, MAX)

class TargetIdentifier(univ.Choice):
    __module__ = __name__


TargetIdentifier.componentType = namedtype.NamedTypes(namedtype.NamedType('hwModules', HardwareModuleIdentifierList().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('communities', CommunityIdentifierList().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))), namedtype.NamedType('allModules', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))), namedtype.NamedType('uri', char.IA5String().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))), namedtype.NamedType('otherName', AnotherName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))))

class SeqNumber(univ.Integer):
    __module__ = __name__


SeqNumber.subtypeSpec = constraint.ValueRangeConstraint(0, 9223372036854775807)

class TAMPMsgRef(univ.Sequence):
    __module__ = __name__


TAMPMsgRef.componentType = namedtype.NamedTypes(namedtype.NamedType('target', TargetIdentifier()), namedtype.NamedType('seqNum', SeqNumber()))

class TAMPStatusQuery(univ.Sequence):
    __module__ = __name__


TAMPStatusQuery.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.DefaultedNamedType('terse', TerseOrVerbose().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value='verbose')), namedtype.NamedType('query', TAMPMsgRef()))
tamp_status_query = rfc5652.ContentInfo()
tamp_status_query['contentType'] = id_ct_TAMP_statusQuery
tamp_status_query['content'] = TAMPStatusQuery()
id_ct_TAMP_statusResponse = _OID(id_tamp, 2)

class KeyIdentifiers(univ.SequenceOf):
    __module__ = __name__


KeyIdentifiers.componentType = KeyIdentifier()
KeyIdentifiers.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)

class TrustAnchorChoiceList(univ.SequenceOf):
    __module__ = __name__


TrustAnchorChoiceList.componentType = TrustAnchorChoice()
TrustAnchorChoiceList.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)

class TAMPSequenceNumber(univ.Sequence):
    __module__ = __name__


TAMPSequenceNumber.componentType = namedtype.NamedTypes(namedtype.NamedType('keyId', KeyIdentifier()), namedtype.NamedType('seqNumber', SeqNumber()))

class TAMPSequenceNumbers(univ.SequenceOf):
    __module__ = __name__


TAMPSequenceNumbers.componentType = TAMPSequenceNumber()
TAMPSequenceNumbers.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)

class TerseStatusResponse(univ.Sequence):
    __module__ = __name__


TerseStatusResponse.componentType = namedtype.NamedTypes(namedtype.NamedType('taKeyIds', KeyIdentifiers()), namedtype.OptionalNamedType('communities', CommunityIdentifierList()))

class VerboseStatusResponse(univ.Sequence):
    __module__ = __name__


VerboseStatusResponse.componentType = namedtype.NamedTypes(namedtype.NamedType('taInfo', TrustAnchorChoiceList()), namedtype.OptionalNamedType('continPubKeyDecryptAlg', AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('communities', CommunityIdentifierList().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.OptionalNamedType('tampSeqNumbers', TAMPSequenceNumbers().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))

class StatusResponse(univ.Choice):
    __module__ = __name__


StatusResponse.componentType = namedtype.NamedTypes(namedtype.NamedType('terseResponse', TerseStatusResponse().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('verboseResponse', VerboseStatusResponse().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))

class TAMPStatusResponse(univ.Sequence):
    __module__ = __name__


TAMPStatusResponse.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.NamedType('query', TAMPMsgRef()), namedtype.NamedType('response', StatusResponse()), namedtype.DefaultedNamedType('usesApex', univ.Boolean().subtype(value=1)))
tamp_status_response = rfc5652.ContentInfo()
tamp_status_response['contentType'] = id_ct_TAMP_statusResponse
tamp_status_response['content'] = TAMPStatusResponse()
id_ct_TAMP_update = _OID(id_tamp, 3)

class TBSCertificateChangeInfo(univ.Sequence):
    __module__ = __name__


TBSCertificateChangeInfo.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('serialNumber', CertificateSerialNumber()), namedtype.OptionalNamedType('signature', AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('issuer', Name().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.OptionalNamedType('validity', Validity().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))), namedtype.OptionalNamedType('subject', Name().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))), namedtype.NamedType('subjectPublicKeyInfo', SubjectPublicKeyInfo().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))), namedtype.OptionalNamedType('exts', Extensions().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 5))))

class TrustAnchorChangeInfo(univ.Sequence):
    __module__ = __name__


TrustAnchorChangeInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('pubKey', SubjectPublicKeyInfo()), namedtype.OptionalNamedType('keyId', KeyIdentifier()), namedtype.OptionalNamedType('taTitle', TrustAnchorTitle()), namedtype.OptionalNamedType('certPath', CertPathControls()), namedtype.OptionalNamedType('exts', Extensions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class TrustAnchorChangeInfoChoice(univ.Choice):
    __module__ = __name__


TrustAnchorChangeInfoChoice.componentType = namedtype.NamedTypes(namedtype.NamedType('tbsCertChange', TBSCertificateChangeInfo().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('taChange', TrustAnchorChangeInfo().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))

class TrustAnchorUpdate(univ.Choice):
    __module__ = __name__


TrustAnchorUpdate.componentType = namedtype.NamedTypes(namedtype.NamedType('add', TrustAnchorChoice().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('remove', SubjectPublicKeyInfo().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))), namedtype.NamedType('change', TrustAnchorChangeInfoChoice().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))))

class TAMPUpdate(univ.Sequence):
    __module__ = __name__


TAMPUpdate.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.DefaultedNamedType('terse', TerseOrVerbose().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value='verbose')), namedtype.NamedType('msgRef', TAMPMsgRef()), namedtype.NamedType('updates', univ.SequenceOf(componentType=TrustAnchorUpdate()).subtype(subtypeSpec=constraint.ValueSizeConstraint(1, MAX))), namedtype.OptionalNamedType('tampSeqNumbers', TAMPSequenceNumbers().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))
tamp_update = rfc5652.ContentInfo()
tamp_update['contentType'] = id_ct_TAMP_update
tamp_update['content'] = TAMPUpdate()
id_ct_TAMP_updateConfirm = _OID(id_tamp, 4)

class StatusCode(univ.Enumerated):
    __module__ = __name__


StatusCode.namedValues = namedval.NamedValues(('success', 0), ('decodeFailure', 1), ('badContentInfo',
                                                                                     2), ('badSignedData',
                                                                                          3), ('badEncapContent',
                                                                                               4), ('badCertificate',
                                                                                                    5), ('badSignerInfo',
                                                                                                         6), ('badSignedAttrs',
                                                                                                              7), ('badUnsignedAttrs',
                                                                                                                   8), ('missingContent',
                                                                                                                        9), ('noTrustAnchor',
                                                                                                                             10), ('notAuthorized',
                                                                                                                                   11), ('badDigestAlgorithm',
                                                                                                                                         12), ('badSignatureAlgorithm',
                                                                                                                                               13), ('unsupportedKeySize',
                                                                                                                                                     14), ('unsupportedParameters',
                                                                                                                                                           15), ('signatureFailure',
                                                                                                                                                                 16), ('insufficientMemory',
                                                                                                                                                                       17), ('unsupportedTAMPMsgType',
                                                                                                                                                                             18), ('apexTAMPAnchor',
                                                                                                                                                                                   19), ('improperTAAddition',
                                                                                                                                                                                         20), ('seqNumFailure',
                                                                                                                                                                                               21), ('contingencyPublicKeyDecrypt',
                                                                                                                                                                                                     22), ('incorrectTarget',
                                                                                                                                                                                                           23), ('communityUpdateFailed',
                                                                                                                                                                                                                 24), ('trustAnchorNotFound',
                                                                                                                                                                                                                       25), ('unsupportedTAAlgorithm',
                                                                                                                                                                                                                             26), ('unsupportedTAKeySize',
                                                                                                                                                                                                                                   27), ('unsupportedContinPubKeyDecryptAlg',
                                                                                                                                                                                                                                         28), ('missingSignature',
                                                                                                                                                                                                                                               29), ('resourcesBusy',
                                                                                                                                                                                                                                                     30), ('versionNumberMismatch',
                                                                                                                                                                                                                                                           31), ('missingPolicySet',
                                                                                                                                                                                                                                                                 32), ('revokedCertificate',
                                                                                                                                                                                                                                                                       33), ('unsupportedTrustAnchorFormat',
                                                                                                                                                                                                                                                                             34), ('improperTAChange',
                                                                                                                                                                                                                                                                                   35), ('malformed',
                                                                                                                                                                                                                                                                                         36), ('cmsError',
                                                                                                                                                                                                                                                                                               37), ('unsupportedTargetIdentifier',
                                                                                                                                                                                                                                                                                                     38), ('other',
                                                                                                                                                                                                                                                                                                           127))

class StatusCodeList(univ.SequenceOf):
    __module__ = __name__


StatusCodeList.componentType = StatusCode()
StatusCodeList.subtypeSpec = constraint.ValueSizeConstraint(1, MAX)

class TerseUpdateConfirm(StatusCodeList):
    __module__ = __name__


class VerboseUpdateConfirm(univ.Sequence):
    __module__ = __name__


VerboseUpdateConfirm.componentType = namedtype.NamedTypes(namedtype.NamedType('status', StatusCodeList()), namedtype.NamedType('taInfo', TrustAnchorChoiceList()), namedtype.OptionalNamedType('tampSeqNumbers', TAMPSequenceNumbers()), namedtype.DefaultedNamedType('usesApex', univ.Boolean().subtype(value=1)))

class UpdateConfirm(univ.Choice):
    __module__ = __name__


UpdateConfirm.componentType = namedtype.NamedTypes(namedtype.NamedType('terseConfirm', TerseUpdateConfirm().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('verboseConfirm', VerboseUpdateConfirm().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))

class TAMPUpdateConfirm(univ.Sequence):
    __module__ = __name__


TAMPUpdateConfirm.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.NamedType('update', TAMPMsgRef()), namedtype.NamedType('confirm', UpdateConfirm()))
tamp_update_confirm = rfc5652.ContentInfo()
tamp_update_confirm['contentType'] = id_ct_TAMP_updateConfirm
tamp_update_confirm['content'] = TAMPUpdateConfirm()
id_ct_TAMP_apexUpdate = _OID(id_tamp, 5)

class TAMPApexUpdate(univ.Sequence):
    __module__ = __name__


TAMPApexUpdate.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.DefaultedNamedType('terse', TerseOrVerbose().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value='verbose')), namedtype.NamedType('msgRef', TAMPMsgRef()), namedtype.NamedType('clearTrustAnchors', univ.Boolean()), namedtype.NamedType('clearCommunities', univ.Boolean()), namedtype.OptionalNamedType('seqNumber', SeqNumber()), namedtype.NamedType('apexTA', TrustAnchorChoice()))
tamp_apex_update = rfc5652.ContentInfo()
tamp_apex_update['contentType'] = id_ct_TAMP_apexUpdate
tamp_apex_update['content'] = TAMPApexUpdate()
id_ct_TAMP_apexUpdateConfirm = _OID(id_tamp, 6)

class TerseApexUpdateConfirm(StatusCode):
    __module__ = __name__


class VerboseApexUpdateConfirm(univ.Sequence):
    __module__ = __name__


VerboseApexUpdateConfirm.componentType = namedtype.NamedTypes(namedtype.NamedType('status', StatusCode()), namedtype.NamedType('taInfo', TrustAnchorChoiceList()), namedtype.OptionalNamedType('communities', CommunityIdentifierList().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('tampSeqNumbers', TAMPSequenceNumbers().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))

class ApexUpdateConfirm(univ.Choice):
    __module__ = __name__


ApexUpdateConfirm.componentType = namedtype.NamedTypes(namedtype.NamedType('terseApexConfirm', TerseApexUpdateConfirm().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('verboseApexConfirm', VerboseApexUpdateConfirm().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))

class TAMPApexUpdateConfirm(univ.Sequence):
    __module__ = __name__


TAMPApexUpdateConfirm.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.NamedType('apexReplace', TAMPMsgRef()), namedtype.NamedType('apexConfirm', ApexUpdateConfirm()))
tamp_apex_update_confirm = rfc5652.ContentInfo()
tamp_apex_update_confirm['contentType'] = id_ct_TAMP_apexUpdateConfirm
tamp_apex_update_confirm['content'] = TAMPApexUpdateConfirm()
id_ct_TAMP_communityUpdate = _OID(id_tamp, 7)

class CommunityUpdates(univ.Sequence):
    __module__ = __name__


CommunityUpdates.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('remove', CommunityIdentifierList().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.OptionalNamedType('add', CommunityIdentifierList().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))

class TAMPCommunityUpdate(univ.Sequence):
    __module__ = __name__


TAMPCommunityUpdate.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.DefaultedNamedType('terse', TerseOrVerbose().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1)).subtype(value='verbose')), namedtype.NamedType('msgRef', TAMPMsgRef()), namedtype.NamedType('updates', CommunityUpdates()))
tamp_community_update = rfc5652.ContentInfo()
tamp_community_update['contentType'] = id_ct_TAMP_communityUpdate
tamp_community_update['content'] = TAMPCommunityUpdate()
id_ct_TAMP_communityUpdateConfirm = _OID(id_tamp, 8)

class TerseCommunityConfirm(StatusCode):
    __module__ = __name__


class VerboseCommunityConfirm(univ.Sequence):
    __module__ = __name__


VerboseCommunityConfirm.componentType = namedtype.NamedTypes(namedtype.NamedType('status', StatusCode()), namedtype.OptionalNamedType('communities', CommunityIdentifierList()))

class CommunityConfirm(univ.Choice):
    __module__ = __name__


CommunityConfirm.componentType = namedtype.NamedTypes(namedtype.NamedType('terseCommConfirm', TerseCommunityConfirm().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('verboseCommConfirm', VerboseCommunityConfirm().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))

class TAMPCommunityUpdateConfirm(univ.Sequence):
    __module__ = __name__


TAMPCommunityUpdateConfirm.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.NamedType('update', TAMPMsgRef()), namedtype.NamedType('commConfirm', CommunityConfirm()))
tamp_community_update_confirm = rfc5652.ContentInfo()
tamp_community_update_confirm['contentType'] = id_ct_TAMP_communityUpdateConfirm
tamp_community_update_confirm['content'] = TAMPCommunityUpdateConfirm()
id_ct_TAMP_seqNumAdjust = _OID(id_tamp, 10)

class SequenceNumberAdjust(univ.Sequence):
    __module__ = __name__


SequenceNumberAdjust.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.NamedType('msgRef', TAMPMsgRef()))
tamp_sequence_number_adjust = rfc5652.ContentInfo()
tamp_sequence_number_adjust['contentType'] = id_ct_TAMP_seqNumAdjust
tamp_sequence_number_adjust['content'] = SequenceNumberAdjust()
id_ct_TAMP_seqNumAdjustConfirm = _OID(id_tamp, 11)

class SequenceNumberAdjustConfirm(univ.Sequence):
    __module__ = __name__


SequenceNumberAdjustConfirm.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.NamedType('adjust', TAMPMsgRef()), namedtype.NamedType('status', StatusCode()))
tamp_sequence_number_adjust_confirm = rfc5652.ContentInfo()
tamp_sequence_number_adjust_confirm['contentType'] = id_ct_TAMP_seqNumAdjustConfirm
tamp_sequence_number_adjust_confirm['content'] = SequenceNumberAdjustConfirm()
id_ct_TAMP_error = _OID(id_tamp, 9)

class TAMPError(univ.Sequence):
    __module__ = __name__


TAMPError.componentType = namedtype.NamedTypes(namedtype.DefaultedNamedType('version', TAMPVersion().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)).subtype(value='v2')), namedtype.NamedType('msgType', univ.ObjectIdentifier()), namedtype.NamedType('status', StatusCode()), namedtype.OptionalNamedType('msgRef', TAMPMsgRef()))
tamp_error = rfc5652.ContentInfo()
tamp_error['contentType'] = id_ct_TAMP_error
tamp_error['content'] = TAMPError()
id_attributes = univ.ObjectIdentifier('2.16.840.1.101.2.1.5')
id_aa_TAMP_contingencyPublicKeyDecryptKey = _OID(id_attributes, 63)

class PlaintextSymmetricKey(univ.OctetString):
    __module__ = __name__


contingency_public_key_decrypt_key = Attribute()
contingency_public_key_decrypt_key['type'] = id_aa_TAMP_contingencyPublicKeyDecryptKey
contingency_public_key_decrypt_key['values'][0] = PlaintextSymmetricKey()
id_pe_wrappedApexContinKey = univ.ObjectIdentifier('1.3.6.1.5.5.7.1.20')

class ApexContingencyKey(univ.Sequence):
    __module__ = __name__


ApexContingencyKey.componentType = namedtype.NamedTypes(namedtype.NamedType('wrapAlgorithm', AlgorithmIdentifier()), namedtype.NamedType('wrappedContinPubKey', univ.OctetString()))
wrappedApexContinKey = Extension()
wrappedApexContinKey['extnID'] = id_pe_wrappedApexContinKey
wrappedApexContinKey['critical'] = 0
wrappedApexContinKey['extnValue'] = univ.OctetString()
_cmsContentTypesMapUpdate = {id_ct_TAMP_statusQuery: TAMPStatusQuery(), id_ct_TAMP_statusResponse: TAMPStatusResponse(), id_ct_TAMP_update: TAMPUpdate(), id_ct_TAMP_updateConfirm: TAMPUpdateConfirm(), id_ct_TAMP_apexUpdate: TAMPApexUpdate(), id_ct_TAMP_apexUpdateConfirm: TAMPApexUpdateConfirm(), id_ct_TAMP_communityUpdate: TAMPCommunityUpdate(), id_ct_TAMP_communityUpdateConfirm: TAMPCommunityUpdateConfirm(), id_ct_TAMP_seqNumAdjust: SequenceNumberAdjust(), id_ct_TAMP_seqNumAdjustConfirm: SequenceNumberAdjustConfirm(), id_ct_TAMP_error: TAMPError()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)
_cmsAttributesMapUpdate = {id_aa_TAMP_contingencyPublicKeyDecryptKey: PlaintextSymmetricKey()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)
_certificateExtensionsMap = {id_pe_wrappedApexContinKey: ApexContingencyKey()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMap)