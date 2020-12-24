# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8649.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5280
id_ce_hashOfRootKey = univ.ObjectIdentifier('1.3.6.1.4.1.51483.2.1')

class HashedRootKey(univ.Sequence):
    __module__ = __name__


HashedRootKey.componentType = namedtype.NamedTypes(namedtype.NamedType('hashAlg', rfc5280.AlgorithmIdentifier()), namedtype.NamedType('hashValue', univ.OctetString()))
_certificateExtensionsMapUpdate = {id_ce_hashOfRootKey: HashedRootKey()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)