# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7292.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import opentype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc2315
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5280
from pyasn1_modules import rfc5958

def _OID(*components):
    output = []
    for x in tuple(components):
        if isinstance(x, univ.ObjectIdentifier):
            output.extend(list(x))
        else:
            output.append(int(x))

    return univ.ObjectIdentifier(output)


pkcs12BagTypeMap = {}
pkcs12CertBagMap = {}
pkcs12CRLBagMap = {}
pkcs12SecretBagMap = {}
DigestInfo = rfc2315.DigestInfo
ContentInfo = rfc5652.ContentInfo
PKCS12Attribute = rfc5652.Attribute
EncryptedPrivateKeyInfo = rfc5958.EncryptedPrivateKeyInfo
PrivateKeyInfo = rfc5958.PrivateKeyInfo

class AttributeType(univ.ObjectIdentifier):
    __module__ = __name__


class AttributeValue(univ.Any):
    __module__ = __name__


class AttributeValues(univ.SetOf):
    __module__ = __name__


AttributeValues.componentType = AttributeValue()

class CMSSingleAttribute(univ.Sequence):
    __module__ = __name__


CMSSingleAttribute.componentType = namedtype.NamedTypes(namedtype.NamedType('attrType', AttributeType()), namedtype.NamedType('attrValues', AttributeValues().subtype(sizeSpec=constraint.ValueSizeConstraint(1, 1)), openType=opentype.OpenType('attrType', rfc5652.cmsAttributesMap)))
rsadsi = _OID(1, 2, 840, 113549)
pkcs = _OID(rsadsi, 1)
pkcs_9 = _OID(pkcs, 9)
certTypes = _OID(pkcs_9, 22)
crlTypes = _OID(pkcs_9, 23)
pkcs_12 = _OID(pkcs, 12)
pkcs_12PbeIds = _OID(pkcs_12, 1)
pbeWithSHAAnd128BitRC4 = _OID(pkcs_12PbeIds, 1)
pbeWithSHAAnd40BitRC4 = _OID(pkcs_12PbeIds, 2)
pbeWithSHAAnd3_KeyTripleDES_CBC = _OID(pkcs_12PbeIds, 3)
pbeWithSHAAnd2_KeyTripleDES_CBC = _OID(pkcs_12PbeIds, 4)
pbeWithSHAAnd128BitRC2_CBC = _OID(pkcs_12PbeIds, 5)
pbeWithSHAAnd40BitRC2_CBC = _OID(pkcs_12PbeIds, 6)

class Pkcs_12PbeParams(univ.Sequence):
    __module__ = __name__


Pkcs_12PbeParams.componentType = namedtype.NamedTypes(namedtype.NamedType('salt', univ.OctetString()), namedtype.NamedType('iterations', univ.Integer()))
bagtypes = _OID(pkcs_12, 10, 1)

class BAG_TYPE(univ.Sequence):
    __module__ = __name__


BAG_TYPE.componentType = namedtype.NamedTypes(namedtype.NamedType('id', univ.ObjectIdentifier()), namedtype.NamedType('unnamed1', univ.Any(), openType=opentype.OpenType('attrType', pkcs12BagTypeMap)))
id_keyBag = _OID(bagtypes, 1)

class KeyBag(PrivateKeyInfo):
    __module__ = __name__


id_pkcs8ShroudedKeyBag = _OID(bagtypes, 2)

class PKCS8ShroudedKeyBag(EncryptedPrivateKeyInfo):
    __module__ = __name__


id_certBag = _OID(bagtypes, 3)

class CertBag(univ.Sequence):
    __module__ = __name__


CertBag.componentType = namedtype.NamedTypes(namedtype.NamedType('certId', univ.ObjectIdentifier()), namedtype.NamedType('certValue', univ.Any().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)), openType=opentype.OpenType('certId', pkcs12CertBagMap)))
x509Certificate = CertBag()
x509Certificate['certId'] = _OID(certTypes, 1)
x509Certificate['certValue'] = univ.OctetString()
sdsiCertificate = CertBag()
sdsiCertificate['certId'] = _OID(certTypes, 2)
sdsiCertificate['certValue'] = char.IA5String()
id_CRLBag = _OID(bagtypes, 4)

class CRLBag(univ.Sequence):
    __module__ = __name__


