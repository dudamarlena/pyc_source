# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/spanyam/personal/astgen/astgen/version.py
# Compiled at: 2019-02-10 15:51:16
# Size of source mod 2**32: 172 bytes
IVERSION = (0, 1, 6, 13)
VERSION = '.'.join(str(i) for i in IVERSION)
MINORVERSION = '.'.join(str(i) for i in IVERSION[:2])
NAME = 'astgen'
NAMEVERSION = NAME + ' ' + VERSION