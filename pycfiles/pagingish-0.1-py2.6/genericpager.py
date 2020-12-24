# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pagingish/genericpager.py
# Compiled at: 2010-02-04 05:16:20
import itertools

class SkipLimitPager(object):
    """
    Generic efficient pager that simply calls a function, passing it item skip
    and limit.

    The func that is passed to the initialiser must have a signature of "def
    func(skip=None, limit=None)".

    Efficient simply means that the pager does not try to calculate any paging
    statistics, i.e. there is no need to calculated total items, total pages,
    etc.
    """

    def __init__(self, func):
        self.func = func

    def get(self, pagesize, pageref=None):
        if pageref is not None:
            pagenum = int(pageref)
        else:
            pagenum = 0
        items = self.func(skip=pagenum * pagesize, limit=pagesize + 1)
        (prev, next) = (None, None)
        if pagenum:
            prev = unicode(pagenum - 1)
        if len(items) > pagesize:
            next = unicode(pagenum + 1)
        items = list(itertools.islice(items, pagesize))
        return {'prev': prev, 'items': items, 'next': next, 'stats': {'page_size': pagesize}}