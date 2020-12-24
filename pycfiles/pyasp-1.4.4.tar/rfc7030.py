# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7030.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5652
MAX = float('inf')
Attribute = rfc5652.Attribute
id_aa_asymmDecryptKeyID = univ.ObjectIdentifier('1.2.840.113549.1.9.16.2.54')

class AsymmetricDecryptKeyIdentifier(univ.OctetString):
    __module__ = __name__


aa_asymmDecryptKeyID = Attribute()
aa_asymmDecryptKeyID['attrType'] = id_aa_asymmDecryptKeyID
aa_asymmDecryptKeyID['attrValues'][0] = AsymmetricDecryptKeyIdentifier()

class AttrOrOID(univ.Choice):
    __module__ = __name__


AttrOrOID.componentType = namedtype.NamedTypes(namedtype.NamedType('oid', univ.ObjectIdentifier()), namedtype.NamedType('attribute', Attribute()))

class CsrAttrs(univ.SequenceOf):
    __module__ = __name__


CsrAttrs.componentType = AttrOrOID()
CsrAttrs.subtypeSpec = constraint.ValueSizeConstraint(0, MAX)
_cmsAttributesMapUpdate = {id_aa_asymmDecryptKeyID: AsymmetricDecryptKeyIdentifier()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)