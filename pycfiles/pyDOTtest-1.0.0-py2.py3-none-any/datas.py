# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyDots\datas.py
# Compiled at: 2017-01-16 16:05:05
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
from collections import MutableMapping, Mapping
from copy import deepcopy
from pyDots import _getdefault, hash_value, literal_field, coalesce, listwrap
_get = object.__getattribute__
_set = object.__setattr__
DEBUG = False

class Data(MutableMapping):
    """
    Please see README.md
    """
    __slots__ = [
     b'_dict']

    def __init__(self, *args, **kwargs):
        """
        CALLING Data(**something) WILL RESULT IN A COPY OF something, WHICH
        IS UNLIKELY TO BE USEFUL. USE wrap() INSTEAD
        """
        if DEBUG:
            d = _get(self, b'_dict')
            for k, v in kwargs.items():
                d[literal_field(k)] = unwrap(v)

        elif args:
            args0 = args[0]
            if isinstance(args0, dict):
                _set(self, b'_dict', args0)
            elif isinstance(args0, Data):
                _set(self, b'_dict', _get(args0, b'_dict'))
            elif isinstance(args0, list):
                _set(self, b'_dict', dict(args0))
            else:
                raise TypeError()
        elif kwargs:
            _set(self, b'_dict', unwrap(kwargs))
        else:
            _set(self, b'_dict', {})

    def __bool__(self):
        return True

    def __nonzero__(self):
        d = _get(self, b'_dict')
        if isinstance(d, dict):
            if d:
                return True
            return False
        return d != None
        return

    def __contains__(self, item):
        if Data.__getitem__(self, item):
            return True
        return False

    def __iter__(self):
        d = _get(self, b'_dict')
        return d.__iter__()

    def __getitem__(self, key):
        if key == None:
            return Null
        else:
            if key == b'.':
                output = _get(self, b'_dict')
                if isinstance(output, Mapping):
                    return self
                return output
            if isinstance(key, str):
                key = key.decode(b'utf8')
            else:
                if not isinstance(key, unicode):
                    from MoLogs import Log
                    Log.error(b'only string keys are supported')
                d = _get(self, b'_dict')
                if key.find(b'.') >= 0:
                    seq = _split_field(key)
                    for n in seq:
                        if isinstance(d, NullType):
                            d = NullType(d, n)
                        elif isinstance(d, list):
                            d = [ _getdefault(dd, n) for dd in d ]
                        else:
                            d = _getdefault(d, n)

                    return wrap(d)
                o = d.get(key)
                if o == None:
                    return NullType(d, key)
            return wrap(o)

    def __setitem__(self, key, value):
        if key == b'':
            from MoLogs import Log
            Log.error(b'key is empty string.  Probably a bad idea')
        if key == None:
            return Null
        else:
            if key == b'.':
                v = unwrap(value)
                _set(self, b'_dict', v)
                return v
            if isinstance(key, str):
                key = key.decode(b'utf8')
            try:
                d = _get(self, b'_dict')
                value = unwrap(value)
                if key.find(b'.') == -1:
                    if value is None:
                        d.pop(key, None)
                    else:
                        d[key] = value
                    return self
                seq = _split_field(key)
                for k in seq[:-1]:
                    d = _getdefault(d, k)

                if value == None:
                    d.pop(seq[(-1)], None)
                elif d == None:
                    d[literal_field(seq[(-1)])] = value
                else:
                    d[seq[(-1)]] = value
                return self
            except Exception as e:
                raise e

            return

    def __getattr__(self, key):
        if isinstance(key, str):
            ukey = key.decode(b'utf8')
        else:
            ukey = key
        d = _get(self, b'_dict')
        o = d.get(ukey)
        if o == None:
            return NullType(d, ukey)
        else:
            return wrap(o)

    def __setattr__(self, key, value):
        if isinstance(key, str):
            ukey = key.decode(b'utf8')
        else:
            ukey = key
        d = _get(self, b'_dict')
        value = unwrap(value)
        if value is None:
            d = _get(self, b'_dict')
            d.pop(key, None)
        else:
            d[ukey] = value
        return self

    def __hash__(self):
        d = _get(self, b'_dict')
        return hash_value(d)

    def __eq__(self, other):
        if self is other:
            return True
        else:
            d = _get(self, b'_dict')
            if not isinstance(d, dict):
                return d == other
            if not d and other == None:
                return True
            if not isinstance(other, Mapping):
                return False
            e = unwrap(other)
            d = _get(self, b'_dict')
            for k, v in d.items():
                if e.get(k) != v:
                    return False

            for k, v in e.items():
                if d.get(k) != v:
                    return False

            return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def get(self, key, default=None):
        d = _get(self, b'_dict')
        return d.get(key, default)

    def items(self):
        d = _get(self, b'_dict')
        return [ (k, wrap(v)) for k, v in d.items() if v != None or isinstance(v, Mapping) ]

    def leaves(self, prefix=None):
        """
        LIKE items() BUT RECURSIVE, AND ONLY FOR THE LEAVES (non dict) VALUES
        """
        return leaves(self, prefix)

    def iteritems(self):
        d = _get(self, b'_dict')
        return ((k, wrap(v)) for k, v in d.iteritems())

    def keys(self):
        d = _get(self, b'_dict')
        return set(d.keys())

    def values(self):
        d = _get(self, b'_dict')
        return listwrap(d.values())

    def clear(self):
        from MoLogs import Log
        Log.error(b'clear() not supported')

    def __len__(self):
        d = _get(self, b'_dict')
        return dict.__len__(d)

    def copy(self):
        return Data(**self)

    def __copy__(self):
        d = _get(self, b'_dict')
        return Data(**d)

    def __deepcopy__(self, memo):
        d = _get(self, b'_dict')
        return wrap(deepcopy(d, memo))

    def __delitem__(self, key):
        if isinstance(key, str):
            key = key.decode(b'utf8')
        if key.find(b'.') == -1:
            d = _get(self, b'_dict')
            d.pop(key, None)
            return
        else:
            d = _get(self, b'_dict')
            seq = _split_field(key)
            for k in seq[:-1]:
                d = d[k]

            d.pop(seq[(-1)], None)
            return

    def __delattr__(self, key):
        if isinstance(key, str):
            key = key.decode(b'utf8')
        d = _get(self, b'_dict')
        d.pop(key, None)
        return

    def setdefault(self, k, d=None):
        if self[k] == None:
            self[k] = d
        return self

    def __str__(self):
        try:
            return dict.__str__(_get(self, b'_dict'))
        except Exception:
            return b'{}'

    def __repr__(self):
        try:
            return b'Data(' + dict.__repr__(_get(self, b'_dict')) + b')'
        except Exception as e:
            return b'Data()'


