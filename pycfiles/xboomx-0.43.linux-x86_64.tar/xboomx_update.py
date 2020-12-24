# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/xboomx/bin/xboomx_update.py
# Compiled at: 2014-01-30 06:22:07
import fileinput, xboomx.db

def main():
    db = xboomx.db.open_shelve()
    item = fileinput.input().next()
    item = item.strip('\n')
    db[item] = db.get(item, 0) + 1
    print item
    db.sync()
    db.close()


main()