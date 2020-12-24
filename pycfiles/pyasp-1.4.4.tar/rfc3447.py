# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3447.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedval
from pyasn1_modules.rfc2437 import *

class OtherPrimeInfo(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('prime', univ.Integer()), namedtype.NamedType('exponent', univ.Integer()), namedtype.NamedType('coefficient', univ.Integer()))


class OtherPrimeInfos(univ.SequenceOf):
    __module__ = __name__
    componentType = OtherPrimeInfo()
    sizeSpec = univ.SequenceOf.sizeSpec + constraint.ValueSizeConstraint(1, MAX)


class RSAPrivateKey(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('two-prime',
                                                                                                                       0), ('multi',
                                                                                                                            1)))), namedtype.NamedType('modulus', univ.Integer()), namedtype.NamedType('publicExponent', univ.Integer()), namedtype.NamedType('privateExponent', univ.Integer()), namedtype.NamedType('prime1', univ.Integer()), namedtype.NamedType('prime2', univ.Integer()), namedtype.NamedType('exponent1', univ.Integer()), namedtype.NamedType('exponent2', univ.Integer()), namedtype.NamedType('coefficient', univ.Integer()), namedtype.OptionalNamedType('otherPrimeInfos', OtherPrimeInfos()))