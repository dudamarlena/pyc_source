# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmpcrypto/__init__.py
# Compiled at: 2018-09-08 14:12:42
__version__ = '0.0.4'
CRYPTOGRAPHY = 'cryptography'
CRYPTODOME = 'Cryptodome'
try:
    import cryptography
    backend = CRYPTOGRAPHY
except ImportError:
    try:
        import Cryptodome
        backend = CRYPTODOME
    except ImportError:
        backend = None

class PysnmpCryptoError(Exception):
    """General pysnmpcrypto error"""
    __module__ = __name__


def _cryptodome_encrypt(cipher_factory, plaintext, key, iv):
    """Use a Pycryptodome cipher factory to encrypt data.

    :param cipher_factory: Factory callable that builds a Pycryptodome Cipher instance based
    on the key and IV
    :type cipher_factory: callable
    :param bytes plaintext: Plaintext data to encrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Encrypted ciphertext
    :rtype: bytes
    """
    encryptor = cipher_factory(key, iv)
    return encryptor.encrypt(plaintext)


def _cryptodome_decrypt(cipher_factory, ciphertext, key, iv):
    """Use a Pycryptodome cipher factory to decrypt data.

    :param cipher_factory: Factory callable that builds a Pycryptodome Cipher instance based
    on the key and IV
    :type cipher_factory: callable
    :param bytes ciphertext: Ciphertext data to decrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Decrypted plaintext
    :rtype: bytes
    """
    decryptor = cipher_factory(key, iv)
    return decryptor.decrypt(ciphertext)


def _cryptography_encrypt(cipher_factory, plaintext, key, iv):
    """Use a cryptography cipher factory to encrypt data.

    :param cipher_factory: Factory callable that builds a cryptography Cipher instance based
    on the key and IV
    :type cipher_factory: callable
    :param bytes plaintext: Plaintext data to encrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Encrypted ciphertext
    :rtype: bytes
    """
    encryptor = cipher_factory(key, iv).encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def _cryptography_decrypt(cipher_factory, ciphertext, key, iv):
    """Use a cryptography cipher factory to decrypt data.

    :param cipher_factory: Factory callable that builds a cryptography Cipher instance based
    on the key and IV
    :type cipher_factory: callable
    :param bytes ciphertext: Ciphertext data to decrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Decrypted plaintext
    :rtype: bytes
    """
    decryptor = cipher_factory(key, iv).decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()


_DECRYPT_MAP = {CRYPTOGRAPHY: _cryptography_decrypt, CRYPTODOME: _cryptodome_decrypt}
_ENCRYPT_MAP = {CRYPTOGRAPHY: _cryptography_encrypt, CRYPTODOME: _cryptodome_encrypt}

def generic_encrypt(cipher_factory_map, plaintext, key, iv):
    """Encrypt data using the available backend.

    :param dict cipher_factory_map: Dictionary that maps the backend name to a cipher factory
    callable for that backend
    :param bytes plaintext: Plaintext data to encrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Encrypted ciphertext
    :rtype: bytes
    """
    if backend is None:
        raise PysnmpCryptoError('Crypto backend not available')
    return _ENCRYPT_MAP[backend](cipher_factory_map[backend], plaintext, key, iv)


def generic_decrypt(cipher_factory_map, ciphertext, key, iv):
    """Decrypt data using the available backend.

    :param dict cipher_factory_map: Dictionary that maps the backend name to a cipher factory
    callable for that backend
    :param bytes ciphertext: Ciphertext data to decrypt
    :param bytes key: Encryption key
    :param bytes IV: Initialization vector
    :returns: Decrypted plaintext
    :rtype: bytes
    """
    if backend is None:
        raise PysnmpCryptoError('Crypto backend not available')
    return _DECRYPT_MAP[backend](cipher_factory_map[backend], ciphertext, key, iv)