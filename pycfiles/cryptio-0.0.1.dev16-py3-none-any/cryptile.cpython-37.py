# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cryptiles/cryptile.py
# Compiled at: 2019-04-06 11:22:41
# Size of source mod 2**32: 538 bytes
from Crypto.Cipher import XOR
import base64

class crypt_data(object):

    def __init__(self, _key):
        """Init self.key like XOR object."""
        self.key = _key

    def encrypt(self, _text):
        """Return encrypted text."""
        cipher = XOR.new(self.key)
        return base64.b64encode(cipher.encrypt(_text))

    def decrypt(self, _text):
        """Return decrypted text."""
        cipher = XOR.new(self.key)
        return cipher.decrypt(base64.b64decode(_text))