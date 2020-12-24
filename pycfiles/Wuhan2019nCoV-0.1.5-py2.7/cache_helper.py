# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wuhanncov/cache_helper.py
# Compiled at: 2020-01-27 02:27:50
cache_set = set()

def print_avoid_cache(msg):
    if cache_set.__contains__(msg):
        return
    print msg
    cache_set.add(msg)