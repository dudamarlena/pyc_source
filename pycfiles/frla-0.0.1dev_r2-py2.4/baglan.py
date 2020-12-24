# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/frla/lib/baglan.py
# Compiled at: 2009-03-25 08:04:29
import pg

def baglan():
    db = pg.connect(dbname='firla', host='localhost', user='mehtap', passwd='')
    return db