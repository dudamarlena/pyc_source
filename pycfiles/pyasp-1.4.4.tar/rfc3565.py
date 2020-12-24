# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc3565.py
# Compiled at: 2019-10-17 01:00:24
from pyasn1.type import constraint
from pyasn1.type import univ
from pyasn1_modules import rfc5280

class AlgorithmIdentifier(rfc5280.AlgorithmIdentifier):
    __module__ = __name__


class AES_IV(univ.OctetString):
    __module__ = __name__


AES_IV.subtypeSpec = constraint.ValueSizeConstraint(16, 16)
id_aes128_CBC = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.2')
id_aes192_CBC = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.22')
id_aes256_CBC = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.42')
id_aes128_wrap = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.5')
id_aes192_wrap = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.25')
id_aes256_wrap = univ.ObjectIdentifier('2.16.840.1.101.3.4.1.45')
_algorithmIdentifierMapUpdate = {id_aes128_CBC: AES_IV(), id_aes192_CBC: AES_IV(), id_aes256_CBC: AES_IV(), id_aes128_wrap: univ.Null(), id_aes192_wrap: univ.Null(), id_aes256_wrap: univ.Null()}
rfc5280.algorithmIdentifierMap.update(_algorithmIdentifierMapUpdate)