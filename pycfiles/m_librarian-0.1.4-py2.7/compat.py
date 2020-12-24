# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/lib.linux-i686-2.7/m_librarian/compat.py
# Compiled at: 2016-07-25 08:50:49
import sys
PY2 = sys.version_info[0] < 3
if PY2:
    string_type = basestring
    unicode_type = unicode
else:
    string_type = str
    unicode_type = str