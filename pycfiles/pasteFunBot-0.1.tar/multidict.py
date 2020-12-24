# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/util/multidict.py
# Compiled at: 2009-07-20 09:44:04
import cgi, copy, sys
from UserDict import DictMixin

class MultiDict(DictMixin):
    """
    An ordered dictionary that can have multiple values for each key.
    Adds the methods getall, getone, mixed, and add to the normal
    dictionary interface.
    """

    def __init__(self, *args, **kw):
        if len(args) > 1:
            raise TypeError('MultiDict can only be called with one positional argument')
        if args:
            if hasattr(args[0], 'iteritems'):
                items = list(args[0].iteritems())
            elif hasattr(args[0], 'items'):
                items = args[0].items()
            else:
                items = list(args[0])
            self._items = items
        else:
            self._items = []
        self._items.extend(kw.iteritems())

    def __getitem__(self, key):
        for (k, v) in self._items:
            if k == key:
                return v

        raise KeyError(repr(key))

    def __setitem__(self, key, value):
        try:
            del self[key]
        except KeyError:
            pass

        self._items.append((key, value))

    def add(self, key, value):
        """
        Add the key and value, not overwriting any previous value.
        """
        self._items.append((key, value))

    def getall(self, key):
        """
        Return a list of all values matching the key (may be an empty list)
        """
        result = []
        for (k, v) in self._items:
            if key == k:
                result.append(v)

        return result

    def getone(self, key):
        """
        Get one value matching the key, raising a KeyError if multiple
        values were found.
        """
        v = self.getall(key)
        if not v:
            raise KeyError('Key not found: %r' % key)
        if len(v) > 1:
            raise KeyError('Multiple values match %r: %r' % (key, v))
        return v[0]

    def mixed(self):
        """
        Returns a dictionary where the values are either single
        values, or a list of values when a key/value appears more than
        once in this dictionary.  This is similar to the kind of
        dictionary often used to represent the variables in a web
        request.
        """
        result = {}
        multi = {}
        for (key, value) in self._items:
            if key in result:
                if key in multi:
                    result[key].append(value)
                else:
                    result[key] = [
                     result[key], value]
                    multi[key] = None
            else:
                result[key] = value

        return result

    def dict_of_lists(self):
        """
        Returns a dictionary where each key is associated with a
        list of values.
        """
        result = {}
        for (key, value) in self._items:
            if key in result:
                result[key].append(value)
            else:
                result[key] = [
                 value]

        return result

    def __delitem__(self, key):
        items = self._items
        found = False
        for i in range(len(items) - 1, -1, -1):
            if items[i][0] == key:
                del items[i]
                found = True

        if not found:
            raise KeyError(repr(key))

    def __contains__(self, key):
        for (k, v) in self._items:
            if k == key:
                return True

        return False

    has_key = __contains__

    def clear(self):
        self._items = []

    def copy(self):
        return MultiDict(self)

    def setdefault(self, key, default=None):
        for (k, v) in self._items:
            if key == k:
                return v

        self._items.append((key, default))
        return default

    def pop(self, key, *args):
        if len(args) > 1:
            raise TypeError, 'pop expected at most 2 arguments, got ' + repr(1 + len(args))
        for i in range(len(self._items)):
            if self._items[i][0] == key:
                v = self._items[i][1]
                del self._items[i]
                return v

        if args:
            return args[0]
        raise KeyError(repr(key))

    def popitem(self):
        return self._items.pop()

    def update(self, other=None, **kwargs):
        if other is None:
            pass
        elif hasattr(other, 'items'):
            self._items.extend(other.items())
        elif hasattr(other, 'keys'):
            for k in other.keys():
                self._items.append((k, other[k]))

        else:
            for (k, v) in other:
                self._items.append((k, v))

            if kwargs:
                self.update(kwargs)
            return

    def __repr__(self):
        items = (', ').join([ '(%r, %r)' % v for v in self._items ])
        return '%s([%s])' % (self.__class__.__name__, items)

    def __len__(self):
        return len(self._items)

    def keys(self):
        return [ k for (k, v) in self._items ]

    def iterkeys(self):
        for (k, v) in self._items:
            yield k

    __iter__ = iterkeys

    def items(self):
        return self._items[:]

    def iteritems(self):
        return iter(self._items)

    def values(self):
        return [ v for (k, v) in self._items ]

    def itervalues(self):
        for (k, v) in self._items:
            yield v


