# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/underdog/github/api-pagination/api_pagination/__init__.py
# Compiled at: 2015-04-24 21:19:11
from math import ceil

class Paginator(object):

    def __init__(self, total, items_per_page):
        """
        Constructor for pagination class

        :param int total: Count of items we are paginating
        :param int items_per_page: How many items to place on each page
        """
        self.total = total
        self.items_per_page = items_per_page

    def get_page_count(self):
        """
        Calculates the amount of pages that exist

        Note: If your data has 0 items per page, you will receive a `ZeroDivisionError`

        :rtype: int
        :returns: Overall amount of pages (e.g. total=50, items_per_page=10 -> 5 pages)
        """
        return int(ceil(float(self.total) / float(self.items_per_page)))

    def get_page_info(self, page):
        """
        Collect information for a given page

        :param int page: Page to get info for
        :rtype: dict
        :returns: Informtation about requested page
            Signature should be `{
                overall: {first_page, last_page, pages, total},
                page: {current_page, next_page, previous_page}
            }`
        """
        page_count = self.get_page_count()
        first_page = 1
        last_page = page_count if page_count else first_page
        previous_page = None
        if page > first_page:
            previous_page = page - 1
            if previous_page > last_page:
                previous_page = last_page
        next_page = None
        if page < last_page:
            next_page = page + 1
            if next_page < first_page:
                next_page = first_page
        return {'overall': {'first_page': first_page, 
                       'last_page': last_page, 
                       'pages': page_count, 
                       'total': self.total}, 
           'page': {'current_page': page, 
                    'next_page': next_page, 
                    'previous_page': previous_page}}

    @classmethod
    def page_info(cls, page, *args, **kwargs):
        """
        Helper to retrieve pagination for a single page

        :param int page: Page to retrieve info for
        :param *args: Params to pass through to `get_page`
        :param **kwargs: Params to pass through to `get_page`
        :returns: Returns same as `get_page`
        """
        paginator = cls(*args, **kwargs)
        return paginator.get_page_info(page)