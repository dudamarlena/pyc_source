# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\arc_r\check_software.py
# Compiled at: 2006-05-05 22:10:08
import sys
(major, minor, micro, releaselevel, serial) = sys.version_info
if major < 2 or major == 2 and minor < 3:
    print 'WARNING: You are using a version of older than that of this Python lower than that '