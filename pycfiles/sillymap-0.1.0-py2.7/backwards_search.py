# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sillymap/backwards_search.py
# Compiled at: 2017-04-04 07:57:30


def backwards_search(p, cl, rank, total_length):
    """Perform backwards search using pattern p, count lookup cl and rank rank

    reference http://alexbowe.com/fm-index/"""
    start = 0
    end = total_length - 1
    for i in range(len(p) - 1, -1, -1):
        if end < start:
            break
        char = p[i]
        count_for_char = cl[char]
        start = count_for_char + rank.rank(start - 1, char)
        end = count_for_char + rank.rank(end, char) - 1

    return (start, end)