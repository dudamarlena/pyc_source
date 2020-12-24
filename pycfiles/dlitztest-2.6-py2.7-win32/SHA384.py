# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Hash\SHA384.py
# Compiled at: 2013-03-13 13:15:35
"""SHA-384 cryptographic hash algorithm.

SHA-384 belongs to the SHA-2_ family of cryptographic hashes.
It produces the 384 bit digest of a message.

    >>> from Crypto.Hash import SHA384
    >>>
    >>> h = SHA384.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

*SHA* stands for Secure Hash Algorithm.

.. _SHA-2: http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf
"""
_revision__ = '$Id$'
__all__ = [
 'new', 'digest_size', 'SHA384Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
try:
    import hashlib
    hashFactory = hashlib.sha384
except ImportError:
    from Crypto.Hash import _SHA384
    hashFactory = _SHA384

class SHA384Hash(HashAlgo):
    """Class that implements a SHA-384 hash
    
    :undocumented: block_size
    """
    oid = b(b'\x06\t`\x86H\x01e\x03\x04\x02\x02')
    digest_size = 48
    block_size = 128

    def __init__(self, data=None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data=None):
        return SHA384Hash(data)


def new(data=None):
    """Return a fresh instance of the hash object.

    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `SHA384Hash.update()`.
        Optional.

    :Return: A `SHA384Hash` object
    """
    return SHA384Hash().new(data)


digest_size = SHA384Hash.digest_size
block_size = SHA384Hash.block_size