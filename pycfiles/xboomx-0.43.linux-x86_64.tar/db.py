# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/xboomx/db.py
# Compiled at: 2013-08-15 04:24:36
import shelve, os

def open_shelve():
    try:
        os.makedirs(os.getenv('HOME') + '/.xboomx')
    except:
        pass

    return shelve.open(os.getenv('HOME') + '/.xboomx/xboomx.db')