# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc7773.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5280
MAX = float('inf')
e_legnamnden = univ.ObjectIdentifier('1.2.752.201')
id_eleg_ce = e_legnamnden + (5, )
id_ce_authContext = id_eleg_ce + (1, )

class AuthenticationContext(univ.Sequence):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('contextType', char.UTF8String()), namedtype.OptionalNamedType('contextInfo', char.UTF8String()))


class AuthenticationContexts(univ.SequenceOf):
    __module__ = __name__
    componentType = AuthenticationContext()
    subtypeSpec = constraint.ValueSizeConstraint(1, MAX)


_certificateExtensionsMapUpdate = {id_ce_authContext: AuthenticationContexts()}
rfc5280.certificateExtensionsMap.update(_certificateExtensionsMapUpdate)