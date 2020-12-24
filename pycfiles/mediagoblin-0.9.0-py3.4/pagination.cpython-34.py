# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/pagination.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 3910 bytes
import urllib, copy
from math import ceil, floor
from itertools import count
from werkzeug.datastructures import MultiDict
from six.moves import zip
PAGINATION_DEFAULT_PER_PAGE = 30

class Pagination(object):
    __doc__ = '\n    Pagination class for database queries.\n\n    Initialization through __init__(self, cursor, page=1, per_page=2),\n    get actual data slice through __call__().\n    '

    def __init__(self, page, cursor, per_page=PAGINATION_DEFAULT_PER_PAGE, jump_to_id=False):
        """
        Initializes Pagination

        Args:
         - page: requested page
         - per_page: number of objects per page
         - cursor: db cursor
         - jump_to_id: object id, sets the page to the page containing the
           object with id == jump_to_id.
        """
        self.page = page
        self.per_page = per_page
        self.cursor = cursor
        self.total_count = self.cursor.count()
        self.active_id = None
        if jump_to_id:
            cursor = copy.copy(self.cursor)
            for doc, increment in list(zip(cursor, count(0))):
                if doc.id == jump_to_id:
                    self.page = 1 + int(floor(increment / self.per_page))
                    self.active_id = jump_to_id
                    break

    def __call__(self):
        """
        Returns slice of objects for the requested page
        """
        return self.cursor.slice((self.page - 1) * self.per_page, self.page * self.per_page)

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or num > self.page - left_current - 1 and num < self.page + right_current or num > self.pages - right_edge:
                if last + 1 != num:
                    yield
                yield num
                last = num
                continue

    def get_page_url_explicit(self, base_url, get_params, page_no):
        """
        Get a page url by adding a page= parameter to the base url
        """
        if isinstance(get_params, MultiDict):
            new_get_params = get_params.to_dict()
        else:
            new_get_params = dict(get_params) or {}
        new_get_params['page'] = page_no
        return '%s?%s' % (
         base_url, urllib.urlencode(new_get_params))

    def get_page_url(self, request, page_no):
        """
        Get a new page url based of the request, and the new page number.

        This is a nice wrapper around get_page_url_explicit()
        """
        return self.get_page_url_explicit(request.full_path, request.GET, page_no)