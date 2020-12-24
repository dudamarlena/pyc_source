# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/rfc1901.py
# Compiled at: 2019-08-18 17:24:05
from pyasn1.type import univ, namedtype, namedval
from pysnmp.proto import rfc1905
version = univ.Integer(namedValues=namedval.NamedValues(('version-2c', 1)))

class Message(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('version', version), namedtype.NamedType('community', univ.OctetString()), namedtype.NamedType('data', rfc1905.PDUs()))