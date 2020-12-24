# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-mongo-reader/example/sampleapp/sampleapp/security.py
# Compiled at: 2015-03-06 17:37:51


def my_mongocall_perm_check(req, db, col, cmd):
    if not col.startswith('user'):
        return False
    return True