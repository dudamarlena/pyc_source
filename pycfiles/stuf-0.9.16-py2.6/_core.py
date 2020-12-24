# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/stuf/_core.py
# Compiled at: 2014-12-21 02:23:28
"""some core stuf."""
from itertools import chain
from collections import MutableMapping
from operator import methodcaller, attrgetter
from .desc import lazy_class, lazy
from .collects import recursive_repr
from .deep import clsname, getcls, clsdict
from .six import getvalues, getitems, getkeys
from .iterable import exhaustcall, exhaustmap
wraps = attrgetter('_wrapped')
delitem = attrgetter('_wrapped.__delitem__')
getitem = attrgetter('_wrapped.__getitem__')
setitem = attrgetter('_wrapped.__setitem__')
length = attrgetter('_wrapped.__len__')
_iter = attrgetter('_wrapped.__iter__')
asdict = attrgetter('_wrapped._asdict')
_reserved = ('allowed _wrapped _map').split()

class baseread(object):

    def __getattr__(self, key, _getter=object.__getattribute__):
        if key == 'iteritems':
            return getitems(self)
        if key == 'iterkeys':
            return getkeys(self)
        if key == 'itervalues':
            return getvalues(self)
        try:
            return self[key]
        except KeyError:
            return _getter(self, key)

    @recursive_repr()
    def __repr__(self):
        items = methodcaller('items')(self)
        kwstr = (', ').join(('{0!s}={1!r}').format(*item) for item in items)
        return ('{0}({1})').format(clsname(self), kwstr)

    @lazy_class
    def _classkeys(self):
        return frozenset(chain(iter(vars(self)), iter(vars(getcls(self))), _reserved))


class basewrite(baseread):

    def __setattr__(self, key, value):
        if key == '_classkeys' or key in self._classkeys:
            clsdict(self)[key] = value
        else:
            try:
                self[key] = value
            except KeyError:
                raise AttributeError(key)

    def __delattr__(self, key):
        if not key == '_classkeys' or key in self._classkeys:
            try:
                del self[key]
            except KeyError:
                raise AttributeError(key)


class corestuf(baseread):
    _map = dict

    def _build(self, iterable):
        try:
            kw = self._map()
            exhaustcall(kw.update, iterable)
        except ValueError:
            kw.update(iterable)

        return kw

    def _mapping(self, iterable):
        return self._map(iterable)

    def _new(self, iterable):
        return getcls(self)(self._build(iterable))

    def _prepop(self, *args, **kw):
        kw.update(self._build(args))
        return kw

    def _pop(self, past, future):

        def closure(key, value, new=self._new):
            try:
                if not hasattr(value, 'capitalize'):
                    trial = new(value)
                    value = trial if trial else value
            except (TypeError, IOError):
                pass

            future[key] = value

        exhaustmap(closure, past)
        return self._postpop(future)

    def _postpop(self, future):
        return future

    def copy(self):
        return self._new(dict(self))


class writestuf(corestuf, basewrite):

    def update(self, *args, **kw):
        self._pop(self._prepop(*args, **kw), self)


class wrapstuf(corestuf):

    def __init__(self, *args, **kw):
        super(wrapstuf, self).__init__()
        self._wrapped = self._pop(self._prepop(*args, **kw), self._map())

    def _postpop(self, future):
        return self._mapping(future)


class writewrapstuf(wrapstuf, writestuf, MutableMapping):

    @lazy
    def __getitem__(self):
        return getitem(self)

    @lazy
    def __setitem__(self):
        return setitem(self)

    @lazy
    def __delitem__(self):
        return delitem(self)

    @lazy
    def __iter__(self):
        return _iter(self)

    @lazy
    def __len__(self):
        return length(self)

    def __reduce__(self):
        return (
         getcls(self), (wraps(self).copy(),))