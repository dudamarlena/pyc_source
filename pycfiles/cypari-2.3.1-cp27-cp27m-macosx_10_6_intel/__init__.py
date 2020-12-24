# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/cypari/Version2/build/lib.macosx-10.6-intel-2.7/cypari/__init__.py
# Compiled at: 2020-03-01 20:27:02
from ._pari import pari, PariError
__all__ = ['pari', 'PariError']
from ._pari import prec_words_to_dec, prec_words_to_bits, prec_bits_to_dec, prec_dec_to_bits
from .version import version_info, __version__