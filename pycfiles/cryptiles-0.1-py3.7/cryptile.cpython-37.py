# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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