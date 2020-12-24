# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/unicodeutil/__init__.py
# Compiled at: 2019-12-28 01:36:24
# Size of source mod 2**32: 780 bytes
import pkg_resources
try:
    from hangulutil import compose_hangul_syllable, decompose_hangul_syllable
    from unicodeutil import CaseFoldingMap, UnicodeBlocks, UnicodeData, casefold, preservesurrogates
except ImportError:
    from .hangulutil import compose_hangul_syllable, decompose_hangul_syllable
    from .unicodeutil import CaseFoldingMap, UnicodeBlocks, UnicodeData, casefold, preservesurrogates
else:
    UNIDATA_VERSION = '12.1.0'
    __all__ = [
     'CaseFoldingMap', 'UnicodeBlocks', 'UnicodeData', 'casefold', 'compose_hangul_syllable', 'decompose_hangul_syllable',
     'preservesurrogates', 'UNIDATA_VERSION']
    __version__ = pkg_resources.get_distribution('unicodeutil').version