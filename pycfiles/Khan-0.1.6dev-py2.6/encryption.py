# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/utils/encryption.py
# Compiled at: 2010-05-12 10:25:54
"""
加密解密
=================================

本模块提供加解密工具.

索引
=================================

* :func:`crypt`
* :class:`Vignere`

=================================

.. autofunction:: crypt
.. autoclass:: Vignere
    :members:
"""
import random, zlib, base64, hashlib
__all__ = [
 'Vignere', 'crypt']

def crypt(text):
    u""" 对明文进行 sha1 加密 """
    sha1 = hashlib.sha1()
    sha1.update(text)
    return sha1.hexdigest()


class Vignere(object):
    """
    用Vignere算法 <http://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher>_ 加解密数据
    """

    def __init__(self, key):
        u"""
        :param key: 用于加密和解密的 key, 要解密一个加密过的数据，必须使用加密时用的 ``key``
        """
        self._key = key

    def encode(self, text):
        u"""
        加密数据
        
        :param text: 要加密的数据
        :type text: string
        
        :rtype: string
        """
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        rand = random.Random(self._key).randrange
        text = zlib.compress(text)
        text = ('').join([ chr(ord(elem) ^ rand(256)) for elem in text ])
        text = base64.urlsafe_b64encode(text)
        return text

    def decode(self, text):
        u"""
        解密数据
        
        :param text: 要解密的数据
        :type text: string
        
        :rtype: string
        """
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        rand = random.Random(self._key).randrange
        text = base64.urlsafe_b64decode(text)
        text = ('').join([ chr(ord(elem) ^ rand(256)) for elem in text ])
        text = zlib.decompress(text)
        return text