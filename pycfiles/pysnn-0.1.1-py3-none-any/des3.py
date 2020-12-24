# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmpcrypto/des3.py
# Compiled at: 2018-02-18 18:45:55
__doc__ = '\nCrypto logic for Reeder 3DES-EDE for USM (Internet draft).\n\nhttps://tools.ietf.org/html/draft-reeder-snmpv3-usm-3desede-00\n'
from pysnmpcrypto import backend, CRYPTODOME, CRYPTOGRAPHY, generic_decrypt, generic_encrypt
if backend == CRYPTOGRAPHY:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
elif backend == CRYPTODOME:
    from Cryptodome.Cipher import DES3

def _cryptodome_cipher(key, iv):
    """Build a Pycryptodome DES3 Cipher object.

    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: DES3 Cipher instance
    """
    return DES3.new(key, DES3.MODE_CBC, iv)


def _cryptography_cipher(key, iv):
    """Build a cryptography TripleDES Cipher object.

    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: TripleDES Cipher instance
    :rtype: cryptography.hazmat.primitives.ciphers.Cipher
    """
    return Cipher(algorithm=algorithms.TripleDES(key), mode=modes.CBC(iv), backend=default_backend())


_CIPHER_FACTORY_MAP = {CRYPTOGRAPHY: _cryptography_cipher, CRYPTODOME: _cryptodome_cipher}

def encrypt(plaintext, key, iv):
    """Encrypt data using triple DES on the available backend.

    :param bytes plaintext: Plaintext data to encrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Encrypted ciphertext
    :rtype: bytes
    """
    return generic_encrypt(_CIPHER_FACTORY_MAP, plaintext, key, iv)


def decrypt(ciphertext, key, iv):
    """Decrypt data using triple DES on the available backend.

    :param bytes ciphertext: Ciphertext data to decrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Decrypted plaintext
    :rtype: bytes
    """
    return generic_decrypt(_CIPHER_FACTORY_MAP, ciphertext, key, iv)