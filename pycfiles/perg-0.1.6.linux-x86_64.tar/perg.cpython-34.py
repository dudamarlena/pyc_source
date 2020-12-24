# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/perg.py
# Compiled at: 2015-06-28 23:25:01
# Size of source mod 2**32: 687 bytes
import string
from re import sre_parse

def parse(s):
    return sre_parse.parse(s)


SAMPLERS = {
 'literal', 'branch', 'in', 'range', 'category', 'max_repeat',
 'any', 'subpattern', 'min_repeat', 'groupref'}
CATEGORIES = {'category_digit': string.digits,  'category_word': string.ascii_letters}