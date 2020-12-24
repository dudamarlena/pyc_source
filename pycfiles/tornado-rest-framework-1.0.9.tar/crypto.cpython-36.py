# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/tornado-rest-framework/rest_framework/core/safe/crypto.py
# Compiled at: 2018-10-24 06:16:23
# Size of source mod 2**32: 4737 bytes
"""
安全加密码工具
"""
import hmac, socket, base64, struct, hashlib, string, binascii
from rest_framework.core.exceptions import IllegalAesKeyError
from rest_framework.utils.transcoder import force_bytes, force_text, str2hex, hex2str
from rest_framework.utils.functional import get_random_string
try:
    from fastpbkdf2 import pbkdf2_hmac
except ImportError:
    from hashlib import pbkdf2_hmac

def constant_time_compare(val1, val2):
    return hmac.compare_digest(force_bytes(val1), force_bytes(val2))


def pbkdf2(password, salt, iterations, dklen=0, digest=None):
    if digest is None:
        digest = hashlib.sha256
    dklen = dklen or None
    password = force_bytes(password)
    salt = force_bytes(salt)
    return pbkdf2_hmac(digest().name, password, salt, iterations, dklen)


def _bin_to_long(x):
    """
    二进制转长整数
    """
    return int(binascii.hexlify(x), 16)


def _long_to_bin(x, hex_format_string):
    """
    长整数转二进制
    """
    return binascii.unhexlify((hex_format_string % x).encode('ascii'))


class ParamError(Exception):
    __doc__ = '\n    参数非法\n    '


class ValidateAppIdError(Exception):
    __doc__ = '\n    非法应用标识\n    '


class PKCS7Encoder(object):
    __doc__ = '\n    提供基于PKCS7算法的加解密接口\n    '
    block_size = 32

    @classmethod
    def encode(cls, text):
        """
        对需要加密的明文进行填充补位
        :param text: 需要进行填充补位操作的明文
        :return: 补齐明文字符串
        """
        text_length = len(text)
        amount_to_pad = cls.block_size - text_length % cls.block_size
        if amount_to_pad == 0:
            amount_to_pad = cls.block_size
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    @classmethod
    def decode(cls, decrypted):
        """
        删除解密后明文的补位字符
        :param decrypted: 解密后的明文
        :return: 删除补位字符后的明文
        """
        pad = ord(decrypted[(-1)])
        if pad < 1 or pad > cls.block_size:
            pad = 0
        return decrypted[:-pad]


pkcs7 = PKCS7Encoder

class MsgCrypt(object):
    __doc__ = '\n    消息的加解密接口\n    '

    def __init__(self, encoding_aec_key):
        """
        :param encoding_aec_key:加密所用的秘钥
        """
        from Crypto.Cipher import AES
        self._MsgCrypt__gen_key(encoding_aec_key)
        self.mode = AES.MODE_CBC

    def __gen_key(self, encoding_aec_key):
        if not isinstance(encoding_aec_key, (bytes, str)):
            raise ValueError('encoding_aec_key type must bytes or str')
        else:
            if isinstance(encoding_aec_key, bytes):
                encoding_aec_key += b'=='
            else:
                encoding_aec_key += '=='
        try:
            self.key = base64.b64decode(encoding_aec_key)
        except:
            raise IllegalAesKeyError('EncodingAESKey Invalid')

    def encrypt(self, text):
        """
        对明文进行加密
        :param text: 需要加密的明文
        :return:
        """
        from Crypto.Cipher import AES
        text = get_random_string(length=16) + force_text(struct.pack('I', socket.htonl(len(text)))) + text
        text = pkcs7.encode(text)
        allowed_chars = string.digits + string.ascii_letters + string.punctuation
        iv = get_random_string(length=16, allowed_chars=allowed_chars)
        cryptor = AES.new(self.key, self.mode, iv)
        cipher_text = cryptor.encrypt(text)
        cipher_text = force_bytes(iv) + cipher_text
        return str2hex(cipher_text)

    def decrypt(self, text):
        """
        对解密后的明文进行补位删除
        :param text: 密文
        :return: 删除填充补位后的明文
        """
        from Crypto.Cipher import AES
        cipher_text = hex2str(text)
        iv = cipher_text[:16]
        cryptor = AES.new(self.key, self.mode, iv)
        plain_text = force_text(cryptor.decrypt(cipher_text[16:])[16:])
        content = pkcs7.decode(plain_text)
        msg_len = socket.ntohl(struct.unpack('I', force_bytes(content[:4]))[0])
        msg_content = content[4:msg_len + 4]
        return msg_content