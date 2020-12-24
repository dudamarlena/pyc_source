# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\string_utils.py
# Compiled at: 2019-07-12 12:27:33
# Size of source mod 2**32: 500 bytes
import unicodedata
from verbecc import grammar_defines

def strip_accents(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))


def starts_with_vowel(s):
    if len(s) == 0:
        return False
    return strip_accents(s)[0] in ('a', 'e', 'i', 'o', 'u')


def unicodefix(s):
    try:
        return s.decode('utf-8')
    except AttributeError:
        return s