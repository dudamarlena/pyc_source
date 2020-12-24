# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5915.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import namedval
from pyasn1.type import tag
from pyasn1.type import univ
from pyasn1_modules import rfc5480

class ECPrivateKey(univ.Sequence):
    __module__ = __name__


ECPrivateKey.componentType = namedtype.NamedTypes(namedtype.NamedType('version', univ.Integer(namedValues=namedval.NamedValues(('ecPrivkeyVer1',
                                                                                                                                1)))), namedtype.NamedType('privateKey', univ.OctetString()), namedtype.OptionalNamedType('parameters', rfc5480.ECParameters().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 0))), namedtype.OptionalNamedType('publicKey', univ.BitString().subtype(explicitTag=tag.Tag(tag.tagClassContext, tag.tagFormatSimple, 1))))