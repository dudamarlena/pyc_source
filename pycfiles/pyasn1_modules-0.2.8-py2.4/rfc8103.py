# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc8103.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import univ

def _OID(*components):
    output = []
    for x in tuple(components):
        if isinstance(x, univ.ObjectIdentifier):
            output.extend(list(x))
        else:
            output.append(int(x))

    return univ.ObjectIdentifier(output)


class AEADChaCha20Poly1305Nonce(univ.OctetString):
    __module__ = __name__


AEADChaCha20Poly1305Nonce.subtypeSpec = constraint.ValueSizeConstraint(12, 12)
id_alg_AEADChaCha20Poly1305 = _OID(1, 2, 840, 113549, 1, 9, 16, 3, 18)