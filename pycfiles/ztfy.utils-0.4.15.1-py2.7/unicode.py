# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/unicode.py
# Compiled at: 2014-05-20 03:36:16
import codecs, string
_unicodeTransTable = {}

def _fillUnicodeTransTable():
    _corresp = [
     (
      'A', [192, 193, 194, 195, 196, 197, 256, 258, 260]),
     (
      'AE', [198]),
     (
      'a', [224, 225, 226, 227, 228, 229, 257, 259, 261]),
     (
      'ae', [230]),
     (
      'C', [199, 262, 264, 266, 268]),
     (
      'c', [231, 263, 265, 267, 269]),
     (
      'D', [208, 270, 272]),
     (
      'd', [240, 271, 273]),
     (
      'E', [200, 201, 202, 203, 274, 276, 278, 280, 282]),
     (
      'e', [232, 233, 234, 235, 275, 277, 279, 281, 283]),
     (
      'G', [284, 286, 288, 290]),
     (
      'g', [285, 287, 289, 291]),
     (
      'H', [292, 294]),
     (
      'h', [293, 295]),
     (
      'I', [204, 205, 206, 207, 296, 298, 300, 302, 304]),
     (
      'i', [236, 237, 238, 239, 297, 299, 301, 303, 305]),
     (
      'IJ', [306]),
     (
      'ij', [307]),
     (
      'J', [308]),
     (
      'j', [309]),
     (
      'K', [310]),
     (
      'k', [311, 312]),
     (
      'L', [313, 315, 317, 319, 321]),
     (
      'l', [314, 316, 318, 320, 322]),
     (
      'N', [209, 323, 325, 327, 330]),
     (
      'n', [241, 324, 326, 328, 329, 331]),
     (
      'O', [210, 211, 212, 213, 214, 216, 332, 334, 336]),
     (
      'o', [242, 243, 244, 245, 246, 248, 333, 335, 337]),
     (
      'OE', [338]),
     (
      'oe', [339]),
     (
      'R', [340, 342, 344]),
     (
      'r', [341, 343, 345]),
     (
      'S', [346, 348, 350, 352]),
     (
      's', [347, 349, 351, 5648, 383]),
     (
      'T', [354, 356, 358]),
     (
      't', [355, 357, 359]),
     (
      'U', [217, 218, 219, 220, 360, 362, 364, 366, 368, 370]),
     (
      'u', [249, 250, 251, 252, 361, 363, 365, 367, 369]),
     (
      'W', [372]),
     (
      'w', [373]),
     (
      'Y', [221, 374, 376]),
     (
      'y', [253, 255, 375]),
     (
      'Z', [377, 379, 381]),
     (
      'z', [378, 380, 382])]
    for char, codes in _corresp:
        for code in codes:
            _unicodeTransTable[code] = char


_fillUnicodeTransTable()

def translateString(s, escapeSlashes=False, forceLower=True, spaces=' ', keep_chars='_-.'):
    """Remove extended characters from string and replace them with 'basic' ones
    
    @param s: text to be cleaned.
    @type s: str or unicode
    @param escapeSlashes: if True, slashes are also converted
    @type escapeSlashes: boolean
    @param forceLower: if True, result is automatically converted to lower case
    @type forceLower: boolean
    @return: text without diacritics
    @rtype: unicode
    """
    if escapeSlashes:
        s = string.replace(s, '\\', '/').split('/')[(-1)]
    s = s.strip()
    if isinstance(s, str):
        s = unicode(s, 'utf8', 'replace')
    s = s.translate(_unicodeTransTable)
    s = ('').join([ a for a in s.translate(_unicodeTransTable) if a.replace(' ', '-') in string.ascii_letters + string.digits + (keep_chars or '')
                  ])
    if forceLower:
        s = s.lower()
    if spaces != ' ':
        s = s.replace(' ', spaces)
    return s


def nvl(value, default=''):
    """Get specified value, or an empty string if value is empty
    
    @param value: text to be checked
    @param default: default value
    @return: value, or default if value is empty
    """
    return value or default


def uninvl(value, default=''):
    """Get specified value converted to unicode, or an empty unicode string if value is empty
    
    @param value: text to be checked
    @type value: str or unicode
    @param default: default value
    @return: value, or default if value is empty
    @rtype: unicode
    """
    try:
        if isinstance(value, unicode):
            return value
        else:
            return codecs.decode(value or default)

    except:
        return codecs.decode(value or default, 'latin1')


def unidict(value):
    """Get specified dict with values converted to unicode
    
    @param value: input dict of strings which may be converted to unicode
    @type value: dict
    @return: input dict converted to unicode
    @rtype: dict
    """
    result = {}
    for key in value:
        result[key] = uninvl(value[key])

    return result


def unilist(value):
    """Get specified list with values converted to unicode
    
    @param value: input list of strings which may be converted to unicode
    @type value: list
    @return: input list converted to unicode
    @rtype: list
    """
    if not isinstance(value, (list, tuple)):
        return uninvl(value)
    return [ uninvl(v) for v in value ]


def encode(value, encoding='utf-8'):
    """Encode given value with encoding"""
    if isinstance(value, unicode):
        return value.encode(encoding)
    return value


def utf8(value):
    """Encode given value tu UTF-8"""
    return encode(value, 'utf-8')


def decode(value, encoding='utf-8'):
    """Decode given value with encoding"""
    if isinstance(value, str):
        return value.decode(encoding)
    return value