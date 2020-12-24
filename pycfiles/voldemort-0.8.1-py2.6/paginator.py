# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/voldemort/paginator.py
# Compiled at: 2014-01-24 01:38:29
import math

class Paginator(object):

    def __init__(self, posts, paginate=5):
        self.__posts = posts
        self.__paginate = paginate
        self.rewind()

    def rewind(self):
        self.__paginate_start = 0 - self.__paginate
        self.__paginate_end = 0
        self.__total_pages = int(math.ceil(float(len(self.__posts)) / float(self.__paginate)))
        self.__current_page = 0

    @property
    def posts(self):
        return self.__posts[self.__paginate_start:self.__paginate_end]

    @property
    def current_page(self):
        return self.__current_page

    @property
    def next_page(self):
        if self.__current_page == self.__total_pages:
            return
        else:
            return self.__current_page + 1
            return

    @property
    def previous_page(self):
        if self.__current_page == 1:
            return
        else:
            return self.__current_page - 1
            return

    @property
    def current_page(self):
        return self.__current_page

    @property
    def total_pages(self):
        return self.__total_pages

    def next(self):
        if self.__current_page < self.__total_pages:
            self.__paginate_start = self.__paginate_end
            self.__paginate_end += self.__paginate
            self.__current_page += 1
            return self
        raise StopIteration

    def __iter__(self):
        return self

    def __repr__(self):
        return 'POSTS FROM %d to %d. PAGE NO: %d TOTAL: %d PREV: %s NEXT: %s' % (
         self.__paginate_start,
         self.__paginate_end,
         self.__current_page,
         self.__total_pages,
         self.previous_page,
         self.next_page)