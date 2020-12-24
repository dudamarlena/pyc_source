# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/windtalker-project/windtalker/asymmetric.py
# Compiled at: 2020-03-04 18:30:56
# Size of source mod 2**32: 3251 bytes
"""
2016年还在由活跃的社区维护的rsa扩展有 ``cryptography`` 和 ``rsa``。 cryp集合了非常
多主流的加密算法, 并且都做了非常多的安全和性能优化(C语言实现)。而rsa是纯Python
实现, 安装非常方便, 使用起来也较为简单。所以本模块最后决定使用rsa进行开发。
"""
from __future__ import print_function, unicode_literals
import rsa
from .cipher import BaseCipher
ERROR_MESSAGE = 'Asymmetric Encryption is for safely transfer secret key only! It is not suitable for file encryption!'

class AsymmetricCipher(BaseCipher):
    __doc__ = "\n    A asymmetric encryption algorithm utility class helps you easily\n    encrypt/decrypt text and files.\n\n    :param my_pubkey: your public key\n    :param my_privkey: your private key\n    :param his_pubkey: other's public key you use to encrypt message\n\n    **中文文档**\n\n    非对称加密器. 主要用于加密少量信息. 通常用于安全地交换秘钥, 然后用该秘钥作为对称加密\n    的钥匙对大量数据进行加密.\n    "
    _encrypt_chunk_size = 53
    _decrypt_chunk_size = 53

    def __init__(self, my_pubkey, my_privkey, his_pubkey):
        self.my_pubkey = my_pubkey
        self.my_privkey = my_privkey
        self.his_pubkey = his_pubkey
        self.sign = None
        self.password = None

    @staticmethod
    def newkeys(nbits=1024):
        """
        Create a new pair of public and private key pair to use.
        """
        pubkey, privkey = rsa.newkeys(nbits, poolsize=1)
        return (pubkey, privkey)

    def encrypt(self, binary, use_sign=True, sign_method='SHA-256', *args, **kwargs):
        """
        Encrypt binary data.

        :param sing_method: one of 'MD5', 'SHA-1', 'SHA-224', SHA-256',
            'SHA-384' or 'SHA-512'
        **中文文档**

        - 发送消息时只需要对方的pubkey
        - 如需使用签名, 则双方都需要持有对方的pubkey
        """
        token = rsa.encrypt(binary, self.his_pubkey)
        if use_sign:
            self.sign = rsa.sign(binary, self.my_privkey, sign_method)
        return token

    def decrypt(self, token, signature=None, *args, **kwargs):
        """
        Decrypt binary data.

        **中文文档**

        - 接收消息时只需要自己的privkey
        - 如需使用签名, 则双方都需要持有对方的pubkey
        """
        binary = rsa.decrypt(token, self.my_privkey)
        if signature:
            rsa.verify(binary, signature, self.his_pubkey)
        return binary

    def encrypt_file(self, **kwargs):
        raise NotImplementedError(ERROR_MESSAGE)

    def decrypt_file(self, **kwargs):
        raise NotImplementedError(ERROR_MESSAGE)

    def encrypt_dir(self, **kwargs):
        raise NotImplementedError(ERROR_MESSAGE)

    def decrypt_dir(self, **kwargs):
        raise NotImplementedError(ERROR_MESSAGE)