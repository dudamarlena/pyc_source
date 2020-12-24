# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7914.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
id_scrypt = univ.ObjectIdentifier('1.3.6.1.4.1.11591.4.11')

class Scrypt_params(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('salt', univ.OctetString()), namedtype.NamedType('costParameter', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX))), namedtype.NamedType('blockSize', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX))), namedtype.NamedType('parallelizationParameter', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX))), namedtype.OptionalNamedType('keyLength', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, MAX))))


_algorithmIdentifierMapUpdate = {id_scrypt: Scrypt_params()}
rfc5280.algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)