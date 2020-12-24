# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/pagination.py
# Compiled at: 2017-07-14 09:11:18
# Size of source mod 2**32: 1840 bytes
from collections import namedtuple
from flask_restframework.queryset_wrapper import QuerysetWrapper
PageInfo = namedtuple('PageInfo', ['page', 'page_size'])

class DefaultPagination:
    qs = None

    def __init__(self, qs, total=None):
        assert isinstance(qs, QuerysetWrapper)
        self.qs = qs
        self.total = 0
        self.count_pages = 0
        self.page = 0
        self.page_size = 10
        if total is None:
            self.total = self.qs.count()
        else:
            self.total = total

    def paginate(self, request):
        """Perform qs filtration"""
        pageInfo = self._get_page_info(request)
        page = pageInfo.page
        page_size = pageInfo.page_size
        full_pages = int(self.total / page_size)
        if self.total % page_size == 0:
            self.count_pages = full_pages
        else:
            self.count_pages = full_pages + 1
        self.page = page
        self.page_size = page_size
        self.qs = self.qs.slice(page_size * (page - 1), page_size * page)

    def update_response(self, data):
        """Updates response: adds information fields like page, page_size etc."""
        return {'results': data, 
         'total': self.total, 
         'pages': self.count_pages, 
         'page': self.page, 
         'page_size': self.page_size}

    def _get_page_info(self, request):
        """
        Returns page info

        :param request:
        :rtype: PageInfo
        """
        return PageInfo(page=int(request.args.get('page', 1)), page_size=int(request.args.get('page_size', 10)))