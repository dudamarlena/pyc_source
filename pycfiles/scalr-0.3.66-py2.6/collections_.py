# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/scalrtools/collections_.py
# Compiled at: 2015-05-22 06:53:03
from operator import itemgetter as _itemgetter
from keyword import iskeyword as _iskeyword
from _abcoll import MutableMapping

def namedtuple(typename, field_names, verbose=False, rename=False):
    """Returns a new subclass of tuple with named fields.

    >>> Point = namedtuple('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # indexable like a plain tuple
    33
    >>> x, y = p                        # unpack like a regular tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p._asdict()                 # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p._replace(x=100)               # _replace() is like str.replace() but targets named fields
    Point(x=100, y=22)

    """
    if isinstance(field_names, basestring):
        field_names = field_names.replace(',', ' ').split()
    field_names = tuple(map(str, field_names))
    if rename:
        names = list(field_names)
        seen = set()
        for (i, name) in enumerate(names):
            if not min(c.isalnum() or c == '_' for c in name) or _iskeyword(name) or not name or name[0].isdigit() or name.startswith('_') or name in seen:
                names[i] = '_%d' % i
            seen.add(name)

        field_names = tuple(names)
    for name in (typename,) + field_names:
        if not min(c.isalnum() or c == '_' for c in name):
            raise ValueError('Type names and field names can only contain alphanumeric characters and underscores: %r' % name)
        if _iskeyword(name):
            raise ValueError('Type names and field names cannot be a keyword: %r' % name)
        if name[0].isdigit():
            raise ValueError('Type names and field names cannot start with a number: %r' % name)

    seen_names = set()
    for name in field_names:
        if name.startswith('_') and not rename:
            raise ValueError('Field names cannot start with an underscore: %r' % name)
        if name in seen_names:
            raise ValueError('Encountered duplicate field name: %r' % name)
        seen_names.add(name)

    numfields = len(field_names)
    argtxt = repr(field_names).replace("'", '')[1:-1]
    reprtxt = (', ').join('%s=%%r' % name for name in field_names)
    template = "class %(typename)s(tuple):\n        '%(typename)s(%(argtxt)s)' \n\n        __slots__ = () \n\n        _fields = %(field_names)r \n\n        def __new__(_cls, %(argtxt)s):\n            return _tuple.__new__(_cls, (%(argtxt)s)) \n\n        @classmethod\n        def _make(cls, iterable, new=tuple.__new__, len=len):\n            'Make a new %(typename)s object from a sequence or iterable'\n            result = new(cls, iterable)\n            if len(result) != %(numfields)d:\n                raise TypeError('Expected %(numfields)d arguments, got %%d' %% len(result))\n            return result \n\n        def __repr__(self):\n            return '%(typename)s(%(reprtxt)s)' %% self \n\n        def _asdict(self):\n            'Return a new dict which maps field names to their values'\n            return dict(zip(self._fields, self)) \n\n        def _replace(_self, **kwds):\n            'Return a new %(typename)s object replacing specified fields with new values'\n            result = _self._make(map(kwds.pop, %(field_names)r, _self))\n            if kwds:\n                raise ValueError('Got unexpected field names: %%r' %% kwds.keys())\n            return result \n\n        def __getnewargs__(self):\n            return tuple(self) \n\n" % locals()
    for (i, name) in enumerate(field_names):
        template += '        %s = _property(_itemgetter(%d))\n' % (name, i)

    if verbose:
        print template
    namespace = dict(_itemgetter=_itemgetter, __name__='namedtuple_%s' % typename, _property=property, _tuple=tuple)
    try:
        exec template in namespace
    except SyntaxError, e:
        raise SyntaxError(e.message + ':\n' + template)

    result = namespace[typename]
    return result


class OrderedDict(dict, MutableMapping):
    """Dictionary that remembers insertion order"""

    def __init__(self, *args, **kwds):
        """Initialize an ordered dictionary.  Signature is the same as for
        regular dictionaries, but keyword arguments are not recommended
        because their insertion order is arbitrary.

        """
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__root
        except AttributeError:
            self.__root = root = [
             None, None, None]
            PREV = 0
            NEXT = 1
            root[PREV] = root[NEXT] = root
            self.__map = {}

        self.update(*args, **kwds)
        return

    def __setitem__(self, key, value, PREV=0, NEXT=1, dict_setitem=dict.__setitem__):
        """od.__setitem__(i, y) <==> od[i]=y"""
        if key not in self:
            root = self.__root
            last = root[PREV]
            last[NEXT] = root[PREV] = self.__map[key] = [last, root, key]
        dict_setitem(self, key, value)

    def __delitem__(self, key, PREV=0, NEXT=1, dict_delitem=dict.__delitem__):
        """od.__delitem__(y) <==> del od[y]"""
        dict_delitem(self, key)
        link = self.__map.pop(key)
        link_prev = link[PREV]
        link_next = link[NEXT]
        link_prev[NEXT] = link_next
        link_next[PREV] = link_prev

    def __iter__(self, NEXT=1, KEY=2):
        """od.__iter__() <==> iter(od)"""
        root = self.__root
        curr = root[NEXT]
        while curr is not root:
            yield curr[KEY]
            curr = curr[NEXT]

    def __reversed__(self, PREV=0, KEY=2):
        """od.__reversed__() <==> reversed(od)"""
        root = self.__root
        curr = root[PREV]
        while curr is not root:
            yield curr[KEY]
            curr = curr[PREV]

    def __reduce__(self):
        """Return state information for pickling"""
        items = [ [k, self[k]] for k in self ]
        tmp = (
         self.__map, self.__root)
        del self.__map
        del self.__root
        inst_dict = vars(self).copy()
        (self.__map, self.__root) = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return (
         self.__class__, (items,))

    def clear(self):
        """od.clear() -> None.  Remove all items from od."""
        try:
            for node in self.__map.itervalues():
                del node[:]

            self.__root[:] = [
             self.__root, self.__root, None]
            self.__map.clear()
        except AttributeError:
            pass

        dict.clear(self)
        return

    setdefault = MutableMapping.setdefault
    update = MutableMapping.update
    pop = MutableMapping.pop
    keys = MutableMapping.keys
    values = MutableMapping.values
    items = MutableMapping.items
    iterkeys = MutableMapping.iterkeys
    itervalues = MutableMapping.itervalues
    iteritems = MutableMapping.iteritems
    __ne__ = MutableMapping.__ne__

    def popitem(self, last=True):
        """od.popitem() -> (k, v), return and remove a (key, value) pair.
        Pairs are returned in LIFO order if last is true or FIFO order if false.

        """
        if not self:
            raise KeyError('dictionary is empty')
        key = next(reversed(self) if last else iter(self))
        value = self.pop(key)
        return (key, value)

    def __repr__(self):
        """od.__repr__() <==> repr(od)"""
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.items())

    def copy(self):
        """od.copy() -> a shallow copy of od"""
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        """OD.fromkeys(S[, v]) -> New ordered dictionary with keys from S
        and values equal to v (which defaults to None).

        """
        d = cls()
        for key in iterable:
            d[key] = value

        return d

    def __eq__(self, other):
        """od.__eq__(y) <==> od==y.  Comparison to another OD is order-sensitive
        while comparison to a regular mapping is order-insensitive.

        """
        if isinstance(other, OrderedDict):
            return len(self) == len(other) and all(_imap(_eq, self.iteritems(), other.iteritems()))
        return dict.__eq__(self, other)

    def __del__(self):
        self.clear()