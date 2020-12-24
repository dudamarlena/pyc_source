# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgp/cipher/wrapper.py
# Compiled at: 2015-08-31 08:17:33
from Crypto.Cipher import blockalgo
from pgp.cipher.base import _InternalObj
__all__ = [
 'CipherWrapper', 'new', 'MODE_CBC', 'MODE_CFB', 'MODE_CTR', 'MODE_EAX',
 'MODE_ECB', 'MODE_OFB', 'MODE_OPENPGP', 'MODE_PGP']

class _Wrapped(_InternalObj):
    _cipher = None

    @classmethod
    def _create_impl(cls, key):
        impl = cls._cipher.new(key)
        return impl

    block_size = None
    key_size = None


def wrap(cipher):
    name = 'Wrapped{0}'.format(cipher.__name__.rsplit('.', 1)[(-1)])
    attrs = {'_cipher': cipher, 
     'block_size': cipher.block_size, 
     'key_size': cipher.key_size}
    return type(name, (_Wrapped,), attrs)


class CipherWrapper(blockalgo.BlockAlgo):

    def __init__(self, cipher, key, *args, **kwargs):
        Wrapped = wrap(cipher)
        blockalgo.BlockAlgo.__init__(self, Wrapped, key, *args, **kwargs)


def new(cipher, key, *args, **kwargs):
    """Create a new wrapped PyCrypto cipher

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

    :Return: an `CipherWrapper` object
    """
    return CipherWrapper(cipher, key, *args, **kwargs)


MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7
MODE_EAX = 9