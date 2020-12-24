# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/util/iter.py
# Compiled at: 2016-03-08 18:12:41
import six
from persistent import Persistent
from itertools import islice, count
from six.moves import zip as izip, map as imap
from cachetools import LRUCache
from zerodb.storage import prefetch

class Sliceable(object):

    def __init__(self, f, cache_size=1000, length=None):
        """
        Makes a sliceable, cached list-like interface to an iterator
        :param callable f: Function which inits the iterator
        """
        self.f = f
        self.cache = LRUCache(cache_size)
        self.stop = 0
        self.length = length
        self.iterator = iter(f())

    def __iter__(self):
        for i in count():
            y = self.__getitem__(i)
            yield y

    def dictify(self):
        for obj in self.__iter__():
            if hasattr(obj, '_p_activate'):
                obj._p_activate()
            yield {k:v for k, v in six.iteritems(obj.__dict__) if not k.startswith('_') if not k.startswith('_')}

    def __len__(self):
        if self.length is None:
            if hasattr(self.iterator, '__len__'):
                return len(self.iterator)
            else:
                return len(list(self.__iter__()))

        else:
            if callable(self.length):
                return self.length()
            else:
                return self.length

        return

    def __getitem__(self, key):
        try:
            if isinstance(key, int) and key >= 0:
                if key in self.cache:
                    return self.cache[key]
                if key < self.stop:
                    self.stop = 0
                    self.iterator = iter(self.f())
                delta = key - self.stop
                result = next(islice(self.iterator, delta, delta + 1))
                self.cache[key] = result
                self.stop = key + 1
                return result
            if isinstance(key, slice):
                if key.start is None and key.stop is None:
                    return list(self.f())
                else:
                    start = key.start or 0
                    step = key.step or 1
                    indexes = count(start, step)
                    index_upd = start
                    while (key.stop is None or index_upd < key.stop) and index_upd in self.cache:
                        index_upd += step

                    if index_upd < self.stop and (key.stop is None or index_upd < key.stop):
                        self.iterator = iter(self.f())
                        result = list(islice(self.iterator, start, key.stop, step))
                        for i, value in izip(indexes, result):
                            self.cache[i] = value

                        self.stop = i + 1 if key.stop is None else key.stop
                        return result
                    result = [ self.cache[i] for i in six.moves.xrange(start, index_upd, step) ]
                    if key.stop is None:
                        result_upd = list(islice(self.iterator, index_upd - self.stop, None, step))
                    else:
                        if index_upd < key.stop:
                            result_upd = list(islice(self.iterator, index_upd - self.stop, key.stop - self.stop, step))
                        else:
                            result_upd = []
                        for i, value in izip(indexes, result_upd):
                            self.cache[i] = value

                    self.stop = key.stop
                    return result + result_upd

            else:
                raise KeyError(('Key must be non-negative integer or slice, not {}').format(key))
        except StopIteration:
            self.iterator = self.f()
            self.stop = 0
            raise

        return

    def __repr__(self):
        """ Visually appealing output showing first 5 elements of the data """
        first_el = self[:6]
        is_long = len(first_el) > 5
        reprs = [ i.__repr__() for i in first_el[:5] ]
        if is_long:
            reprs.append('...')
        if len(reprs) <= 1:
            return '[' + ('').join(reprs) + ']'
        else:
            l = len(reprs)
            out = []
            for i, s in enumerate(reprs):
                if i == 0:
                    s = '[' + s
                else:
                    s = ' ' + s
                if i == l - 1:
                    s = s + ']'
                else:
                    s = s + ','
                out.append(s)

            return ('\n').join(out)

    def __unicode__(self):
        return self.__repr__()


class DBList(Sliceable):

    def __init__(self, query_f, db, **kw):
        """
        :param function query_f: Function which returns results of the query in format (size, uids)
        :param zerodb.DB db: Currend DB instance
        """
        self.db = db

        def get_object(uid):
            obj = db._objects[uid]
            obj._p_uid = uid
            return obj

        def f():
            self.length, it = query_f()
            return imap(get_object, it)

        super(DBList, self).__init__(f, **kw)


class ListPrefetch(Sliceable):
    prefetch_size = 20

    def __getitem__(self, key):
        previous_stop = self.stop
        result = super(ListPrefetch, self).__getitem__(key)
        if self.stop != previous_stop:
            try:
                if isinstance(key, six.integer_types):
                    tail = super(ListPrefetch, self).__getitem__(slice(key + 1, key + self.prefetch_size + 1))
                elif isinstance(key, slice):
                    if key.stop:
                        tail = super(ListPrefetch, self).__getitem__(slice(key.stop + 1, key.stop + self.prefetch_size + 1))
                    else:
                        tail = []
            except StopIteration:
                tail = []

            if isinstance(result, list):
                prefetch(result + tail)
            elif isinstance(result, Persistent):
                prefetch([result] + tail)
        return result


class DBListPrefetch(ListPrefetch, DBList):

    def __init__(self, query_f, db, **kw):
        DBList.__init__(self, query_f, db, **kw)