# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/catalyze/helpers/AESCrypto.py
# Compiled at: 2015-07-23 11:36:59
import base64, binascii, struct
from Crypto.Cipher import AES

class Decryption(object):
    """
    Base Decryption class
    """

    def __init__(self, filepath, key, iv):
        self.filepath = filepath
        self.key = self.decode(key)
        self.init_vector = self.decode(iv)

    @staticmethod
    def decode(encoded_text):
        """
        Decodes the base64 encoded text.
        """
        return binascii.unhexlify(base64.b64decode(encoded_text))

    def decrypt(self, output_filepath):
        """
        Decrypt the file and write it to the output filepath.
        """
        with open(self.filepath, 'rb') as (enc_file):
            origsize = struct.unpack('<Q', enc_file.read(struct.calcsize('Q')))[0]
            with open(output_filepath, 'wb') as (plain_file):
                cipher = AES.new(self.key, mode=AES.MODE_CBC, IV=self.init_vector)
                chunk_size = 24576
                while True:
                    chunk = enc_file.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    plain_file.write(cipher.decrypt(chunk))

                plain_file.truncate(origsize)