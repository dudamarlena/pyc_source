# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/plists/utils.py
# Compiled at: 2015-03-22 01:08:53


def makeIndentString(indentStr, level=0):
    out = ''
    if indentStr is not None:
        out = '\n' + indentStr * level
    return out