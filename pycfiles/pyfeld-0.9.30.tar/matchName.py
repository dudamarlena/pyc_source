# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/matchName.py
# Compiled at: 2017-11-23 08:41:51
import Levenshtein

def match_something(item, list):
    item = item.replace(' ', '')
    item = item.replace('.', '')
    item = item.replace(',', '')
    lowest = list[0]
    lowestdelta = Levenshtein.distance(item, list[0])
    for entry in list:
        delta = Levenshtein.distance(item, entry)
        if delta < lowestdelta:
            lowestdelta = delta
            lowest = entry

    print (
     delta, item, entry)
    return lowest


if __name__ == '__main__':
    result = match_something('t. v.', ['television', 'tcf', 'tv'])
    print result