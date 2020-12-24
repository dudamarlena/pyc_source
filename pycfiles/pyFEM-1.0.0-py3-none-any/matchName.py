# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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