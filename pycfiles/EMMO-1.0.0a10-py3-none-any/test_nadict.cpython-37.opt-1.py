# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /emmo/tests/test_nadict.py
# Compiled at: 2020-04-10 04:40:37
# Size of source mod 2**32: 355 bytes
import sys, os
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo.nadict import NADict
n = NADict(a=1, b=NADict(c=3, d=4))
assert n.a == 1
assert n.b.c == 3
assert n.b.d == 4
assert n['b.c'] == 3