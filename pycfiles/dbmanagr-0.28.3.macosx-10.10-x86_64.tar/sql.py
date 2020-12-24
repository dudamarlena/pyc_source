# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dbmanagr/utils/sql.py
# Compiled at: 2015-10-11 07:17:06


def sanitise(s):
    if s is None:
        return ''
    else:
        return s.replace("'", "''")