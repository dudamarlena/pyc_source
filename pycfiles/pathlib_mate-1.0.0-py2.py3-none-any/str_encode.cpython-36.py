# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/pathlib_mate-project/pathlib_mate/str_encode.py
# Compiled at: 2020-03-14 12:17:18
# Size of source mod 2**32: 504 bytes
import binascii

def encode_hexstr(text):
    """
    Convert any utf-8 string to hex string.

    **中文文档**

    将任意utf-8字符串编码为16进制字符串。
    """
    return binascii.b2a_hex(text.encode('utf-8')).decode('utf-8')


def decode_hexstr(text):
    """
    Reverse operation of :func:`encode_hexstr`.

    **中文文档**

    将16进制字符串解码为原字符串。
    """
    return binascii.a2b_hex(text.encode('utf-8')).decode('utf-8')