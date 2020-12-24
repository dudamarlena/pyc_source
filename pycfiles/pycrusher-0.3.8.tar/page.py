# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/page.py
# Compiled at: 2017-01-13 23:45:16
import six
from .utils import safe_int
from .pageitem import PageItem
from .relationship import Relationship

@six.python_2_unicode_compatible
class Page(Relationship):
    """A Page represents a a page of results returned by CrunchBase.
    Page contains useful information regarding how many items there are
    in total (total_items), items per page (items_per_page), etc.

    A page contains information for going to the prev/next page (if available).

    The data that is used to initialize a Page looks like this::

        "data": {
            "paging": {
                "items_per_page": 1000,
                "current_page": 1,
                "number_of_pages": 1,
                "next_page_url": null,
                "prev_page_url": null,
                "total_items": 1,
                "sort_order": "custom"
            },
            "items": [
             {
                "properties": {
                    "path": "organization/example",
                    "name": "Example",
                    "updated_at": 1423666090,
                    "created_at": 1371717055,
                 },
                 "type": "Organization",
                 "uuid": "uuid"
             }
            ]
        }
    """

    def __init__(self, name, data):
        self.name = name
        paging = data.get('paging')
        self.total_items = safe_int(paging.get('total_items')) or 0
        self.first_page_url = paging.get('first_page_url')
        self.sort_order = paging.get('sort_order')
        self.next_page_url = paging.get('next_page_url')
        self.prev_page_url = paging.get('prev_page_url')
        self.items_per_page = safe_int(paging.get('items_per_page'))
        self.current_page = paging.get('current_page') or 0
        self.number_of_pages = safe_int(paging.get('number_of_pages')) or 0
        self.items = [ PageItem.build(item) for item in data.get('items') ]

    def __str__(self):
        return ('Page {name} {current}/{pages} Per Page: {per_page} Total items: {total}').format(name=self.name, current=self.current_page, pages=self.number_of_pages, per_page=self.items_per_page, total=self.total_items)

    def __repr__(self):
        return self.__str__()