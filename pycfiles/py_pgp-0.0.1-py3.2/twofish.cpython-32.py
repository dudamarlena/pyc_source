# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/cipher/twofish.py
# Compiled at: 2015-08-31 08:17:33
from __future__ import absolute_import
from Crypto.Cipher import blockalgo
import twofish as twofish_impl
from pgp.cipher.base import _InternalObj
__all__ = [
 'TwofishCipher', 'new', 'MODE_CBC', 'MODE_CFB', 'MODE_CTR', 'MODE_EAX',
 'MODE_ECB', 'MODE_OFB', 'MODE_OPENPGP', 'MODE_PGP']

class _TwofishObj(_InternalObj):

    @classmethod
    def _create_impl(cls, key):
        return twofish_impl.Twofish(bytes(key))

    block_size = 16
    key_size = (16, 24, 32)


class TwofishCipher(blockalgo.BlockAlgo):

    def __init__(self, key, *args, **kwargs):
        blockalgo.BlockAlgo.__init__(self, _TwofishObj, key, *args, **kwargs)


def new(key, *args, **kwargs):
    """Create a new Twofish cipher

    :Parameters:
      key : byte string
        The secret key to use in the symmetric cipher.
        Its length may vary from 5 to 16 bytes.
    :Keywords:
      mode : a *MODE_** constant
        The chaining mode to use for encryption or decryption.
        Default is `MODE_ECB`.
      IV : byte string
        (*Only* `MODE_CBC`, `MODE_CFB`, `MODE_OFB`, `MODE_OPENPGP`).

        The initialization vector to use for encryption or decryption.

        It is ignored for `MODE_ECB` and `MODE_CTR`.

        For `MODE_OPENPGP`, IV must be `block_size` bytes long for
        encryption and `block_size` +2 bytes for decryption (in the
        latter case, it is actually the *encrypted* IV which was
        prefixed to the ciphertext). It is mandatory.

        For all other modes, it must be 8 bytes long.
      nonce : byte string
        (*Only* `MODE_EAX`).
        A mandatory value that must never be reused for any other
        encryption. There are no restrictions on its length, but it is
        recommended to use at least 16 bytes.
      counter : callable
        (*Only* `MODE_CTR`). A stateful function that returns the next
        *counter block*, which is a byte string of `block_size` bytes.
        For better performance, use `Crypto.Util.Counter`.
      mac_len : integer
        (*Only* `MODE_EAX`). Length of the MAC, in bytes.
        It must be no larger than 8 (which is the default).
      segment_size : integer
        (*Only* `MODE_CFB`).The number of bits the plaintext and
        ciphertext are segmented in.
        It must be a multiple of 8. If 0 or not specified, it will be
        assumed to be 8.

    :Return: an `TwofishCipher` object
    """
    return TwofishCipher(key, *args, **kwargs)


MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
MODE_EAX = 9
block_size = _TwofishObj.block_size
key_size = _TwofishObj.key_size