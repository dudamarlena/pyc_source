# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Hash\MD4.py
# Compiled at: 2013-03-13 13:15:35
"""MD4 cryptographic hash algorithm.

MD4 is specified in RFC1320_ and produces the 128 bit digest of a message.

    >>> from Crypto.Hash import MD4
    >>>
    >>> h = MD4.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

MD4 stand for Message Digest version 4, and it was invented by Rivest in 1990.

This algorithm is insecure. Do not use it for new designs.

.. _RFC1320: http://tools.ietf.org/html/rfc1320
"""
_revision__ = '$Id$'
__all__ = [
 'new', 'digest_size', 'MD4Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
import Crypto.Hash._MD4 as _MD4
hashFactory = _MD4

class MD4Hash(HashAlgo):
    """Class that implements an MD4 hash
    
    :undocumented: block_size
    """
    oid = b(b'\x06\x08*\x86H\x86\xf7\r\x02\x04')
    digest_size = 16
    block_size = 64

    def __init__(self, data=None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data=None):
        return MD4Hash(data)


def new(data=None):
    """Return a fresh instance of the hash object.

    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `MD4Hash.update()`.
        Optional.

    :Return: A `MD4Hash` object
    """
    return MD4Hash().new(data)


digest_size = MD4Hash.digest_size
block_size = MD4Hash.block_size