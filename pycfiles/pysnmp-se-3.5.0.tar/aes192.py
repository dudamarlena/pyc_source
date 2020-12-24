# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/eso/priv/aes192.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto.secmod.eso.priv import aesbase

class AesBlumenthal192(aesbase.AbstractAesBlumenthal):
    """AES 192 bit encryption (Internet draft)

       Reeder AES encryption:

       http://tools.ietf.org/html/draft-blumenthal-aes-usm-04
    """
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 1)
    keySize = 24


class Aes192(aesbase.AbstractAesReeder):
    """AES 192 bit encryption (Internet draft)

    Reeder AES encryption with non-standard key localization algorithm
    borrowed from Reeder 3DES draft:

    http://tools.ietf.org/html/draft-blumenthal-aes-usm-04
    https://tools.ietf.org/html/draft-reeder-snmpv3-usm-3desede-00

    Known to be used by many vendors including Cisco and others.
    """
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 101)
    keySize = 24