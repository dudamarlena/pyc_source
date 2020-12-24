# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Misc.py
# Compiled at: 2015-06-30 06:52:38
""" Misc functions """
FILTER_DOUBLES = filter_doubles = lambda lst: list(set(lst))
LOCATE = lambda source, dist, itm: dist[source.index(itm)] if itm in source else None
FIND = lambda source, dist, itm: [ dist[i] for i in [ i for i in range(len(source)) if source[i] == itm ] ]