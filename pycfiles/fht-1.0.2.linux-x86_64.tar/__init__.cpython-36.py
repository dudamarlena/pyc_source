# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.6/site-packages/fht/__init__.py
# Compiled at: 2017-06-20 09:40:47
# Size of source mod 2**32: 176 bytes
from __future__ import absolute_import
from fht._fht import *

def test(level=1, verbosity=1):
    from numpy.testing import Tester
    return Tester().test(level, verbosity)