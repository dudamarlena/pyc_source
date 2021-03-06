# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc4211.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc3280
from pyasn1_modules import rfc3852
MAX = float('inf')

def _buildOid(*components):
    output = []
    for x in tuple(components):
        if isinstance(x, univ.ObjectIdentifier):
            output.extend(list(x))
        else:
            output.append(int(x))

    return univ.ObjectIdentifier(output)


id_pkix = _buildOid(1, 3, 6, 1, 5, 5, 7)
id_pkip = _buildOid(id_pkix, 5)
id_regCtrl = _buildOid(id_pkip, 1)

class SinglePubInfo(univ.Sequence):
    __module__ = __name__


SinglePubInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('pubMethod', univ.Integer(namedValues=namedval.NamedValues(('dontCare',
                                                                                                                                   0), ('x500',
                                                                                                                                        1), ('web',
                                                                                                                                             2), ('ldap',
                                                                                                                                                  3)))), namedtype.OptionalNamedType('pubLocation', rfc3280.GeneralName()))

class UTF8Pairs(char.UTF8String):
    __module__ = __name__


class PKMACValue(univ.Sequence):
    __module__ = __name__


PKMACValue.componentType = namedtype.NamedTypes(namedtype.NamedType('algId', rfc3280.AlgorithmIdentifier()), namedtype.NamedType('value', univ.BitString()))

class POPOSigningKeyInput(univ.Sequence):
    __module__ = __name__


POPOSigningKeyInput.componentType = namedtype.NamedTypes(namedtype.NamedType('authInfo', univ.Choice(componentType=namedtype.NamedTypes(namedtype.NamedType('sender', rfc3280.GeneralName().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('publicKeyMAC', PKMACValue())))), namedtype.NamedType('publicKey', rfc3280.SubjectPublicKeyInfo()))

class POPOSigningKey(univ.Sequence):
    __module__ = __name__


POPOSigningKey.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('poposkInput', POPOSigningKeyInput().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('algorithmIdentifier', rfc3280.AlgorithmIdentifier()), namedtype.NamedType('signature', univ.BitString()))

class Attributes(univ.SetOf):
    __module__ = __name__


Attributes.componentType = rfc3280.Attribute()

class PrivateKeyInfo(univ.Sequence):
    __module__ = __name__


PrivateKeyInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('version', univ.Integer()), namedtype.NamedType('privateKeyAlgorithm', rfc3280.AlgorithmIdentifier()), namedtype.NamedType('privateKey', univ.OctetString()), namedtype.OptionalNamedType('attributes', Attributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))))

class EncryptedValue(univ.Sequence):
    __module__ = __name__


EncryptedValue.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('intendedAlg', rfc3280.AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('symmAlg', rfc3280.AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.OptionalNamedType('encSymmKey', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))), namedtype.OptionalNamedType('keyAlg', rfc3280.AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 3))), namedtype.OptionalNamedType('valueHint', univ.OctetString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))), namedtype.NamedType('encValue', univ.BitString()))

class EncryptedKey(univ.Choice):
    __module__ = __name__


EncryptedKey.componentType = namedtype.NamedTypes(namedtype.NamedType('encryptedValue', EncryptedValue()), namedtype.NamedType('envelopedData', rfc3852.EnvelopedData().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))))

class KeyGenParameters(univ.OctetString):
    __module__ = __name__


class PKIArchiveOptions(univ.Choice):
    __module__ = __name__


PKIArchiveOptions.componentType = namedtype.NamedTypes(namedtype.NamedType('encryptedPrivKey', EncryptedKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('keyGenParameters', KeyGenParameters().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('archiveRemGenPrivKey', univ.Boolean().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))
id_regCtrl_authenticator = _buildOid(id_regCtrl, 2)
id_regInfo = _buildOid(id_pkip, 2)
id_regInfo_certReq = _buildOid(id_regInfo, 2)

class ProtocolEncrKey(rfc3280.SubjectPublicKeyInfo):
    __module__ = __name__


class Authenticator(char.UTF8String):
    __module__ = __name__


class SubsequentMessage(univ.Integer):
    __module__ = __name__


SubsequentMessage.namedValues = namedval.NamedValues(('encrCert', 0), ('challengeResp',
                                                                       1))

class AttributeTypeAndValue(univ.Sequence):
    __module__ = __name__


AttributeTypeAndValue.componentType = namedtype.NamedTypes(namedtype.NamedType('type', univ.ObjectIdentifier()), namedtype.NamedType('value', univ.Any()))

class POPOPrivKey(univ.Choice):
    __module__ = __name__


POPOPrivKey.componentType = namedtype.NamedTypes(namedtype.NamedType('thisMessage', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('subsequentMessage', SubsequentMessage().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('dhMAC', univ.BitString().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))), namedtype.NamedType('agreeMAC', PKMACValue().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))), namedtype.NamedType('encryptedKey', rfc3852.EnvelopedData().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 4))))

