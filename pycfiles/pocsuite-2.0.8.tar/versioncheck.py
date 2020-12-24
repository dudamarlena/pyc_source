# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/utils/versioncheck.py
# Compiled at: 2018-11-28 03:20:09
"""
Copyright (c) 2014-2016 pocsuite developers (https://seebug.org)
See the file 'docs/COPYING' for copying permission
"""
import sys
PYVERSION = sys.version.split()[0]
if PYVERSION >= '3' or PYVERSION < '2.6':
    exit("[-] incompatible Python version detected ('%s'). For successfully running pocsuite you'll have to use version 2.6 or 2.7 (visit 'http://www.python.org/download/')" % PYVERSION)