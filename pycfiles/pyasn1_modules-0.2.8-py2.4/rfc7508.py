# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7508.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import univ
from pyasn1_modules import rfc5652
import string
MAX = float('inf')

class Algorithm(univ.Enumerated):
    __module__ = __name__
    namedValues = namedval.NamedValues(('canonAlgorithmSimple', 0), ('canonAlgorithmRelaxed',
                                                                     1))


class HeaderFieldStatus(univ.Integer):
    __module__ = __name__
    namedValues = namedval.NamedValues(('duplicated', 0), ('deleted', 1), ('modified',
                                                                           2))


class HeaderFieldName(char.VisibleString):
    __module__ = __name__
    subtypeSpec = constraint.PermittedAlphabetConstraint(*string.printable) - constraint.PermittedAlphabetConstraint(':')


class HeaderFieldValue(char.UTF8String):
    __module__ = __name__


class HeaderField(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('field-Name', HeaderFieldName()), namedtype.NamedType('field-Value', HeaderFieldValue()), namedtype.DefaultedNamedType('field-Status', HeaderFieldStatus().subtype(value='duplicated')))


class HeaderFields(univ.SequenceOf):
    __module__ = __name__
    componentType = HeaderField()
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


class SecureHeaderFields(univ.Set):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('canonAlgorithm', Algorithm()), namedtype.NamedType('secHeaderFields', HeaderFields()))


id_aa = univ.ObjectIdentifier((1, 2, 840, 113549, 1, 9, 16, 2))
id_aa_secureHeaderFieldsIdentifier = id_aa + (55, )
_cmsAttributesMapUpdate = {id_aa_secureHeaderFieldsIdentifier: SecureHeaderFields()}
rfc5652.cmsAttributesMap.update(_cmsAttributesMapUpdate)