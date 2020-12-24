# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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