class ProofOfPossession(univ.Choice):
    __module__ = __name__


ProofOfPossession.componentType = namedtype.NamedTypes(namedtype.NamedType('raVerified', univ.Null().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('signature', POPOSigningKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))), namedtype.NamedType('keyEncipherment', POPOPrivKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 2))), namedtype.NamedType('keyAgreement', POPOPrivKey().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))))

class OptionalValidity(univ.Sequence):
    __module__ = __name__


OptionalValidity.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('notBefore', rfc3280.Time().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.OptionalNamedType('notAfter', rfc3280.Time().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 1))))

class CertTemplate(univ.Sequence):
    __module__ = __name__


CertTemplate.componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('version', rfc3280.Version().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('serialNumber', univ.Integer().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.OptionalNamedType('signingAlg', rfc3280.AlgorithmIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))), namedtype.OptionalNamedType('issuer', rfc3280.Name().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 3))), namedtype.OptionalNamedType('validity', OptionalValidity().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 4))), namedtype.OptionalNamedType('subject', rfc3280.Name().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 5))), namedtype.OptionalNamedType('publicKey', rfc3280.SubjectPublicKeyInfo().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 6))), namedtype.OptionalNamedType('issuerUID', rfc3280.UniqueIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 7))), namedtype.OptionalNamedType('subjectUID', rfc3280.UniqueIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 8))), namedtype.OptionalNamedType('extensions', rfc3280.Extensions().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 9))))

class Controls(univ.SequenceOf):
    __module__ = __name__


Controls.componentType = AttributeTypeAndValue()
Controls.sizeSpec = constraint.ValueSizeConstraint(1, MAX)

class CertRequest(univ.Sequence):
    __module__ = __name__


CertRequest.componentType = namedtype.NamedTypes(namedtype.NamedType('certReqId', univ.Integer()), namedtype.NamedType('certTemplate', CertTemplate()), namedtype.OptionalNamedType('controls', Controls()))

class CertReqMsg(univ.Sequence):
    __module__ = __name__


CertReqMsg.componentType = namedtype.NamedTypes(namedtype.NamedType('certReq', CertRequest()), namedtype.OptionalNamedType('popo', ProofOfPossession()), namedtype.OptionalNamedType('regInfo', univ.SequenceOf(componentType=AttributeTypeAndValue())))

class CertReqMessages(univ.SequenceOf):
    __module__ = __name__


CertReqMessages.componentType = CertReqMsg()
CertReqMessages.sizeSpec = constraint.ValueSizeConstraint(1, MAX)

class CertReq(CertRequest):
    __module__ = __name__


id_regCtrl_pkiPublicationInfo = _buildOid(id_regCtrl, 3)

class CertId(univ.Sequence):
    __module__ = __name__


CertId.componentType = namedtype.NamedTypes(namedtype.NamedType('issuer', rfc3280.GeneralName()), namedtype.NamedType('serialNumber', univ.Integer()))

class OldCertId(CertId):
    __module__ = __name__


class PKIPublicationInfo(univ.Sequence):
    __module__ = __name__


PKIPublicationInfo.componentType = namedtype.NamedTypes(namedtype.NamedType('action', univ.Integer(namedValues=namedval.NamedValues(('dontPublish',
                                                                                                                                     0), ('pleasePublish',
                                                                                                                                          1)))), namedtype.OptionalNamedType('pubInfos', univ.SequenceOf(componentType=SinglePubInfo())))

class EncKeyWithID(univ.Sequence):
    __module__ = __name__


EncKeyWithID.componentType = namedtype.NamedTypes(namedtype.NamedType('privateKey', PrivateKeyInfo()), namedtype.OptionalNamedType('identifier', univ.Choice(componentType=namedtype.NamedTypes(namedtype.NamedType('string', char.UTF8String()), namedtype.NamedType('generalName', rfc3280.GeneralName())))))
id_regCtrl_protocolEncrKey = _buildOid(id_regCtrl, 6)
id_regCtrl_oldCertID = _buildOid(id_regCtrl, 5)
id_smime = _buildOid(1, 2, 840, 113549, 1, 9, 16)

class PBMParameter(univ.Sequence):
    __module__ = __name__


PBMParameter.componentType = namedtype.NamedTypes(namedtype.NamedType('salt', univ.OctetString()), namedtype.NamedType('owf', rfc3280.AlgorithmIdentifier()), namedtype.NamedType('iterationCount', univ.Integer()), namedtype.NamedType('mac', rfc3280.AlgorithmIdentifier()))
id_regCtrl_regToken = _buildOid(id_regCtrl, 1)
id_regCtrl_pkiArchiveOptions = _buildOid(id_regCtrl, 4)
id_regInfo_utf8Pairs = _buildOid(id_regInfo, 1)
id_ct = _buildOid(id_smime, 1)
id_ct_encKeyWithID = _buildOid(id_ct, 21)

class RegToken(char.UTF8String):
    __module__ = __name__