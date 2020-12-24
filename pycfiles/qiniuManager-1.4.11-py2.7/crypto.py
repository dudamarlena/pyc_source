# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/qiniuManager/crypto.py
# Compiled at: 2017-09-26 22:59:06
"""使用用户名加密API Key"""
import sys, getpass
from itertools import cycle
__all__ = [
 'encrypt', 'decrypt']
if sys.version_info.major == 2:
    from base64 import encodestring, decodestring

    def encrypt(s):
        """
        (py2) encrypt with xor cycle username
        :param s: str
        :return: str
        """
        return encodestring(bytes(('').join([ bytes(chr(ord(i) ^ ord(j)).encode()) for i, j in zip(s, cycle(getpass.getuser()))
                                            ]))).replace('\n', '')


    def decrypt(s):
        """
        (py2) decrypt with xor cycle username
        :param s: str
        :return: str
        """
        return ('').join([ bytes(chr(ord(i) ^ ord(j)).encode()) for i, j in zip(decodestring(s), cycle(getpass.getuser()))
                         ])


else:
    from base64 import encodebytes, decodebytes

    def encrypt(s):
        """
        (py3) encrypt with xor cycle username
        :param s: str
        :return: str
        """
        return encodebytes(bytes(('').join([ bytes(chr(i ^ ord(j)).encode()) for i, j in zip(s.encode(), cycle(getpass.getuser()))
                                           ]))).replace('\n', '').decode()


    def decrypt(s):
        """
        (py3) decrypt with xor cycle username
        :param s: str
        :return: str
        """
        return ('').join([ bytes(chr(i ^ ord(j)).encode()) for i, j in zip(decodebytes(s.encode()), cycle(getpass.getuser()))
                         ]).decode()