# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/utils/pagination.py
# Compiled at: 2018-07-30 04:16:25
# Size of source mod 2**32: 13318 bytes
import math
from functools import reduce
from django.core.paginator import Paginator, QuerySetPaginator, Page, InvalidPage, PageNotAnInteger, EmptyPage
__all__ = ('InvalidPage', 'ExPaginator', 'DiggPaginator', 'QuerySetDiggPaginator')

class ExPage(Page):

    def page_to_json(self):
        return {'paginator':{'count':self.paginator.count, 
          'num_pages':self.paginator.num_pages}, 
         'page_range':self.page_range, 
         'has_next':self.has_next(), 
         'has_previous':self.has_previous(), 
         'has_other_pages':self.has_other_pages(), 
         'next_page_number':self.next_page_number() if self.has_next() else None, 
         'previous_page_number':self.previous_page_number() if self.has_previous() else None, 
         'start_index':self.start_index(), 
         'end_index':self.end_index(), 
         'number':self.number}


class ExPaginator(Paginator):
    __doc__ = 'Adds a ``softlimit`` option to ``page()``. If True, querying a\n    page number larger than max. will not fail, but instead return the\n    last available page.\n\n    This is useful when the data source can not provide an exact count\n    at all times (like some search engines), meaning the user could\n    possibly see links to invalid pages at some point which we wouldn\'t\n    want to fail as 404s.\n\n    >>> items = range(1, 1000)\n    >>> paginator = ExPaginator(items, 10)\n    >>> paginator.page(1000)\n    Traceback (most recent call last):\n    InvalidPage: That page contains no results\n    >>> paginator.page(1000, softlimit=True)\n    <Page 100 of 100>\n\n    # [bug] graceful handling of non-int args\n    >>> paginator.page("str")\n    Traceback (most recent call last):\n    InvalidPage: That page number is not an integer\n    '

    def _ensure_int(self, num, e):
        try:
            return int(num)
        except ValueError:
            raise e

    def _get_page(self, *args, **kwargs):
        return ExPage(*args, **kwargs)

    def page(self, number, softlimit=False):
        try:
            return super(ExPaginator, self).page(number)
        except InvalidPage as e:
            number = self._ensure_int(number, e)
            if number > self.num_pages:
                if softlimit:
                    return self.page((self.num_pages), softlimit=False)
            raise e


