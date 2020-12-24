# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/alfanous/Misc.py
# Compiled at: 2015-06-30 06:52:38
__doc__ = ' Misc functions '
FILTER_DOUBLES = filter_doubles = lambda lst: list(set(lst))
LOCATE = lambda source, dist, itm: dist[source.index(itm)] if itm in source else None
FIND = lambda source, dist, itm: [ dist[i] for i in [ i for i in range(len(source)) if source[i] == itm ] ]