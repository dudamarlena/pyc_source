# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/wechat_sdk/lib/crypto/exceptions.py
# Compiled at: 2016-04-12 23:03:20
from wechat_sdk.exceptions import WechatSDKException

class CryptoException(WechatSDKException):
    """加密解密异常基类"""
    pass


class CryptoComputeSignatureError(CryptoException):
    """签名计算错误"""
    pass


class EncryptAESError(CryptoException):
    """AES加密错误"""
    pass


class DecryptAESError(CryptoException):
    """AES解密错误"""
    pass


class IllegalBuffer(CryptoException):
    """不合法的缓冲区"""
    pass


class ValidateAppIDError(CryptoException):
    """验证AppID错误"""
    pass


class ValidateSignatureError(CryptoException):
    """验证签名错误"""
    pass


class ValidateAESKeyError(CryptoException):
    """验证AES Key错误"""
    pass