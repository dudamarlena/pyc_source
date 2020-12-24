# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip32_key_ser.py
# Compiled at: 2020-04-18 05:28:28
# Size of source mod 2**32: 5007 bytes
from .base58 import Base58Decoder, Base58Encoder
from .bip32_ex import Bip32KeyError

class Bip32KeySerConst:
    __doc__ = ' Class container for BIP32 key serialize constants. '
    EXTENDED_KEY_LEN = 78


class Bip32KeyDeserializer:
    __doc__ = ' BIP32key deserializer class. It deserializes a key. '

    def __init__(self, key_str):
        """ Construct class.

        Args:
            key_str (str): Serialized key string
        """
        self.m_key_str = key_str
        self.m_depth = 0
        self.m_fprint = b''
        self.m_index = 0
        self.m_chain = b''
        self.m_secret = b''
        self.m_is_public = False

    def DeserializeKey(self, key_net_ver):
        """ Deserialize a key.

        Args:
            key_net_ver (KeyNetVersions object): Key net versions object
        """
        key_bytes = Base58Decoder.CheckDecode(self.m_key_str)
        if len(key_bytes) != Bip32KeySerConst.EXTENDED_KEY_LEN:
            raise Bip32KeyError('Invalid extended key (wrong length)')
        elif key_bytes[:4] == key_net_ver.Public():
            self.m_is_public = True
        else:
            if key_bytes[:4] == key_net_ver.Private():
                self.m_is_public = False
            else:
                raise Bip32KeyError('Invalid extended key (wrong net version)')
        self.m_depth = key_bytes[4]
        self.m_fprint = key_bytes[5:9]
        self.m_index = int.from_bytes(key_bytes[9:13], 'big')
        self.m_chain = key_bytes[13:45]
        self.m_secret = key_bytes[45:78]

    def GetKeyParts(self):
        """ Get deserialized key parts.

        Returns:
            tuple: Deserialized key parts
        """
        return (
         self.m_depth, self.m_fprint, self.m_index, self.m_chain, self.m_secret)

    def IsPublic(self):
        """ Get if deserialized key is public.

        Returns:
            bool: True if public, false otherwise
        """
        return self.m_is_public


class Bip32KeySerializer:
    __doc__ = ' BIP32key serializer class. It serializes private/public keys. '

    def __init__(self, bip32_obj):
        """ Construct class.

        Args:
            bip32_obj (Bip32 object): Bip32 object
        """
        self.m_bip32_obj = bip32_obj

    def SerializePublicKey(self):
        """ Serialize the Bip32 object public key.

        Returns:
            bytes: Serialized public key
        """
        return self._Bip32KeySerializer__SerializeKey(self.m_bip32_obj.PublicKey().RawCompressed().ToBytes(), self.m_bip32_obj.KeyNetVersions().Public())

    def SerializePrivateKey(self):
        """ Serialize the Bip32 object private key.

        Returns:
            str: Serialized private key
        """
        return self._Bip32KeySerializer__SerializeKey(b'\x00' + self.m_bip32_obj.PrivateKey().Raw().ToBytes(), self.m_bip32_obj.KeyNetVersions().Private())

    def __SerializeKey(self, key_bytes, key_net_ver):
        """ Serialize the specified key bytes.

        Args:
            key_bytes (bytes)  : Key bytes
            key_net_ver (bytes): Key net version

        Returns:
            str: Serialized key
        """
        depth = self.m_bip32_obj.Depth().to_bytes(1, 'big')
        fprint = self.m_bip32_obj.ParentFingerPrint()
        index = self.m_bip32_obj.Index().to_bytes(4, 'big')
        chain = self.m_bip32_obj.Chain()
        ser_key = key_net_ver + depth + fprint + index + chain + key_bytes
        return Base58Encoder.CheckEncode(ser_key)