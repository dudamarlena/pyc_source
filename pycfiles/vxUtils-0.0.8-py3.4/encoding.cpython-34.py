# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vxUtils/encoding.py
# Compiled at: 2017-01-31 12:24:26
# Size of source mod 2**32: 1031 bytes
"""
author : vex1023
email : vex1023@qq.com
"""
from __future__ import absolute_import, unicode_literals
import six
__all__ = [
 'to_text', 'to_binary', 'is_string', 'byte2int']
string_types = (
 six.string_types, six.text_type, six.binary_type)

def to_text(value, encoding='utf-8'):
    if isinstance(value, six.text_type):
        return value
    if isinstance(value, six.binary_type):
        return value.decode(encoding)
    return six.text_type(value)


def to_binary(value, encoding='utf-8'):
    if isinstance(value, six.binary_type):
        return value
    if isinstance(value, six.text_type):
        return value.encode(encoding)
    return six.binary_type(value)


def is_string(value):
    return isinstance(value, string_types)


def byte2int(s, index=0):
    """Get the ASCII int value of a character in a string.
    :param s: a string
    :param index: the position of desired character
    :return: ASCII int value
    """
    if six.PY2:
        return ord(s[index])
    return s[index]