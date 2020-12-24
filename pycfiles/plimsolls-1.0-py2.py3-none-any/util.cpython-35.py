# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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