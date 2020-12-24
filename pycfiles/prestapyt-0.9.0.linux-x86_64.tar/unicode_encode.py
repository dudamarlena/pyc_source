# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/prestapyt/unicode_encode.py
# Compiled at: 2016-09-01 03:41:47


def unicode2encoding(text, encoding='utf-8'):
    if isinstance(text, unicode):
        try:
            text = text.encode(encoding)
        except Exception:
            pass

    return text


def encode(text, encoding='utf-8'):
    if isinstance(text, (str, unicode)):
        return unicode2encoding(text, encoding=encoding)
    return str(text)