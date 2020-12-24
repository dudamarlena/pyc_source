# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\filthypasswordgenerator\data\makeenglish.py
# Compiled at: 2019-02-22 11:20:36
# Size of source mod 2**32: 256 bytes
import sys, csv
with open('en') as (en):
    encsv = csv.reader(en)
    words = []
    for row in encsv:
        words.append(row[0])

    print(tuple(words))
    with open('out', 'w') as (out):
        outcsv = csv.writer(out)
        outcsv.writerow(tuple(words))