# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/future/moves/subprocess.py
# Compiled at: 2016-10-27 16:05:38
# Size of source mod 2**32: 251 bytes
from __future__ import absolute_import
from future.utils import PY2, PY26
from subprocess import *
if PY2:
    __future_module__ = True
    from commands import getoutput, getstatusoutput
if PY26:
    from future.backports.misc import check_output