# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/Paste-1.7.5.1-py2.6.egg/paste/util/looper.py
# Compiled at: 2012-02-27 07:41:58
__doc__ = "\nHelper for looping over sequences, particular in templates.\n\nOften in a loop in a template it's handy to know what's next up,\npreviously up, if this is the first or last item in the sequence, etc.\nThese can be awkward to manage in a normal Python loop, but using the\nlooper you can get a better sense of the context.  Use like::\n\n    >>> for loop, item in looper(['a', 'b', 'c']):\n    ...     print loop.number, item\n    ...     if not loop.last:\n    ...         print '---'\n    1 a\n    ---\n    2 b\n    ---\n    3 c\n\n"
__all__ = [
 'looper']

class looper(object):
    """
    Helper for looping (particularly in templates)
    
    Use this like::
    
        for loop, item in looper(seq):
            if loop.first:
                ...
    """

    def __init__(self, seq):
        self.seq = seq

    def __iter__(self):
        return looper_iter(self.seq)

    def __repr__(self):
        return '<%s for %r>' % (
         self.__class__.__name__, self.seq)


class looper_iter(object):

    def __init__(self, seq):
        self.seq = list(seq)
        self.pos = 0

    def __iter__(self):
        return self

    def next(self):
        if self.pos >= len(self.seq):
            raise StopIteration
        result = (
         loop_pos(self.seq, self.pos), self.seq[self.pos])
        self.pos += 1
        return result


class loop_pos(object):

    def __init__(self, seq, pos):
        self.seq = seq
        self.pos = pos

    def __repr__(self):
        return '<loop pos=%r at %r>' % (
         self.seq[pos], pos)

    def index(self):
        return self.pos

    index = property(index)

    def number(self):
        return self.pos + 1

    number = property(number)

    def item(self):
        return self.seq[self.pos]

    item = property(item)

    def next(self):
        try:
            return self.seq[(self.pos + 1)]
        except IndexError:
            return

        return

    next = property(next)

    def previous(self):
        if self.pos == 0:
            return None
        else:
            return self.seq[(self.pos - 1)]

    previous = property(previous)

    def odd(self):
        return not self.pos % 2

    odd = property(odd)

    def even(self):
        return self.pos % 2

    even = property(even)

    def first(self):
        return self.pos == 0

    first = property(first)

    def last(self):
        return self.pos == len(self.seq) - 1

    last = property(last)

    def length(self):
        return len(self.seq)

    length = property(length)

    def first_group(self, getter=None):
        """
        Returns true if this item is the start of a new group,
        where groups mean that some attribute has changed.  The getter
        can be None (the item itself changes), an attribute name like
        ``'.attr'``, a function, or a dict key or list index.
        """
        if self.first:
            return True
        return self._compare_group(self.item, self.previous, getter)

    def last_group(self, getter=None):
        """
        Returns true if this item is the end of a new group,
        where groups mean that some attribute has changed.  The getter
        can be None (the item itself changes), an attribute name like
        ``'.attr'``, a function, or a dict key or list index.
        """
        if self.last:
            return True
        return self._compare_group(self.item, self.next, getter)

    def _compare_group(self, item, other, getter):
        if getter is None:
            return item != other
        else:
            if isinstance(getter, basestring) and getter.startswith('.'):
                getter = getter[1:]
                if getter.endswith('()'):
                    getter = getter[:-2]
                    return getattr(item, getter)() != getattr(other, getter)()
                return getattr(item, getter) != getattr(other, getter)
            else:
                if callable(getter):
                    return getter(item) != getter(other)
                else:
                    return item[getter] != other[getter]
            return