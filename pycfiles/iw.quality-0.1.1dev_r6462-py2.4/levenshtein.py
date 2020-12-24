# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/quality/levenshtein.py
# Compiled at: 2007-10-12 08:24:06
""" Base filters
"""
from Levenshtein import ratio

def search_similarities(code_mapping, treshold=0.7):
    similar = []
    items = code_mapping.items()
    done = []
    for (key, value) in items:
        done.append(key)
        code = str(value.code)
        for (key2, value2) in items:
            if key2 == key or key2 in done:
                continue
            code2 = str(value2.code)
            res = ratio(code, code2)
            if res > treshold:
                yield (
                 res, value.key, value2.key)