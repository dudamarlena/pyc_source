# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/Ari/src/callisto-core/callisto_core/delivery/security.py
# Compiled at: 2019-08-07 16:42:06
# Size of source mod 2**32: 2400 bytes
import nacl.secret, nacl.utils
from django.conf import settings

def encrypt_text(key, sensitive_text):
    """
    Encrypts a report using the given secret key.
    Requires a stretched key with a length of 32 bytes.
    The encryption uses PyNacl & Salsa20 stream cipher.

    Returns:
      bytes: the encrypted bytes of the sensitive_text

    """
    box = nacl.secret.SecretBox(key)
    message = sensitive_text.encode('utf-8')
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    return box.encrypt(message, nonce)


def decrypt_text(key, encrypted_text):
    """Decrypts an encrypted report.

    Returns:
      str: the decrypted encrypted_text as a string

    Raises:
      CryptoError: In case of a failure to decrypt the encrypted_text

    """
    box = nacl.secret.SecretBox(key)
    decrypted = box.decrypt(bytes(encrypted_text)).decode('utf-8')
    return decrypted


def pepper(encrypted_report):
    """
    Uses a secret value stored on the server to encrypt
    an already encrypted report, to add protection if the database
    is breached but the server is not.

    Requires settings.PEPPER to be set to a 32 byte value.
    In production, this value should be set via environment parameter.
    Uses PyNacl's Salsa20 stream cipher.

    Args:
      encrypted_report (bytes): the encrypted report

    Returns:
      bytes: a further encrypted report

    """
    pepper = settings.PEPPER
    box = nacl.secret.SecretBox(pepper)
    nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
    return box.encrypt(encrypted_report, nonce)


def unpepper(peppered_report):
    """
    Decrypts a report that has been peppered with the _pepper method.
    Requires settings.PEPPER to be set to a 32 byte value.
    In production, this value should be set via environment parameter.

    Args:
      peppered_report(bytes): a report that has been encrypted
        using a secret key then encrypted using the pepper

    Returns:
      bytes: the report, still encrypted with the secret key

    Raises:
      CryptoError: If the pepper fails to decrypt the record.
    """
    pepper = settings.PEPPER
    box = nacl.secret.SecretBox(pepper)
    decrypted = box.decrypt(bytes(peppered_report))
    return decrypted