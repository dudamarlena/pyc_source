# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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