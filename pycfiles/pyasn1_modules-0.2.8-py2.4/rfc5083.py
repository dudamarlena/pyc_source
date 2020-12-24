# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5083.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5652
MAX = float('inf')
id_ct_authEnvelopedData = univ.ObjectIdentifier('1.2.840.113549.1.9.16.1.23')

class AuthEnvelopedData(univ.Sequence):
    __module__ = __name__


AuthEnvelopedData.componentType = namedtype.NamedTypes(namedtype.NamedType('version', rfc5652.CMSVersion()), namedtype.OptionalNamedType('originatorInfo', rfc5652.OriginatorInfo().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatConstructed, 0))), namedtype.NamedType('recipientInfos', rfc5652.RecipientInfos()), namedtype.NamedType('authEncryptedContentInfo', rfc5652.EncryptedContentInfo()), namedtype.OptionalNamedType('authAttrs', rfc5652.AuthAttributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))), namedtype.NamedType('mac', rfc5652.MessageAuthenticationCode()), namedtype.OptionalNamedType('unauthAttrs', rfc5652.UnauthAttributes().subtype(implicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 2))))
_cmsContentTypesMapUpdate = {id_ct_authEnvelopedData: AuthEnvelopedData()}
rfc5652.cmsContentTypesMap.update(_cmsContentTypesMapUpdate)