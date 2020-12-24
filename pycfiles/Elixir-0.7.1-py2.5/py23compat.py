# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/elixir/py23compat.py
# Compiled at: 2009-10-02 06:19:50
try:
    set = set
except NameError:
    from sets import Set as set

orig_cmp = cmp

def sort_list(l, cmp=None, key=None, reverse=False):
    try:
        l.sort(cmp, key, reverse)
    except TypeError, e:
        if not str(e).startswith('sort expected at most 1 arguments'):
            raise
        if cmp is None:
            cmp = orig_cmp
        if key is not None:
            cmp = lambda self, other, cmp=cmp: cmp(key(self), key(other))
        if reverse:
            cmp = lambda self, other, cmp=cmp: -cmp(self, other)
        l.sort(cmp)

    return


try:
    sorted = sorted
except NameError:

    def sorted(l, cmp=None, key=None, reverse=False):
        sorted_list = list(l)
        sort_list(sorted_list, cmp, key, reverse)
        return sorted_list


try:
    ('').rsplit

    def rsplit(s, delim, maxsplit):
        return s.rsplit(delim, maxsplit)


except AttributeError:

    def rsplit(s, delim, maxsplit):
        """Return a list of the words of the string s, scanning s
        from the end. To all intents and purposes, the resulting
        list of words is the same as returned by split(), except
        when the optional third argument maxsplit is explicitly
        specified and nonzero. When maxsplit is nonzero, at most
        maxsplit number of splits - the rightmost ones - occur,
        and the remainder of the string is returned as the first
        element of the list (thus, the list will have at most
        maxsplit+1 elements). New in version 2.4.
        >>> rsplit('foo.bar.baz', '.', 0)
        ['foo.bar.baz']
        >>> rsplit('foo.bar.baz', '.', 1)
        ['foo.bar', 'baz']
        >>> rsplit('foo.bar.baz', '.', 2)
        ['foo', 'bar', 'baz']
        >>> rsplit('foo.bar.baz', '.', 99)
        ['foo', 'bar', 'baz']
        """
        assert maxsplit >= 0
        if maxsplit == 0:
            return [s]
        items = s.split(delim)
        if maxsplit < len(items):
            items[:(-maxsplit)] = [
             delim.join(items[:-maxsplit])]
        return items