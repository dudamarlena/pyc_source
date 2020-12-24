# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/plists/utils.py
# Compiled at: 2015-03-22 01:08:53


def makeIndentString(indentStr, level=0):
    out = ''
    if indentStr is not None:
        out = '\n' + indentStr * level
    return out