# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmpcrypto/aes.py
# Compiled at: 2018-02-18 18:45:55
__doc__ = '\nCrypto logic for RFC3826.\n\nhttps://tools.ietf.org/html/rfc3826\n'
from pysnmpcrypto import backend, CRYPTODOME, CRYPTOGRAPHY, generic_decrypt, generic_encrypt
if backend == CRYPTOGRAPHY:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
elif backend == CRYPTODOME:
    from Cryptodome.Cipher import AES

def _cryptodome_cipher(key, iv):
    """Build a Pycryptodome AES Cipher object.

    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: AES Cipher instance
    """
    return AES.new(key, AES.MODE_CFB, iv, segment_size=128)


def _cryptography_cipher(key, iv):
    """Build a cryptography AES Cipher object.

    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: AES Cipher instance
    :rtype: cryptography.hazmat.primitives.ciphers.Cipher
    """
    return Cipher(algorithm=algorithms.AES(key), mode=modes.CFB(iv), backend=default_backend())


_CIPHER_FACTORY_MAP = {CRYPTOGRAPHY: _cryptography_cipher, CRYPTODOME: _cryptodome_cipher}

def encrypt(plaintext, key, iv):
    """Encrypt data using AES on the available backend.

    :param bytes plaintext: Plaintext data to encrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Encrypted ciphertext
    :rtype: bytes
    """
    return generic_encrypt(_CIPHER_FACTORY_MAP, plaintext, key, iv)


def decrypt(ciphertext, key, iv):
    """Decrypt data using AES on the available backend.

    :param bytes ciphertext: Ciphertext data to decrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Decrypted plaintext
    :rtype: bytes
    """
    return generic_decrypt(_CIPHER_FACTORY_MAP, ciphertext, key, iv)