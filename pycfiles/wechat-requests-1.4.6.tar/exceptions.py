# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pipeline\wechat\src\wechat\message\exceptions.py
# Compiled at: 2018-05-16 06:10:21


class MessageProcessException(Exception):

    def __init__(self, *args, **kwargs):
        self.handler = kwargs.pop('handler', None)
        self.raw_message = kwargs.pop('raw_message', None)
        super(MessageProcessException, self).__init__(*args, **kwargs)
        return


class MessageCryptoProcessError(Exception):
    """failed to process the encrypt or decrypt"""
    pass


class InvalidAESKeyError(MessageCryptoProcessError):
    pass


class SignatureError(MessageCryptoProcessError):
    pass


class InvalidSignature(MessageCryptoProcessError):
    pass


class ReceiveMsgFormatError(MessageCryptoProcessError):
    """receive message is not in the right format"""
    pass


class EncryptError(MessageCryptoProcessError):
    pass


class DecryptError(MessageCryptoProcessError):
    pass


class InvalidAppid(MessageCryptoProcessError):
    pass