# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\todopy\filter.py
# Compiled at: 2011-12-15 09:18:51


class StringFilter(object):
    r"""Filter todo model based on a string.

    Only those todos that the string matches are passed thru the filter.

    >>> from model import Model
    >>> m = Model()
    >>> m.extend(["My first todo", "My second todo", u'Meikän unicode-todo'])
    >>> f = StringFilter("second", m)
    >>> len(f)
    1
    >>> f.total()
    3
    >>> list([t.todo for t in f])
    ['My second todo']
    >>> f = StringFilter("todo", m)
    >>> len(f)
    3
    >>> list([t.todo for t in f])
    ['My first todo', 'My second todo', u'Meik\xc3\xa4n unicode-todo']
    >>> f = StringFilter('first', StringFilter('todo', m))
    >>> len(f)
    1
    >>> f.total()
    3
    >>> list([t.todo for t in f])
    ['My first todo']
    """

    def __init__(self, string, model):
        self.string = string
        self.model = model

    @staticmethod
    def find_as_utf8(needle, haystack):
        needle = unicode(needle) if type(needle) != unicode else needle
        haystack = unicode(haystack) if type(haystack) != unicode else haystack
        return needle in haystack

    def __iter__(self):

        class Iter(object):

            def __init__(self, filter):
                self.filter = filter
                self.iter = iter(self.filter.model)

            def __iter__(self):
                return self

            def next(self):
                candidate = self.iter.next()
                while not StringFilter.find_as_utf8(self.filter.string, candidate.todo):
                    candidate = self.iter.next()

                return candidate

        return Iter(self)

    def __len__(self):
        return len(list([ x for x in self.model if StringFilter.find_as_utf8(self.string, x.todo) ]))

    def total(self):
        return self.model.total()