# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/loc-project/loc/locales.py
# Compiled at: 2018-10-10 14:29:41
# Size of source mod 2**32: 373 bytes
"""
Define locale code.
"""

class Locale(object):
    __doc__ = '\n    Hardcoded locale code table.\n    '
    en_US = 'en-US'
    zh_CN = 'zh-CN'
    zh_TW = 'zh-TW'
    fr_FR = 'fr_FR'
    de_DE = 'de-DE'
    ja_JA = 'ja-JA'
    es_ES = 'es-ES'


locale_list = [value for key, value in Locale.__dict__.items() if not key.startswith('_')]