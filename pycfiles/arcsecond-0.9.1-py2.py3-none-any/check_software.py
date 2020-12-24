# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\arc_r\check_software.py
# Compiled at: 2006-05-05 22:10:08
import sys
(major, minor, micro, releaselevel, serial) = sys.version_info
if major < 2 or major == 2 and minor < 3:
    print 'WARNING: You are using a version of older than that of this Python lower than that '