class DiggPaginator(ExPaginator):
    __doc__ = '\n    Based on Django\'s default paginator, it adds "Digg-style" page ranges\n    with a leading block of pages, an optional middle block, and another\n    block at the end of the page range. They are available as attributes\n    on the page:\n\n    {# with: page = digg_paginator.page(1) #}\n    {% for num in page.leading_range %} ...\n    {% for num in page.main_range %} ...\n    {% for num in page.trailing_range %} ...\n\n    Additionally, ``page_range`` contains a nun-numeric ``False`` element\n    for every transition between two ranges.\n\n    {% for num in page.page_range %}\n        {% if not num %} ...  {# literally output dots #}\n        {% else %}{{ num }}\n        {% endif %}\n    {% endfor %}\n\n    Additional arguments passed to the constructor allow customization of\n    how those bocks are constructed:\n\n    body=5, tail=2\n\n    [1] 2 3 4 5 ... 91 92\n    |_________|     |___|\n    body            tail\n              |_____|\n              margin\n\n    body=5, tail=2, padding=2\n\n    1 2 ... 6 7 [8] 9 10 ... 91 92\n            |_|     |__|\n             ^padding^\n    |_|     |__________|     |___|\n    tail    body             tail\n\n    ``margin`` is the minimum number of pages required between two ranges; if\n    there are less, they are combined into one.\n\n    When ``align_left`` is set to ``True``, the paginator operates in a\n    special mode that always skips the right tail, e.g. does not display the\n    end block unless necessary. This is useful for situations in which the\n    exact number of items/pages is not actually known.\n\n    # odd body length\n    >>> print DiggPaginator(range(1,1000), 10, body=5).page(1)\n    1 2 3 4 5 ... 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=5).page(100)\n    1 2 ... 96 97 98 99 100\n\n    # even body length\n    >>> print DiggPaginator(range(1,1000), 10, body=6).page(1)\n    1 2 3 4 5 6 ... 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=6).page(100)\n    1 2 ... 95 96 97 98 99 100\n\n    # leading range and main range are combined when close; note how\n    # we have varying body and padding values, and their effect.\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=2, margin=2).page(3)\n    1 2 3 4 5 ... 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=6, padding=2, margin=2).page(4)\n    1 2 3 4 5 6 ... 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=1, margin=2).page(6)\n    1 2 3 4 5 6 7 ... 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=2, margin=2).page(7)\n    1 2 ... 5 6 7 8 9 ... 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=1, margin=2).page(7)\n    1 2 ... 5 6 7 8 9 ... 99 100\n\n    # the trailing range works the same\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=2, margin=2, ).page(98)\n    1 2 ... 96 97 98 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=6, padding=2, margin=2, ).page(97)\n    1 2 ... 95 96 97 98 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=1, margin=2, ).page(95)\n    1 2 ... 94 95 96 97 98 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=2, margin=2, ).page(94)\n    1 2 ... 92 93 94 95 96 ... 99 100\n    >>> print DiggPaginator(range(1,1000), 10, body=5, padding=1, margin=2, ).page(94)\n    1 2 ... 92 93 94 95 96 ... 99 100\n\n    # all three ranges may be combined as well\n    >>> print DiggPaginator(range(1,151), 10, body=6, padding=2).page(7)\n    1 2 3 4 5 6 7 8 9 ... 14 15\n    >>> print DiggPaginator(range(1,151), 10, body=6, padding=2).page(8)\n    1 2 3 4 5 6 7 8 9 10 11 12 13 14 15\n    >>> print DiggPaginator(range(1,151), 10, body=6, padding=1).page(8)\n    1 2 3 4 5 6 7 8 9 ... 14 15\n\n    # no leading or trailing ranges might be required if there are only\n    # a very small number of pages\n    >>> print DiggPaginator(range(1,80), 10, body=10).page(1)\n    1 2 3 4 5 6 7 8\n    >>> print DiggPaginator(range(1,80), 10, body=10).page(8)\n    1 2 3 4 5 6 7 8\n    >>> print DiggPaginator(range(1,12), 10, body=5).page(1)\n    1 2\n\n    # test left align mode\n    >>> print DiggPaginator(range(1,1000), 10, body=5, align_left=True).page(1)\n    1 2 3 4 5\n    >>> print DiggPaginator(range(1,1000), 10, body=5, align_left=True).page(50)\n    1 2 ... 48 49 50 51 52\n    >>> print DiggPaginator(range(1,1000), 10, body=5, align_left=True).page(97)\n    1 2 ... 95 96 97 98 99\n    >>> print DiggPaginator(range(1,1000), 10, body=5, align_left=True).page(100)\n    1 2 ... 96 97 98 99 100\n\n    # padding: default value\n    >>> DiggPaginator(range(1,1000), 10, body=10).padding\n    4\n\n    # padding: automatic reduction\n    >>> DiggPaginator(range(1,1000), 10, body=5).padding\n    2\n    >>> DiggPaginator(range(1,1000), 10, body=6).padding\n    2\n\n    # padding: sanity check\n    >>> DiggPaginator(range(1,1000), 10, body=5, padding=3)\n    Traceback (most recent call last):\n    ValueError: padding too large for body (max 2)\n    '

    def __init__(self, *args, **kwargs):
        self.body = kwargs.pop('body', 10)
        self.tail = kwargs.pop('tail', 2)
        self.align_left = kwargs.pop('align_left', False)
        self.margin = kwargs.pop('margin', 4)
        max_padding = int(math.ceil(self.body / 2.0) - 1)
        self.padding = kwargs.pop('padding', min(4, max_padding))
        if self.padding > max_padding:
            raise ValueError('padding too large for body (max %d)' % max_padding)
        (super().__init__)(*args, **kwargs)

    def get_queryset_for_instance(self, instance_pk):
        try:
            instance_pk = int(instance_pk)
            if hasattr(self.object_list, 'values_list'):
                if callable(self.object_list.values_list):
                    instance_pk_list = list(self.object_list.values_list('pk', flat=True))
            else:
                instance_pk_list = [o.pk for o in self.object_list]
            object_index = instance_pk_list.index(instance_pk)
            page = int(math.ceil(float(object_index + 1) / self.per_page))
        except (ValueError, AttributeError, TypeError):
            page = 1

        return self.get_queryset_for_page(page)

    def get_queryset_for_page(self, page=1):
        if page is None:
            page = 1
        else:
            try:
                page = int(page)
            except (ValueError, TypeError) as e:
                page = 1

        try:
            queryset = self.page(page)
        except PageNotAnInteger:
            queryset = self.page(1)
        except EmptyPage:
            queryset = self.page(self.num_pages)

        return queryset

    def page(self, number, *args, **kwargs):
        page = (super().page)(number, *args, **kwargs)
        number = int(number)
        num_pages, body, tail, padding, margin = (
         self.num_pages, self.body, self.tail, self.padding, self.margin)
        main_range = list(map(int, [
         math.floor(number - body / 2.0) + 1,
         math.floor(number + body / 2.0)]))
        if main_range[0] < 1:
            main_range = list(map(abs(main_range[0] - 1).__add__, main_range))
        elif main_range[1] > num_pages:
            main_range = list(map((num_pages - main_range[1]).__add__, main_range))
        else:
            if main_range[0] <= tail + margin:
                leading = []
                main_range = [
                 1, max(body, min(number + padding, main_range[1]))]
                main_range[0] = 1
            else:
                leading = list(range(1, tail + 1))
            if self.align_left:
                trailing = []
            else:
                if main_range[1] >= num_pages - (tail + margin) + 1:
                    trailing = []
                    if not leading:
                        main_range = [
                         1, num_pages]
                    else:
                        main_range = [
                         min(num_pages - body + 1, max(number - padding, main_range[0])), num_pages]
                else:
                    trailing = list(range(num_pages - tail + 1, num_pages + 1))
        main_range = [
         max(main_range[0], 1), min(main_range[1], num_pages) - 1]
        page.main_range = list(range(main_range[0], main_range[1] + 2))
        page.leading_range = leading
        page.trailing_range = trailing
        page.page_range = reduce(lambda x, y: x + (x and y and [False]) + y, [
         page.leading_range, page.main_range, page.trailing_range])
        page.__class__ = DiggPage
        return page


class DiggPage(ExPage):

    def __str__(self):
        return ' ... '.join(filter(None, [
         ' '.join(map(str, self.leading_range)),
         ' '.join(map(str, self.main_range)),
         ' '.join(map(str, self.trailing_range))]))


class QuerySetDiggPaginator(DiggPaginator, QuerySetPaginator):
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()

class Paginator(DiggPaginator):
    pass