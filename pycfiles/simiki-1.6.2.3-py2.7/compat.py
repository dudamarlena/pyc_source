# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/simiki/compat.py
# Compiled at: 2017-06-02 11:17:28
"""
Python compat for python version and os system
"""
import sys
_ver = sys.version_info
is_py2 = _ver[0] == 2
is_py3 = _ver[0] == 3
_platform = sys.platform
is_windows = _platform.startswith('win32')
is_linux = _platform.startswith('linux')
is_osx = _platform.startswith('darwin')
if is_py2:
    unicode = unicode
    basestring = basestring
    xrange = xrange
    raw_input = raw_input
if is_py3:
    unicode = str
    basestring = (str, bytes)
    xrange = range
    raw_input = input