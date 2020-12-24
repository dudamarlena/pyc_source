# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/plists/version.py
# Compiled at: 2015-03-22 02:45:07
IVERSION = (0, 0, 4)
VERSION = ('.').join(str(i) for i in IVERSION)
MINORVERSION = ('.').join(str(i) for i in IVERSION[:2])
NAME = 'plist'
NAMEVERSION = NAME + ' ' + VERSION