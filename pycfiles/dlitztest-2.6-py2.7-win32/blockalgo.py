# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\Cipher\blockalgo.py
# Compiled at: 2013-03-13 13:15:35
"""Module with definitions common to all block ciphers."""
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from Crypto.Util.py21compat import *
from Crypto.Util.py3compat import *
MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_PGP = 4
MODE_OFB = 5
MODE_CTR = 6
MODE_OPENPGP = 7

def _getParameter(name, index, args, kwargs, default=None):
    """Find a parameter in tuple and dictionary arguments a function receives"""
    param = kwargs.get(name)
    if len(args) > index:
        if param:
            raise ValueError("Parameter '%s' is specified twice" % name)
        param = args[index]
    return param or default


class BlockAlgo:
    """Class modelling an abstract block cipher."""

    def __init__(self, factory, key, *args, **kwargs):
        self.mode = _getParameter('mode', 0, args, kwargs, default=MODE_ECB)
        self.block_size = factory.block_size
        if self.mode != MODE_OPENPGP:
            self._cipher = factory.new(key, *args, **kwargs)
            self.IV = self._cipher.IV
        else:
            self._done_first_block = False
            self._done_last_block = False
            self.IV = _getParameter('iv', 1, args, kwargs)
            if not self.IV:
                raise ValueError('MODE_OPENPGP requires an IV')
            IV_cipher = factory.new(key, MODE_CFB, b('\x00') * self.block_size, segment_size=self.block_size * 8)
            if len(self.IV) == self.block_size:
                self._encrypted_IV = IV_cipher.encrypt(self.IV + self.IV[-2:] + b('\x00') * (self.block_size - 2))[:self.block_size + 2]
            elif len(self.IV) == self.block_size + 2:
                self._encrypted_IV = self.IV
                self.IV = IV_cipher.decrypt(self.IV + b('\x00') * (self.block_size - 2))[:self.block_size + 2]
                if self.IV[-2:] != self.IV[-4:-2]:
                    raise ValueError('Failed integrity check for OPENPGP IV')
                self.IV = self.IV[:-2]
            else:
                raise ValueError('Length of IV must be %d or %d bytes for MODE_OPENPGP' % (
                 self.block_size, self.block_size + 2))
            self._cipher = factory.new(key, MODE_CFB, self._encrypted_IV[-self.block_size:], segment_size=self.block_size * 8)

    def encrypt(self, plaintext):
        """Encrypt data with the key and the parameters set at initialization.
        
        The cipher object is stateful; encryption of a long block
        of data can be broken up in two or more calls to `encrypt()`.
        That is, the statement:
            
            >>> c.encrypt(a) + c.encrypt(b)

        is always equivalent to:

             >>> c.encrypt(a+b)

        That also means that you cannot reuse an object for encrypting
        or decrypting other data with the same key.

        This function does not perform any padding.
       
         - For `MODE_ECB`, `MODE_CBC`, and `MODE_OFB`, *plaintext* length
           (in bytes) must be a multiple of *block_size*.

         - For `MODE_CFB`, *plaintext* length (in bytes) must be a multiple
           of *segment_size*/8.

         - For `MODE_CTR`, *plaintext* can be of any length.

         - For `MODE_OPENPGP`, *plaintext* must be a multiple of *block_size*,
           unless it is the last chunk of the message.

        :Parameters:
          plaintext : byte string
            The piece of data to encrypt.
        :Return:
            the encrypted data, as a byte string. It is as long as
            *plaintext* with one exception: when encrypting the first message
            chunk with `MODE_OPENPGP`, the encypted IV is prepended to the
            returned ciphertext.
        """
        if self.mode == MODE_OPENPGP:
            padding_length = (self.block_size - len(plaintext) % self.block_size) % self.block_size
            if padding_length > 0:
                if self._done_last_block:
                    raise ValueError('Only the last chunk is allowed to have length not multiple of %d bytes', self.block_size)
                self._done_last_block = True
                padded = plaintext + b('\x00') * padding_length
                res = self._cipher.encrypt(padded)[:len(plaintext)]
            else:
                res = self._cipher.encrypt(plaintext)
            if not self._done_first_block:
                res = self._encrypted_IV + res
                self._done_first_block = True
            return res
        return self._cipher.encrypt(plaintext)

    def decrypt(self, ciphertext):
        """Decrypt data with the key and the parameters set at initialization.
        
        The cipher object is stateful; decryption of a long block
        of data can be broken up in two or more calls to `decrypt()`.
        That is, the statement:
            
            >>> c.decrypt(a) + c.decrypt(b)

        is always equivalent to:

             >>> c.decrypt(a+b)

        That also means that you cannot reuse an object for encrypting
        or decrypting other data with the same key.

        This function does not perform any padding.
       
         - For `MODE_ECB`, `MODE_CBC`, and `MODE_OFB`, *ciphertext* length
           (in bytes) must be a multiple of *block_size*.

         - For `MODE_CFB`, *ciphertext* length (in bytes) must be a multiple
           of *segment_size*/8.

         - For `MODE_CTR`, *ciphertext* can be of any length.

         - For `MODE_OPENPGP`, *plaintext* must be a multiple of *block_size*,
           unless it is the last chunk of the message.

        :Parameters:
          ciphertext : byte string
            The piece of data to decrypt.
        :Return: the decrypted data (byte string, as long as *ciphertext*).
        """
        if self.mode == MODE_OPENPGP:
            padding_length = (self.block_size - len(ciphertext) % self.block_size) % self.block_size
            if padding_length > 0:
                if self._done_last_block:
                    raise ValueError('Only the last chunk is allowed to have length not multiple of %d bytes', self.block_size)
                self._done_last_block = True
                padded = ciphertext + b('\x00') * padding_length
                res = self._cipher.decrypt(padded)[:len(ciphertext)]
            else:
                res = self._cipher.decrypt(ciphertext)
            return res
        return self._cipher.decrypt(ciphertext)