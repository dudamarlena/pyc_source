# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/encryption/_nacl.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 3752 bytes
from builtins import str
import nacl
from nacl.secret import SecretBox
overhead = 16 + SecretBox.NONCE_SIZE

def encrypt(message, keyPath):
    """
    Encrypts a message given a path to a local file containing a key.

    :param message: The message to be encrypted.
    :param keyPath: A path to a file containing a 256-bit key (and nothing else).
    :type message: bytes
    :type keyPath: str
    :rtype: bytes

    A constant overhead is added to every encrypted message (for the nonce and MAC).
    >>> import tempfile
    >>> k = tempfile.mktemp()
    >>> with open(k, 'wb') as f:
    ...     _ = f.write(nacl.utils.random(SecretBox.KEY_SIZE))
    >>> message = 'test'.encode('utf-8')
    >>> len(encrypt(message, k)) == overhead + len(message)
    True
    >>> import os
    >>> os.remove(k)
    """
    with open(keyPath, 'rb') as (f):
        key = f.read()
    if len(key) != SecretBox.KEY_SIZE:
        raise ValueError('Key is %d bytes, but must be exactly %d bytes' % (len(key),
         SecretBox.KEY_SIZE))
    else:
        sb = SecretBox(key)
        nonce = nacl.utils.random(SecretBox.NONCE_SIZE)
        assert len(nonce) == SecretBox.NONCE_SIZE
    return bytes(sb.encrypt(message, nonce))


def decrypt(ciphertext, keyPath):
    """
    Decrypts a given message that was encrypted with the encrypt() method.

    :param ciphertext: The encrypted message (as a string).
    :param keyPath: A path to a file containing a 256-bit key (and nothing else).
    :type ciphertext: bytes
    :type keyPath: str
    :rtype: bytes

    Raises an error if ciphertext was modified
    >>> import tempfile
    >>> k = tempfile.mktemp()
    >>> with open(k, 'wb') as f:
    ...     _ = f.write(nacl.utils.random(SecretBox.KEY_SIZE))
    >>> ciphertext = encrypt("testMessage".encode('utf-8'), k)
    >>> ciphertext = b'5' + ciphertext[1:]
    >>> decrypt(ciphertext, k) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    CryptoError: Decryption failed. Ciphertext failed verification

    Otherwise works correctly
    >>> decrypt(encrypt("testMessage".encode('utf-8'), k), k).decode('utf-8') in (u'testMessage', b'testMessage', 'testMessage') # doctest: +ALLOW_UNICODE
    True

    >>> import os
    >>> os.remove(k)
    """
    with open(keyPath, 'rb') as (f):
        key = f.read()
    if len(key) != SecretBox.KEY_SIZE:
        raise ValueError('Key is %d bytes, but must be exactly %d bytes' % (len(key),
         SecretBox.KEY_SIZE))
    sb = SecretBox(key)
    return sb.decrypt(ciphertext)