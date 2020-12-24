# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/utils.py
# Compiled at: 2008-06-07 18:20:23
"""Utilities"""

class groupby(dict):
    """SQL-like GROUPBY class including the logic in a Unix-like "sort | uniq".
    
    See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/259173
    """
    __module__ = __name__

    def __init__(self, seq, key=lambda x: x):
        for value in seq:
            k = key(value)
            self.setdefault(k, []).append(value)

    __iter__ = dict.iteritems