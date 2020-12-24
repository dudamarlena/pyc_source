# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/site_settings/crypt.py
# Compiled at: 2020-03-30 17:48:04
# Size of source mod 2**32: 2631 bytes
from builtins import str
import base64
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from django.conf import settings

def aes_key_from_conf_key(string):
    return SHA256.new(string).digest()


def aes_key_for_site_settings():
    if len(settings.SITE_SETTINGS_KEY) == 32:
        return settings.SITE_SETTINGS_KEY.encode()
    return aes_key_from_conf_key(settings.SITE_SETTINGS_KEY.encode())


SITE_SETTINGS_AES_KEY = aes_key_for_site_settings()

def encrypt(value):
    """Return the encrypted value of the setting.
    Uses the character '\x00' as padding.
    """
    cipher = AES.new(SITE_SETTINGS_AES_KEY, AES.MODE_ECB)
    value = str(value).encode()
    padding = AES.block_size - len(value) % AES.block_size
    for i in range(padding):
        value += b'\x00'

    ciphertext = cipher.encrypt(value)
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext.decode()


def decrypt(value):
    """Return the decrypted value of the setting.
    This removes the padding character '\x00'
    """
    cipher = AES.new(SITE_SETTINGS_AES_KEY, AES.MODE_ECB)
    value = value.encode()
    value = base64.b64decode(value)
    value = cipher.decrypt(value)
    return value.replace(b'\x00', b'').decode()


def test():
    """Check if original values and decrypted values
    will still be equal to each other.
    """
    from tendenci.apps.site_settings.models import Setting
    s = Setting.objects.all()
    for x in s:
        code = encrypt(x.value)
        decode = decrypt(code)
        if x.value != decode:
            print('not equal!')