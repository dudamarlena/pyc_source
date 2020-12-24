# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/hstools/compat.py
# Compiled at: 2019-10-10 13:29:58
# Size of source mod 2**32: 257 bytes
from __future__ import print_function
import sys, urllib
is_py2 = sys.version[0] == '2'
if is_py2:
    import Queue as queue
    input = raw_input
    urlencode = urllib.pathname2url
else:
    import queue
    urlencode = urllib.parse.quote