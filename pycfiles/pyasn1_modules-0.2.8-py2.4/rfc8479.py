# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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