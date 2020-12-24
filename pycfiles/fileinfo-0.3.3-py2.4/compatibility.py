# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/compatibility.py
# Compiled at: 2008-06-07 07:55:08
"""Utilities"""
try:
    s = set((1, ))
except NameError:
    from sets import Set as set