def leaves(value, prefix=None):
    """
    LIKE items() BUT RECURSIVE, AND ONLY FOR THE LEAVES (non dict) VALUES
    SEE wrap_leaves FOR THE INVERSE

    :param value: THE Mapping TO TRAVERSE
    :param prefix:  OPTIONAL PREFIX GIVEN TO EACH KEY
    :return: Data, WHICH EACH KEY BEING A PATH INTO value TREE
    """
    prefix = coalesce(prefix, b'')
    output = []
    for k, v in value.items():
        try:
            if isinstance(v, Mapping):
                output.extend(leaves(v, prefix=prefix + literal_field(k) + b'.'))
            else:
                output.append((prefix + literal_field(k), unwrap(v)))
        except Exception as e:
            from MoLogs import Log
            Log.error(b'Do not know how to handle', cause=e)

    return output


def _split_field(field):
    """
    SIMPLE SPLIT, NO CHECKS
    """
    return [ k.replace(b'\x07', b'.') for k in field.replace(b'\\.', b'\x07').split(b'.') ]


class _DictUsingSelf(dict):

    def __init__(self, **kwargs):
        """
        CALLING Data(**something) WILL RESULT IN A COPY OF something, WHICH
        IS UNLIKELY TO BE USEFUL. USE wrap() INSTEAD
        """
        dict.__init__(self)

    def __bool__(self):
        return True

    def __getitem__(self, key):
        if key == None:
            return Null
        else:
            if isinstance(key, str):
                key = key.decode(b'utf8')
            d = self
            if key.find(b'.') >= 0:
                seq = _split_field(key)
                for n in seq:
                    d = _getdefault(self, n)

                return wrap(d)
            o = dict.get(d, None)
            if o == None:
                return NullType(d, key)
            return wrap(o)

    def __setitem__(self, key, value):
        if key == b'':
            from MoLogs import Log
            Log.error(b'key is empty string.  Probably a bad idea')
        if isinstance(key, str):
            key = key.decode(b'utf8')
        d = self
        try:
            value = unwrap(value)
            if key.find(b'.') == -1:
                if value is None:
                    dict.pop(d, key, None)
                else:
                    dict.__setitem__(d, key, value)
                return self
            seq = _split_field(key)
            for k in seq[:-1]:
                d = _getdefault(d, k)

            if value == None:
                dict.pop(d, seq[(-1)], None)
            else:
                dict.__setitem__(d, seq[(-1)], value)
            return self
        except Exception as e:
            raise e

        return

    def __getattr__(self, key):
        if isinstance(key, str):
            ukey = key.decode(b'utf8')
        else:
            ukey = key
        d = self
        o = dict.get(d, ukey, None)
        if o == None:
            return NullType(d, ukey)
        else:
            return wrap(o)

    def __setattr__(self, key, value):
        if isinstance(key, str):
            ukey = key.decode(b'utf8')
        else:
            ukey = key
        d = self
        value = unwrap(value)
        if value is None:
            dict.pop(d, key, None)
        else:
            dict.__setitem__(d, ukey, value)
        return self

    def __hash__(self):
        return hash_value(self)

    def __eq__(self, other):
        if self is other:
            return True
        else:
            d = self
            if not d and other == None:
                return True
            if not isinstance(other, Mapping):
                return False
            e = unwrap(other)
            for k, v in dict.items(d):
                if e.get(k) != v:
                    return False

            for k, v in e.items():
                if dict.get(d, k, None) != v:
                    return False

            return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def get(self, key, default=None):
        return wrap(dict.get(self, key, default))

    def items(self):
        return [ (k, wrap(v)) for k, v in dict.items(self) if v != None or isinstance(v, Mapping) ]

    def leaves(self, prefix=None):
        """
        LIKE items() BUT RECURSIVE, AND ONLY FOR THE LEAVES (non dict) VALUES
        """
        prefix = coalesce(prefix, b'')
        output = []
        for k, v in self.items():
            if isinstance(v, Mapping):
                output.extend(wrap(v).leaves(prefix=prefix + literal_field(k) + b'.'))
            else:
                output.append((prefix + literal_field(k), v))

        return output

    def iteritems(self):
        for k, v in dict.iteritems(self):
            yield (k, wrap(v))

    def keys(self):
        return set(dict.keys(self))

    def values(self):
        return listwrap(dict.values(self))

    def clear(self):
        from MoLogs import Log
        Log.error(b'clear() not supported')

    def __len__(self):
        d = _get(self, b'_dict')
        return d.__len__()

    def copy(self):
        return Data(**self)

    def __copy__(self):
        return Data(**self)

    def __deepcopy__(self, memo):
        return wrap(dict.__deepcopy__(self, memo))

    def __delitem__(self, key):
        if isinstance(key, str):
            key = key.decode(b'utf8')
        if key.find(b'.') == -1:
            dict.pop(self, key, None)
            return
        else:
            d = self
            seq = _split_field(key)
            for k in seq[:-1]:
                d = d[k]

            d.pop(seq[(-1)], None)
            return

    def __delattr__(self, key):
        if isinstance(key, str):
            key = key.decode(b'utf8')
        dict.pop(self, key, None)
        return

    def setdefault(self, k, d=None):
        if self[k] == None:
            self[k] = d
        return self

    def __str__(self):
        try:
            return dict.__str__(self)
        except Exception as e:
            return b'{}'

    def __repr__(self):
        try:
            return b'Data(' + dict.__repr__(self) + b')'
        except Exception as e:
            return b'Data()'


def _str(value, depth):
    """
    FOR DEBUGGING POSSIBLY RECURSIVE STRUCTURES
    """
    output = []
    if depth > 0 and isinstance(value, Mapping):
        for k, v in value.items():
            output.append(str(k) + b'=' + _str(v, depth - 1))

        return b'{' + (b',\n').join(output) + b'}'
    else:
        if depth > 0 and isinstance(value, list):
            for v in value:
                output.append(_str(v, depth - 1))

            return b'[' + (b',\n').join(output) + b']'
        return str(type(value))


from pyDots.nones import Null, NullType
from pyDots import unwrap, wrap