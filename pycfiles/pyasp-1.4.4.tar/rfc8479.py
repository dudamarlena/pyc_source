# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8479.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5652
id_attr_validation_parameters = univ.ObjectIdentifier('1.3.6.1.4.1.2312.18.8.1')

class ValidationParams(univ.Sequence):
    __module__ = __name__


ValidationParams.componentType = namedtype.NamedTypes(namedtype.NamedType('hashAlg', univ.ObjectIdentifier()), namedtype.NamedType('seed', univ.OctetString()))
at_validation_parameters = rfc5652.Attribute()
at_validation_parameters['attrType'] = id_attr_validation_parameters
at_validation_parameters['attrValues'][0] = ValidationParams()
_cmsAttributesMapUpdate = {id_attr_validation_parameters: ValidationParams()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)