# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/utils/versioncheck.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import sys
PYVERSION = sys.version.split()[0]
if PYVERSION >= '3' or PYVERSION < '2.6':
    exit("[CRITICAL] incompatible Python version detected ('%s'). For successfully running sqlmap you'll have to use version 2.6 or 2.7 (visit 'http://www.python.org/download/')" % PYVERSION)
extensions = ('gzip', 'ssl', 'sqlite3', 'zlib')
try:
    for _ in extensions:
        __import__(_)

except ImportError as ex:
    errMsg = 'missing one or more core extensions (%s) ' % (', ').join("'%s'" % _ for _ in extensions)
    errMsg += 'most probably because current version of Python has been '
    errMsg += "built without appropriate dev packages (e.g. 'libsqlite3-dev')"
    exit(errMsg)