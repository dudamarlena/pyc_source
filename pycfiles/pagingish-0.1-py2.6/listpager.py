# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pagingish/listpager.py
# Compiled at: 2010-02-04 05:16:20


class Pager(object):

    def __init__(self, data):
        self.data = list(data)

    def get(self, pagesize, pageref=None):
        if pageref is None:
            pageref = 1
        else:
            pageref = int(pageref)
        item_count = len(self.data)
        total_pages = (item_count - 1) // pagesize + 1
        if pageref - 1 < 1:
            prevref = None
        else:
            prevref = unicode(pageref - 1)
        if pageref + 1 > total_pages:
            nextref = None
        else:
            nextref = unicode(pageref + 1)
        stats = {'page_number': pageref, 'item_count': item_count, 'total_pages': total_pages, 'page_size': pagesize}
        start = pagesize * (pageref - 1)
        end = pagesize * pageref
        return {'prev': prevref, 'items': self.data[start:end], 'next': nextref, 'stats': stats}