class UnicodeMultiDict(DictMixin):
    """
    A MultiDict wrapper that decodes returned values to unicode on the
    fly. Decoding is not applied to assigned values.

    The key/value contents are assumed to be ``str``/``strs`` or
    ``str``/``FieldStorages`` (as is returned by the ``paste.request.parse_``
    functions).

    Can optionally also decode keys when the ``decode_keys`` argument is
    True.

    ``FieldStorage`` instances are cloned, and the clone's ``filename``
    variable is decoded. Its ``name`` variable is decoded when ``decode_keys``
    is enabled.

    """

    def __init__(self, multi=None, encoding=None, errors='strict', decode_keys=False):
        self.multi = multi
        if encoding is None:
            encoding = sys.getdefaultencoding()
        self.encoding = encoding
        self.errors = errors
        self.decode_keys = decode_keys
        return

    def _decode_key(self, key):
        if self.decode_keys:
            try:
                key = key.decode(self.encoding, self.errors)
            except AttributeError:
                pass

        return key

    def _decode_value(self, value):
        """
        Decode the specified value to unicode. Assumes value is a ``str`` or
        `FieldStorage`` object.

        ``FieldStorage`` objects are specially handled.
        """
        if isinstance(value, cgi.FieldStorage):
            value = copy.copy(value)
            if self.decode_keys:
                value.name = value.name.decode(self.encoding, self.errors)
            value.filename = value.filename.decode(self.encoding, self.errors)
        else:
            try:
                value = value.decode(self.encoding, self.errors)
            except AttributeError:
                pass

        return value

    def __getitem__(self, key):
        return self._decode_value(self.multi.__getitem__(key))

    def __setitem__(self, key, value):
        self.multi.__setitem__(key, value)

    def add(self, key, value):
        """
        Add the key and value, not overwriting any previous value.
        """
        self.multi.add(key, value)

    def getall(self, key):
        """
        Return a list of all values matching the key (may be an empty list)
        """
        return [ self._decode_value(v) for v in self.multi.getall(key) ]

    def getone(self, key):
        """
        Get one value matching the key, raising a KeyError if multiple
        values were found.
        """
        return self._decode_value(self.multi.getone(key))

    def mixed(self):
        """
        Returns a dictionary where the values are either single
        values, or a list of values when a key/value appears more than
        once in this dictionary.  This is similar to the kind of
        dictionary often used to represent the variables in a web
        request.
        """
        unicode_mixed = {}
        for (key, value) in self.multi.mixed().iteritems():
            if isinstance(value, list):
                value = [ self._decode_value(value) for value in value ]
            else:
                value = self._decode_value(value)
            unicode_mixed[self._decode_key(key)] = value

        return unicode_mixed

    def dict_of_lists(self):
        """
        Returns a dictionary where each key is associated with a
        list of values.
        """
        unicode_dict = {}
        for (key, value) in self.multi.dict_of_lists().iteritems():
            value = [ self._decode_value(value) for value in value ]
            unicode_dict[self._decode_key(key)] = value

        return unicode_dict

    def __delitem__(self, key):
        self.multi.__delitem__(key)

    def __contains__(self, key):
        return self.multi.__contains__(key)

    has_key = __contains__

    def clear(self):
        self.multi.clear()

    def copy(self):
        return UnicodeMultiDict(self.multi.copy(), self.encoding, self.errors)

    def setdefault(self, key, default=None):
        return self._decode_value(self.multi.setdefault(key, default))

    def pop(self, key, *args):
        return self._decode_value(self.multi.pop(key, *args))

    def popitem(self):
        (k, v) = self.multi.popitem()
        return (self._decode_key(k), self._decode_value(v))

    def __repr__(self):
        items = (', ').join([ '(%r, %r)' % v for v in self.items() ])
        return '%s([%s])' % (self.__class__.__name__, items)

    def __len__(self):
        return self.multi.__len__()

    def keys(self):
        return [ self._decode_key(k) for k in self.multi.iterkeys() ]

    def iterkeys(self):
        for k in self.multi.iterkeys():
            yield self._decode_key(k)

    __iter__ = iterkeys

    def items(self):
        return [ (self._decode_key(k), self._decode_value(v)) for (k, v) in self.multi.iteritems()
               ]

    def iteritems(self):
        for (k, v) in self.multi.iteritems():
            yield (self._decode_key(k), self._decode_value(v))

    def values(self):
        return [ self._decode_value(v) for v in self.multi.itervalues() ]

    def itervalues(self):
        for v in self.multi.itervalues():
            yield self._decode_value(v)


__test__ = {'general': "\n    >>> d = MultiDict(a=1, b=2)\n    >>> d['a']\n    1\n    >>> d.getall('c')\n    []\n    >>> d.add('a', 2)\n    >>> d['a']\n    1\n    >>> d.getall('a')\n    [1, 2]\n    >>> d['b'] = 4\n    >>> d.getall('b')\n    [4]\n    >>> d.keys()\n    ['a', 'a', 'b']\n    >>> d.items()\n    [('a', 1), ('a', 2), ('b', 4)]\n    >>> d.mixed()\n    {'a': [1, 2], 'b': 4}\n    >>> MultiDict([('a', 'b')], c=2)\n    MultiDict([('a', 'b'), ('c', 2)])\n    "}
if __name__ == '__main__':
    import doctest
    doctest.testmod()