# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\droopy\droopy_doctest.py
# Compiled at: 2011-10-24 14:00:42
from droopy.factory import DroopyFactory
from droopy.lang.english import English

def _(text):
    return DroopyFactory.create_full_droopy(text, English())