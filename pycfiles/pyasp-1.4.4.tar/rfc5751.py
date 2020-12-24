# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5751.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import opentype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc8018

def _OID(*components):
    output = []
    for x in tuple(components):
        if isinstance(x, univ.ObjectIdentifier):
            output.extend(list(x))
        else:
            output.append(int(x))

    return univ.ObjectIdentifier(output)


IssuerAndSerialNumber = rfc5652.IssuerAndSerialNumber
RecipientKeyIdentifier = rfc5652.RecipientKeyIdentifier
SubjectKeyIdentifier = rfc5652.SubjectKeyIdentifier
rc2CBC = rfc8018.rc2CBC
smimeCapabilities = univ.ObjectIdentifier('1.2.840.113549.1.9.15')
smimeCapabilityMap = {}

class SMIMECapability(univ.Sequence):
    __module__ = __name__


SMIMECapability.componentType = namedtype.NamedTypes(namedtype.NamedType('capabilityID', univ.ObjectIdentifier()), namedtype.OptionalNamedType('parameters', univ.Any(), openType=opentype.OpenType('capabilityID', smimeCapabilityMap)))

class SMIMECapabilities(univ.SequenceOf):
    __module__ = __name__


SMIMECapabilities.componentType = SMIMECapability()

class SMIMECapabilitiesParametersForRC2CBC(univ.Integer):
    __module__ = __name__


id_smime = univ.ObjectIdentifier('1.2.840.113549.1.9.16')
id_aa = _OID(id_smime, 2)
id_aa_encrypKeyPref = _OID(id_aa, 11)

class SMIMEEncryptionKeyPreference(univ.Choice):
    __module__ = __name__


SMIMEEncryptionKeyPreference.componentType = namedtype.NamedTypes(namedtype.NamedType('issuerAndSerialNumber', IssuerAndSerialNumber().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('receipentKeyId', RecipientKeyIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('subjectAltKeyIdentifier', SubjectKeyIdentifier().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))
id_cap = _OID(id_smime, 11)
id_cap_preferBinaryInside = _OID(id_cap, 1)
_cmsAttributesMapUpdate = {smimeCapabilities: SMIMECapabilities(), id_aa_encrypKeyPref: SMIMEEncryptionKeyPreference()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)
_smimeCapabilityMapUpdate = {rc2CBC: SMIMECapabilitiesParametersForRC2CBC()}
smimeCapabilityMap.update(_smimeCapabilityMapUpdate)