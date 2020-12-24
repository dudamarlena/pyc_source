# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/quran/buckwalter.py
# Compiled at: 2009-11-24 19:02:13
_unicode_to_buckwalter = {'ء': "'", 'آ': '|', 
   'أ': '>', 
   'ؤ': '&', 
   'إ': '<', 
   'ئ': '}', 
   'ا': 'A', 
   'ب': 'b', 
   'ة': 'p', 
   'ت': 't', 
   'ث': 'v', 
   'ج': 'j', 
   'ح': 'H', 
   'خ': 'x', 
   'د': 'd', 
   'ذ': '*', 
   'ر': 'r', 
   'ز': 'z', 
   'س': 's', 
   'ش': '$', 
   'ص': 'S', 
   'ض': 'D', 
   'ط': 'T', 
   'ظ': 'Z', 
   'ع': 'E', 
   'غ': 'g', 
   'ـ': '_', 
   'ف': 'f', 
   'ق': 'q', 
   'ك': 'k', 
   'ل': 'l', 
   'م': 'm', 
   'ن': 'n', 
   'ه': 'h', 
   'و': 'w', 
   'ى': 'Y', 
   'ي': 'y', 
   'ً': 'F', 
   'ٌ': 'N', 
   'ٍ': 'K', 
   'َ': 'a', 
   'ُ': 'u', 
   'ِ': 'i', 
   'ّ': '~', 
   'ْ': 'o', 
   'ٓ': '^', 
   'ٔ': '#', 
   'ٰ': '`', 
   'ٱ': '{', 
   'پ': 'P', 
   'چ': 'J', 
   'ڤ': 'V', 
   'گ': 'G', 
   'ۜ': ':', 
   '۟': '@', 
   '۠': '"', 
   'ۢ': '[', 
   'ۣ': ';', 
   'ۥ': ',', 
   'ۦ': '.', 
   'ۨ': '!', 
   '۪': '-', 
   '۫': '+', 
   '۬': '%', 
   'ۭ': ']', 
   ' ': ' '}
_buckwalter_to_unicode = {}
for (u, bw) in _unicode_to_buckwalter.iteritems():
    _buckwalter_to_unicode[bw] = u

def buckwalter_to_unicode(str):
    r"""
    >>> buckwalter_to_unicode('yaHoyaY`')
    u'\u064a\u064e\u062d\u0652\u064a\u064e\u0649\u0670'
    """
    ret = ''
    for c in str:
        ret += _buckwalter_to_unicode[c]

    return ret


def unicode_to_buckwalter(str):
    r"""
    >>> unicode_to_buckwalter(u'\u064a\u064e\u062d\u0652\u064a\u064e\u0649\u0670')
    'yaHoyaY`'
    """
    ret = ''
    for c in str:
        ret += _unicode_to_buckwalter[c]

    return ret