# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/xboomx/bin/xboomx_sort.py
# Compiled at: 2014-01-30 06:23:02
import fileinput, xboomx.db

def main():
    db = xboomx.db.open_shelve()
    items = []
    for input_item in fileinput.input():
        input_item = input_item.strip('\n')
        items.append((db.get(input_item, 0), input_item))

    items.sort(key=lambda x: x[0], reverse=True)
    for item in items:
        print item[1]

    db.close()


main()