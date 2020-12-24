# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\ThirdParty\Xvif\Smart_len.py
# Compiled at: 2004-10-12 17:59:14
import re

def smart_len(s):
    l = 0
    for c in s:
        if not 55296 <= ord(c) < 56320:
            l += 1

    return l