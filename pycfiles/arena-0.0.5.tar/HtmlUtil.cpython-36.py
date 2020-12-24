# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\ProgramData\lib\site-packages\arelle\HtmlUtil.py
# Compiled at: 2018-02-26 09:10:06
# Size of source mod 2**32: 917 bytes
__doc__ = '\nCreated on April 14, 2011\n\n@author: Mark V Systems Limited\n(c) Copyright 2011 Mark V Systems Limited, All rights reserved.\n'
try:
    import regex as re
except ImportError:
    import re

def attrValue(str, name):
    prestuff, matchedName, valuePart = str.lower().partition('charset')
    value = []
    endSep = None
    beforeEquals = True
    for c in valuePart:
        if value:
            if c == endSep or c.isspace() or c in ';':
                break
            value.append(c)
        else:
            if beforeEquals:
                if c == '=':
                    beforeEquals = False
                else:
                    if c in ('"', "'"):
                        endSep = c
                    else:
                        if c == ';':
                            break
                        elif not c.isspace():
                            value.append(c)

    return ''.join(value)