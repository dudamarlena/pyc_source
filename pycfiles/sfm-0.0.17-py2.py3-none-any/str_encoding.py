# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/single_file_module-project/sfm/str_encoding.py
# Compiled at: 2019-04-21 23:26:23
import base64, binascii

def encode_base64_urlsafe(text):
    u"""Convert any utf-8 string to url safe string using base64 encoding.

    **中文文档**

    将任意utf-8字符串用base64编码算法编码为纯数字和字母。
    """
    return base64.urlsafe_b64encode(text.encode('utf-8')).decode('utf-8')


def decode_base64_urlsafe(text):
    u"""Reverse operation of :func:`encode_base64_urlsafe`.

    **中文文档**

    将base64字符串解码为原字符串。
    """
    return base64.urlsafe_b64decode(text.encode('utf-8')).decode('utf-8')


def encode_hexstr(text):
    u"""Convert any utf-8 string to hex string.

    **中文文档**

    将任意utf-8字符串编码为16进制字符串。
    """
    return binascii.b2a_hex(text.encode('utf-8')).decode('utf-8')


def decode_hexstr(text):
    u"""Reverse operation of :func:`encode_hexstr`.

    **中文文档**

    将16进制字符串解码为原字符串。
    """
    return binascii.a2b_hex(text.encode('utf-8')).decode('utf-8')