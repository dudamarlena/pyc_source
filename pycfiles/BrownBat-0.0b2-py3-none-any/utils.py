# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/brownant/utils.py
# Compiled at: 2014-10-08 05:32:06
from six import text_type

def to_bytes_safe(text, encoding='utf-8'):
    """Convert the input value into bytes type.

    If the input value is string type and could be encode as UTF-8 bytes, the
    encoded value will be returned. Otherwise, the encoding has failed, the
    origin value will be returned as well.

    :param text: the input value which could be string or bytes.
    :param encoding: the expected encoding be used while converting the string
                     input into bytes.
    :rtype: :class:`~__builtin__.bytes`
    """
    if not isinstance(text, (bytes, text_type)):
        raise TypeError('must be string type')
    if isinstance(text, text_type):
        return text.encode(encoding)
    return text