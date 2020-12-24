# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/logviewer/flask_validator/pagination.py
# Compiled at: 2017-01-12 12:04:40
# Size of source mod 2**32: 1360 bytes
from collections import namedtuple
PageInfo = namedtuple('PageInfo', ['page', 'page_size'])

class DefaultPagination:

    def __init__(self, qs):
        self.qs = qs
        self.total = 0
        self.count_pages = 0
        self.page = 0
        self.page_size = 10

    def paginate(self, request):
        """Perform qs filtration"""
        pageInfo = self._get_page_info(request)
        page = pageInfo.page
        page_size = pageInfo.page_size
        self.total = self.qs.count()
        self.count_pages = int(self.total / page_size) + 1
        self.page = page
        self.page_size = page_size
        self.qs = self.qs[page_size * (page - 1):page_size * page]

    def update_response(self, data):
        """Updates response: adds information fields like page, page_size etc."""
        return {'results':data, 
         'total':self.total, 
         'pages':self.count_pages, 
         'page':self.page, 
         'page_size':self.page_size}

    def _get_page_info(self, request):
        """
        Returns page info

        :param request:
        :rtype: PageInfo
        """
        return PageInfo(page=(int(request.args.get('page', 1))),
          page_size=(int(request.args.get('page_size', 10))))