# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\runall.py
# Compiled at: 2009-11-09 02:09:08
import doctest, mod2doctest, basicexample_test as A
for mod in [A]:
    doctest.testmod(m=mod, optionflags=mod2doctest.DEFAULT_DOCTEST_FLAGS)