# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Cipher\Blowfish.py
# Compiled at: 2013-03-14 04:43:25
"""Blowfish symmetric cipher

Blowfish_ is a symmetric block cipher designed by Bruce Schneier.

It has a fixed data block size of 8 bytes and its keys can vary in length
from 32 to 448 bits (4 to 56 bytes).

Blowfish is deemed secure and it is fast. However, its keys should be chosen
to be big enough to withstand a brute force attack (e.g. at least 16 bytes).

As an example, encryption can be done as follows:

    >>> from Crypto.Cipher import Blowfish
    >>> from Crypto import Random
    >>> from struct import pack
    >>>
    >>> bs = Blowfish.block_size
    >>> key = b'An arbitrarily long key'
    >>> iv = Random.new().read(bs)
    >>> cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    >>> plaintext = b'docendo discimus '
    >>> plen = bs - divmod(len(plaintext),bs)[1]
    >>> padding = [plen]*plen
    >>> padding = pack('b'*plen, *padding)
    >>> msg = iv + cipher.encrypt(plaintext + padding)

.. _Blowfish: http://www.schneier.com/blowfish.html

:undocumented: __revision__, __package__
"""
__revision__ = '$Id$'
from Crypto.Cipher import blockalgo
from Crypto.Cipher import _Blowfish

class BlowfishCipher(blockalgo.BlockAlgo):
    """Blowfish cipher object"""

    def __init__(self, key, *args, **kwargs):
        """Initialize a Blowfish cipher object
        
        See also `new()` at the module level."""
        blockalgo.BlockAlgo.__init__(self, _Blowfish, key, *args, **kwargs)


def new(key, *args, **kwargs):
    """Create a new Blowfish cipher

    :Parameters:
      key : byte string
        The secret key to use in the symmetric cipher.
        Its length can vary from 4 to 56 bytes.
    :Keywords:
      mode : a *MODE_** constant
        The chaining mode to use for encryption or decryption.
        Default is `MODE_ECB`.
      IV : byte string
        The initialization vector to use for encryption or decryption.
        
        It is ignored for `MODE_ECB` and `MODE_CTR`.

        For `MODE_OPENPGP`, IV must be `block_size` bytes long for encryption
        and `block_size` +2 bytes for decryption (in the latter case, it is
        actually the *encrypted* IV which was prefixed to the ciphertext).
        It is mandatory.
       
        For all other modes, it must be `block_size` bytes longs.
      counter : callable
        (*Only* `MODE_CTR`). A stateful function that returns the next
        *counter block*, which is a byte string of `block_size` bytes.
        For better performance, use `Crypto.Util.Counter`.
      segment_size : integer
        (*Only* `MODE_CFB`).The number of bits the plaintext and ciphertext
        are segmented in.
        It must be a multiple of 8. If 0 or not specified, it will be assumed to be 8.

    :Return: a `BlowfishCipher` object
    """
    return BlowfishCipher(key, *args, **kwargs)


MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
block_size = 8
key_size = xrange(4, 57)