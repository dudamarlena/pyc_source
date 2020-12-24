# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/lib/crypto/base.py
# Compiled at: 2016-07-24 13:14:38
import base64, string, random, struct, socket, six
from Crypto.Cipher import AES
from wechat_sdk.lib.crypto.pkcs7 import PKCS7Encoder
from wechat_sdk.lib.crypto.exceptions import EncryptAESError, DecryptAESError, IllegalBuffer, ValidateAppIDError
from wechat_sdk.utils import to_text, to_binary

class BaseCrypto(object):
    """提供接收和推送给公众平台消息的加解密接口"""

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self, text, appid):
        u"""对明文进行加密

        @param text: 需要加密的明文
        @return: 加密得到的字符串
        """
        text = self.get_random_str() + struct.pack('I', socket.htonl(len(text))) + to_binary(text) + appid
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        try:
            ciphertext = cryptor.encrypt(text)
            return base64.b64encode(ciphertext)
        except Exception as e:
            raise EncryptAESError(e)

    def decrypt(self, text, appid):
        u"""对解密后的明文进行补位删除

        @param text: 密文
        @return: 删除填充补位后的明文
        """
        try:
            cryptor = AES.new(self.key, self.mode, self.key[:16])
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception as e:
            raise DecryptAESError(e)

        try:
            if six.PY2:
                pad = ord(plain_text[(-1)])
            else:
                pad = plain_text[(-1)]
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack('I', content[:4])[0])
            xml_content = content[4:xml_len + 4]
            from_appid = content[xml_len + 4:]
        except Exception as e:
            raise IllegalBuffer(e)

        if from_appid != appid:
            raise ValidateAppIDError()
        return xml_content

    def get_random_str(self):
        u""" 随机生成16位字符串

        @return: 16位字符串
        """
        rule = string.letters + string.digits
        return ('').join(random.sample(rule, 16))