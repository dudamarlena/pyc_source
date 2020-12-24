# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/proto/secmod/eso/priv/aes256.py
# Compiled at: 2019-08-18 17:24:05
from pysnmp.proto.secmod.eso.priv import aesbase

class AesBlumenthal256(aesbase.AbstractAesBlumenthal):
    """AES 256 bit encryption (Internet draft)

       http://tools.ietf.org/html/draft-blumenthal-aes-usm-04
    """
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 2)
    keySize = 32


class Aes256(aesbase.AbstractAesReeder):
    """AES 256 bit encryption (Internet draft)

    Reeder AES encryption with non-standard key localization algorithm
    borrowed from Reeder 3DES draft:

    http://tools.ietf.org/html/draft-blumenthal-aes-usm-04
    https://tools.ietf.org/html/draft-reeder-snmpv3-usm-3desede-00

    Known to be used by many vendors including Cisco and others.
    """
    __module__ = __name__
    serviceID = (1, 3, 6, 1, 4, 1, 9, 12, 6, 1, 102)
    keySize = 32