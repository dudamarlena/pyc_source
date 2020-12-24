# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pagination/paginator.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 5771 bytes
from django.core.paginator import Paginator, Page, PageNotAnInteger, EmptyPage

class InfinitePaginator(Paginator):
    __doc__ = "\n    Paginator designed for cases when it's not important to know how many total\n    pages.  This is useful for any object_list that has no count() method or can\n    be used to improve performance for MySQL by removing counts.\n\n    The orphans parameter has been removed for simplicity and there's a link\n    template string for creating the links to the next and previous pages.\n    "

    def __init__(self, object_list, per_page, allow_empty_first_page=True, link_template='/page/%d/'):
        orphans = 0
        super(InfinitePaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)
        del self._num_pages
        del self._count
        self.link_template = link_template

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except ValueError:
            raise PageNotAnInteger('That page number is not an integer')

        if number < 1:
            raise EmptyPage('That page number is less than 1')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        page_items = self.object_list[bottom:top]
        if not page_items:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return InfinitePage(page_items, number, self)

    def _get_count(self):
        """
        Returns the total number of objects, across all pages.
        """
        raise NotImplementedError

    count = property(_get_count)

    def _get_num_pages(self):
        """
        Returns the total number of pages.
        """
        raise NotImplementedError

    num_pages = property(_get_num_pages)

    def _get_page_range(self):
        """
        Returns a 1-based range of pages for iterating through within
        a template for loop.
        """
        raise NotImplementedError

    page_range = property(_get_page_range)


class InfinitePage(Page):

    def __repr__(self):
        return '<Page %s>' % self.number

    def has_next(self):
        """
        Checks for one more item than last on this page.
        """
        try:
            next_item = self.paginator.object_list[(self.number * self.paginator.per_page)]
        except IndexError:
            return False
        else:
            return True

    def end_index(self):
        """
        Returns the 1-based index of the last object on this page,
        relative to total objects found (hits).
        """
        return (self.number - 1) * self.paginator.per_page + len(self.object_list)

    def next_link(self):
        if self.has_next():
            return self.paginator.link_template % (self.number + 1)

    def previous_link(self):
        if self.has_previous():
            return self.paginator.link_template % (self.number - 1)


class FinitePaginator(InfinitePaginator):
    __doc__ = "\n    Paginator for cases when the list of items is already finite.\n\n    A good example is a list generated from an API call. This is a subclass\n    of InfinitePaginator because we have no idea how many items exist in the\n    full collection.\n\n    To accurately determine if the next page exists, a FinitePaginator MUST be\n    created with an object_list_plus that may contain more items than the\n    per_page count.  Typically, you'll have an object_list_plus with one extra\n    item (if there's a next page).  You'll also need to supply the offset from\n    the full collection in order to get the page start_index.\n\n    This is a very silly class but useful if you love the Django pagination\n    conventions.\n    "

    def __init__(self, object_list_plus, per_page, offset=None, allow_empty_first_page=True, link_template='/page/%d/'):
        super(FinitePaginator, self).__init__(object_list_plus, per_page, allow_empty_first_page, link_template)
        self.offset = offset

    def validate_number(self, number):
        super(FinitePaginator, self).validate_number(number)
        if not self.object_list:
            if number == 1 and self.allow_empty_first_page:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def page(self, number):
        """
        Returns a Page object for the given 1-based page number.
        """
        number = self.validate_number(number)
        page_items = self.object_list[:self.per_page]
        return FinitePage(page_items, number, self)


class FinitePage(InfinitePage):

    def has_next(self):
        """
        Checks for one more item than last on this page.
        """
        try:
            next_item = self.paginator.object_list[self.paginator.per_page]
        except IndexError:
            return False
        else:
            return True

    def start_index(self):
        """
        Returns the 1-based index of the first object on this page,
        relative to total objects in the paginator.
        """
        return self.paginator.offset