# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc4043.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5280
id_pkix = univ.ObjectIdentifier((1, 3, 6, 1, 5, 5, 7))
id_on = id_pkix + (8, )
id_on_permanentIdentifier = id_on + (3, )

class PermanentIdentifier(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.OptionalNamedType('identifierValue', char.UTF8String()), namedtype.OptionalNamedType('assigner', univ.ObjectIdentifier()))


_anotherNameMapUpdate = {id_on_permanentIdentifier: PermanentIdentifier()}
rfc5280.anotherNameMap.update(_anotherNameMapUpdate)