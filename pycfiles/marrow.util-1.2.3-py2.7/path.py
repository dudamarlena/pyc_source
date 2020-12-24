# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/marrow/util/path.py
# Compiled at: 2012-10-11 17:43:38
import collections
from marrow.util.compat import binary, unicode
try:
    from urlparse import urlparse
    from urllib import quote_plus, unquote_plus
except ImportError:
    from urllib.parse import urlparse, quote_plus, unquote_plus

__all__ = [
 'Path']

class Path(collections.deque):

    def __init__(self, value=None, separator='/', encoded=False):
        self.separator = unicode(separator)
        super(Path, self).__init__()
        if value is not None:
            self._assign(value, encoded)
        return

    def _assign(self, value, encoded=False):
        self.clear()
        if value is None:
            return
        else:
            if isinstance(value, (binary, unicode)):
                self.extend((unquote_plus(i) if encoded else i) for i in unicode(value).split(self.separator))
                return
            self.extend(value)
            return

    def __set__(self, obj, value):
        self._assign(value)

    def __str__(self):
        return self.separator.join(quote_plus(i) for i in self)

    def __unicode__(self):
        return unicode(self.separator).join(self)

    def __add__(self, other):
        return self.__class__(unicode(self) + unicode(other))

    def __repr__(self):
        return '<Path %r>' % super(Path, self).__repr__()

    def __cmp__(self, other):
        """Perform type coersion and attempt to compare.
        
        This works for most builtin types that accept an iterable as
        the first argument, e.g. list, tuple, and set, and will work
        for str and unicode, too.
        """
        return cmp(type(other)(self), other)

    def __eq__(self, other):
        if isinstance(other, (binary, unicode)):
            return unicode(self) == unicode(other)
        return list(self) == list(other)

    def __getitem__(self, i):
        try:
            return super(Path, self).__getitem__(i)
        except TypeError:
            return Path([ self[j] for j in range(*i.indices(len(self))) ])

    def __abs__(self):
        if self[0] != '':
            return Path([''] + list(self))
        return self