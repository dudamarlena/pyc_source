# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/doakey/Sync/Programming/reflowrst/reflowrst/tools/make_enumerator.py
# Compiled at: 2018-01-26 15:31:48
# Size of source mod 2**32: 938 bytes
import string
from .roman import toRoman

def make_enumerator(enumerator_type, enumerator_level):
    """Make an enumerator given the type and level"""
    enumerator = ''
    if 'hashtag' in enumerator_type:
        enumerator = '#'
    else:
        if 'arabic' in enumerator_type:
            enumerator = str(enumerator_level)
        else:
            if 'alpha' in enumerator_type:
                enumerator = string.ascii_lowercase[(enumerator_level - 1)]
            else:
                if 'roman' in enumerator_type:
                    enumerator = toRoman(enumerator_level)
    if 'upper' in enumerator_type:
        enumerator = enumerator.upper()
    else:
        if 'lower' in enumerator_type:
            enumerator = enumerator.lower()
        if 'period' in enumerator_type:
            enumerator = enumerator + '.'
        else:
            if 'full_parenthesis' in enumerator_type:
                enumerator = '(' + enumerator + ')'
            elif 'right_parenthesis' in enumerator_type:
                enumerator = enumerator + ')'
    return enumerator