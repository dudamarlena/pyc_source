# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plim/util.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 385 bytes
import sys
PY3K = sys.version_info >= (3, 0)
if PY3K:
    from io import StringIO
    joined = lambda buf: ''.join(buf)
    space_separated = lambda buf: ' '.join(buf)
    u = str
    MAXSIZE = sys.maxsize
else:
    from StringIO import StringIO
    joined = lambda buf: u('').join(buf)
    space_separated = lambda buf: u(' ').join(buf)
    u = unicode
    MAXSIZE = sys.maxint