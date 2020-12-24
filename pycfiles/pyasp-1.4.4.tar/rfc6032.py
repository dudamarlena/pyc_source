# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc6032.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5652
from pyasn1_modules import rfc5083
id_aa_KP_contentDecryptKeyID = univ.ObjectIdentifier('2.16.840.1.101.2.1.5.66')

class ContentDecryptKeyID(univ.OctetString):
    __module__ = __name__


aa_content_decrypt_key_identifier = rfc5652.Attribute()
aa_content_decrypt_key_identifier['attrType'] = id_aa_KP_contentDecryptKeyID
aa_content_decrypt_key_identifier['attrValues'][0] = ContentDecryptKeyID()
id_ct_KP_encryptedKeyPkg = univ.ObjectIdentifier('2.16.840.1.101.2.1.2.78.2')

class EncryptedKeyPackage(univ.Choice):
    __module__ = __name__


EncryptedKeyPackage.componentType = namedtype.NamedTypes(namedtype.NamedType('encrypted', rfc5652.EncryptedData()), namedtype.NamedType('enveloped', rfc5652.EnvelopedData().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.NamedType('authEnveloped', rfc5083.AuthEnvelopedData().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))
_cmsAttributesMapUpdate = {id_aa_KP_contentDecryptKeyID: ContentDecryptKeyID()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)
_cmsContentTypesMapUpdate = {id_ct_KP_encryptedKeyPkg: EncryptedKeyPackage()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)