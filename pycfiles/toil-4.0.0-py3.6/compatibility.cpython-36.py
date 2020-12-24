# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/compatibility.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 621 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
from past.builtins import str as oldstr
import sys
USING_PYTHON2 = True if sys.version_info < (3, 0) else False

def compat_oldstr(s):
    if USING_PYTHON2:
        return oldstr(s)
    else:
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s


def compat_bytes(s):
    if USING_PYTHON2:
        return bytes(s)
    else:
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s


def compat_plain(s):
    if USING_PYTHON2:
        return s
    else:
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s