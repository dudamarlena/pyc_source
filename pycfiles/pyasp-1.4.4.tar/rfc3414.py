# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3414.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ

class UsmSecurityParameters(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('msgAuthoritativeEngineID', univ.OctetString()), namedtype.NamedType('msgAuthoritativeEngineBoots', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 2147483647))), namedtype.NamedType('msgAuthoritativeEngineTime', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 2147483647))), namedtype.NamedType('msgUserName', univ.OctetString().subtype(subtypeSpec=constraint.ValueSizeConstraint(0, 32))), namedtype.NamedType('msgAuthenticationParameters', univ.OctetString()), namedtype.NamedType('msgPrivacyParameters', univ.OctetString()))