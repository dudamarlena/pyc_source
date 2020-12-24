# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vasily/src/isounidecode/isounidecode/unidecode.py
# Compiled at: 2017-06-11 17:15:19
# Size of source mod 2**32: 1546 bytes
import sys
from .codes import codes
if sys.version_info[0] >= 3:
    unichr = chr

def build_8859_translation(codes):
    codes_8859 = {}
    for code in codes:
        translation = codes[code]
        tr_8859 = translation
        try:
            tr_8859 = unichr(code).encode('iso-8859-1')
        except UnicodeEncodeError:
            pass

        codes_8859[code] = tr_8859

    codes_8859[ord('Ĳ')] = b'IJ'
    codes_8859[ord('ĳ')] = b'ij'
    codes_8859[ord('Š')] = b'S'
    codes_8859[ord('š')] = b's'
    codes_8859[ord('Ž')] = b'Z'
    codes_8859[ord('ž')] = b'z'
    codes_8859[ord('Œ')] = b'OE'
    codes_8859[ord('œ')] = b'oe'
    codes_8859[ord('Ÿ')] = b'Y'
    codes_8859[ord('ÿ')] = b'y'
    codes_8859[ord('Š')] = b'S'
    codes_8859[ord('š')] = b's'
    codes_8859[ord('Ž')] = b'Z'
    codes_8859[ord('ž')] = b'z'
    return codes_8859


codes_8859 = build_8859_translation(codes)
translations = {'ascii': codes, 
 'iso8859-1': codes_8859}

def unidecode(u, translation='ascii'):
    print('Yo')
    trans_table = translations[translation]
    parts = []
    for c in u:
        print('c', c)
        cc = ord(c)
        print('cc', cc)
        parts.append(trans_table.get(ord(c), b''))

    print('parts', parts)
    return (b'').join(translations[translation].get(ord(c), b'') for c in u)