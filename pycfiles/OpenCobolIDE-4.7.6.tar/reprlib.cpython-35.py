# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/moves/reprlib.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 161 bytes
from __future__ import absolute_import
from future.utils import PY3
if PY3:
    from reprlib import *
else:
    __future_module__ = True
    from repr import *