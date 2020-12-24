# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/moves/collections.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 417 bytes
from __future__ import absolute_import
import sys
from future.utils import PY2, PY26
__future_module__ = True
from collections import *
if PY2:
    from UserDict import UserDict
    from UserList import UserList
    from UserString import UserString
if PY26:
    from future.backports.misc import OrderedDict, Counter
if sys.version_info < (3, 3):
    from future.backports.misc import ChainMap, _count_elements