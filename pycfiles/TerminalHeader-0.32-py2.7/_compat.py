# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\theader\markupsafe\_compat.py
# Compiled at: 2016-01-25 01:09:29
"""
    markupsafe._compat
    ~~~~~~~~~~~~~~~~~~

    Compatibility module for different Python versions.

    :copyright: (c) 2013 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""
import sys
PY2 = sys.version_info[0] == 2
if not PY2:
    text_type = str
    string_types = (str,)
    unichr = chr
    int_types = (int,)
else:
    text_type = unicode
    string_types = (str, unicode)
    unichr = unichr
    int_types = (int, long)