CRLBag.componentType = namedtype.NamedTypes(namedtype.NamedType('crlId', univ.ObjectIdentifier()), namedtype.NamedType('crlValue', univ.Any().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)), openType=opentype.OpenType('crlId', pkcs12CRLBagMap)))
x509CRL = CRLBag()
x509CRL['crlId'] = _OID(crlTypes, 1)
x509CRL['crlValue'] = univ.OctetString()
id_secretBag = _OID(bagtypes, 5)

class SecretBag(univ.Sequence):
    __module__ = __name__


SecretBag.componentType = namedtype.NamedTypes(namedtype.NamedType('secretTypeId', univ.ObjectIdentifier()), namedtype.NamedType('secretValue', univ.Any().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)), openType=opentype.OpenType('secretTypeId', pkcs12SecretBagMap)))
id_safeContentsBag = _OID(bagtypes, 6)

class SafeBag(univ.Sequence):
    __module__ = __name__


SafeBag.componentType = namedtype.NamedTypes(namedtype.NamedType('bagId', univ.ObjectIdentifier()), namedtype.NamedType('bagValue', univ.Any().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0)), openType=opentype.OpenType('bagId', pkcs12BagTypeMap)), namedtype.OptionalNamedType('bagAttributes', univ.SetOf(componentType=PKCS12Attribute())))

class SafeContents(univ.SequenceOf):
    __module__ = __name__


SafeContents.componentType = SafeBag()

class AuthenticatedSafe(univ.SequenceOf):
    __module__ = __name__


AuthenticatedSafe.componentType = ContentInfo()

class MacData(univ.Sequence):
    __module__ = __name__


MacData.componentType = namedtype.NamedTypes(namedtype.NamedType('mac', DigestInfo()), namedtype.NamedType('macSalt', univ.OctetString()), namedtype.DefaultedNamedType('iterations', univ.Integer().subtype(value=1)))

class PFX(univ.Sequence):
    __module__ = __name__


PFX.componentType = namedtype.NamedTypes(namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('v3',
                                                                                                                       3)))), namedtype.NamedType('authSafe', ContentInfo()), namedtype.OptionalNamedType('macData', MacData()))
pkcs_9_at_localKeyId = _OID(pkcs_9, 21)
localKeyId = CMSSingleAttribute()
localKeyId['attrType'] = pkcs_9_at_localKeyId
localKeyId['attrValues'][0] = univ.OctetString()
pkcs_9_ub_pkcs9String = univ.Integer(255)
pkcs_9_ub_friendlyName = univ.Integer(pkcs_9_ub_pkcs9String)
pkcs_9_at_friendlyName = _OID(pkcs_9, 20)

class FriendlyName(char.BMPString):
    __module__ = __name__


FriendlyName.subtypeSpec = constraint.ValueSizeConstraint(1, pkcs_9_ub_friendlyName)
friendlyName = CMSSingleAttribute()
friendlyName['attrType'] = pkcs_9_at_friendlyName
friendlyName['attrValues'][0] = FriendlyName()
_pkcs12BagTypeMap = {id_keyBag: KeyBag(), id_pkcs8ShroudedKeyBag: PKCS8ShroudedKeyBag(), id_certBag: CertBag(), id_CRLBag: CRLBag(), id_secretBag: SecretBag(), id_safeContentsBag: SafeBag()}
pkcs12BagTypeMap.update(_pkcs12BagTypeMap)
_pkcs12CertBagMap = {_OID(certTypes, 1): univ.OctetString(), _OID(certTypes, 2): char.IA5String()}
pkcs12CertBagMap.update(_pkcs12CertBagMap)
_pkcs12CRLBagMap = {_OID(crlTypes, 1): univ.OctetString()}
pkcs12CRLBagMap.update(_pkcs12CRLBagMap)
_algorithmIdentifierMapUpdate = {pbeWithSHAAnd128BitRC4: Pkcs_12PbeParams(), pbeWithSHAAnd40BitRC4: Pkcs_12PbeParams(), pbeWithSHAAnd3_KeyTripleDES_CBC: Pkcs_12PbeParams(), pbeWithSHAAnd2_KeyTripleDES_CBC: Pkcs_12PbeParams(), pbeWithSHAAnd128BitRC2_CBC: Pkcs_12PbeParams(), pbeWithSHAAnd40BitRC2_CBC: Pkcs_12PbeParams()}
rfc5280.algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)
_cmsAttributesMapUpdate = {pkcs_9_at_friendlyName: FriendlyName(), pkcs_9_at_localKeyId: univ.OctetString()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)