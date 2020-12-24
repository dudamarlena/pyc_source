# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/windtalker-project/windtalker/symmetric.py
# Compiled at: 2020-03-04 18:00:49
# Size of source mod 2**32: 3342 bytes
from __future__ import print_function, unicode_literals
import base64
from cryptography.fernet import Fernet
from pathlib_mate import Path
from . import fingerprint
from . import py23
from .cipher import BaseCipher
from .exc import PasswordError
if py23.is_py2:
    input = raw_input
HOME_DIR = Path.home()
WINDTALKER_CONFIG_FILE = Path(HOME_DIR, '.windtalker')

def read_windtalker_password():
    return WINDTALKER_CONFIG_FILE.read_text(encoding='utf-8').strip()


class SymmetricCipher(BaseCipher):
    __doc__ = '\n    A symmetric encryption algorithm utility class helps you easily\n    encrypt/decrypt text, files and even a directory.\n\n    :param password: The secret password you use to encrypt all your message.\n      If you feel uncomfortable to put that in your code, you can leave it\n      empty. The system will ask you manually enter that later.\n\n    **中文文档**\n\n    对称加密器。\n    '
    _encrypt_chunk_size = 1048576
    _decrypt_chunk_size = 1398200

    def __init__(self, password=None):
        if password:
            fernet_key = self.any_text_to_fernet_key(password)
            self.fernet = Fernet(fernet_key)
        else:
            if WINDTALKER_CONFIG_FILE.exists():
                self.set_password(read_windtalker_password())
            else:
                self.input_password()

    def any_text_to_fernet_key(self, text):
        """
        Convert any text to a fernet key for encryption.

        :type text: str
        :rtype: bytes
        """
        md5 = fingerprint.fingerprint.of_text(text)
        fernet_key = base64.b64encode(md5.encode('utf-8'))
        return fernet_key

    def input_password(self):
        """
        Manually enter a password for encryption on keyboard.
        """
        password = input('Please enter your secret key (case sensitive): ')
        self.set_password(password)

    def set_password(self, password):
        """
        Set a new password for encryption.
        """
        self.__init__(password=password)

    def set_encrypt_chunk_size(self, size):
        if 1048576 < size < 104857600:
            self._encrypt_chunk_size = size
            self._decrypt_chunk_size = len(self.encrypt(b'x' * size))
        else:
            print('encrypt chunk size has to be between 1MB and 100MB')

    @property
    def metadata(self):
        return {'_encrypt_chunk_size':self._encrypt_chunk_size, 
         '_decrypt_chunk_size':self._decrypt_chunk_size}

    def encrypt(self, binary, *args, **kwargs):
        """
        Encrypt binary data.

        :type binary: bytes
        :rtype: bytes
        """
        return self.fernet.encrypt(binary)

    def decrypt(self, binary, *args, **kwargs):
        """
        Decrypt binary data.

        :type binary: bytes
        :rtype: bytes
        """
        try:
            return self.fernet.decrypt(binary)
        except:
            raise PasswordError('Opps, wrong magic word!')