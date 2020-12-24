# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\Smart_len.py
# Compiled at: 2004-10-12 17:59:14
import re

def smart_len(s):
    l = 0
    for c in s:
        if not 55296 <= ord(c) < 56320:
            l += 1

    return l