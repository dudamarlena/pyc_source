# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/Crypto.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 942 bytes
import cryptography.hazmat.primitives as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import cryptography.hazmat.backends.openssl.backend as openssl_backend

def generate_ssh_key(passphrase=None, key_size=4096):
    key = rsa.generate_private_key(backend=openssl_backend,
      public_exponent=65537,
      key_size=key_size)
    encryption = crypto_serialization.BestAvailableEncryption(passphrase.encode('utf-8')) if passphrase else crypto_serialization.NoEncryption()
    private_key = key.private_bytes(crypto_serialization.Encoding.PEM, crypto_serialization.PrivateFormat.PKCS8, encryption)
    public_key = key.public_key().public_bytes(crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH)
    return (
     public_key.decode('utf-8'), private_key.decode('utf-8'))