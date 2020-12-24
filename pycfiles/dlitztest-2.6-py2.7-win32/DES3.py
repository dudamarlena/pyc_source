# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Cipher\DES3.py
# Compiled at: 2013-03-14 04:43:25
"""Triple DES symmetric cipher

`Triple DES`__ (or TDES or TDEA or 3DES) is a symmetric block cipher standardized by NIST_.
It has a fixed data block size of 8 bytes. Its keys are 128 (*Option 1*) or 192
bits (*Option 2*) long.
However, 1 out of 8 bits is used for redundancy and do not contribute to
security. The effective key length is respectively 112 or 168 bits.

TDES consists of the concatenation of 3 simple `DES` ciphers.

The plaintext is first DES encrypted with *K1*, then decrypted with *K2*,
and finally encrypted again with *K3*.  The ciphertext is decrypted in the reverse manner.

The 192 bit key is a bundle of three 64 bit independent subkeys: *K1*, *K2*, and *K3*.

The 128 bit key is split into *K1* and *K2*, whereas *K1=K3*.

It is important that all subkeys are different, otherwise TDES would degrade to
single `DES`.

TDES is cryptographically secure, even though it is neither as secure nor as fast
as `AES`.

As an example, encryption can be done as follows:

    >>> from Crypto.Cipher import DES3
    >>> from Crypto import Random
    >>> from Crypto.Util import Counter
    >>>
    >>> key = b'Sixteen byte key'
    >>> nonce = Random.new().read(DES3.block_size/2)
    >>> ctr = Counter.new(DES3.block_size*8/2, prefix=nonce)
    >>> cipher = DES3.new(key, DES3.MODE_CTR, counter=ctr)
    >>> plaintext = b'We are no longer the knights who say ni!'
    >>> msg = nonce + cipher.encrypt(plaintext)

.. __: http://en.wikipedia.org/wiki/Triple_DES
.. _NIST: http://csrc.nist.gov/publications/nistpubs/800-67/SP800-67.pdf

:undocumented: __revision__, __package__
"""
__revision__ = '$Id$'
from Crypto.Cipher import blockalgo
from Crypto.Cipher import _DES3

class DES3Cipher(blockalgo.BlockAlgo):
    """TDES cipher object"""

    def __init__(self, key, *args, **kwargs):
        """Initialize a TDES cipher object
        
        See also `new()` at the module level."""
        blockalgo.BlockAlgo.__init__(self, _DES3, key, *args, **kwargs)


def new(key, *args, **kwargs):
    """Create a new TDES cipher

    :Parameters:
      key : byte string
        The secret key to use in the symmetric cipher.
        It must be 16 or 24 bytes long. The parity bits will be ignored.
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

    :Attention: it is important that all 8 byte subkeys are different,
      otherwise TDES would degrade to single `DES`.
    :Return: an `DES3Cipher` object
    """
    return DES3Cipher(key, *args, **kwargs)


MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
block_size = 8
key_size = (16, 24)