# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/lib/crypto/pkcs7.py
# Compiled at: 2016-04-12 23:03:20
from wechat_sdk.utils import to_binary, to_text

class PKCS7Encoder(object):
    """提供基于PKCS7算法的加解密接口"""
    block_size = 32

    @classmethod
    def encode(cls, text):
        u"""
        对需要加密的明文进行填充补位
        @param text: 需要进行填充补位操作的明文
        @return: 补齐明文字符串
        """
        text_length = len(text)
        amount_to_pad = cls.block_size - text_length % cls.block_size
        if amount_to_pad == 0:
            amount_to_pad = cls.block_size
        pad = to_binary(chr(amount_to_pad))
        return text + pad * amount_to_pad

    @classmethod
    def decode(cls, decrypted):
        u"""
        删除解密后明文的补位字符
        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        pad = ord(decrypted[(-1)])
        if pad < 1 or pad > 32:
            pad = 0
        return decrypted[:-pad]