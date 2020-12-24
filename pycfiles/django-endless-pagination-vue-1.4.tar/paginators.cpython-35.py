# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/martin/windows/Desarrollo/Python/django-endless-pagination-vue/bin/django-endless-pagination-vue/tests/endless_pagination/paginators.py
# Compiled at: 2016-11-21 17:40:01
# Size of source mod 2**32: 4255 bytes
"""Customized Django paginators."""
from __future__ import unicode_literals
from math import ceil
from django.core.paginator import EmptyPage, Page, PageNotAnInteger, Paginator

class CustomPage(Page):
    __doc__ = 'Handle different number of items on the first page.'

    def start_index(self):
        """Return the 1-based index of the first item on this page."""
        paginator = self.paginator
        if paginator.count == 0:
            return 0
        if self.number == 1:
            return 1
        return (self.number - 2) * paginator.per_page + paginator.first_page + 1

    def end_index(self):
        """Return the 1-based index of the last item on this page."""
        paginator = self.paginator
        if self.number == paginator.num_pages:
            return paginator.count
        return (self.number - 1) * paginator.per_page + paginator.first_page


class BasePaginator(Paginator):
    __doc__ = 'A base paginator class subclassed by the other real paginators.\n\n    Handle different number of items on the first page.\n    '

    def __init__(self, object_list, per_page, **kwargs):
        self._num_pages = None
        if 'first_page' in kwargs:
            self.first_page = kwargs.pop('first_page')
        else:
            self.first_page = per_page
        super(BasePaginator, self).__init__(object_list, per_page, **kwargs)

    def get_current_per_page(self, number):
        if number == 1:
            return self.first_page
        return self.per_page


class DefaultPaginator(BasePaginator):
    __doc__ = 'The default paginator used by this application.'

    def page(self, number):
        number = self.validate_number(number)
        if number == 1:
            bottom = 0
        else:
            bottom = (number - 2) * self.per_page + self.first_page
        top = bottom + self.get_current_per_page(number)
        if top + self.orphans >= self.count:
            top = self.count
        return CustomPage(self.object_list[bottom:top], number, self)

    def _get_num_pages(self):
        if self._num_pages is None:
            if self.count == 0 and not self.allow_empty_first_page:
                self._num_pages = 0
            else:
                hits = max(0, self.count - self.orphans - self.first_page)
                self._num_pages = int(ceil(hits / float(self.per_page))) + 1
            return self._num_pages

    num_pages = property(_get_num_pages)


class LazyPaginator(BasePaginator):
    __doc__ = 'Implement lazy pagination.'

    def validate_number(self, number):
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')

        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        number = self.validate_number(number)
        current_per_page = self.get_current_per_page(number)
        if number == 1:
            bottom = 0
        else:
            bottom = (number - 2) * self.per_page + self.first_page
        top = bottom + current_per_page
        objects = list(self.object_list[bottom:top + self.orphans + 1])
        objects_count = len(objects)
        if objects_count > current_per_page + self.orphans:
            self._num_pages = number + 1
            objects = objects[:current_per_page]
        else:
            if number != 1 and objects_count <= self.orphans:
                raise EmptyPage('That page contains no results')
            else:
                self._num_pages = number
        return CustomPage(objects, number, self)

    def _get_count(self):
        raise NotImplementedError

    count = property(_get_count)

    def _get_num_pages(self):
        return self._num_pages

    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        raise NotImplementedError

    page_range = property(_get_page_range)