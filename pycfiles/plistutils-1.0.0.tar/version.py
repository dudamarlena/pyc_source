# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/plists/version.py
# Compiled at: 2015-03-22 02:45:07
IVERSION = (0, 0, 4)
VERSION = ('.').join(str(i) for i in IVERSION)
MINORVERSION = ('.').join(str(i) for i in IVERSION[:2])
NAME = 'plist'
NAMEVERSION = NAME + ' ' + VERSION