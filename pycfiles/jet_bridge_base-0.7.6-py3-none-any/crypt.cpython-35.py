# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/crypt.py
# Compiled at: 2020-03-04 16:40:12
# Size of source mod 2**32: 766 bytes
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
backend = default_backend()

def decrypt(message_encrypted, secret_key):
    message_salt = message_encrypted[-24:]
    message_payload = message_encrypted[:-24]
    salt = base64.b64decode(message_salt)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=backend)
    key = base64.urlsafe_b64encode(kdf.derive(bytes(secret_key, encoding='utf8')))
    f = Fernet(key)
    return f.decrypt(bytes(message_payload, encoding='latin1')).decode('utf8')