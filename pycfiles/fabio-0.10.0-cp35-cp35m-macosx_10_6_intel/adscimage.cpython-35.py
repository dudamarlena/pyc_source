# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/adscimage.py
# Compiled at: 2020-04-03 09:02:03
# Size of source mod 2**32: 1118 bytes
"""
Compatibility code with ADSC format.

This module is now renamed into :mod:`fabio.dtrekimage`.
"""
from . import dtrekimage
AdscImage = dtrekimage.DtrekImage
adscimage = dtrekimage.DtrekImage