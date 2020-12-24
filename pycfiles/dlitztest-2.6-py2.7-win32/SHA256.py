# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Hash\SHA256.py
# Compiled at: 2013-03-13 13:15:35
"""SHA-256 cryptographic hash algorithm.

SHA-256 belongs to the SHA-2_ family of cryptographic hashes.
It produces the 256 bit digest of a message.

    >>> from Crypto.Hash import SHA256
    >>>
    >>> h = SHA256.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

*SHA* stands for Secure Hash Algorithm.

.. _SHA-2: http://csrc.nist.gov/publications/fips/fips180-2/fips180-2.pdf
"""
_revision__ = '$Id$'
__all__ = [
 'new', 'digest_size', 'SHA256Hash']
from Crypto.Util.py3compat import *
from Crypto.Hash.hashalgo import HashAlgo
try:
    import hashlib
    hashFactory = hashlib.sha256
except ImportError:
    from Crypto.Hash import _SHA256
    hashFactory = _SHA256

class SHA256Hash(HashAlgo):
    """Class that implements a SHA-256 hash
    
    :undocumented: block_size
    """
    oid = b(b'\x06\t`\x86H\x01e\x03\x04\x02\x01')
    digest_size = 32
    block_size = 64

    def __init__(self, data=None):
        HashAlgo.__init__(self, hashFactory, data)

    def new(self, data=None):
        return SHA256Hash(data)


def new(data=None):
    """Return a fresh instance of the hash object.

    :Parameters:
       data : byte string
        The very first chunk of the message to hash.
        It is equivalent to an early call to `SHA256Hash.update()`.
        Optional.

    :Return: A `SHA256Hash` object
    """
    return SHA256Hash().new(data)


digest_size = SHA256Hash.digest_size
block_size = SHA256Hash.block_size