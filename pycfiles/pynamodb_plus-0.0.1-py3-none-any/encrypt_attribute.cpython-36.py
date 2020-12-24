# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pynamodb_mate-project/pynamodb_mate/encrypt_attribute.py
# Compiled at: 2020-03-04 19:15:27
# Size of source mod 2**32: 1563 bytes
__doc__ = '\nImplement Client Side Encryption Attribute for Unicode, Binary, Numbers and\nJson data.\n'
from json import loads as json_loads, dumps as json_dumps
from pynamodb.attributes import UnicodeAttribute, BinaryAttribute
from windtalker import SymmetricCipher

class SymmetricEncryptedAttribute(object):
    encrypt_key = None
    _cipher = None

    def get_cipher(self):
        """
        :rtype: SymmtricCipher
        """
        if self._cipher is None:
            if self.encrypt_key:
                self._cipher = SymmetricCipher(password=(self.encrypt_key))
            else:
                raise Exception
        return self._cipher


class EncryptUnicodeAttribute(UnicodeAttribute, SymmetricEncryptedAttribute):

    def serialize(self, value):
        return self.get_cipher().encrypt_text(value)

    def deserialize(self, value):
        return self.get_cipher().decrypt_text(value)


class EncryptBinaryAttribute(BinaryAttribute, SymmetricEncryptedAttribute):

    def serialize(self, value):
        return self.get_cipher().encrypt_binary(value)

    def deserialize(self, value):
        return self.get_cipher().decrypt_binary(value)


class EncryptedNumberAttribute(UnicodeAttribute, SymmetricEncryptedAttribute):

    def serialize(self, value):
        return self.get_cipher().encrypt_text(json_dumps(value))

    def deserialize(self, value):
        return json_loads(self.get_cipher().decrypt_text(value))


class EncryptedJsonAttribute(EncryptedNumberAttribute):
    pass