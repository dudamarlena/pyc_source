# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sillymap/count_lookup.py
# Compiled at: 2017-01-10 06:29:24
from collections import Counter

def count_lookup(text):
    """Returns a lookup table for c, returning the 
    number of characthers in text lexically smaller than c.
    """
    char_count = Counter(text)
    lookup = {}
    current_count = 0
    for c in sorted(list(set(text))):
        lookup[c] = current_count
        current_count += char_count[c]

    return lookup