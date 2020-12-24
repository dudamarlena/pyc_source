# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Romanization.py
# Compiled at: 2015-06-30 06:52:38
BUCKWALTER2UNICODE = {"'": 'ء', '|': 'آ', 
   '>': 'أ', 
   '&': 'ؤ', 
   '<': 'إ', 
   '}': 'ئ', 
   'A': 'ا', 
   'b': 'ب', 
   'p': 'ة', 
   't': 'ت', 
   'v': 'ث', 
   'j': 'ج', 
   'H': 'ح', 
   'x': 'خ', 
   'd': 'د', 
   '*': 'ذ', 
   'r': 'ر', 
   'z': 'ز', 
   's': 'س', 
   '$': 'ش', 
   'S': 'ص', 
   'D': 'ض', 
   'T': 'ط', 
   'Z': 'ظ', 
   'E': 'ع', 
   'g': 'غ', 
   '_': 'ـ', 
   'f': 'ف', 
   'q': 'ق', 
   'k': 'ك', 
   'l': 'ل', 
   'm': 'م', 
   'n': 'ن', 
   'h': 'ه', 
   'w': 'و', 
   'Y': 'ى', 
   'y': 'ي', 
   'F': 'ً', 
   'N': 'ٌ', 
   'K': 'ٍ', 
   'a': 'َ', 
   'u': 'ُ', 
   'i': 'ِ', 
   '~': 'ّ', 
   'o': 'ْ', 
   '`': 'ٰ', 
   '{': 'ٱ', 
   '^': 'ٓ', 
   '#': 'ٔ', 
   ':': 'ۜ', 
   '@': '۟', 
   '"': '۠', 
   '[': 'ۢ', 
   ';': 'ۣ', 
   ',': 'ۥ', 
   '.': 'ۦ', 
   '!': 'ۨ', 
   '-': '۪', 
   '+': '۫', 
   '%': '۬', 
   ']': 'ۭ'}
ISO2UNICODE = {'ˌ': 'ء', 'ˈ': 'أ', 
   'ˈ': 'ؤ', 
   'ˈ': 'ئ', 
   'ʾ': 'ا', 
   'b': 'ب', 
   'ẗ': 'ة', 
   't': 'ت', 
   'ṯ': 'ث', 
   'ǧ': 'ج', 
   'ḥ': 'ح', 
   'ẖ': 'خ', 
   'd': 'د', 
   'ḏ': 'ذ', 
   'r': 'ر', 
   'z': 'ز', 
   's': 'س', 
   'š': 'ش', 
   'ṣ': 'ص', 
   'ḍ': 'ض', 
   'ṭ': 'ط', 
   'ẓ': 'ظ', 
   'ʿ': 'ع', 
   'ġ': 'غ', 
   'f': 'ف', 
   'q': 'ق', 
   'k': 'ك', 
   'l': 'ل', 
   'm': 'م', 
   'n': 'ن', 
   'h': 'ه', 
   'w': 'و', 
   'ỳ': 'ى', 
   'y': 'ي', 
   'á': 'ً', 
   'ú': 'ٌ', 
   'í': 'ٍ', 
   'a': 'َ', 
   'u': 'ُ', 
   'i': 'ِ', 
   '°': 'ْ'}
ROMANIZATION_SYSTEMS_MAPPINGS = {'buckwalter': BUCKWALTER2UNICODE, 
   'iso': ISO2UNICODE, 
   'arabtex': None}

def guess_romanization_system():
    """ @todo """
    pass


def transliterate(mode, string, ignore='', reverse=False):
    """ encode & decode different  romanization systems """
    if ROMANIZATION_SYSTEMS_MAPPINGS.has_key(mode):
        MAPPING = ROMANIZATION_SYSTEMS_MAPPINGS[mode]
    else:
        MAPPING = {}
    if reverse:
        mapping = {}
        for k, v in MAPPING.items():
            mapping[v] = k

    else:
        mapping = MAPPING
    result = ''
    for char in string:
        if mapping.has_key(char) and char not in ignore:
            result += mapping[char]
        else:
            result += char

    return result