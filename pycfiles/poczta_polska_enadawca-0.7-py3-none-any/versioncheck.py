# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/hysia/Code/Pocsuite/pocsuite/lib/utils/versioncheck.py
# Compiled at: 2018-11-28 03:20:09
__doc__ = "\nCopyright (c) 2014-2016 pocsuite developers (https://seebug.org)\nSee the file 'docs/COPYING' for copying permission\n"
import sys
PYVERSION = sys.version.split()[0]
if PYVERSION >= '3' or PYVERSION < '2.6':
    exit("[-] incompatible Python version detected ('%s'). For successfully running pocsuite you'll have to use version 2.6 or 2.7 (visit 'http://www.python.org/download/')" % PYVERSION)