# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/tools/get_enumerator_level.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 493 bytes
from .roman import fromRoman
import string

def get_enumerator_level(enumerator, enumerator_type):
    enumerator = enumerator[0:-1]
    if 'hashtag' in enumerator_type:
        return 0
    if 'full_parenthesis' in enumerator_type:
        enumerator = enumerator[1:]
    if 'arabic' in enumerator_type:
        return int(enumerator)
    else:
        if 'alpha' in enumerator_type:
            return string.ascii_lowercase.index(enumerator.lower()) + 1
        return fromRoman(enumerator)