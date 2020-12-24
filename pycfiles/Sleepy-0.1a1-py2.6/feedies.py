# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-i386/egg/sleepy/feedies.py
# Compiled at: 2011-04-26 07:21:02
from itertools import chain

def merge(*feeds):
    return sorted(chain(*feeds), key=lambda entry: getattr(entry, getattr(entry, 'sort_key', None) or 'published'), reverse=True)