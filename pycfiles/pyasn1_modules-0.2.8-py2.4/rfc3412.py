# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3412.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc1905

class ScopedPDU(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('contextEngineId', univ.OctetString()), namedtype.NamedType('contextName', univ.OctetString()), namedtype.NamedType('data', rfc1905.PDUs()))


class ScopedPduData(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('plaintext', ScopedPDU()), namedtype.NamedType('encryptedPDU', univ.OctetString()))


class HeaderData(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('msgID', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 2147483647))), namedtype.NamedType('msgMaxSize', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(484, 2147483647))), namedtype.NamedType('msgFlags', univ.OctetString().subtype(subtypeSpec=constraint.ValueSizeConstraint(1, 1))), namedtype.NamedType('msgSecurityModel', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, 2147483647))))


class SNMPv3Message(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('msgVersion', univ.Integer().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 2147483647))), namedtype.NamedType('msgGlobalData', HeaderData()), namedtype.NamedType('msgSecurityParameters', univ.OctetString()), namedtype.NamedType('msgData', ScopedPduData()))