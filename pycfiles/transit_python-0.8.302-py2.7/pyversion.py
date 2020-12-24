# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/transit/pyversion.py
# Compiled at: 2017-12-12 16:52:26
import sys
PY3 = sys.version_info[0] == 3
PY2 = sys.version_info[0] == 2
if PY3:
    string_types = (
     str,)
    unicode_type = str
    unicode_f = chr
else:
    string_types = (
     str, unicode)
    unicode_type = unicode
    unicode_f = unichr
if PY3:
    long_type = int
    int_type = int
    int_types = (int,)
    number_types = (int, float)
else:
    long_type = long
    int_type = int
    int_types = (long, int)
    number_types = (long, int, float)

def isnumber_type(t):
    return t in number_types


if PY3:
    imap = map
    izip = zip

    def iteritems(d):
        return d.items()


else:
    import itertools
    imap = itertools.imap
    izip = itertools.izip

    def iteritems(d):
        return d.iteritems()